---
id: 02-players
title: 调研 AI 芯片主要玩家
owner: researcher
depends_on: []
status: done
attempts: 1
outputs:
  - report/chapters/02-players.md
  - report/data/players-data.yaml
quality_gate:
  status: passed
  notes: []
next_steps: []
---

## 任务说明

撰写 AI 芯片主要市场玩家章节初稿，包含：
- 头部玩家概览（NVIDIA、AMD、Intel、Google TPU、AWS Trainium、国产芯片等）
- 各玩家市场份额估算（2024 年数据）
- 产品线对比（主要芯片型号、定位、算力规格）
- 数据来源标注（即使是示例数据也注明"示例数据"）

## 产出文件

- `report/chapters/02-players.md`
- `report/data/players-data.yaml`（玩家数据）

## 写回合约

完成后请将以下字段写回本 task 文件 `.agent-team/tasks/02-players.md`：
```yaml
outputs: [你产出的文件路径列表]
quality_gate:
  status: passed | failed
  notes: [failed 时的原因列表；passed 时留空 []]
next_steps: [可选后续建议]
```
未写回视为任务未完成。
