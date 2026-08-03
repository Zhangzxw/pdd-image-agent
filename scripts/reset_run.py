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


def assert_safe_directory(path: Path, *, label: str, must_be_under: Path | None = None) -> None:
    path = path.resolve()
    if path == Path(path.anchor) or len(path.parts) < 4:
        raise SystemExit(f"拒绝清理不安全的 {label} 路径: {path}")
    if must_be_under is not None:
        base = must_be_under.resolve()
        try:
            path.relative_to(base)
        except ValueError as exc:
            raise SystemExit(f"{label} 必须位于 {base} 内: {path}") from exc


def archive_records(source: Path, archive_root: Path, group: str, extensions: set[str]) -> list[str]:
    archived: list[str] = []
    if not source.exists():
        return archived
    for item in source.rglob("*"):
        if not item.is_file() or item.suffix.lower() not in extensions:
            continue
        relative = item.relative_to(source)
        target = archive_root / group / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        archived.append(str(Path(group) / relative))
    return archived


def clear_directory(path: Path) -> int:
    path.mkdir(parents=True, exist_ok=True)
    removed = 0
    for child in list(path.iterdir()):
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
        removed += 1
    return removed


def main() -> int:
    config = load_json(ROOT / "batch_config.json")
    cleanup = config.get("run_cleanup", {})
    if not cleanup.get("enabled", True):
        print(json.dumps({"status": "SKIPPED", "reason": "run_cleanup.enabled=false"}, ensure_ascii=False))
        return 0

    tasks_dir = resolve_path(config.get("tasks_dir", "tasks"))
    output_dir = resolve_path(config["output_dir"])
    records_dir = resolve_path(config.get("records_dir", "run_records"))
    history_dir = resolve_path(config.get("history_dir", "history"))
    assert_safe_directory(tasks_dir, label="tasks", must_be_under=ROOT)
    assert_safe_directory(history_dir, label="history", must_be_under=ROOT)
    assert_safe_directory(records_dir, label="records", must_be_under=ROOT)
    assert_safe_directory(output_dir, label="output")
    if len({tasks_dir, output_dir, history_dir, records_dir}) != 4:
        raise SystemExit("tasks、output、history、records 路径不得相同")

    run_id = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S_%f")
    archive_root = history_dir / run_id
    extensions = {str(x).lower() for x in cleanup.get("record_extensions", [".json", ".md", ".txt", ".csv", ".log"])}
    archived: list[str] = []
    if cleanup.get("archive_records_before_cleanup", True):
        archived.extend(archive_records(tasks_dir, archive_root, "tasks_records", extensions))
        archived.extend(archive_records(records_dir, archive_root, "run_records", extensions))

    removed_tasks = clear_directory(tasks_dir) if cleanup.get("clear_tasks", True) else 0
    removed_output = clear_directory(output_dir) if cleanup.get("clear_output", True) else 0
    removed_records = clear_directory(records_dir) if cleanup.get("clear_records", True) else 0
    archive_root.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "PASSED",
        "run_id": run_id,
        "archived_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "archive_directory": str(archive_root),
        "archived_record_count": len(archived),
        "archived_records": archived,
        "removed_task_entries": removed_tasks,
        "removed_output_entries": removed_output,
        "removed_record_entries": removed_records,
        "note": "记录文件先从 tasks/run_records 归档；旧候选图、最终图和临时下载已按新批次规则清除。",
    }
    (archive_root / "archive_manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
