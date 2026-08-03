# Dreamina 5.0Pro 产品替换执行流程

## 1. 预检

1. 运行 `dreamina image2image -h`，确认支持 `5.0Pro + 1k + 1:1`；不支持时停止，不静默降级。
2. 运行 `dreamina user_credit`，说明任务数、生成张数、模型、分辨率和预计积分。

## 2. 输入隔离

- `EnterImage` 只用于视觉反推与 Prompt，不上传给即梦。
- `image2image --images` 只传当前任务的 `ProductImage` 副本，且只传一次。
- Prompt 承载目标效果图的文案、布局、场景、道具、特效和风格。

## 3. 固定提交

```powershell
$prompt = Get-Content -Raw -Encoding UTF8 "<output>\xxx_prompt.txt"
dreamina image2image --images "<product-image>" --prompt=$prompt --model_version="5.0Pro" --ratio="1:1" --resolution_type="1k" --generate_num=1 --poll=30
```

记录开始时间、命令、输入文件、Prompt 文件、参数、预计积分和 CLI 输出。只有存在 `submit_id` 且状态为 `querying` 或 `success` 才算提交成功。

## 4. 查询与下载

用 `dreamina query_result --submit_id=<id> --download_dir=<records_dir>` 查询下载，候选图不得下载到 `OutputIamge`。将完整参数、提交 ID、状态、积分、结果 URL、下载路径和结束时间写入 `run_records/xxx_dreamina.json`，同步写入 `run_records/xxx_execution.md`。仅将最终选中的通过图复制为 `OutputIamge/xxx_final.png`。

## 5. 失败与自动重试

- `REJECTED`、提交失败、查询失败或生成失败自动进入重试队列；每个任务最多重试2次，任一轮通过后立即停止。
- 先按分级 QA 报告差异、修订片段和预计新增积分，然后直接重试，不等待用户再次确认。
- QA失败只修改对应 Prompt 片段；生成失败无候选图时先去除重复/冲突措辞，再减少非核心装饰，始终保留核心文字、产品事实和目标构图。
- 保持 `5.0Pro + 1K + 1:1 + 单产品图输入`；不得自行改用默认模型、2K、多参考图或本地拼图。
- 每轮独立记录 attempt 编号、Prompt、submit_id、状态、积分、候选图和 QA，并在最终日志中标出采用哪一轮。
- 若返回合规确认、登录失效、余额不足、参数不支持，或连续两次无有效 `submit_id`，停止重试并请用户处理。

## 6. 输出收尾

运行 `python scripts/finalize_output.py`。确认 `OutputIamge` 只含 `_final` 图片；分析、Prompt、日志、JSON、QA 和候选图全部位于 `run_records`。
