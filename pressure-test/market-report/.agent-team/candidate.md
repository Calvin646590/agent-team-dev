---
generated_at: 2026-05-26T21:10:00Z
publish_strategy: overlay
apply_policy: require-review
quality: passed
task_failures: []
integration_errors: []
quality_unknowns: []
artifacts:
  - source_fork: .agent-team/forks/researcher-01-market-size/
    file: report/chapters/01-market-size.md
    destination: report/chapters/01-market-size.md
  - source_fork: .agent-team/forks/researcher-01-market-size/
    file: report/data/market-figures.yaml
    destination: report/data/market-figures.yaml
  - source_fork: .agent-team/forks/researcher-02-players/
    file: report/chapters/02-players.md
    destination: report/chapters/02-players.md
  - source_fork: .agent-team/forks/researcher-02-players/
    file: report/data/players-data.yaml
    destination: report/data/players-data.yaml
  - source_fork: .agent-team/forks/researcher-03-tech-trends/
    file: report/chapters/03-tech-trends.md
    destination: report/chapters/03-tech-trends.md
  - source_fork: .agent-team/forks/analyst-04-competitive/
    file: report/analysis/competitive-landscape.md
    destination: report/analysis/competitive-landscape.md
  - source_fork: .agent-team/forks/analyst-05-forecast/
    file: report/analysis/forecast-2026.md
    destination: report/analysis/forecast-2026.md
  - source_fork: .agent-team/forks/formatter-06-format/
    file: report/final/full-report.md
    destination: report/final/full-report.md
  - source_fork: .agent-team/forks/formatter-07-summary/
    file: report/summary.md
    destination: report/summary.md
conflicts: []
rollback_hint: "rm -rf .agent-team/forks/  # 主工作区未修改，删除 forks 即完全回滚"
---

# PublishCandidate — market-report

收口结论：**quality = passed**。9 个子任务全部 `quality_gate: passed`（07-summary 经第 2 次尝试已写回 passed），无冲突、无集成错误、无未知项。等待主会话按 `apply_policy: require-review` 走 present → 用户裁决 → apply。

## 1. 产物清单（9 个文件，source fork → destination）

| # | task | owner | source (fork 内) | destination (主工作区) | size |
|---|------|-------|------------------|------------------------|------|
| 1 | 01-market-size | researcher | `.agent-team/forks/researcher-01-market-size/report/chapters/01-market-size.md` | `report/chapters/01-market-size.md` | 8.1 KB |
| 2 | 01-market-size | researcher | `.agent-team/forks/researcher-01-market-size/report/data/market-figures.yaml` | `report/data/market-figures.yaml` | 5.3 KB |
| 3 | 02-players | researcher | `.agent-team/forks/researcher-02-players/report/chapters/02-players.md` | `report/chapters/02-players.md` | 8.3 KB |
| 4 | 02-players | researcher | `.agent-team/forks/researcher-02-players/report/data/players-data.yaml` | `report/data/players-data.yaml` | 9.1 KB |
| 5 | 03-tech-trends | researcher | `.agent-team/forks/researcher-03-tech-trends/report/chapters/03-tech-trends.md` | `report/chapters/03-tech-trends.md` | 11.1 KB |
| 6 | 04-competitive | analyst | `.agent-team/forks/analyst-04-competitive/report/analysis/competitive-landscape.md` | `report/analysis/competitive-landscape.md` | 12.3 KB |
| 7 | 05-forecast | analyst | `.agent-team/forks/analyst-05-forecast/report/analysis/forecast-2026.md` | `report/analysis/forecast-2026.md` | 12.2 KB |
| 8 | 06-format | formatter | `.agent-team/forks/formatter-06-format/report/final/full-report.md` | `report/final/full-report.md` | 52.0 KB |
| 9 | 07-summary | formatter | `.agent-team/forks/formatter-07-summary/report/summary.md` | `report/summary.md` | 1.7 KB |

## 2. quality_gate 汇总

| task_id | owner | quality_gate | attempts | 备注 |
|---------|-------|--------------|----------|------|
| 01-market-size | researcher | passed | 1 | — |
| 02-players | researcher | passed | 1 | — |
| 03-tech-trends | researcher | passed | 1 | — |
| 04-competitive | analyst | passed | 1 | — |
| 05-forecast | analyst | passed | 1 | — |
| 06-format | formatter | passed | 1 | — |
| 07-summary | formatter | passed | 2 | 第 1 次失败，重跑后通过 |

- 全部 passed → `task_failures: []`
- 无 pending → `quality_unknowns: []`
- kind=research 无构建产物，按规则跳过集成验证 → `integration_errors: []`

## 3. 冲突检查

按各 fork outputs 声明做路径对比：9 个 destination 路径互不重叠，**无冲突**。
`conflicts: []`。

## 4. apply 预览（用户执行 `/agent-team accept` 后等价于以下命令）

```bash
cd "/Users/calvinlee/Downloads/Claud code/Agent team/pressure-test/market-report"

mkdir -p report/chapters report/data report/analysis report/final

cp .agent-team/forks/researcher-01-market-size/report/chapters/01-market-size.md       report/chapters/01-market-size.md
cp .agent-team/forks/researcher-01-market-size/report/data/market-figures.yaml         report/data/market-figures.yaml
cp .agent-team/forks/researcher-02-players/report/chapters/02-players.md               report/chapters/02-players.md
cp .agent-team/forks/researcher-02-players/report/data/players-data.yaml               report/data/players-data.yaml
cp .agent-team/forks/researcher-03-tech-trends/report/chapters/03-tech-trends.md       report/chapters/03-tech-trends.md
cp .agent-team/forks/analyst-04-competitive/report/analysis/competitive-landscape.md   report/analysis/competitive-landscape.md
cp .agent-team/forks/analyst-05-forecast/report/analysis/forecast-2026.md              report/analysis/forecast-2026.md
cp .agent-team/forks/formatter-06-format/report/final/full-report.md                   report/final/full-report.md
cp .agent-team/forks/formatter-07-summary/report/summary.md                            report/summary.md
```

策略 `overlay`：直接落到主工作区相对路径；目标目录不存在则先 `mkdir -p`。
策略 `apply_policy: require-review`：主会话必须先 present 完整 diff 给用户确认，**不可** auto-apply。

## 5. 回滚

- **apply 前回滚**（candidate 还未落盘）：忽略本 candidate 即可，主工作区未变更。
- **apply 后回滚**：主工作区在 apply 前没有这些路径下的同名文件（首次产出），执行下述命令即可还原：
  ```bash
  rm -rf report/chapters report/data report/analysis report/final report/summary.md
  ```
- **完全清理 forks**（确认无需保留 agent 中间产物时）：
  ```bash
  rm -rf .agent-team/forks/
  ```
  主工作区未修改的前提下，删除 forks 即完全回到 agent-team 执行前的状态。
- 若需更稳妥的快照式回滚，参考 `.agent-team/snapshots/<task-id>/`（ADR-0041）。
