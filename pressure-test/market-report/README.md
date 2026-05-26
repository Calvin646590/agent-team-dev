# market-report

AI 芯片市场调研报告项目（agent-team research 场景测试专用）。

## 功能目标

生成一份"2025 年 AI 芯片市场分析报告"，含数据调研、竞品分析、趋势预测、可视化图表描述，多角色协作产出。

## 角色分工

- **researcher**：调研数据、撰写各章节初稿
- **analyst**：交叉验证数据、写竞品对比和趋势分析
- **formatter**：整合各章节、统一格式、生成目录和摘要

---

## team-config

```yaml
kind: research
mode_default: commander
isolation: directory-fork
publish_strategy: overlay
apply_policy: require-review
files_scope_enforcement: strict

derivation_rules:
  - pattern: "research|data|survey|investigate"
    roles: [researcher]
  - pattern: "analy|compare|trend|forecast"
    roles: [analyst]
  - pattern: "format|assemble|summary|toc"
    roles: [formatter]
  - fallback: coordinator

retry:
  max_attempts: 3
  backoff: exponential

agents:
  researcher:
    capabilities: [web-search, data-collection, markdown]
    files_scope:
      write: ["report/chapters/**/*.md", "report/data/**"]
      read: ["report/**", "README.md"]
  analyst:
    capabilities: [data-analysis, comparison, markdown]
    files_scope:
      write: ["report/analysis/**/*.md"]
      read: ["report/**", "README.md"]
  formatter:
    capabilities: [markdown, formatting, document-assembly]
    files_scope:
      write: ["report/final/**", "report/summary.md"]
      read: ["report/**", "README.md"]
```

---

## DAG 设计（7 子任务）

| 子任务 | owner | depends_on |
|--------|-------|------------|
| 01-market-size | researcher | -- |
| 02-players | researcher | -- |
| 03-tech-trends | researcher | -- |
| 04-competitive | analyst | 01, 02 |
| 05-forecast | analyst | 01, 03 |
| 06-format | formatter | 04, 05 |
| 07-summary | formatter | 06 |

```
01-market-size ──► 04-competitive ──► 06-format ──► 07-summary
02-players ────►       ▲
03-tech-trends ──► 05-forecast ──►
```

Wave 预期：Wave 1 = {01, 02, 03}（3 并发）→ Wave 2 = {04, 05}（2 并发）→ Wave 3 = {06} → Wave 4 = {07}

## 项目结构（目标）

```
report/
  chapters/
    01-market-size.md
    02-players.md
    03-tech-trends.md
  analysis/
    competitive-landscape.md
    forecast-2026.md
  data/
    market-figures.yaml
  final/
    full-report.md
  summary.md
```
