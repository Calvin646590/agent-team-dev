---
id: 06-format
title: 整合全文报告
owner: formatter
depends_on: [04-competitive, 05-forecast]
status: done
attempts: 1
outputs:
  - report/final/full-report.md
quality_gate:
  status: passed
  notes: []
next_steps: []
---

## 任务说明

整合所有章节和分析，生成完整报告，包含：
- 完整目录（含页码/锚点）
- 章节编号统一（1. 2. 3. 4. 5.）
- 统一标题层级（H1 报告标题、H2 章节、H3 子章节）
- 统一术语（如"AI 芯片"vs"人工智能芯片"选一）
- 统一引用格式
- 合并所有章节内容到一个文件

## 上游产物（需读取）

- `report/chapters/01-market-size.md`
- `report/chapters/02-players.md`
- `report/chapters/03-tech-trends.md`
- `report/analysis/competitive-landscape.md`
- `report/analysis/forecast-2026.md`

## 产出文件

- `report/final/full-report.md`

## 写回合约

完成后请将以下字段写回本 task 文件 `.agent-team/tasks/06-format.md`：
```yaml
outputs: [你产出的文件路径列表]
quality_gate:
  status: passed | failed
  notes: [failed 时的原因列表；passed 时留空 []]
next_steps: [可选后续建议]
```
未写回视为任务未完成。
