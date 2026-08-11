---
name: pdd-full-replica
description: Run high-fidelity Pinduoduo competitor-image reconstruction with Dreamina 5.0Pro at 1:1 and 2K through a numbered two-mode entry: “1. 拼多多全复刻模式” for target-product-only upload with local competitor analysis, or “2. 竞品双参考高精度模式” for target-product plus competitor-image guidance and bounded product-palette adaptation. Use when the user invokes $pdd-full-replica or names either mode. A bare invocation presents only the two numbered choices; once selected, the skill automatically archives/resets prior runs and, after the single conflict/retention confirmation, proceeds directly to paid generation and bounded hard-failure retries without further confirmation.
---

# 拼多多全复刻模式

把本技能视为 2026 年 7 月 23 日 14:21 节点的独立实验分支。不要修改或调用当前 `$pdd-product-image-studio`，不要混入其 OCR 硬门槛、版式槽位合同、昆虫替换策略或双重积分预算逻辑。本技能仅移植兼容的产品身份锁定层，并独立固定使用 2K 输出。

## 固定输入与输出

- 目标效果图：`C:\Users\admin\Desktop\拼多多产品数据整理\EnterImage`
- 自有产品图：`C:\Users\admin\Desktop\拼多多产品数据整理\ProductImage`
- 最终图：`C:\Users\admin\Desktop\拼多多产品数据整理\OutputIamge`
- 技能内部记录：相对于本技能目录的 `tasks`、`run_records`、`history`
- 标准模式中，`EnterImage` 只用于视觉反推，不上传即梦。
- “竞品双参考高精度模式”中，`EnterImage` 与主产品图同时上传即梦；竞品图只提供二维构图与非产品场景，产品图仍是产品身份的唯一事实来源。
- `ProductImage` 中以 `00_` 开头的唯一图片是全部任务的主产品图与唯一 Dreamina 图片输入，也是包装、LOGO、标签位置、原生文字、产品几何、颜色和可见材质的唯一身份权威；其余图片作为产品细节事实图，仅供本地分析，不上传即梦。

## 0723 复刻合同

1. 把每张 `EnterImage` 当作目标成图，不是宽泛风格参考。
2. 完整复刻目标图的排版、画外宣传文案、营销文案、数字、标点、换行、字体类别、字号层级、字重、描边、阴影、界面结构、场景、道具、特效、光影、镜头和氛围。
3. 仅将竞品商品替换成 `ProductImage` 中的真实产品；产品外形、品牌、包装、主图案、主要参数、净含量、可辨识主印刷信息和原始颜色以产品图为准。
4. 标准单参考模式只允许把画外字体的填充色、描边色、阴影色，以及底部框体或通栏的填充色、边框色和已有渐变色映射到产品包装色板。竞品双参考高精度模式按 [dual-reference-high-precision-mode.md](references/dual-reference-high-precision-mode.md) 启用“限定配色适配”：在构图、结构、材质、纹理、光源和渐变方向不变的前提下，额外允许背景色系与徽章/勋章色系适配产品色板；产品、人物、道具和邻接细节仍不得被统一调色。
5. 默认保留竞品画外促销与营销文案，不主动改写或删减。若出现明确第三方商标、店铺名、价格、认证、赠品或与自有产品事实冲突的规格，先暂停并向用户确认。
6. 固定生成参数：`dreamina image2image / 5.0Pro / 1:1 / 2k / 1张`。标准模式只上传主产品图；用户明确说“竞品双参考高精度模式”时，按 [dual-reference-high-precision-mode.md](references/dual-reference-high-precision-mode.md) 同时上传竞品图与主产品图。禁止改用 1K、其他模型或本地拼图，除非用户明确调整实验变量。
7. 坚持由 Dreamina 单次图生图完成融合成图；不使用本地抠图、局部覆盖、包装替换、文字重绘或生成后修补。严格执行 [product-identity-lock.md](references/product-identity-lock.md)：产品允许整体等比例缩放、平移、自然光影融合，以及不改变源图观察视角的刚性二维平面旋转；不得改变透视、厚度、正背面关系、标签排版或补画未知侧面。核心包装结构、Logo、可辨认包装文字、品名、主要参数和主图案必须与 `ProductImage` 一致；无法可靠辨认的微型印刷文字尽最大程度保留，不作为自动硬拒绝项。
8. 严格执行 [font-policy.md](references/font-policy.md)：每张成图的画外文字最多使用 2 种字体，这是硬约束；首选拼多多正黑体（PDDZHT），模型无法准确调用时改用“拼多多正黑体风格的粗黑无衬线体”。产品包装原生字体属于产品身份的一部分，不计入画外字体数量，也不得为满足字体上限而改写。
9. 严格执行“主体占比锁”：从目标图逐件测量商品顶部、底部、左右边界、宽高、边界框面积、总商品面积、双商品间隙、重叠率和出框程度，并写入分析、Prompt 与 QA。用户要求“撑满”“放大主体”“和参考产品一样大”时自动启用满版模式：商品建议高度 95%–110%，允许顶部或底部轻微出框，双商品可见间隙建议 0%–2%；始终保持真实宽高比，不得用拉伸、压缩或三维视角重建换取占比。
10. 严格执行“版式回归锁”：任何产品大小、位置、间隙或遮挡重试都必须重新逐项列出标题文字及填充/描边/阴影、标签底框、图标数量、宣传文案、字体规则和框体结构。禁止使用“保持上一轮不变”“沿用已正确内容”等弱指令代替完整约束。产品占比修复成功但标题、图标、文案、颜色或框体走样时仍为 `REJECTED`。
11. 严格执行 [composition-lock.md](references/composition-lock.md)：竞品只提供二维构图关系，不提供包装结构。记录构图类型、视觉质量分布、留白地图、锚线、视线路径和遮挡图；禁止因 1:1 画布自动改成中心或对称构图，禁止用通用“主体40%–60%”“必须留白”等美学规则覆盖目标图事实。
12. 图生图产品权威、光影边界和核心可见区属于提交硬门禁：`00_` 主产品图是唯一产品母版；光影只能改变自然高光、明暗过渡、轮廓光、接触阴影和投影，不得改变包装底色、印刷、Logo颜色或材质本色；Logo、品名和规格核心区不得被泡沫、手指、强高光、徽章或其他产品错误遮挡。

## 模式选择（编号入口）

本技能只提供以下两个执行模式：

1. **拼多多全复刻模式**（内部名：`standard_single_reference`）
   - 竞品图只在本地用于视觉反推与像素测量；提交即梦时仅上传 `ProductImage/00_` 主产品图。
   - 适合优先保护产品包装、品牌、文字和颜色稳定性的常规全复刻任务。
   - 使用标准构图 QA；允许的画外配色适配范围遵循通用规则。
2. **竞品双参考高精度模式**（内部名：`dual_reference_high_precision`）
   - 提交即梦时同时上传目标产品图与竞品图，以竞品图锁定二维构图、角度、占比、遮挡和版式骨架。
   - 上传顺序固定为：图片 1 = 目标产品身份母版，图片 2 = 竞品二维构图母版；不得反转。
   - 使用宽容构图 QA：像素测量用于诊断和 Prompt 引导，不把坐标、底栏高度、字号比例的小到中等偏差直接判为失败。产品身份、冲突映射、核心文案、商品数量和整体构图骨架仍为硬约束。
   - 默认启用限定配色适配：背景色系、画外文字色、横幅色与徽章/勋章色从目标产品色板取样；只换颜色属性，不改轮廓、坐标、占比、材质、纹理、圆角、分区、图标、光影方向和渐变结构。产品包装保持原色。用户要求完全保留竞品原配色时，关闭本项。
   - 商品仍位于参考图同一主要区域、主次关系与阅读顺序未改变时，边界未完全贴边、左右留白差异、标题字号或底栏高度的小到中等偏差只记 `NOTE`，不得为此自动付费重试。

### 入口判定（硬约束）

- 用户仅调用 `$pdd-full-replica`，且同一条消息没有模式编号、模式名称或明确的单双参考意图时，不得归档、重置、扫描或调用即梦，只输出：

  ```text
  请选择使用模式：

  1. 拼多多全复刻模式
     仅上传目标产品图；竞品图只在本地反推，产品身份更稳。

  2. 竞品双参考高精度模式
     同时上传目标产品图和竞品图，更适合锁定构图、角度、占比和遮挡。

  回复“1”或“2”即可。
  ```

- `1`、`模式1`、`拼多多全复刻模式`、`全复刻模式`、`标准单参考模式`均映射到模式 1。
- `2`、`模式2`、`竞品双参考高精度模式`、`双参考高精度模式`、`双参考`均映射到模式 2。
- 用户在调用技能的同一条消息中已经写明编号、模式名称或明确要求“只上传目标产品图/同时上传目标产品图和竞品图”时，直接选定对应模式，不显示菜单，也不再询问模式确认。
- 模式被选定后，立即进入自动归档、重置和预检；模式选择只对当前批次有效。下一次裸调用仍显示两个编号选项。
- 模式选择属于入口路由，不计入后续唯一一次“冲突替换与原样保留”确认，也不触发积分消耗。

## 精简用户输出协议（硬约束）

内部预检、自动归档重置、图像分析、冲突映射、Prompt 生成、Dreamina 查询、QA、重试与日志必须完整执行。裸调用时，用户可见流程允许先出现一次编号模式选择；模式确定后只保留“一次冲突/保留确认”和“最终交付”。

### 内部阶段：自动归档、重置与预检

- 只有模式确定后，才自动归档上一批记录并重置；不得再询问“是否确认归档并重置”。
- 归档和重置成功后直接预检并分析；正常情况不单独播报。
- 预检失败时简要报告阻断原因与保留状态，不展开内部检查过程。

### 唯一用户确认：扫描、冲突替换与原样保留

- 只列出确实需要用户决定的第三方商标、店铺名、价格、认证、赠品、规格或产品事实冲突，以及拟采用的替换/保留方式。
- 同一条消息须明确说明其余无需处理的画外声明将全部原样保留。
- 即使没有冲突，也输出一次扫描结论，明确“其余画外声明全部原样保留”，让用户确认整体版式、替换项与保留项。
- 用户已经逐项给出替换与保留方案，或回复“确认上述处理方式/确认保留执行”等同义表达时，视为唯一确认已完成；不得重复询问。
- 同一条确认消息可告知任务数、模式、固定参数、预计积分和当前余额，但只能请求用户确认冲突替换与原样保留，不能另设付费确认。

### 确认后自动付费生成

- 用户完成冲突/保留确认后，立即执行 Dreamina 生成；不得再询问“确认提交并执行生成”。
- 该唯一确认长期覆盖本批首轮提交及技能合同内最多两次自动重试。任务数、固定参数、预计积分和余额属于信息披露，不构成第二次确认门槛。
- 生成期间默认静默：不播报常规提交成功、排队、查询中、下载中、逐文件分析、内部文件落盘或无变化轮询。
- 仅在以下异常或成本变化节点输出 commentary：`QA 不通过且即将自动重试`、`登录失效`、`需要合规确认`、`余额不足`、`参数不支持`、`连续两次远端调用无有效 submit_id`。QA 重试消息只包含失败证据、将修改的 Prompt 片段和预计新增积分。
- 用户主动询问进度时，提供一次简短状态快照，不因此恢复逐步播报。

生成成本信息只作告知，例如：`已按确认方案进入生成：N 个任务，5.0Pro / 1:1 / 2K；首轮预计 X 积分，含硬失败重试最高 Y 积分；当前余额 Z。`

### 最终交付

- final 只展示最终选中图片，并汇总任务数、`PASSED / PASSED_WITH_NOTES / REJECTED` 数量、总尝试次数、实际积分、余额和输出路径。
- 不在 final 重复分析过程、完整 Prompt、常规轮询记录或用户已经确认过的处理方案；只有未完成任务才补充最短阻断说明。

### 禁止的交互膨胀

- 禁止逐文件播报“正在读取/正在分析/已写入”。
- 禁止反复报告没有变化的远端状态。
- 禁止把内部 A–E 分析文档、锁定字段、完整 Prompt 或 QA 清单默认展开给用户；用户明确要求查看时再提供。
- 禁止索取归档确认或付费确认；除裸调用所需的一次编号模式选择外，每批只允许索取一次扫描后的冲突/替换/保留确认。
- 精简交互不得省略任何内部硬门禁，也不得把 `REJECTED` 图片作为最终图交付。

## 执行

先完整读取以下规则：

- [analysis-schema.md](references/analysis-schema.md)
- [composition-lock.md](references/composition-lock.md)
- [product-identity-lock.md](references/product-identity-lock.md)
- [text-mapping-rules.md](references/text-mapping-rules.md)
- [color-adaptation-rules.md](references/color-adaptation-rules.md)
- [font-policy.md](references/font-policy.md)
- [prompt-rules.md](references/prompt-rules.md)
- [dreamina-agent-workflow.md](references/dreamina-agent-workflow.md)
- [qa-checklist.md](references/qa-checklist.md)
- [execution-log-schema.md](references/execution-log-schema.md)
- 选择“竞品双参考高精度模式”时，再完整读取 [dual-reference-high-precision-mode.md](references/dual-reference-high-precision-mode.md)。

需要三瓶装示范时再读取 [example-slek-three-pack.md](references/example-slek-three-pack.md)。

将包含本文件的目录记为 `<SKILL_DIR>`，然后依次执行：

```powershell
python "<SKILL_DIR>\scripts\reset_run.py"
python "<SKILL_DIR>\scripts\validate_batch.py"
python "<SKILL_DIR>\scripts\prepare_batch.py"
```

预检失败时停止，不清理新输入，也不调用即梦。预检通过后逐张生成：

- `<stem>_analysis.md`
- `<stem>_prompt_attempt1.txt`
- `<stem>_dreamina_attempt1.json`
- `<stem>_qa_attempt1.md`
- `<stem>_execution.md`

写 Prompt 前先从 `00_` 主产品图建立产品身份保护清单：逐字记录可辨认的品牌、品名、规格、净含量、关键参数和标签文字；另行记录 LOGO 的轮廓、颜色、位置与比例，以及产品轮廓、结构、材质和源图观察角度。该清单必须写入分析文件，并逐项进入 `[PRODUCT_IDENTITY_LOCK]` 段；缺失时不得提交。

同时建立 `image2image_source_authority / lighting_application_boundary / composition_lock / core_visibility_zone`。竞品瓶型、管型、瓶盖、泵头、标签和包装图案不得作为可复刻结构；只能提取其数量、边界框、二维方向、展示大小、层级、遮挡和接触关系。

完成唯一的冲突/保留确认后，直接按 `dreamina-cli` 的帮助与登录规则调用即梦；不得增加付费确认。登录失效时完成登录并明确报告成功。

## Prompt 原则与固定顺序

- 最终提交 Prompt 只包含可执行画面指令；分析、角色设定、步骤、置信度、用户确认和 QA 说明仅留在分析文档，绝不混入即梦 Prompt。
- Prompt 按以下顺序组装：`[PRODUCT_IDENTITY_LOCK]` 与唯一母版声明 → 光影边界 → `[COMPOSITION_LOCK]` → `subject_occupancy_lock` → `core_visibility_zone` → KEY 邻接细节 → `layout_regression_lock` 与全量画外文字 → 场景/人物/镜头 → 字体和限定配色 → 精简竞品排除项及通用负面约束。
- 产品段必须位于 Prompt 首部，并紧接着逐字列出保护文字清单、LOGO 描述、结构/材质/主色锚点和源图观察角度；不得只写“文字正确”或“产品一致”。
- 逐区写明每个可见元素和每段精确文字，不使用“同参考图”“类似竞品”等模糊替代词。
- 每条 Prompt 必须明确写入画外字体上限、PDDZHT 首选与粗黑无衬线回退；包装原生字体排除在计数之外。
- 保留目标图原有数量关系、坐标、占比、前后层级、背景结构、软装、道具、特效和光影关系；双参考模式只按其限定配色适配规则改变允许的颜色属性。
- 单独建立并写入 `product_adjacent_detail_inventory`：逐件检查产品顶部、左右轮廓、瓶底/落点、接触面和前后遮挡区，识别泡沫、水珠、水花、粉末、颗粒、液体、烟雾、光圈、倒影、接触阴影及其他贴近产品的细节；不得把泡沫误并入毛巾、云雾或普通高光。关键邻接细节必须进入 Prompt 和 QA。
- 写入产品事实锁、产品原色锁和多件商品同母版约束；多件商品只允许尺寸、位置、前后层级和安全二维倾角不同。
- `composition_lock` 不得只写“中心构图/三分构图”；必须落地为视觉质量、留白、锚线、阅读路径、前中后景与遮挡关系。
- `subject_occupancy_lock` 写明逐件边界框、商品高度、单件/总面积占比、双商品间隙、重叠率和出框方向；满版模式明确“高度95%–110%、间隙0%–2%、允许轻微出框、保持真实宽高比”。
- `core_visibility_zone` 分别保护 Logo、品名、规格和主图案区，明确每个前景元素的允许/禁止遮挡边界。
- 产品尺寸或姿态重试时启用 `layout_regression_lock`，完整重申全部标题、填充色、描边色、阴影、标签底框、图标数量、宣传文案、字体与框体结构；不得写“保持上一轮不变”。
- 每项允许适配的元素记录“目标原色 → 产品取样色 → 最终映射色”。标准模式仅记录画外文字与底部框体；双参考模式还记录背景色系和徽章/勋章色系，并证明其结构、材质与光影未改变。
- 框体使用“实际属性正向描述 + 差分负向约束”，按目标图真实圆角、描边、阴影、透明度和渐变生成；禁止统一套用“无圆角/无描边”。
- 画外字体默认 1 种、硬上限 2 种；只有目标图存在重要第二字体层级时才启用第二种。
- Prompt 推荐 900–1600 个中文字符，硬上限 2000；不为凑长度重复约束。
- 禁止额外商品、产品变形、重新设计包装、错误品牌、核心包装文字错乱、Logo 扭曲、主要参数改写、核心文案错字、乱码、水印和二维码。

## 0723 QA 与重试

以下为标准模式 QA。启用“竞品双参考高精度模式”时，必须改用 [dual-reference-high-precision-mode.md](references/dual-reference-high-precision-mode.md) 的宽容 QA 分级；不得把标准模式的像素构图硬门槛覆盖到双参考模式。

- 同时对照目标图和产品图，检查商品结构、产品主事实、核心营销文字、排版与界面结构、产品原色、限定配色、场景和商业氛围。
- 对照 `product_adjacent_detail_inventory` 检查产品邻接细节：承担落地、遮挡、卖点表达或主要视觉质感的关键泡沫、水珠、颗粒、液体、光效等若完全缺失或被替换成另一种材质，即 `REJECTED`；低显著度细节的数量、密度或形状小幅差异记为 `NOTE`。
- 单独清点画外字体：超过 2 种即 `REJECTED`；未准确呈现 PDDZHT 但使用了“拼多多正黑体风格的粗黑无衬线体”且总数不超过 2 种，可继续按其他 QA 项判定。包装原生字体不参与该计数。
- 对照身份保护清单逐区检查：产品轮廓与比例、瓶盖/喷头/盒体结构、LOGO 轮廓及位置、每条可辨认保护文字、标签边界、材质、清晰度和源图观察视角；允许整件产品及其包装文字同步进行刚性二维平面旋转，任一核心项拉伸、扭曲、错字、漏字、增笔、错位、模糊或虚焦即 `REJECTED`。
- 对照 `subject_occupancy_lock` 检查顶部、底部、宽度、单件/总面积、间隙、重叠率和出框程度；满版任务若主体仍明显偏小、双商品分散或留有超过目标图的大块空隙即 `REJECTED`。不得为通过占比检查接受产品变形。
- 对照 `layout_regression_lock` 逐项回归标题颜色与描边、标签底框、图标数量、文案、字体和框体。任一原本正确项在尺寸重试后走样，结论仍为 `REJECTED`。
- 对照 `composition_lock` 检查商品组、标题区、徽章区和底栏区的视觉质量、留白、锚线、阅读顺序及遮挡关系；通用美学更“好看”但偏离目标构图时仍为 `REJECTED`。
- 对照 `lighting_application_boundary` 检查产品是否被场景染色、统一滤镜、强光洗掉包装文字或改变材质本色；任一发生即 `REJECTED`。
- 对照 `core_visibility_zone` 检查 Logo、品名和规格是否被手、泡沫、徽章、强高光或前件错误覆盖。
- 使用 `PASSED / PASSED_WITH_NOTES / REJECTED`。无法可靠辨认的包装微型说明属于提示项，不启用现代 OCR 自动硬拒绝；产品品牌、品名、主要参数和核心包装图案明显错误仍是阻断项。
- `PASSED_WITH_NOTES` 可进入最终输出，这是 0723 节点的原始行为。
- `REJECTED`、提交失败、查询失败或生成失败自动进入重试；每任务最多重试 2 次，总计最多 3 次付费尝试。只修改失败对应的 Prompt 片段，任一轮通过后立即停止。
- 自动重试前在 commentary 说明失败证据、Prompt 差异和预计新增积分；初次确认后不再次等待确认，但登录、合规、余额不足、参数不支持或连续两次无有效 `submit_id` 时停止。

## 收尾

把分析、Prompt、JSON、QA、日志和候选图全部留在 `run_records`。只把最终选中的 `PASSED` 或 `PASSED_WITH_NOTES` 图片复制为 `OutputIamge/<任务名>_final.png`，然后执行：

```powershell
python "<SKILL_DIR>\scripts\finalize_output.py"
```

确认 `OutputIamge` 只包含 `_final` 图片，并报告任务数、通过/提示通过/拒绝数、尝试次数、实际积分、余额和输出路径。
