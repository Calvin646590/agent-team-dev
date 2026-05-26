# 方案 C 验证套件 —— 操作指南

> 第二轮调研推断"plugin 内 agent 不能调用项目级 .claude/agents/ subagent"，但推论有疑点。
> 本套件让你在自己的 Claude Code Desktop 里**实测一次**，给出事实判断。
> 全程预计 5-10 分钟。

---

## ⚠️ 实测结论（2026-05-17，第十轮）—— 先读这里

本套件已跑完，结论与最初假设**不同**：

| 测项 | 角色 | 结果 |
|------|------|------|
| `test-coordinator`（plugin 内 subagent）→ 调 `hello-business` | **负向验证** | ❌ subagent 拿不到 Agent 工具，调不了任何 subagent |
| `test-orchestrate`（plugin 内 **skill**）→ 主会话 → 调 `hello-business` | **C' 正向验证** | ✅ 主会话保留 Agent 工具，成功调到项目级 subagent |

**真正的结论**：方案 C 形式上不成立（subagent 不能派 subagent），但**方案 C'（主会话作为 Coordinator skill）成立**。
框架层凡需"派人"的组件必须是 skill（跑在主会话），详见 [../03-讨论记录/2026-05-16-第十轮-验证结论与形态调整.md](../03-讨论记录/2026-05-16-第十轮-验证结论与形态调整.md) 与 ADR-0032。

下面的"步骤 3/4 正向验证 plugin agent → 项目级 subagent"已**作废为负向验证**，仅留作历史记录。新的正向路径是触发 `test-orchestrate` skill（plugin v0.0.3）。

---

## 🔬 阶段二实测（plugin v0.0.4）—— V-11 / V-10

> 这两项是编码门槛里风险最高的。**plugin 已被卸载**（installed_plugins.json 为空），请先重装 v0.0.4 的 zip，cmd+Q 完全退出 Desktop 再重开，然后在 `test-project` 目录的**主会话**里逐项跑。
> 安装方式同下方"验证步骤·步骤 2"。装完务必 cmd+Q 重启。

### V-11：skill 能否中途接力另一个 skill（决定框架层是 3 skill 还是 1 skill）

在 test-project 主会话输入框直接敲（**不要让它派 subagent**）：

```
测试接力
```

触发 `test-relay-a` skill。它会尝试用 Skill 工具调起 `test-relay-b`，并报告三问：
1. 主会话有没有 Skill 工具
2. 有没有从一个 skill 里成功调起另一个 skill
3. 有没有看到 `RELAY-B EXECUTED` 标记

**判定**：
- 三问都 yes → V-11 通过，3 个框架 skill 可接力，现架构成立
- 任一 no → V-11 不通过，Coordinator/Scheduler/Mediator 须合并为 1 个 orchestration skill

把主会话完整输出原样贴回来。

### V-10：主会话能否并发调多个 subagent 并收敛（T3 命脉）

在 test-project 主会话输入框直接敲：

```
测试并发
```

触发 `test-parallel` skill。它会**在一条消息里同时派** worker-1/2/3（每个 sleep 2 秒），然后报告：
1. 三个 worker 是否都返回
2. 返回能否区分（PID/编号各不同）
3. 耗时看是并发(≈2s) 还是串行(≈6s)
4. 收敛是否可靠（无丢失/串台）

**判定**：
- 三个都回 + 可区分 + 收敛可靠 → V-10 通过（真并行是加分，串行也可接受但要记录）
- 丢返回 / 串台 / 调不动 → V-10 不通过，T3 调度需重设计

把主会话完整输出原样贴回来。

> V-11 / V-10 已于 2026-05-22 实测通过（详见第十三轮记录）。

---

## 🔬 阶段二剩余实测（plugin v0.0.5）—— V-4 / V-6 / V-7 / V-8

> 装 v0.0.5 的 zip（含新 skill + 一个 PreToolUse hook），cmd+Q 完全退出 Desktop 重开，**以 test-project 为项目根**打开会话（V-10 已证：项目级 subagent 按会话根注册，根必须是 test-project）。
> test-project 已 `git init`（V-4 worktree 需要 git 仓库）。
> 四项可一口气跑，每项把主会话完整输出贴回。

### V-4：subagent 在独立 worktree 里运行
触发词：
```
测试隔离
```
`test-worktree` skill 会先报告主会话的 pwd/分支，再调 `worker-wt`（声明 `isolation: worktree`），对比两者。
**判定**：worker-wt 的 pwd 是独立 worktree 路径 + 独立分支 → 通过；与主会话相同 → 未隔离。

### V-6：PreToolUse hook 拦截
触发词：
```
测试钩子
```
`test-hook` skill 先跑一条普通命令（应通过），再跑含 `STRICT_TRIPWIRE` 的命令（应被 hook 拦截，返回含 "V-6 HOOK FIRED"）。
**判定**：普通命令通 + tripwire 被拦 + 看到 "V-6 HOOK FIRED" → 通过；tripwire 正常打印了 → hook 没生效（可能要在 plugin.json 显式声明 hooks）。

### V-7：主会话 ↔ subagent 共享文件
触发词：
```
测试共享文件
```
`test-shared-file` skill 写 `.agent-team/workspace/from-main.txt` → 调 `worker-io` 读它并写 `from-worker.txt` → 主会话再读回。
**判定**：worker 读到主会话 marker + 主会话读到 worker 回写 → 双向通过。

### V-8：缺 .claude/agents/ 的错误体验
触发词：
```
测试激活检查
```
`test-init-check` skill 演示两分支：当前项目（应列出角色）+ 故意不存在的路径（应给含 `/team init` 提示的可操作错误）。
**判定**：存在分支列角色 + 缺失分支给可操作错误（非只丢 not found） → 通过。

> V-4/6/7/8 已于 2026-05-22 实测通过（详见第十四轮记录）。V-1~V-11 原语全绿。

---

## 🔬 集成验证（plugin v0.0.6）—— V-12 / V-13（高级审查 R-3）

> 高级审查指出：V-1~V-11 验的是**单点原语**，**集成**未验。这两项捅集成的两个最大未知。
> 装 v0.0.6 zip，cmd+Q 重开，**以 test-project 为项目根**打开会话。test-project 已 git init。
> 这两项是**探索性**验证（不是简单 pass/fail），如实把输出贴回，结论我来下。

### V-12：多 subagent 各自 worktree 并发 + 跨 worktree 同步
触发词：
```
测试worktree同步
```
`test-worktree-sync` skill 三步探：① 并发调 worker-wt-a/b（各 isolation worktree、各提交一个文件）② 主会话能否把它们的分支合并回 main（= Scheduler 收集上游产物）③ 合并后新起 worker-wt-c，看它的 worktree 能否看到上游产物。
**回答**：并发+worktree 成立？上游分支可回收？下游能见上游？若下游见不到 → git 同步模型不可行，跨 agent 交接改用 `.agent-team/workspace/` 共享文件（V-7 已证）。

### V-13：PreToolUse hook 能否识别"当前哪个 subagent"
触发词：
```
测试钩子身份
```
`test-hook-identity` skill：清空 dump → 主会话发一个标记 Bash 调用 → 调 worker-hook 发另一个标记 Bash 调用 → 读 `.agent-team/hook-payloads.jsonl` 对比两条 payload。
**回答**：hook 对 subagent 调用也触发吗？payload 里有没有 agent 身份字段（或 cwd/session 等间接信号）？→ 决定 strict 模式 per-agent files_scope 可不可行。

> 两项跑完把输出都贴回。**这俩 + 后续端到端 demo 才是真正的编码门槛**（R-3）。

---

## 套件内容

```
07-验证套件/
├── agent-team-c-validation.zip          # ⭐ v0.0.6，用这个安装到 Desktop
├── agent-team-c-validation.plugin       # 同样内容，仅扩展名不同
├── plugin/                              # zip 的源目录（仅供查看/修改后重打包）
│   ├── .claude-plugin/plugin.json       # ⚠️ manifest 必须在 .claude-plugin/ 子目录里
│   ├── agents/test-coordinator.md       # 负向验证（subagent 不能派 subagent）
│   ├── hooks/
│   │   ├── hooks.json                   # PreToolUse hook 声明（matcher: Bash）
│   │   └── pretooluse-check.sh          # V-6 拦截（STRICT_TRIPWIRE 即 deny）+ V-13 dump payload
│   └── skills/
│       ├── test-orchestrate/SKILL.md    # C' 正向验证（已通过）— "测试编排"
│       ├── test-relay-a/SKILL.md        # V-11 接力发起方（已通过）— "测试接力"
│       ├── test-relay-b/SKILL.md        # V-11 被接力方
│       ├── test-parallel/SKILL.md       # V-10 并发收敛（已通过）— "测试并发"
│       ├── test-worktree/SKILL.md       # V-4 worktree 隔离（已通过）— "测试隔离"
│       ├── test-hook/SKILL.md           # V-6 hook 拦截（已通过）— "测试钩子"
│       ├── test-shared-file/SKILL.md    # V-7 共享文件（已通过）— "测试共享文件"
│       ├── test-init-check/SKILL.md     # V-8 错误体验（已通过）— "测试激活检查"
│       ├── test-worktree-sync/SKILL.md  # V-12 worktree并发+同步 — "测试worktree同步"
│       └── test-hook-identity/SKILL.md  # V-13 hook 身份识别 — "测试钩子身份"
└── test-project/                        # 模拟用户项目（已 git init，V-4/V-12 需要）
    └── .claude/agents/
        ├── hello-business.md            # C' 验证用项目级 subagent
        ├── worker-1/2/3.md              # V-10 并发 worker（sleep 2s）
        ├── worker-wt.md                 # V-4 worktree worker
        ├── worker-io.md                 # V-7 共享文件 worker
        ├── worker-wt-a/b.md             # V-12 上游 producer（worktree，提交文件）
        ├── worker-wt-c.md               # V-12 下游 consumer（看能否见上游）
        └── worker-hook.md               # V-13 hook 身份探针
```

> 如果你修改了 `plugin/` 下的内容，重新打包（**注意 `.claude-plugin/plugin.json` 必须在 zip 根目录下**）：
> ```bash
> cd 07-验证套件/plugin && rm -f ../agent-team-c-validation.zip ../agent-team-c-validation.plugin && \
>   zip -r ../agent-team-c-validation.zip . -x "*.DS_Store" && \
>   cp ../agent-team-c-validation.zip ../agent-team-c-validation.plugin
> ```

## 验证步骤

### 步骤 1：进入测试项目目录

```bash
cd "/Users/calvinlee/Downloads/Claud code/Agent team/docs/07-验证套件/test-project"
```

### 步骤 2：在 Claude Code Desktop 里安装 plugin

打开 Claude Code Desktop，按以下任一方式安装：

- **方式 A（推荐，拖拽）**：把 `agent-team-c-validation.zip`（或 `.plugin`）拖到 Desktop 的 plugin 安装入口
- **方式 B（命令）**：在 Desktop 里运行
  ```
  /plugin install /Users/calvinlee/Downloads/Claud\ code/Agent\ team/docs/07-验证套件/agent-team-c-validation.zip
  ```

安装成功后，会出现一个名叫 `agent-team-c-validation` 的 plugin，里面有一个 agent `test-coordinator`。

> 如果两种方式都不行，告诉我具体的错误提示，我换打包形式（比如调整 plugin.json 字段、用不同的目录布局）。

### 步骤 3：运行基线测试（先验证项目级 subagent 本身能用）

在 Claude Code Desktop 主会话里输入：
```
/agents
```
**期望**：列表里能看到 `hello-business`（来自 `.claude/agents/`）。
- ✅ 看到 → 项目级 subagent 注册成功，进步骤 4
- ❌ 没看到 → 项目级机制本身有问题，跟方案 C 无关，先排查这一层

然后让主会话直接调一次：
```
请用 Agent 工具调用 hello-business，把它返回的内容原样贴给我
```
**期望**：返回 `hello from project-level subagent (PID=..., cwd=...)`。
- ✅ 返回了 → 主会话→项目级 subagent 通了，进步骤 4
- ❌ 失败 → 把失败信息贴给我，跟方案 C 无关

### 步骤 4：核心验证（plugin agent → 项目级 subagent）

让主会话调用 plugin 里的 `test-coordinator`：
```
请用 Agent 工具调用 test-coordinator（来自 plugin），它会自己尝试再调用 hello-business。
把整个调用链的结果（包括失败信息）原样贴给我。
```

**关注点**：
1. test-coordinator 报告的 `pwd` 与 `ls .claude/agents/` 输出
2. test-coordinator 是否能"看到" hello-business 在可用列表里
3. test-coordinator 调用 hello-business 的结果（成功 / 错误名 / 错误信息）

### 步骤 5：把结果原样贴回来

不要解读、不要美化，把步骤 3 + 步骤 4 的输出原样贴给我，我来判断方案 C 是否立得住。

## 结果矩阵

| 步骤 3 基线 | 步骤 4 plugin→项目 | 结论 |
|------------|-------------------|------|
| ✅ | ✅ | 方案 C 立得住，继续推进 |
| ✅ | ❌ NotFound | plugin 内 agent 看不见项目级 subagent，方案 C 不行，退到 B |
| ✅ | ❌ Permission/Priority | 优先级阻断真实存在，方案 C 不行，退到 B |
| ❌ | — | 项目级机制本身有问题，先排查环境 |

## 备注

- 如果你的 Claude Code Desktop 还不支持本地 plugin 挂载，可以告诉我，我换成"用户级 agents" 的版本（业务 agent 放 `~/.claude/agents/`）做对比验证 —— 但这是另一个方案了，不是方案 C
- 如果你嫌操作麻烦，也可以告诉我，我给一个更简的 fallback 方案设计
