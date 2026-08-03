from __future__ import annotations
import csv, json, re, shutil
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def resolve_path(value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else (ROOT / p)

def safe_stem(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '-', value)
    value = re.sub(r'\s+', '-', value)
    value = re.sub(r'-+', '-', value).strip('-_. ')
    return value or 'task'

def copy_unique(source: Path, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / source.name
    idx = 2
    while dest.exists():
        dest = dest_dir / f'{source.stem}-{idx}{source.suffix}'
        idx += 1
    shutil.copy2(source, dest)
    return dest

def iter_images(folder: Path, extensions: set[str]):
    if not folder.exists():
        return []
    return sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in extensions], key=lambda p: p.name.lower())

@dataclass
class TaskItem:
    task_id: str
    competitor_image: str
    product_image: str
    match_reason: str
    output_stem: str
    status: str
    note: str = ''

def main() -> int:
    config = load_json(ROOT / 'batch_config.json')
    competitor_dir = resolve_path(config['competitor_dir'])
    product_dir = resolve_path(config['product_dir'])
    tasks_dir = resolve_path(config['tasks_dir'])
    output_dir = resolve_path(config['output_dir'])
    records_dir = resolve_path(config.get('records_dir', 'run_records'))
    extensions = set(x.lower() for x in config.get('image_extensions', []))
    tasks_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    records_dir.mkdir(parents=True, exist_ok=True)
    competitors = iter_images(competitor_dir, extensions)
    products = iter_images(product_dir, extensions)
    if not competitors:
        raise SystemExit(f'竞品图目录中未找到图片: {competitor_dir}')
    if not products:
        raise SystemExit(f'产品图目录中未找到图片: {product_dir}')
    fallback_name = config.get('fallback_product', '')
    fallback_path = product_dir / fallback_name if fallback_name else None
    has_single_global = len(products) == 1 and bool(config.get('allow_single_product_for_all', True))
    product_map = {p.stem.lower(): p for p in products}
    template = load_json(ROOT / 'assets/product-brief-template.json')
    manifest = []
    for child in tasks_dir.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
    for index, comp in enumerate(competitors, start=1):
        comp_key = comp.stem.lower()
        matched_product = None
        reason = ''
        note = ''
        status = 'ready'
        if has_single_global:
            matched_product = products[0]
            reason = 'single_product_for_all'
        elif comp_key in product_map:
            matched_product = product_map[comp_key]
            reason = 'same_stem_match'
        elif bool(config.get('allow_fallback_product', False)) and fallback_path and fallback_path.is_file():
            matched_product = fallback_path
            reason = 'fallback_product'
        else:
            reason = 'unmatched_skipped'
            status = 'skipped'
            note = '未找到匹配产品图'
        task_id = f'{index:03d}_{safe_stem(comp.stem)}'
        output_stem = safe_stem(comp.stem)
        item = TaskItem(task_id, str(comp), str(matched_product) if matched_product else '', reason, output_stem, status, note)
        manifest.append(item)
        if status != 'ready':
            continue
        task_dir = tasks_dir / task_id
        comp_target = copy_unique(comp, task_dir / 'input' / 'competitor')
        prod_target = copy_unique(matched_product, task_dir / 'input' / 'product')
        brief = json.loads(json.dumps(template))
        brief['job_id'] = task_id
        brief['platform'] = config.get('platform', 'pinduoduo')
        brief['purpose'] = config.get('purpose', '商品主图')
        brief['canvas']['aspect_ratio'] = config.get('default_canvas', {}).get('aspect_ratio', '1:1')
        brief['canvas']['width'] = config.get('default_canvas', {}).get('width', 1024)
        brief['canvas']['height'] = config.get('default_canvas', {}).get('height', 1024)
        target_rel = str(comp_target.relative_to(task_dir)).replace('\\', '/')
        brief['inputs']['target_effect_images'] = [target_rel]
        brief['inputs']['own_product_images'] = [str(prod_target.relative_to(task_dir)).replace('\\', '/')]
        brief['must_keep'] = config.get('must_keep', brief['must_keep'])
        brief['must_not_include'] = config.get('must_not_include', brief['must_not_include'])
        brief['generation'] = json.loads(json.dumps(config.get('generation_engine', brief.get('generation', {}))))
        brief['reference_copy']['preserve_original_wording'] = bool(config.get('preserve_reference_marketing_copy', True))
        brief['transformation']['preserve_reference_marketing_copy'] = bool(config.get('preserve_reference_marketing_copy', True))
        brief['transformation']['preserve_reference_promotional_copy'] = bool(config.get('preserve_reference_promotional_copy', True))
        brief['transformation']['preserve_reference_layout'] = bool(config.get('preserve_reference_layout', True))
        brief['transformation']['preserve_reference_props_and_effects'] = bool(config.get('preserve_reference_props_and_effects', True))
        brief['transformation']['auto_rewrite_reference_claims'] = bool(config.get('auto_rewrite_reference_claims', False))
        brief['inputs']['reference_role'] = config.get('reference_image_role', 'target_effect_for_reverse_engineering')
        brief['inputs']['generation_image_inputs'] = config.get('generation_input_mode', 'own_product_only')
        brief['generation']['input_mode'] = 'own_product_only'
        brief['generation']['competitor_image_upload'] = False
        brief['generation']['input_order'] = ['own_product_source_of_truth']
        brief['output']['directory'] = str(output_dir)
        brief['output']['records_directory'] = str(records_dir)
        brief['output']['final_images_only'] = True
        brief['output']['generate_execution_log'] = bool(config.get('generate_execution_log', True))
        brief['qa_policy'] = json.loads(json.dumps(config.get('qa_policy', brief.get('qa_policy', {}))))
        save_json(task_dir / 'product-brief.json', brief)
    manifest_json = [asdict(x) for x in manifest]
    save_json(tasks_dir / 'batch_manifest.json', manifest_json)
    with (tasks_dir / 'batch_manifest.csv').open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['task_id','competitor_image','product_image','match_reason','output_stem','status','note'])
        writer.writeheader()
        for row in manifest_json:
            writer.writerow(row)
    summary = {
        'total_competitors': len(competitors),
        'total_products': len(products),
        'ready_tasks': sum(1 for x in manifest if x.status == 'ready'),
        'skipped_tasks': sum(1 for x in manifest if x.status != 'ready'),
        'manifest_json': str(tasks_dir / 'batch_manifest.json'),
        'manifest_csv': str(tasks_dir / 'batch_manifest.csv'),
    }
    save_json(tasks_dir / 'batch_summary.json', summary)
    print('批量任务准备完成')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
