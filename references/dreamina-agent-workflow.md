# Dreamina 5.0Pro 双参考执行流程

## 预检

运行 `dreamina image2image -h` 确认 `5.0Pro + 2k + 1:1`，再运行 `dreamina user_credit`。不支持时停止，不静默降级。

在任何付费生成前运行 `python -c "from PIL import Image"`。若默认解释器缺少Pillow，改用环境中已安装Pillow的Python解释器并将其记录为`qa_python`；仍不可用则停止并报告依赖异常，不得先扣分生成。

生成前先为当前竞品图建立 `luminance-regions.json`，至少覆盖全图、背景和逐件产品；标题、横幅、徽章与底栏存在时一并记录。完成参考图分区取样，并把高调亮度锁、元素级明亮色板和产品光影锁写入Prompt前30%。

## 固定输入

- 图片1：`ProductImage/00_` 主产品图，是唯一产品身份母版。
- 图片2：当前竞品图，只提供构图、展示姿态、场景和版式，不提供包装身份事实。
- 产品详情图只供本地分析，不上传。
- 每轮由 Dreamina 一次完成整图；禁止本地抠图、覆盖、补字和合成。

## 固定提交

```powershell
$prompt = Get-Content -Raw -Encoding UTF8 "<prompt-path>"
$images = "<product-image>,<competitor-image>"
dreamina image2image --images $images --prompt=$prompt --model_version="5.0Pro" --ratio="1:1" --resolution_type="2k" --generate_num=1 --poll=30
```

双图必须作为一个逗号分隔的 `--images` 值传入，产品在前、竞品在后。提交前检查 Prompt 含产品保护文字、核心画外文案、包装拓扑排除和明亮层级，且不含 `�`。只有存在 `submit_id` 且状态为 `querying` 或 `success` 才算成功。

## 查询、QA与重试

候选图下载到 `run_records`，不得直接进入 `OutputIamge`。候选图必须与竞品并排检查长轴、端点锚点、姿态类别、轮廓/视觉质量面积和KEY场景结构。只对硬失败自动重试，每任务最多2次；NOTE不重试。重试完整重申产品身份、包装拓扑、构图姿态、视觉质量、KEY结构、版式和视觉层级，并把失败项放到 Prompt 前30%。登录、合规、余额、参数异常或连续两次无有效提交ID时停止。

每个候选图下载后必须运行 `scripts/luminance_qa.py`。退出码`0`表示通过或带提示；`2`表示量化拒绝；`3`表示必须人工复核且不得自动重试；`4`表示依赖缺失并立即停止。人工复核必须同时对照图片1，排除目标包装固有色差、合法色板映射和轻微区域错位；只有确认统一染色、高光明显丢失、背景系统性压暗或重阴影破坏视觉层级后才升级为硬失败。读取JSON中的失败区域与指标后生成亮度专项重试Prompt，不得笼统写“整体更亮”。单纯亮度失败最多自动重试1次；重试必须逐项恢复失败区域的参考明度角色，并锁定已经正确的产品、构图、人物、文案和结构。

## 收尾

只把最终通过图复制为 `_final.png`，执行 `scripts/finalize_output.py`，并记录尝试次数、积分、余额和最终路径。
