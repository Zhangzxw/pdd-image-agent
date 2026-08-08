from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def resolve_path(value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else (ROOT / p)

def main() -> int:
    cfg = load_json(ROOT / 'batch_config.json')
    errors, warnings = [], []
    comp_dir = resolve_path(cfg.get('competitor_dir', 'EnterImage'))
    prod_dir = resolve_path(cfg.get('product_dir', 'ProductImage'))
    out_dir = resolve_path(cfg.get('output_dir', 'OutputIamge'))
    records_dir = resolve_path(cfg.get('records_dir', 'run_records'))
    tasks_dir = resolve_path(cfg.get('tasks_dir', 'tasks'))
    exts = {x.lower() for x in cfg.get('image_extensions', ['.png','.jpg','.jpeg','.webp'])}
    engine = cfg.get('generation_engine', {})
    cleanup = cfg.get('run_cleanup', {})
    output_policy = cfg.get('output_policy', {})
    qa_policy = cfg.get('qa_policy', {})
    identity_lock = cfg.get('product_identity_lock', {})
    composition_lock = cfg.get('composition_lock', {})
    source_authority = cfg.get('image2image_source_authority', {})
    lighting_boundary = cfg.get('lighting_application_boundary', {})
    visibility_zone = cfg.get('core_visibility_zone', {})
    execution_log = cfg.get('execution_log', {})
    if not comp_dir.exists():
        errors.append(f'竞品图目录不存在: {comp_dir}')
    if not prod_dir.exists():
        errors.append(f'产品图目录不存在: {prod_dir}')
    comp_count = sum(1 for p in comp_dir.iterdir() if p.is_file() and p.suffix.lower() in exts) if comp_dir.exists() else 0
    prod_count = sum(1 for p in prod_dir.iterdir() if p.is_file() and p.suffix.lower() in exts) if prod_dir.exists() else 0
    if comp_count == 0:
        warnings.append('竞品图目录中还没有图片')
    if prod_count == 0:
        warnings.append('产品图目录中还没有图片')
    product_roles = cfg.get('product_image_roles', {})
    if product_roles.get('mode') == 'primary_first_details_rest' and prod_dir.exists():
        primary_prefix = str(product_roles.get('primary_name_prefix', '00_')).lower()
        primary_candidates = [p for p in prod_dir.iterdir() if p.is_file() and p.suffix.lower() in exts and p.name.lower().startswith(primary_prefix)]
        if product_roles.get('require_exactly_one_primary', True) and len(primary_candidates) != 1:
            errors.append(f'ProductImage 必须有且只有一张以 {primary_prefix} 开头的主产品图，当前找到 {len(primary_candidates)} 张')
        if product_roles.get('details_for_analysis_only') is not True:
            errors.append('product_image_roles.details_for_analysis_only 必须为 true')
    if engine.get('provider') != 'dreamina':
        errors.append('generation_engine.provider 必须为 dreamina')
    if engine.get('command') != 'image2image':
        errors.append('generation_engine.command 必须为 image2image')
    if engine.get('model_version') != '5.0Pro':
        errors.append('generation_engine.model_version 必须为 5.0Pro')
    if engine.get('ratio') != '1:1':
        errors.append('generation_engine.ratio 必须为 1:1')
    if engine.get('resolution_type') != '2k':
        errors.append('generation_engine.resolution_type 必须为 2k')
    if engine.get('input_mode') != 'own_product_only':
        errors.append('generation_engine.input_mode 必须为 own_product_only')
    if engine.get('competitor_image_upload', True):
        errors.append('generation_engine.competitor_image_upload 必须为 false')
    if engine.get('allow_model_fallback', True):
        errors.append('generation_engine.allow_model_fallback 必须为 false')
    if cfg.get('reference_image_role') != 'target_effect_for_reverse_engineering':
        errors.append('reference_image_role 必须为 target_effect_for_reverse_engineering')
    if cfg.get('reference_fidelity_mode') != 'full_visual_replication':
        errors.append('reference_fidelity_mode 必须为 full_visual_replication')
    for key in ('preserve_reference_marketing_copy', 'preserve_reference_promotional_copy', 'preserve_reference_layout', 'preserve_reference_props_and_effects'):
        if cfg.get(key) is not True:
            errors.append(f'{key} 必须为 true')
    if cfg.get('auto_rewrite_reference_claims') is not False:
        errors.append('auto_rewrite_reference_claims 必须为 false')
    if identity_lock.get('enabled') is not True:
        errors.append('product_identity_lock.enabled 必须为 true')
    if identity_lock.get('authority_role') != 'primary_product_image':
        errors.append('product_identity_lock.authority_role 必须为 primary_product_image')
    if identity_lock.get('prompt_marker') != '[PRODUCT_IDENTITY_LOCK]':
        errors.append('product_identity_lock.prompt_marker 必须为 [PRODUCT_IDENTITY_LOCK]')
    if identity_lock.get('preserve_source_viewpoint') is not True:
        errors.append('product_identity_lock.preserve_source_viewpoint 必须为 true')
    expected_transforms = ['uniform_scale', 'translation', 'rigid_2d_rotation', 'bounded_lighting_blend']
    if identity_lock.get('allowed_transforms') != expected_transforms:
        errors.append('product_identity_lock.allowed_transforms 必须为等比例缩放、平移、刚性二维旋转和有边界光影融合')
    if identity_lock.get('visual_qa_required') is not True:
        errors.append('product_identity_lock.visual_qa_required 必须为 true')
    if identity_lock.get('ocr_hard_gate') is not False:
        errors.append('product_identity_lock.ocr_hard_gate 必须为 false，保持 0723 非 OCR 硬门禁行为')
    if composition_lock.get('enabled') is not True or composition_lock.get('prompt_marker') != '[COMPOSITION_LOCK]':
        errors.append('composition_lock 必须启用且 prompt_marker 为 [COMPOSITION_LOCK]')
    required_composition = {'composition_archetype','visual_mass_map','negative_space_map','composition_anchor_lines','visual_flow_path','occlusion_graph','depth_layers'}
    if not required_composition.issubset(set(composition_lock.get('required_fields', []))):
        errors.append('composition_lock.required_fields 缺少构图锁必填字段')
    if composition_lock.get('competitor_packaging_structure_transfer') is not False:
        errors.append('竞品包装物理结构不得迁移')
    if source_authority.get('single_product_master') is not True or source_authority.get('same_master_product_for_multipack') is not True:
        errors.append('image2image_source_authority 必须锁定唯一产品母版与多件同母版')
    if source_authority.get('competitor_image_upload') is not False:
        errors.append('image2image_source_authority.competitor_image_upload 必须为 false')
    if lighting_boundary.get('enabled') is not True:
        errors.append('lighting_application_boundary 必须启用')
    protected_lighting = {'package_base_color','printed_content','logo_color','label_boundary','material_base','opacity'}
    if not protected_lighting.issubset(set(lighting_boundary.get('protected', []))):
        errors.append('lighting_application_boundary.protected 缺少包装保护字段')
    if visibility_zone.get('enabled') is not True:
        errors.append('core_visibility_zone 必须启用')
    for required_block in ('composition_lock','lighting_application_boundary','core_visibility_zone','multiproduct_identity_consistency'):
        if required_block not in qa_policy.get('blocking', []):
            errors.append(f'qa_policy.blocking 必须包含 {required_block}')
    if not execution_log.get('enabled') or not execution_log.get('per_task') or not execution_log.get('batch_summary'):
        errors.append('execution_log 必须启用 per_task 与 batch_summary')
    if qa_policy.get('decision_levels') != ['PASSED', 'PASSED_WITH_NOTES', 'REJECTED']:
        errors.append('qa_policy.decision_levels 必须包含 PASSED/PASSED_WITH_NOTES/REJECTED')
    if 'product_identity_lock' not in qa_policy.get('blocking', []):
        errors.append('qa_policy.blocking 必须包含 product_identity_lock')
    generate_num = engine.get('generate_num', 1)
    if not isinstance(generate_num, int) or not 1 <= generate_num <= 10:
        errors.append('generation_engine.generate_num 必须是 1-10 的整数')
    elif generate_num != 1:
        errors.append('标准流程 generation_engine.generate_num 必须为 1')
    if not engine.get('warn_before_credit_use', True):
        warnings.append('建议开启 warn_before_credit_use，避免未提示即提交付费生成')
    if not cleanup.get('enabled', False):
        errors.append('run_cleanup.enabled 必须为 true，确保每次 RUN 前清理旧批次')
    if not cleanup.get('archive_records_before_cleanup', False):
        errors.append('run_cleanup.archive_records_before_cleanup 必须为 true，确保旧记录先归档')
    if not cleanup.get('clear_records', False):
        errors.append('run_cleanup.clear_records 必须为 true')
    if output_policy.get('final_images_only') is not True:
        errors.append('output_policy.final_images_only 必须为 true')
    if output_policy.get('final_name_suffix') != '_final':
        errors.append('output_policy.final_name_suffix 必须为 _final')
    if output_policy.get('move_non_final_to_records') is not True:
        errors.append('output_policy.move_non_final_to_records 必须为 true')
    history_dir = resolve_path(cfg.get('history_dir', 'history'))
    try:
        history_dir.resolve().relative_to(ROOT.resolve())
    except ValueError:
        errors.append(f'history_dir 必须位于项目内: {history_dir}')
    try:
        records_dir.resolve().relative_to(ROOT.resolve())
    except ValueError:
        errors.append(f'records_dir 必须位于项目内: {records_dir}')
    out_dir.mkdir(parents=True, exist_ok=True)
    tasks_dir.mkdir(parents=True, exist_ok=True)
    records_dir.mkdir(parents=True, exist_ok=True)
    result = {
        'status': 'FAILED' if errors else ('PASSED_WITH_WARNINGS' if warnings else 'PASSED'),
        'errors': errors,
        'warnings': warnings,
        'competitor_count': comp_count,
        'product_count': prod_count,
        'output_dir': str(out_dir),
        'tasks_dir': str(tasks_dir),
        'history_dir': str(history_dir),
        'records_dir': str(records_dir),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0

if __name__ == '__main__':
    raise SystemExit(main())
