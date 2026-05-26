---
id: 04-competitive
title: 竞品对比分析
owner: analyst
depends_on: [01-market-size, 02-players]
status: done
attempts: 1
outputs:
  - report/analysis/competitive-landscape.md
quality_gate:
  status: passed
  notes: []
next_steps: []
---

## 任务说明

基于 researcher 的调研数据，撰写竞品对比分析，包含：
- 主要玩家横向对比（算力、功耗、价格、生态）
- 市场定位矩阵（高端训练 vs 推理 vs 边缘端）
- 竞争格局分析（护城河、差异化策略）
- 数据交叉验证：如发现上游数据矛盾，在文中明确标注

## 上游产物（需读取）

- `report/chapters/01-market-size.md`
- `report/data/market-figures.yaml`
- `report/chapters/02-players.md`
- `report/data/players-data.yaml`

## 产出文件

- `report/analysis/competitive-landscape.md`

## 写回合约

完成后请将以下字段写回本 task 文件 `.agent-team/tasks/04-competitive.md`：
```yaml
outputs: [你产出的文件路径列表]
quality_gate:
  status: passed | failed
  notes: [failed 时的原因列表；passed 时留空 []]
next_steps: [可选后续建议]
```
未写回视为任务未完成。
