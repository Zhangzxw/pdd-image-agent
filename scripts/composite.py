from __future__ import annotations
import argparse, json
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont

def resolve(base: Path, value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else (base / p).resolve()

def color(value: str | None, default: str = '#FFFFFF'):
    return ImageColor.getcolor(value or default, 'RGBA')

def default_font_path() -> Path | None:
    candidates = [Path(r'C:\Windows\Fonts\msyh.ttc'), Path(r'C:\Windows\Fonts\msyhbd.ttc'), Path(r'C:\Windows\Fonts\simhei.ttf'), Path(r'C:\Windows\Fonts\arial.ttf')]
    return next((p for p in candidates if p.is_file()), None)

def load_font(font_path: str, size: int, base: Path):
    path = resolve(base, font_path) if font_path else default_font_path()
    if path and path.is_file():
        return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()

def fit_text(draw, text, box_px, font_path, start_size, min_size, spacing, stroke_width, base):
    x, y, w, h = box_px
    for size in range(start_size, min_size - 1, -1):
        font = load_font(font_path, size, base)
        bbox = draw.multiline_textbbox((0,0), text, font=font, spacing=spacing, stroke_width=stroke_width, align='center')
        if bbox[2] - bbox[0] <= w and bbox[3] - bbox[1] <= h:
            return font, bbox
    font = load_font(font_path, min_size, base)
    bbox = draw.multiline_textbbox((0,0), text, font=font, spacing=spacing, stroke_width=stroke_width, align='center')
    return font, bbox

def add_shadow(canvas, layer, xy, config):
    if not config.get('enabled', True):
        return
    width, height = canvas.size
    ox = int(float(config.get('offset', [0.01,0.015])[0]) * width)
    oy = int(float(config.get('offset', [0.01,0.015])[1]) * height)
    blur = max(1, int(float(config.get('blur_ratio', 0.02)) * width))
    opacity = max(0, min(255, int(float(config.get('opacity', 0.3)) * 255)))
    alpha = layer.getchannel('A')
    shadow = Image.new('RGBA', layer.size, (0,0,0,0))
    shadow.putalpha(alpha.point(lambda p: p * opacity // 255))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(shadow, (xy[0] + ox, xy[1] + oy))

def add_image_layer(canvas, spec, base):
    source = Image.open(resolve(base, spec['path'])).convert('RGBA')
    target_width = max(1, int(canvas.width * float(spec.get('width_ratio', 0.5))))
    target_height = max(1, round(source.height * target_width / source.width))
    source = source.resize((target_width, target_height), Image.Resampling.LANCZOS)
    center = spec.get('center', [0.5,0.5])
    cx = int(float(center[0]) * canvas.width)
    cy = int(float(center[1]) * canvas.height)
    xy = (cx - source.width // 2, cy - source.height // 2)
    add_shadow(canvas, source, xy, spec.get('shadow', {}))
    canvas.alpha_composite(source, xy)

def add_text_layer(canvas, spec, base):
    draw = ImageDraw.Draw(canvas)
    bx, by, bw, bh = [float(v) for v in spec['box']]
    box_px = (int(bx * canvas.width), int(by * canvas.height), int(bw * canvas.width), int(bh * canvas.height))
    text = str(spec.get('text', ''))
    align = spec.get('align', 'center')
    spacing = int(spec.get('line_spacing', 6))
    stroke_width = int(spec.get('stroke_width', 0))
    font, bbox = fit_text(draw, text, box_px, str(spec.get('font_path', '')), int(spec.get('font_size', 64)), int(spec.get('min_font_size', 20)), spacing, stroke_width, base)
    x, y, w, h = box_px
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    tx = x + (w - text_w) // 2
    ty = y + (h - text_h) // 2 - bbox[1]
    draw.multiline_text((tx, ty), text, font=font, fill=color(spec.get('fill'), '#FFFFFF'), spacing=spacing, align=align, stroke_width=stroke_width, stroke_fill=color(spec.get('stroke_fill'), '#000000'))

def main() -> int:
    parser = argparse.ArgumentParser(description='精确合成产品图和文案')
    parser.add_argument('--spec', required=True)
    args = parser.parse_args()
    spec_path = Path(args.spec).resolve()
    base = spec_path.parent
    spec = json.loads(spec_path.read_text(encoding='utf-8'))
    canvas_spec = spec['canvas']
    width, height = int(canvas_spec['width']), int(canvas_spec['height'])
    bg_value = str(canvas_spec.get('background', '')).strip()
    if bg_value:
        canvas = Image.open(resolve(base, bg_value)).convert('RGBA')
        canvas = canvas.resize((width, height), Image.Resampling.LANCZOS)
    else:
        canvas = Image.new('RGBA', (width, height), (255,255,255,255))
    for layer in spec.get('layers', []):
        if layer.get('type') == 'image':
            add_image_layer(canvas, layer, base)
        elif layer.get('type') == 'text':
            add_text_layer(canvas, layer, base)
    output = resolve(base, canvas_spec['output'])
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() in {'.jpg','.jpeg'}:
        canvas.convert('RGB').save(output, quality=95, subsampling=0)
    else:
        canvas.save(output)
    print(f'已输出: {output}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
