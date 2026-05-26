---
id: 07-summary
title: 撰写执行摘要
owner: formatter
depends_on: [06-format]
status: done
attempts: 2
outputs:
  - report/summary.md
quality_gate:
  status: passed
  notes: []
next_steps: []
---

## 任务说明

基于整合完成的完整报告，撰写执行摘要，包含：
- 核心发现（3–5 条要点）
- 市场规模与增速一句话结论
- 最值得关注的竞争格局变化
- 2026 年预测核心结论
- 总字数 300 字以内

## 上游产物（需读取）

- `report/final/full-report.md`

## 产出文件

- `report/summary.md`

## 写回合约

完成后请将以下字段写回本 task 文件 `.agent-team/tasks/07-summary.md`：
```yaml
outputs: [你产出的文件路径列表]
quality_gate:
  status: passed | failed
  notes: [failed 时的原因列表；passed 时留空 []]
next_steps: [可选后续建议]
```
未写回视为任务未完成。
