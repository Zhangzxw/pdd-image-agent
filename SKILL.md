---
name: pdd-full-replica
description: Run high-fidelity Pinduoduo dual-reference reconstruction with Dreamina 5.0Pro at 1:1 and 2K. Use the target product as the only identity and geometry authority while matching competitor composition, typography, high-key luminance, product lighting, and bounded color adaptation. A bare invocation automatically archives/resets, requests one conflict/retention confirmation, then generates with adaptive region-based luminance QA and bounded hard-failure retries.
---

# 竞品双参考高精度复刻

将每张竞品图视为目标视觉构图母版：复刻构图、人物、场景、画外文案槽位、主体数量、位置、大小、姿态、透视、重叠、底栏和阅读顺序；只把竞品商品替换为目标产品。固定上传顺序为：图片1=`ProductImage/00_` 目标产品身份母版，图片2=当前 `EnterImage` 竞品构图与姿态母版。图片2绝不提供产品包装事实。

## 固定目录与参数

- 竞品图：`C:\Users\admin\Desktop\拼多多产品数据整理\EnterImage`
- 产品图：`C:\Users\admin\Desktop\拼多多产品数据整理\ProductImage`
- 最终图：`C:\Users\admin\Desktop\拼多多产品数据整理\OutputIamge`
- 内部记录：技能目录下 `tasks / run_records / history`
- 参数：`dreamina image2image / 5.0Pro / 1:1 / 2k / 1张`
- `00_` 开头的唯一图片是产品包装、Logo、原生文字、几何、主色、材质与观察角度的唯一权威；其他产品详情图只供本地事实核对，不上传。
- 禁止本地抠图、覆盖、补字、包装合成或生成后修补；每轮由 Dreamina 完成整张图。

## 入口与用户交互

- 用户调用 `$pdd-full-replica` 后直接进入本工作流，不显示模式菜单，不要求模式编号。
- 立即自动归档上一批并重置，然后校验、建任务和扫描图片；不得询问归档确认。
- 每批只保留一次用户确认：完成内部分析后，必须按 [adjustment-confirmation-template.md](references/adjustment-confirmation-template.md) 输出可直接编辑的逐图调整清单。逐张列出商品替换、第三方元素、每条可见文案、人物/道具、背景/构图和光影的`修改为 / 删除 / 保留`动作；同一条消息明确“其余不冲突内容原样保留”。不得用分析摘要、表格或笼统的“清理竞品元素”代替该清单。
- 用户逐项给出方案或回复确认后，直接提交即梦；不得追加付费确认。该确认覆盖首轮和每任务最多2次硬失败重试。
- 生成期间默认静默。只在硬失败即将重试、登录/合规/余额/参数异常或连续两次无有效 `submit_id` 时输出简短状态。
- final 展示最终图片，并汇总任务数、`PASSED / PASSED_WITH_NOTES / REJECTED`、尝试次数、实际积分、余额和输出路径。

## 用户可编辑调整清单

- 生成前的详细视觉诊断、坐标、亮度数据、风险评级和包装拓扑写入内部记录；除非用户主动索要，不把这些分析术语堆入确认消息。
- 用户可见确认消息按图片顺序使用`1. 图1：`、`2. 图2：`。每图先写商品替换与包装结构，再写第三方品牌/账号/价格/认证，然后逐条写画外文案，最后写人物、场景、道具、构图、背景和光影。
- 每个动作单独成行，使用可编辑短句：`“原文”修改为“建议文案”`、`“原文”保留`、`删除“原文/元素”`、`竞品商品替换为目标产品`。同一句不得混合两个相反动作。
- 原图可辨文字必须逐字引用，包括数字、百分号、规格、账号、标点和英文；多个不同区域不得合并成“其他文案”。无法确认的字符标为`[原文局部不可辨]`并给出处理建议，不得猜写成事实。
- 建议替换文案必须来自目标产品可确认事实或明确标为建议；不得默认替用户删除其可能希望保留的强钩子。第三方事实冲突仍应明确建议删除或替换，等待用户在同一清单中改写。
- 每图末尾用一句话集中列出要保留的构图骨架、人物、场景、道具和光影；需要配色适配时写清具体背景区域和方向，不只写“适配产品”。
- 所有图片之后追加一条共同限制，概括不新增的价格、认证、赠品、浓度、店铺或未经确认声明；最后只问：`请直接修改以上清单，或回复“确认”后生成。`

## 竞争视觉诊断闭环

- 扫描图片后、汇总冲突映射前，完整执行 [competitive-visual-analysis.md](references/competitive-visual-analysis.md) 的生成前分析：包装风格定调、0.3秒视觉路径、卖点钩子、手机缩略图前三抓眼元素、七类细节风险和P0–P3优化队列。
- 每个结论必须引用图中具体元素、区域、文字、颜色、占比、人物、道具或光影，不得泛泛评价“高级感”“专业感”。
- 生成前只能对比竞品可见事实、目标产品身份约束和拟采用的复刻策略；不得把未生成图片写成真实结果。
- 用户确认后，把不改变产品事实、确认文案和构图骨架的P0/P1安全优化转成可执行Prompt；分析角色、步骤、评级和解释不得进入Prompt。
- 候选图下载后，用同一框架对真实成图复盘，逐项输出风格偏移、实际0.3秒路径、钩子保留/丢失/新增和七类`✅ / ⚠️ / ❌`细节表。
- 该诊断不扩大自动重试范围：只有产品身份、构图骨架、核心文案/最强钩子、第一视觉落点或手机缩略图核心识别发生硬失败时才重试；普通质感和装饰偏差仍记`NOTE`。

## 产品身份与包装拓扑锁

生成前从 `00_` 主图建立并写入分析及 Prompt：

1. `protected_texts / protected_logo / geometry_anchor / material_anchor / viewpoint_anchor`。
2. `product_geometry_fidelity_lock`：从目标主图量化整体宽高比、瓶盖/泵头宽高比、瓶颈高度占比、肩部宽度与对称性、标签边界、液位、瓶底厚度及关键平行线；这些比例来自图片1，不得为匹配图片2的竞品瓶型而改变。
3. `allowed_pack_elements`：目标包装确实存在的Logo、品名区、标签分区、图案、徽章、图标、色块、组件和文字栏。
4. `absent_pack_elements`：竞品包装存在、但目标包装明确不存在的圆章、认证章、环形文字、图标、色块、泵头、瓶盖或其他结构。
5. `protected_empty_zones`：目标包装中必须保持空白、纯色或连续纹理的区域；不得被竞品元素、文字、徽章或装饰填入。
6. `competitor_packaging_collision_map`：逐项把图片2显著包装元素与图片1对比；所有不在白名单内的元素首轮即进入排除项，不等待成图失败后补充。
7. `lighting_application_boundary / core_visibility_zone`：光影只作用于自然高光、明暗过渡、轮廓光、接触阴影和投影；不得改变包装底色、印刷、Logo颜色、标签边界、材质本色或透明度。Logo、品名、规格与主图案不得被遮挡。

先判定 `pose_mode`：正面、近正面、横置但标签仍正对镜头、或仅靠画布平面滚转即可达到的倾斜姿态，一律使用 `rigid_2d`，不因倾角大就自动启用三维；只有可见侧面、明显俯仰/偏航、强透视缩短、倾倒开瓶、真实出液结构或复杂空间遮挡确实无法由二维旋转实现时，才使用 `controlled_3d_pose`。两种模式都允许整体等比例缩放、平移和有边界光影融合；`controlled_3d_pose` 只重建必要观察关系与真实可见结构，不得改变 `product_geometry_fidelity_lock`。若姿态和目标几何冲突，优先级固定为：产品几何与包装身份 > Logo/品名可读性 > 姿态类别与象限 > 精确倾角和竞品透视。若未知结构没有目标详情依据且竞品也不可见，列为一次确认中的风险项，不得擅自补画。多件商品必须来自同一母版，包装、Logo、文字和颜色完全一致。

## 构图、占比与版式

- 完整执行 [composition-lock.md](references/composition-lock.md)，记录构图类型、视觉质量分布、留白地图、锚线、阅读路径、遮挡图和景深层级；不能只写“中心构图”“同参考图”。
- 执行主体占比锁：记录逐件边界框、顶部/底部、宽高、面积、出框、间隙、重叠率和层级。用户要求“撑满”时建议高度95%–110%、双商品间隙0%–2%、允许轻微出框，但保持真实宽高比。
- 主体边界框只约束整体等比缩放和位置，不得反推瓶宽、瓶高、瓶盖、瓶颈、肩部、标签或瓶底的局部比例；目标产品与竞品瓶型差异大时，允许在同一区域内留下少量额外留白，不得用拉伸或透视重塑填满竞品边界框。
- 执行 `product_pose_lock`：记录每件商品长轴起点/终点、角度、象限、瓶口/瓶盖锚点、底端锚点、标签中心朝向、俯仰/偏航/滚转估计、关键交点与遮挡关系；姿态复杂时这些参数优先于笼统边界框。
- 执行 `visual_mass_lock`：除轮廓面积外，记录不透明/高对比标签面积、亮暗质量中心和透明主体的可见质量。透明瓶不得因轮廓显轻而自动放大，实色包装也不得因标签显重而自动缩小。
- 执行 `critical_scene_structure_lock`：逐项锁定竞品图中的分隔线、框架、仪器底座、管线路径、小图标、平台、承托物和其他维持构图骨架的KEY结构；不得以“背景氛围”概括或遗漏。
- 执行邻接细节清单：泡沫、水珠、液体、膏体、矿石、颗粒、倒影、阴影等 KEY 项必须独立进入 Prompt 和 QA；竞品包装内容不得伪装成场景细节。
- 执行版式回归锁：每轮完整列出标题、数字、标点、换行、坐标、填充、描边、光效、字体、标签底框、图标数量、徽章和底栏。重试不得使用“保持其他不变”等弱指令。
- 删除文字或结构时执行删除闭环：同时删除文字、对应底框/横幅/图标，用该位置原背景、纹理和光影自然补齐；不得留下空框、残字、伪文字或自动扩张的替代元素。

## 明亮色相适配与视觉层级

在保持竞品构图、背景几何、空间类型、纹理、景深、光源方向、明暗结构、横幅轮廓和徽章材质不变的前提下，仅对用户允许变色的背景、画外文字、横幅/底栏和徽章/勋章做有限色板映射。默认优先保持竞品背景的色相、饱和度、明度分区和空间纵深，不自动套用全局蓝色或高饱和滤镜。

### 色相＋明度保持

- 背景整体保持浅、明亮、通透；原图高明度区域必须继续高明度，不因目标产品含深蓝、深红等颜色而整体压暗。
- 颜色映射同时记录 `hue_family / luminance_role / saturation_role`。色相可改，原有高、中、低明度关系和视觉对比必须保持。
- 红色使用亮红、高饱和红或高光红，不使用暗红、酒红；蓝色使用亮蓝、天蓝、电光蓝或蓝白渐变，不使用大面积藏蓝、暗蓝；其他颜色同理优先明亮阶。
- 主标题和次标题优先使用亮色。需要适配背景时，可沿用或增强原图已有的白色/亮色描边、外发光、荧光边缘、电镀高光或闪光质感，但不得改变文字边界、字号、换行和位置，也不得无依据叠加多种光效造成廉价或难读。
- 横幅、底栏、徽章和勋章使用亮色系与高明度渐变；深色只允许小面积用于细描边、局部分隔和必要对比，不得成为这些元素的主体色。
- 人物肤色、服装本色、道具、泡沫、水体、矿石、产品邻接细节和目标产品包装不得被统一染色或套全局滤镜。
- 若色板适配会吞没黑色结构线、深色仪器框、冷暖对比或关键道具边界，关键结构的原色与对比优先于统一配色。

### 视觉优先级

1. 最高级：主产品、主标题、次标题。必须清晰、精致、高对比，承担第一至第三视觉落点。
2. 次级：横幅、徽章、勋章。必须明亮易读，但不能抢过主产品与标题。
3. 最后：背景。负责明亮氛围与空间承托，不得通过高饱和、大面积高光或复杂纹理抢占主体。

最终视觉结果必须是：画面整体明亮通透；主产品、主标题和次标题高质感且突出；横幅与徽章层级清楚；背景浅亮但退后。

### 参考图分区亮度锁

生成前必须从竞品参考图建立 `luminance_region_map`，至少覆盖：`global / background / product / headline / banner / badge / bottom_bar` 中实际存在的区域。每区记录一个或多个归一化矩形框及参考 `mean_luma / p50_luma / p90_luma / dark_ratio`。产品区必须按逐件边界框取样；不存在的横幅、徽章或底栏不得虚构区域。

将 `[HIGH_KEY_LUMINANCE_LOCK]` 与 `[PRODUCT_LIGHTING_LOCK]` 放入 Prompt 前30%，不得埋在字体、排除项或风格形容词之后：

- 图片2是整体曝光、白场亮度、产品高光面积、阴影强度和色块明度的唯一参考。
- 背景保持参考图高调白场或原有高明度氛围，禁止灰蓝蒙层、暗角、低曝光和全局冷暖滤镜。
- 目标产品包装原色不受环境光染色；白色/透明区域保持宽幅柔和高光，瓶盖只允许浅灰塑形，接触阴影浅、软、窄。
- 红、蓝及其他允许适配的元素逐项记录亮度角色；不得仅写“适配产品配色”。

候选图下载后必须运行 `scripts/luminance_qa.py`，用任务的 `luminance_region_map` 同参考图比较。亮度QA用于发现系统性压暗，不要求目标包装与竞品包装具有相同固有明度。结果分为 `PASSED / PASSED_WITH_NOTES / REVIEW_REQUIRED / REJECTED`：

- 全图或背景平均亮度下降5%–10%记`NOTE`；全图下降超过10%进入人工复核。背景下降超过10%时，只有参考`HIGH/MID`实际降为`LOW`才量化硬失败；仍处于同一亮度等级时进入人工复核，避免纵横比适配、人物/产品重排或固定框语义错位造成误拒绝。
- 产品区平均下降超过7%、暗像素增加超过0.03或P90下降超过0.05，单项只记`NOTE`；平均下降超过12%且暗像素增加超过0.06或P90下降超过0.08时进入人工复核，不自动拒绝。
- 标题暗像素增加超过0.08、横幅/徽章/底栏超过0.05先记`NOTE`；超过0.12/0.10或参考`HIGH/MID`区域降为`LOW`时进入人工复核，不得仅据固定框自动拒绝。用户确认删除、替换或改写后不再保持原语义的`banner / badge / bottom_bar`区域只作提示。只有背景跨亮度等级的系统性压暗，或肉眼确认灰蓝染色、高光丢失、重阴影导致核心内容不突出时才`REJECTED`。
- `REVIEW_REQUIRED`必须同时对照图片1核验包装原色、高光、环境染色与接触阴影；固有包装色差、合法色板映射或轻微区域错位记`NOTE`，不得自动付费重试。

## 字体

- 画外文字默认1种字体，硬上限2种；首选PDDZHT，失败时使用拼多多正黑体风格粗黑无衬线体。
- 包装原生字体不计入画外字体数量且禁止修改。

## Prompt 组装与风险前置

- Prompt 只含可执行画面指令，不混入分析、步骤、确认、QA或角色说明。
- 自适应顺序：普通正面或低姿态复杂度任务使用 `[DUAL_REFERENCE_AUTHORITY]` → `[PRODUCT_IDENTITY_LOCK]` → 当前最高风险 → 光影边界 → `[COMPOSITION_LOCK]`；横置、倾倒、开瓶、强透视或构图偏差风险高的任务使用 `[DUAL_REFERENCE_AUTHORITY]` → `[COMPOSITION_DOMINANT]`（构图、姿态、视觉质量和关键结构）→ 精简 `[PRODUCT_IDENTITY_LOCK]` → 当前最高风险。两类任务都必须把身份、姿态、视觉质量和KEY结构放在前30%，之后再写邻接细节、版式文字、场景/字体/配色和精简排除项。
- 当前任务最高风险必须出现在 Prompt 前30%：例如亮度压暗、非母版徽章回流、删除闭环、手指结构、开瓶结构、包装文字、满版占比或多商品一致性。参考图属于高调/浅亮画面时，亮度锁始终视为P0风险并前置。
- 目标产品和竞品瓶型、瓶盖或肩部差异明显时，把 `[PRODUCT_GEOMETRY_FIDELITY_LOCK]` 放入前30%，逐项写入目标比例与关键平行线；不得仅写“产品不变”。
- 产品身份核心段只出现一次；保护文字和微型文字集中列一次；删除重复形容词和同义负面词。推荐1000–1400个中文字符，硬上限2000。
- 竞品显著包装特征必须形成正向白名单与反向排除的闭环；正向产品身份描述优先于过长负面清单。

## QA 与重试

- 使用 [dual-reference-high-precision-mode.md](references/dual-reference-high-precision-mode.md) 的宽容构图 QA。
- 提交首轮付费生成前先执行 `python -c "from PIL import Image"`；缺少Pillow时改用已安装Pillow的解释器，仍不可用则停止并报告环境异常，不得先生成后发现QA无法运行。
- 使用 `scripts/luminance_qa.py --reference <图片2> --candidate <候选图> --regions <luminance-regions.json> --output <luminance-qa.json>` 执行分区亮度QA。退出码`0`为通过或带提示，`2`为量化拒绝，`3`为人工复核，`4`为依赖缺失。若未提供分区文件，脚本只验证全图，任务不得因此跳过背景和产品区人工复核。
- 硬失败：目标产品换色/换包装/换Logo/换品名规格；白名单外包装元素新增；`protected_empty_zones` 被填入；整体宽高比、瓶盖宽高比、瓶颈高度、肩部对称性、标签边界、液位或瓶底厚度出现肉眼明显漂移；平行边变成梯形收敛；产品数量或姿态类别错误；长轴方向落入错误象限或偏差约大于15°；瓶口/底端锚点、关键交点或遮挡关系明显错误；视觉质量偏移约大于20%并改变画面平衡；目标产品严重拉伸、弯曲、包装重绘，或受控三维姿态导致Logo/核心文字明显失真；用户确认的核心替换/删除/保留文案错误；构图骨架改变；KEY邻接细节或KEY场景结构完全缺失；手部明显畸形；整体被压暗导致最高级内容不突出。
- NOTE：长轴角度约6°–15°、视觉质量约10%–20%、中小幅坐标/字号/留白/边界/间隙差异，以及不影响身份的微型包装字近似，前提是主要区域、阅读顺序、姿态类别、产品身份和核心文案正确。受控三维姿态本身不构成失败。
- 只有硬失败自动重试，每任务总计最多2次；其中单纯亮度失败最多自动重试1次，另一次额度优先保留给产品身份、包装、构图和核心文案。`NOTE`与未被人工确认的`REVIEW_REQUIRED`不重试。只强化失败项，但完整重申产品、构图、版式和亮度层级。产品几何形变时采用固定降级链：第一次重试改为 `rigid_2d`、禁止三维透视并完整量化几何；仍形变时，第二次重试把几何锁置于最高优先级并把二维倾角降低到约5°–10°，必要时接近正面平视。不得为了精确角度继续牺牲瓶型。

## 执行

完整读取：

- [competitive-visual-analysis.md](references/competitive-visual-analysis.md)
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
- [dual-reference-high-precision-mode.md](references/dual-reference-high-precision-mode.md)
- [adjustment-confirmation-template.md](references/adjustment-confirmation-template.md)

依次运行：

```powershell
python "<SKILL_DIR>\scripts\reset_run.py"
python "<SKILL_DIR>\scripts\validate_batch.py"
python "<SKILL_DIR>\scripts\prepare_batch.py"
```

确认冲突映射后，以一个逗号分隔的 `--images` 值提交，顺序固定为产品图在前、竞品图在后。Prompt 用 UTF-8 回读并核对产品保护文字、核心画外文案和无替换字符。分析、Prompt、JSON、QA、日志和候选图留在 `run_records`；只把最终通过图复制为 `OutputIamge/<任务名>_final.png`，最后运行 `scripts/finalize_output.py`。
