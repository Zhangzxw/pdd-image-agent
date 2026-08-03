from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_path(value: str) -> Path:
    path = Path(value)
    return (path if path.is_absolute() else ROOT / path).resolve()


def is_final_image(path: Path, suffix: str, extensions: set[str]) -> bool:
    return path.is_file() and path.suffix.lower() in extensions and path.stem.endswith(suffix)


def unique_target(folder: Path, name: str) -> Path:
    target = folder / name
    index = 2
    while target.exists():
        target = folder / f"{Path(name).stem}-{index}{Path(name).suffix}"
        index += 1
    return target


def main() -> int:
    config = load_json(ROOT / "batch_config.json")
    output_dir = resolve_path(config["output_dir"])
    records_dir = resolve_path(config.get("records_dir", "run_records"))
    policy = config.get("output_policy", {})
    suffix = str(policy.get("final_name_suffix", "_final"))
    extensions = {str(x).lower() for x in policy.get("allowed_final_extensions", [".png", ".jpg", ".jpeg", ".webp"])}
    output_dir.mkdir(parents=True, exist_ok=True)
    records_dir.mkdir(parents=True, exist_ok=True)
    cleanup_dir = records_dir / "output_cleanup" / datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    moved: list[dict[str, str]] = []
    for item in list(output_dir.iterdir()):
        if is_final_image(item, suffix, extensions):
            continue
        cleanup_dir.mkdir(parents=True, exist_ok=True)
        target = unique_target(cleanup_dir, item.name)
        shutil.move(str(item), str(target))
        moved.append({"source": str(item), "target": str(target)})
    finals = sorted(str(x) for x in output_dir.iterdir() if is_final_image(x, suffix, extensions))
    report = {
        "status": "PASSED",
        "output_dir": str(output_dir),
        "records_dir": str(records_dir),
        "moved_non_final_count": len(moved),
        "moved": moved,
        "final_image_count": len(finals),
        "final_images": finals,
    }
    report_path = records_dir / "finalize_output_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
