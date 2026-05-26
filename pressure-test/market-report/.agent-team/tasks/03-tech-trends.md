---
id: 03-tech-trends
title: 调研 AI 芯片技术趋势
owner: researcher
depends_on: []
status: done
attempts: 1
outputs:
  - report/chapters/03-tech-trends.md
quality_gate:
  status: passed
  notes: []
next_steps: []
---

## 任务说明

撰写 AI 芯片技术趋势章节初稿，包含：
- 当前主流架构（GPU、TPU、NPU、FPGA、存算一体等）
- 关键技术方向（先进封装、HBM 内存、光互联、量子+AI 融合等）
- 制程节点演进（3nm、2nm 路线图）
- 软件生态（CUDA 护城河、ROCm、MLIR 等）
- 数据来源标注（即使是示例数据也注明"示例数据"）

## 产出文件

- `report/chapters/03-tech-trends.md`

## 写回合约

完成后请将以下字段写回本 task 文件 `.agent-team/tasks/03-tech-trends.md`：
```yaml
outputs: [你产出的文件路径列表]
quality_gate:
  status: passed | failed
  notes: [failed 时的原因列表；passed 时留空 []]
next_steps: [可选后续建议]
```
未写回视为任务未完成。
