# 目标效果图复刻 Prompt 规则

## 分离与组装顺序

分析文档与提交 Prompt 必须物理分离。提交 Prompt 只包含可执行画面指令，禁止混入角色设定、分析步骤、置信度、用户确认、QA和输出格式说明。

固定顺序：

1. `[PRODUCT_IDENTITY_LOCK]`、保护清单与唯一产品母版声明。
2. `lighting_application_boundary`。
3. `[COMPOSITION_LOCK]`。
4. `subject_occupancy_lock` 与多商品一致性。
5. `core_visibility_zone`。
6. `product_adjacent_detail_inventory` 中的 KEY 项。
7. `layout_regression_lock` 与全部画外文字。
8. 场景、人物、道具、特效和镜头。
9. 字体与限定配色。
10. 精简竞品排除项和通用负面约束。

产品身份锁必须位于 Prompt 首部。推荐 900–1600 个中文字符，硬上限 2000；不设最低长度，不为凑长度重复约束。超限时优先删除重复形容词和非核心装饰，不得删减产品身份、构图、主体坐标、核心文案和 KEY 细节。

## 产品身份与图生图边界

- 图片1是唯一产品外观母版；竞品图不上传即梦，产品详情图只供本地核对。
- Prompt 首段使用 [product-identity-lock.md](product-identity-lock.md) 的固定段，并紧接 `protected_texts / protected_logo / geometry_anchor / material_anchor / viewpoint_anchor` 实际值。
- 竞品瓶型、管型、瓶盖、泵头、厚度、标签、品牌色和包装图案不可迁移；竞品只提供二维构图关系。
- 光影只允许改变自然高光、明暗过渡、轮廓光、接触阴影和落地投影；不得改变包装底色、Logo颜色、印刷内容、标签边界、材质本色或透明度，不得套场景统一滤镜。
- 微型不可辨说明尽最大程度保留位置、行数、颜色和印刷密度，不主动改写、不虚构可读内容。

## 构图锁

- 按 [composition-lock.md](composition-lock.md) 写入 `composition_archetype / visual_mass_map / negative_space_map / composition_anchor_lines / visual_flow_path / occlusion_graph / depth_layers`。
- 构图类型不能代替具体关系；禁止只写“中心构图”“三分构图”“与参考图一致”。
- 不因 1:1 画布自动居中或对称，不用“主体40%–60%”“必须留白”等通用原则覆盖目标图事实。
- 辅助人物、矿石、花朵、泡沫和道具不得抢占目标图第一视觉落点。

## 主体占比与多商品一致性

- 写明每件商品 `left/top/right/bottom`、高度、边界框面积、可见面积、二维方向和出框方向；多商品写总面积、间隙、重叠率、遮挡率和前后层级。
- `full_bleed_mode=true` 时写入高度95%–110%、允许顶部或底部轻微出框、双商品可见间隙0%–2%，同时保持真实宽高比。
- 多商品写入 `same_master_product=true`：包装、颜色、Logo、品名、规格和标签完全同款，只允许整体大小、位置、前后层级和安全二维倾角不同。
- 二维倾角按目标方向和幅度使用动态安全区间；常规建议0°–15°，文字密集或已出现失真风险时收敛到0°–8°，不设统一5°硬上限。
- 不得为完整展示包装而静默缩小，不得用拉伸、压缩、透视或三维重建换取占比。

## 核心可见区

分别写明 `logo_zone / product_name_zone / specification_zone / primary_pattern_zone` 的坐标及允许遮挡比例。手指、泡沫、徽章、强高光和其他产品不得错误遮挡；前件只按目标图遮挡后件非核心区域。

## 产品邻接细节

- 每个细节记录 `source_class / transfer_policy / 显著度`。只将 `KEEP` 和 `KEEP_WITH_BOUNDARY` 写入正向 Prompt。
- `competitor_packaging_content + REJECT` 写入精简竞品排除项，不得作为场景细节迁移。
- 每个 KEY 项独立描述准确材质、相对产品位置、覆盖范围、密度/尺度、透明度、前后层级及接触或遮挡关系。
- 禁止用“丰富细节”“自然融合”概括泡沫、水珠、液体、倒影或接触阴影。

## 版式回归锁

- 每条首轮和重试 Prompt 完整列出标题、数字、标点、换行、填充、描边、阴影、字体、字号层级、坐标、底框、图标数量、徽章和底部通栏。
- 每个框体按目标图实际属性写“正向描述 + 差分反向禁止”，包括形状、圆角、透明度、描边、阴影、渐变和外发光；不得统一禁止目标图本来存在的属性。
- 逐区记录文字与产品的真实层级，不得统一假定全部画外文字位于产品上层。
- 重试不得写“保持上一轮不变”“沿用正确内容”“只修改产品大小”；必须完整重申产品身份、构图、占比和版式锁。

## 字体与限定配色

- 画外文字默认1种字体，硬上限2种；首选PDDZHT，无法准确调用时使用拼多多正黑体风格粗黑无衬线体。只有目标图存在重要第二字体层级时启用第二种。
- 包装原生字体不计入画外字体数量，禁止修改或替换。
- 只允许映射画外文字的填充/描边/阴影和底部框体的填充/边框/原有渐变色。产品、背景、人物、道具、图标和特效不得借配色优化改色。
- 每个可变颜色记录“目标原色 → 产品取样色 → 最终映射色”，保持清晰对比。

## 竞品排除与负面约束

建立精简 `competitor_exclusion_terms`：只列显著且易误迁移的竞品品牌、Logo、规格、物理结构、主色和标签特征，不无限枚举微型文字，不重复同一负面词。正向产品身份描述优先于负面清单。

追加禁止项：额外商品、产品拉伸压缩弯曲、三维视角改变、透视变换、局部旋转、包装重绘、产品换色、场景滤镜染色、Logo扭曲、核心文字错漏增笔、伪文字、主体虚焦、错误材质、核心文案错字、乱码、水印和二维码。

## 提交前覆盖门禁

逐项核对：

- `PRODUCT_IDENTITY_LOCK` 位于首段并含完整保护清单。
- 存在 `image2image_source_authority / lighting_application_boundary`。
- 存在完整 `composition_lock / subject_occupancy_lock / core_visibility_zone`。
- 多商品存在 `same_master_product=true`。
- 每个 KEY 邻接细节均有可执行片段，竞品包装内容均为 REJECT。
- 每个画外文字和框体均进入 `layout_regression_lock`。
- Prompt 未出现角色设定、分析步骤、用户确认或 QA 元指令。
- 不出现“参考原图”“类似竞品”“保持其他不变”等弱表达。
