# README 模板 与 /team init 命令

> 状态：初稿（2026-05-17） · 阶段一设计收尾产出
> 目的：降低新项目搭建成本（N-4 易用性 / F-14）。一个项目要跑 agent-team，需要两样东西：
> 1. 根 `README.md` 里的 `team-config`（本项目的协作规则）
> 2. `.claude/agents/<name>.md` × N（本项目的业务角色）
> `/team init` 负责把这两样的骨架一键生成。

---

## 一、team-config 完整模板

放在项目根 `README.md` 里（用一个 ```yaml 代码块）。**字段已对齐 ADR-0033 的 publish 拆分**。

```yaml
# ── 必填 ──
kind: development                  # development | content | research | office
                                   # 决定 isolation / publish_strategy / apply_policy 的默认值

# ── 策略（可选，留空则按 kind 取默认；见下方默认表）──
# isolation: git-worktree          # git-worktree | directory-fork | none
# publish_strategy: pr-style       # pr-style | overlay | direct      —— 怎么交付（ADR-0033）
# apply_policy: require-review      # auto-apply | require-review | dry-run  —— 要不要/怎么应用（ADR-0033）

# ── 协作行为（可选）──
mode_default: observer             # commander | observer  (peer 留作 v2)
scheduling: dag                    # dag | parallel-force
files_scope_enforcement: advisory  # advisory | strict
none_concurrency: serial           # serial | file-parallel  (仅 isolation=none 生效)

# ── 失败重试（可选，Scheduler 用，ADR-0035）──
retry:
  max_attempts: 3
  base_seconds: 5
  timeout_minutes: 10

# ── 派生规则（必填至少一条兜底）──
derivation_rules:
  - pattern: "API|后端|数据库"
    roles: [backend-developer, dba]
  - pattern: "UI|前端|界面"
    roles: [frontend-developer]
  - pattern: ".*"                  # 兜底：没命中就交给 Coordinator LLM 判断
    fallback: coordinator

# ── 外部连接器（可选，office 常用，ADR-0031）──
# connectors:
#   - name: gmail
#     mcp_server: "@anthropic/mcp-gmail"
#   - name: excel
#     mcp_server: "@anthropic/mcp-excel"
```

### kind → 默认策略对照表（ADR-0017 / 0033）

| kind | isolation | publish_strategy | apply_policy |
|------|-----------|------------------|--------------|
| development | git-worktree | pr-style | require-review |
| content | directory-fork | overlay | require-review |
| research | directory-fork | overlay | require-review |
| office | none | direct | dry-run |

> 任意字段都能显式覆盖。例如 development 项目想"只看 diff 不真合"：`apply_policy: dry-run`。

---

## 二、业务 agent 骨架（`.claude/agents/<name>.md`）

每个角色一个文件，放在项目的 `.claude/agents/` 目录（Claude Code 原生项目级 subagent 位置，ADR-0009 修订）。

```markdown
---
# Claude Code 原生字段
name: backend-developer
description: 负责 Next.js API 与数据库交互
tools: [Read, Write, Edit, Bash]
model: opus

# team 扩展字段
role: business
capabilities:
  - 实现 REST API
  - 编写数据库查询
files_scope:
  read: ["src/**", "schema.prisma"]
  write: ["src/api/**", "prisma/migrations/**"]
handoff_to_hint: [tester]          # 仅 hint，真实下游由 Scheduler 看 next_steps
escalate_to: mediator              # 卡住上报（实际由 Scheduler 重试用尽后转 Mediator）
triggers: ["后端", "API"]
quality_gates:
  - 测试通过
  - lint 无错误
---

[这个 agent 的工作风格、技术偏好、约束、不允许做的事]
```

---

## 三、`/team init` 命令设计

### 定位
`/team init` 是 plugin 提供的 **slash command**（不是 skill），用于在一个还没配置的项目里快速搭出上面两样骨架。

> 形态说明：init 只做"生成文件 + 提示"，不需要派 agent，本可做 subagent；但它要写项目目录、且和用户来回确认，做成 slash command（运行在主会话）最自然。

### 交互流程

```
/team init [kind]
  │
  1. 检测当前项目状态
  │   - 已有 .claude/agents/ 且非空 → 提示"已配置，是否追加角色？"，不覆盖
  │   - 无 → 继续
  │
  2. 确定 kind
  │   - 命令带了 kind 参数 → 用它
  │   - 没带 → 问用户（development/content/research/office），或读项目特征猜测后让用户确认
  │     （如有 package.json + .git → 猜 development）
  │
  3. 生成根 README 的 team-config
  │   - 若 README 已存在 → 在末尾追加 team-config 代码块（不动原内容）
  │   - 若不存在 → 新建 README，含 team-config + 简短项目说明占位
  │   - 字段按 kind 填默认值，策略字段留注释（让用户知道可覆盖）
  │
  4. 生成 .claude/agents/ 骨架
  │   - 按 kind 给一组"建议角色"的占位文件（见下），每个含完整 frontmatter + 待填 system prompt
  │   - 文件里用 TODO 注释标出"这里写这个角色的工作风格"
  │
  5. 给用户下一步清单
      - "已生成 X 个角色骨架，请编辑 .claude/agents/*.md 填实职责"
      - "team-config 已写入 README，可调整 derivation_rules"
      - "改完后说'开始干 <任务>'即可启动"
```

### 各 kind 的建议角色骨架（仅起点，用户可增删）

| kind | 建议角色占位 |
|------|------------|
| development | architect, backend-developer, frontend-developer, tester |
| content | researcher, writer, editor |
| research | researcher, analyst, writer |
| office | data-collector, data-cleaner, reporter |

> 这些只是**骨架占位**，不是 plugin 内置业务模板（ADR-0011 仍成立：业务角色项目级完全自定义）。init 生成的是"带 frontmatter 的空壳 + TODO"，职责仍由用户填。

### 错误与边界
- 不是 git 仓库且 kind=development → 提示"development 默认 git-worktree 隔离需要 git 仓库，建议先 `git init` 或改 isolation"
- 已有同名 agent 文件 → 跳过该文件，不覆盖，提示用户
- 生成后**不自动启动 team** —— 让用户先填实角色再启动

---

## 四、最小可跑示例（office）

```
q2-finance/
├── README.md                       # 含 team-config: kind: office
└── .claude/agents/
    ├── data-collector.md
    ├── data-cleaner.md
    └── reporter.md
```

`/team init office` 生成上面骨架 → 用户填实三个角色 → 说"帮我整理 Q2 财务表" → team 启动。

---

## 待细化（留作后续）
- init 生成的骨架 system prompt 模板要不要按 kind 给不同提示词起手
- `/team init` 是否支持从已有 `.claude/agents/` 反向生成 derivation_rules
- README 已有复杂内容时，team-config 代码块的定位（末尾 vs 专门章节）
