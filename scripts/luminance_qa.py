from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import Image
except ModuleNotFoundError:
    print(
        "亮度QA缺少依赖 Pillow。请改用已安装 Pillow 的 Python 解释器；不得在依赖缺失时提交付费生成。",
        file=sys.stderr,
    )
    raise SystemExit(4)


DEFAULT_THRESHOLDS = {
    "global_mean_drop_note": 0.05,
    "global_mean_drop_review": 0.10,
    "background_mean_drop_note": 0.05,
    "background_mean_drop_reject": 0.10,
    "product_mean_drop_note": 0.07,
    "product_mean_drop_review": 0.12,
    "product_dark_ratio_increase_note": 0.03,
    "product_dark_ratio_increase_review": 0.06,
    "product_p90_drop_note": 0.05,
    "product_p90_drop_review": 0.08,
    "headline_dark_ratio_increase_note": 0.08,
    "headline_dark_ratio_increase_review": 0.12,
    "secondary_dark_ratio_increase_note": 0.05,
    "secondary_dark_ratio_increase_review": 0.10,
}

LINEAR_LUT = [
    round(
        (
            value / 255.0 / 12.92
            if value / 255.0 <= 0.04045
            else ((value / 255.0 + 0.055) / 1.055) ** 2.4
        )
        * 255
    )
    for value in range(256)
]


def load_regions(path: Path | None) -> dict[str, list[list[float]]]:
    if path is None:
        return {"global": [[0.0, 0.0, 1.0, 1.0]]}
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw = raw.get("regions", raw)
    regions: dict[str, list[list[float]]] = {}
    for name, value in raw.items():
        boxes = value.get("boxes", []) if isinstance(value, dict) else value
        if len(boxes) == 4 and all(isinstance(x, (int, float)) for x in boxes):
            boxes = [boxes]
        clean: list[list[float]] = []
        for box in boxes:
            if len(box) != 4:
                raise ValueError(f"区域 {name} 的矩形必须包含4个归一化坐标")
            left, top, right, bottom = (float(x) for x in box)
            if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
                raise ValueError(f"区域 {name} 坐标越界: {box}")
            clean.append([left, top, right, bottom])
        if clean:
            regions[str(name)] = clean
    regions.setdefault("global", [[0.0, 0.0, 1.0, 1.0]])
    return regions


def linear_gray(image: Image.Image) -> Image.Image:
    # 每张图只转换一次，避免按区域重复处理整张2K图片。
    return image.convert("RGB").point(LINEAR_LUT * 3).convert("L")


def merge_histograms(gray: Image.Image, boxes: list[list[float]]) -> tuple[list[int], int]:
    width, height = gray.size
    merged = [0] * 256
    count = 0
    for left, top, right, bottom in boxes:
        pixel_box = (
            round(left * width),
            round(top * height),
            round(right * width),
            round(bottom * height),
        )
        crop = gray.crop(pixel_box)
        hist = crop.histogram()
        count += crop.width * crop.height
        for index, value in enumerate(hist):
            merged[index] += value
    return merged, count


def percentile(hist: list[int], count: int, fraction: float) -> float:
    target = max(1, round(count * fraction))
    cumulative = 0
    for index, value in enumerate(hist):
        cumulative += value
        if cumulative >= target:
            return index / 255.0
    return 1.0


def metrics(gray: Image.Image, boxes: list[list[float]]) -> dict[str, float]:
    hist, count = merge_histograms(gray, boxes)
    if count == 0:
        raise ValueError("取样区域没有像素")
    mean = sum(index * value for index, value in enumerate(hist)) / count / 255.0
    dark_limit = int(0.15 * 255)
    dark_ratio = sum(hist[: dark_limit + 1]) / count
    return {
        "mean_luma": round(mean, 6),
        "p50_luma": round(percentile(hist, count, 0.50), 6),
        "p90_luma": round(percentile(hist, count, 0.90), 6),
        "dark_ratio": round(dark_ratio, 6),
        "pixel_count": count,
    }


def role(mean_luma: float) -> str:
    if mean_luma >= 0.65:
        return "HIGH"
    if mean_luma >= 0.25:
        return "MID"
    return "LOW"


def compare_region(name: str, reference: dict[str, float], candidate: dict[str, float]) -> dict[str, Any]:
    ref_mean = reference["mean_luma"]
    mean_drop = (ref_mean - candidate["mean_luma"]) / ref_mean if ref_mean else 0.0
    dark_increase = candidate["dark_ratio"] - reference["dark_ratio"]
    p90_drop = reference["p90_luma"] - candidate["p90_luma"]
    ref_role = role(ref_mean)
    candidate_role = role(candidate["mean_luma"])
    failures: list[str] = []
    review_flags: list[str] = []
    notes: list[str] = []

    if name == "global":
        if mean_drop > DEFAULT_THRESHOLDS["global_mean_drop_review"]:
            review_flags.append("global_mean_luma_drop_review")
        elif mean_drop > DEFAULT_THRESHOLDS["global_mean_drop_note"]:
            notes.append("global_mean_luma_drop_note")
    if name == "background":
        if mean_drop > DEFAULT_THRESHOLDS["background_mean_drop_reject"]:
            # 纵横比适配、人物/产品重排会让固定背景框采到不同语义。
            # 只有明显跨亮度等级才可自动拒绝；同等级下降交给人工复核。
            if ref_role in {"HIGH", "MID"} and candidate_role == "LOW":
                failures.append("background_luminance_role_downgrade")
            else:
                review_flags.append("background_mean_luma_drop_review")
        elif mean_drop > DEFAULT_THRESHOLDS["background_mean_drop_note"]:
            notes.append("background_mean_luma_drop_note")
    if name.startswith("product"):
        severe_mean = mean_drop > DEFAULT_THRESHOLDS["product_mean_drop_review"]
        severe_dark = dark_increase > DEFAULT_THRESHOLDS["product_dark_ratio_increase_review"]
        severe_p90 = p90_drop > DEFAULT_THRESHOLDS["product_p90_drop_review"]
        if severe_mean and (severe_dark or severe_p90):
            # 图片1与图片2可能是不同固有明度的包装，产品区只进入人工复核，不能自动拒绝。
            review_flags.append("product_compound_darkening_review")
        elif (
            mean_drop > DEFAULT_THRESHOLDS["product_mean_drop_note"]
            or dark_increase > DEFAULT_THRESHOLDS["product_dark_ratio_increase_note"]
            or p90_drop > DEFAULT_THRESHOLDS["product_p90_drop_note"]
        ):
            notes.append("product_luminance_difference_note")
    if name in {"headline", "banner", "badge", "bottom_bar"}:
        if ref_role in {"HIGH", "MID"} and candidate_role == "LOW":
            # 外部文案可能已按用户确认删除或改写，固定框不再对应原语义。
            # 自动量化仅提示人工核验，不据此触发付费重试。
            review_flags.append("luminance_role_downgrade_review")
    if name == "headline":
        if dark_increase > DEFAULT_THRESHOLDS["headline_dark_ratio_increase_review"]:
            review_flags.append("headline_dark_ratio_increase_review")
        elif dark_increase > DEFAULT_THRESHOLDS["headline_dark_ratio_increase_note"]:
            notes.append("headline_dark_ratio_increase_note")
    if name in {"banner", "badge", "bottom_bar"}:
        if dark_increase > DEFAULT_THRESHOLDS["secondary_dark_ratio_increase_review"]:
            review_flags.append("secondary_dark_ratio_increase_review")
        elif dark_increase > DEFAULT_THRESHOLDS["secondary_dark_ratio_increase_note"]:
            notes.append("secondary_dark_ratio_increase_note")

    status = "PASSED"
    if failures:
        status = "REJECTED"
    elif review_flags:
        status = "REVIEW_REQUIRED"
    elif notes:
        status = "PASSED_WITH_NOTES"

    return {
        "reference": reference,
        "candidate": candidate,
        "reference_role": ref_role,
        "candidate_role": candidate_role,
        "mean_drop_ratio": round(mean_drop, 6),
        "dark_ratio_increase": round(dark_increase, 6),
        "p90_drop": round(p90_drop, 6),
        "status": status,
        "failures": failures,
        "review_flags": review_flags,
        "notes": notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="对参考图与候选图执行分区亮度QA")
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--regions", type=Path, help="JSON分区文件；缺省时只检测全图")
    parser.add_argument("--output", type=Path, help="可选JSON输出路径")
    args = parser.parse_args()

    regions = load_regions(args.regions)
    with Image.open(args.reference) as ref_image, Image.open(args.candidate) as cand_image:
        ref_gray = linear_gray(ref_image)
        cand_gray = linear_gray(cand_image)
        results = {
            name: compare_region(
                name,
                metrics(ref_gray, boxes),
                metrics(cand_gray, boxes),
            )
            for name, boxes in regions.items()
        }

    failed_regions = [name for name, item in results.items() if item["status"] == "REJECTED"]
    review_regions = [name for name, item in results.items() if item["status"] == "REVIEW_REQUIRED"]
    noted_regions = [name for name, item in results.items() if item["status"] == "PASSED_WITH_NOTES"]
    status = "PASSED"
    if failed_regions:
        status = "REJECTED"
    elif review_regions:
        status = "REVIEW_REQUIRED"
    elif noted_regions:
        status = "PASSED_WITH_NOTES"
    report = {
        "status": status,
        "reference": str(args.reference.resolve()),
        "candidate": str(args.candidate.resolve()),
        "regions_file": str(args.regions.resolve()) if args.regions else None,
        "thresholds": DEFAULT_THRESHOLDS,
        "failed_regions": failed_regions,
        "review_regions": review_regions,
        "noted_regions": noted_regions,
        "regions": results,
        "notes": [] if args.regions else ["未提供分区文件，仅检测global；必须补做背景、产品及版式区域复核。"],
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    if failed_regions:
        return 2
    if review_regions:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
