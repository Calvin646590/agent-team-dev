---
id: 05-forecast
title: 市场趋势预测（2026）
owner: analyst
depends_on: [01-market-size, 03-tech-trends]
status: done
attempts: 1
outputs:
  - report/analysis/forecast-2026.md
quality_gate:
  status: passed
  notes: []
next_steps: []
---

## 任务说明

基于市场规模数据和技术趋势，撰写 2026 年市场预测，包含：
- 市场规模预测（悲观/中性/乐观三场景）
- 技术采用曲线预测（哪些技术方向会加速/放缓）
- 关键驱动因素与风险因素
- 数据交叉验证：如发现上游数据矛盾，在文中明确标注

## 上游产物（需读取）

- `report/chapters/01-market-size.md`
- `report/data/market-figures.yaml`
- `report/chapters/03-tech-trends.md`

## 产出文件

- `report/analysis/forecast-2026.md`

## 写回合约

完成后请将以下字段写回本 task 文件 `.agent-team/tasks/05-forecast.md`：
```yaml
outputs: [你产出的文件路径列表]
quality_gate:
  status: passed | failed
  notes: [failed 时的原因列表；passed 时留空 []]
next_steps: [可选后续建议]
```
未写回视为任务未完成。
