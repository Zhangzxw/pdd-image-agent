---
name: pdd-full-replica
description: Restore and run the 2026-07-23 high-fidelity Pinduoduo competitor-image reconstruction workflow. Use when the user invokes $pdd-full-replica to reproduce EnterImage layouts, promotional copy, typography, scene, props, effects, lighting and composition while replacing only the product with ProductImage through Dreamina 5.0Pro image2image at 1:1 and 1K. This is an isolated legacy debugging skill and must not inherit the current pdd-product-image-studio OCR hard gate, slot-contract validator, 2K settings, or modern remediation rules.
---

# 拼多多全复刻模式

把本技能视为 2026 年 7 月 23 日 14:21 节点的独立实验分支。不要修改或调用当前 `$pdd-product-image-studio`，不要混入其 OCR 硬门槛、版式槽位合同、2K 参数、昆虫替换策略或双重积分预算逻辑。

## 固定输入与输出

- 目标效果图：`C:\Users\admin\Desktop\拼多多产品数据整理\EnterImage`
- 自有产品图：`C:\Users\admin\Desktop\拼多多产品数据整理\ProductImage`
- 最终图：`C:\Users\admin\Desktop\拼多多产品数据整理\OutputIamge`
- 技能内部记录：相对于本技能目录的 `tasks`、`run_records`、`history`
- `EnterImage` 只用于视觉反推，不上传即梦。
- `ProductImage` 是 Dreamina 唯一图片输入与产品事实来源。
- `ProductImage` 中以 `00_` 开头的唯一图片是全部任务的主产品图与唯一 Dreamina 图片输入；其余图片作为产品细节事实图，仅供本地分析，不上传即梦。

## 0723 复刻合同

1. 把每张 `EnterImage` 当作目标成图，不是宽泛风格参考。
2. 完整复刻目标图的排版、画外宣传文案、营销文案、数字、标点、换行、字体类别、字号层级、字重、描边、阴影、界面结构、场景、道具、特效、光影、镜头和氛围。
3. 仅将竞品商品替换成 `ProductImage` 中的真实产品；产品外形、品牌、包装、主图案、主要参数、净含量、可辨识主印刷信息和原始颜色以产品图为准。
4. 只允许把画外字体的填充色、描边色、阴影色，以及底部框体或通栏的填充色、边框色和已有渐变色映射到产品包装色板。不得借配色优化改变其他元素。
5. 默认保留竞品画外促销与营销文案，不主动改写或删减。若出现明确第三方商标、店铺名、价格、认证、赠品或与自有产品事实冲突的规格，先暂停并向用户确认。
6. 固定生成参数：`dreamina image2image / 5.0Pro / 1:1 / 1k / 1张`。禁止改用 2K、其他模型、多参考图或本地拼图，除非用户本次明确要求调整实验变量。
7. 坚持由 Dreamina 单次图生图完成融合成图；不使用本地抠图、局部覆盖、包装替换、文字重绘或生成后修补。核心包装结构、Logo、品名、主要参数和主图案必须与 `ProductImage` 一致；无法可靠辨认的微型印刷文字尽最大程度保留，不作为自动硬拒绝项。

## 执行

先完整读取以下规则：

- [analysis-schema.md](references/analysis-schema.md)
- [text-mapping-rules.md](references/text-mapping-rules.md)
- [color-adaptation-rules.md](references/color-adaptation-rules.md)
- [prompt-rules.md](references/prompt-rules.md)
- [dreamina-agent-workflow.md](references/dreamina-agent-workflow.md)
- [qa-checklist.md](references/qa-checklist.md)
- [execution-log-schema.md](references/execution-log-schema.md)

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

在首次付费调用前显示任务数、固定参数和预计积分，并取得用户一次确认。随后按 `dreamina-cli` 的帮助与登录规则调用即梦；登录失效时完成登录并明确报告成功。

## Prompt 原则

- 产品段首句固定写入：“产品外观、核心印刷文字、品牌 Logo、配色与包装结构必须与目标产品图完全一致。”随后逐项列明核心包装结构、Logo、品名、主要参数和主图案；微型印刷文字使用“按输入图尽最大程度保留，不得主动改写或虚构”表述。
- 逐区写明每个可见元素和每段精确文字，不使用“同参考图”“类似竞品”等模糊替代词。
- 保留目标图原有数量关系、坐标、占比、前后层级、背景、软装、道具、特效和冷暖关系。
- 写入产品事实锁、产品原色锁和多件商品复制约束，但保持 Prompt 集中于视觉复刻，不添加现代槽位标记或冗长通用政策段。
- 每项画外文字与底部框体记录“目标原色 → 产品取样色 → 最终映射色”；其余颜色不得改变。
- 禁止额外商品、产品变形、重新设计包装、错误品牌、核心包装文字错乱、Logo 扭曲、主要参数改写、核心文案错字、乱码、水印和二维码。

## 0723 QA 与重试

- 同时对照目标图和产品图，检查商品结构、产品主事实、核心营销文字、排版与界面结构、产品原色、限定配色、场景和商业氛围。
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
