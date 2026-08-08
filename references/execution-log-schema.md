# 详细执行日志格式

每个任务在 `run_records` 生成 `xxx_execution.md`，不得写入 `OutputIamge`，不得只写“已生成”。

## 日志结构

1. 任务元数据：任务 ID、时间、目标效果图、产品事实图、配对规则和输出路径。
2. 输入预检：像素、格式、透明背景、可读性、异常与处理。
3. 反推逻辑：主体、文字、风格、色彩、光影、构图、镜头、材质和分辨率；列出关键发现、置信度和冲突项。
4. 产品身份、图生图母版与光影边界：记录 `protected_texts / protected_logo / geometry_anchor / material_anchor / viewpoint_anchor / image2image_source_authority / lighting_application_boundary`；确认图片1为唯一母版，竞品包装结构不可迁移；记录允许的等比缩放、平移、有边界光影融合和刚性二维旋转。
5. 构图、主体占比与核心可见区：记录 `composition_archetype / visual_mass_map / negative_space_map / composition_anchor_lines / visual_flow_path / occlusion_graph / depth_layers`，以及逐件 `subject_occupancy_lock / core_visibility_zone`；多件记录 `same_master_product`、总面积、间隙、重叠率和遮挡率。
6. 邻接细节：逐项记录 `source_class / transfer_policy / KEY-SUPPORTING-MICRO`、位置、材质、层级、覆盖和遮挡边界；竞品包装内容必须为 REJECT。
7. 颜色适配：产品色板、取样区域和 HEX；每个可变画外元素记录 `目标原色 → 产品取样色 → 最终映射色`。
8. Prompt 组装：证明固定顺序、元指令隔离、完整四锁、框体差分负约束、字体规则、精简竞品排除项和字符上限均通过。
9. 生成配置：Dreamina 命令、模型、比例、分辨率、数量、唯一图片输入、帮助命令和积分检查。
10. 提交与查询：按 attempt 记录时间、`submit_id`、状态、积分、下载路径和失败信息。
11. 后置 QA：逐项核验产品身份、构图、占比、核心可见区、邻接细节、光影边界、原色、字体、文案、框体、图标和场景，分别给出可见证据及 `PASSED / NOTE / REJECTED`。
12. 自动重试：记录上一轮证据、Prompt差异、预计/实际新增积分、上限和停止原因；完整重申产品身份、构图、占比和版式锁。
13. 最终交付：记录选中 attempt、分析/Prompt/JSON/QA 路径及最终图绝对路径。

批次另生成 `batch_execution_summary.md`，汇总任务数、成功/带提示/拒绝数量、积分、提交 ID、输出路径与未解决问题。
