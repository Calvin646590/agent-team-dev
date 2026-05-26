---
id: 01-market-size
title: 调研 AI 芯片市场规模
owner: researcher
depends_on: []
status: done
attempts: 1
outputs:
  - report/chapters/01-market-size.md
  - report/data/market-figures.yaml
quality_gate:
  status: passed
  notes: []
next_steps: []
---

## 任务说明

撰写 AI 芯片市场规模章节初稿，包含：
- 2023–2025 年全球 AI 芯片市场规模数据（含同比增速）
- 细分市场（训练芯片 vs 推理芯片；云端 vs 边缘）
- 主要地区市场份额（北美、亚太、欧洲）
- 数据来源标注（即使是示例数据也注明"示例数据"）

## 产出文件

- `report/chapters/01-market-size.md`
- `report/data/market-figures.yaml`（市场规模数据）

## 写回合约

完成后请将以下字段写回本 task 文件 `.agent-team/tasks/01-market-size.md`：
```yaml
outputs: [你产出的文件路径列表]
quality_gate:
  status: passed | failed
  notes: [failed 时的原因列表；passed 时留空 []]
next_steps: [可选后续建议]
```
未写回视为任务未完成。
