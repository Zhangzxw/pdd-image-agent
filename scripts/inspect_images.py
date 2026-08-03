from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image

IMAGE_SUFFIXES = {'.png','.jpg','.jpeg','.webp','.bmp','.tif','.tiff'}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def collect(paths: list[str]):
    items = []
    for raw in paths:
        p = Path(raw)
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES:
            items.append(p)
        elif p.is_dir():
            items.extend(sorted([x for x in p.rglob('*') if x.is_file() and x.suffix.lower() in IMAGE_SUFFIXES]))
    return items

def main() -> int:
    parser = argparse.ArgumentParser(description='检查图片信息')
    parser.add_argument('paths', nargs='+')
    args = parser.parse_args()
    records = []
    for path in collect(args.paths):
        with Image.open(path) as img:
            records.append({'path': str(path), 'format': img.format, 'width': img.width, 'height': img.height, 'mode': img.mode, 'size_bytes': path.stat().st_size, 'sha256': sha256(path)})
    print(json.dumps(records, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
