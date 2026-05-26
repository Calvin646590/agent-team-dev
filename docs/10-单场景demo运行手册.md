# 单场景 demo 运行手册（development）

> 阶段三端到端 demo。**第一目标已变**：第一次 demo（自然语言"用 team…"）发现框架被主会话绕过了（R-8）——没进 Coordinator/Scheduler、没 .agent-team、没 worktree、没 Merger，主会话自己并行派 agent 把活干了还撞了依赖竞态。
> 所以本版改用 **`/team start` 强制入口**（plugin v0.1.1 新增 command），并换一个**真正需要协作的难任务**。
> **首要观察**：框架到底进没进（见下方观察表第 0 行）。其次才是 R-1（上下文）/ R-2（调度可靠性）。

## 交付物
- **plugin**：`agent-team.zip`（项目根，v0.1.1：3 skill + 2 subagent + strict hook + **`/team` 强制入口 command**）
- **demo 项目**：`demo/string-utils/`（git 仓库，已重置到干净基线：只有 capitalize + truncate；team-config + developer/tester/doc-writer）

## demo 任务（难任务，含真实依赖 + 多文件 + 新建文件）
> /team start 给 string-utils 加两个函数：`slugify(s)`（转 URL slug）和 `slugifyUnique(strs)`（对字符串数组逐个 slugify，重复的加 -2/-3 后缀去重，**内部复用 slugify**）。写完整测试，更新 README API 列表，并**新建 CHANGELOG.md** 记录本次新增。

为什么这个任务能逼出框架：
- **真实代码依赖**：slugifyUnique 依赖 slugify → 必须先有 slugify（DAG 依赖，不能乱并行）
- **下游真依赖上游**：tester / doc-writer 要等实现完成才能写测试/文档
- **多文件 + 新建文件**：src / test / README / 新 CHANGELOG.md
- 任务规模足够，主会话"一眼做掉"的诱惑小，更可能真的走框架

预期 DAG（由 Coordinator/Scheduler 自行拆，不强求一致）：
```
01 developer: slugify              depends_on: []
02 developer: slugifyUnique(复用slugify)  depends_on: [01]
03 tester:    两者的测试           depends_on: [02]
04 doc-writer:README + CHANGELOG   depends_on: [02]
```
→ 串行链 01→02 压 V-12（worktree 同步）；02 完成后 03/04 并发压 V-10。

---

## 操作步骤

### 1. 安装 plugin
把项目根的 `agent-team.zip` 拖进 Claude Code Desktop（或 `/plugin install <agent-team.zip 路径>`）。

### 1b. 注册 /team 全局命令（⚠️ 必须，一次性）
Plugin 内的 `commands/` 不会注册用户可输入的 slash command（ADR-0045）。需额外复制：
```bash
mkdir -p ~/.claude/commands
cp "<项目根>/agent-team/commands/team.md" ~/.claude/commands/team.md
```
或直接用已有文件：
```bash
cp "/Users/calvinlee/Downloads/Claud code/Agent team/agent-team/commands/team.md" ~/.claude/commands/team.md
```

### 2. 完全重启
cmd+Q 退出 Desktop，重开。

### 3. 以 demo 项目为根打开会话
项目根目录：
```
/Users/calvinlee/Downloads/Claud code/Agent team/demo/string-utils
```
（V-13 结论：项目级 subagent 按会话根注册，必须以 demo 项目为根）

### 4. 基线确认（可选但建议）
主会话直接敲，确认环境对：
```
/plugin                  # 看 agent-team 在列表且 enabled
请用 Agent 工具调用 developer，让它只报告自己的 files_scope，原样贴
```
能调到 developer → 项目级 agent 注册 OK。

### 5. 触发 team（用强制入口 /team，不要用自然语言）
主会话直接敲 slash command（R-8：自然语言会被绕过，必须用 /team）：
```
/team start 给 string-utils 加两个函数：slugify(s)（转 URL slug：小写、空格转连字符、去掉非字母数字连字符的字符）和 slugifyUnique(strs)（对字符串数组逐个 slugify，重复的加 -2/-3 后缀去重，内部复用 slugify）。写完整测试，更新 README API 列表，并新建 CHANGELOG.md 记录本次新增。
```
> `/team` 现已可用（步骤 1b 完成后）。若仍 Unknown command，检查步骤 1b 是否执行 + Desktop 是否完全重启。

### 6. 全程观察并记录
让它跑完 T0→T4。**第 0 行是本次最关键的——先确认框架到底进没进**：

| # | 观察项 | 关注什么 | 对应 |
|---|--------|---------|------|
| **0** | **框架是否真的进了** | 跑的过程里有没有：① 复杂度闸门询问 ② 写 `.agent-team/tasks/*.md` + index.md ③ 用 worktree 派业务 agent ④ Merger 出 candidate ⑤ 最终是"待审 diff"而非"已偷偷改完 main"。**全有=框架进了；只要主会话又"读文件→并行派 agent→直接改完"=R-8 复现，框架仍被绕过** | **R-8（头号）** |
| 1 | Coordinator 复杂度闸门 | 有没有先判断"要不要 team"（ADR-0040） | 设计 |
| 2 | 派生 + 拆解 | 派了哪几个 agent、DAG 拆得对不对、**有没有尊重 slugifyUnique→slugify 的依赖**（不能乱并行） | R-2 |
| 3 | **主会话上下文增长** | 跑完上下文用了多少；subagent 返回是落盘+摘要还是全吞进来 | **R-1** |
| 4 | **Scheduler 调度可靠性** | 漏 ready / 重复派 / status 算错；每轮有没有重读 index.md 自检 | **R-2** |
| 5 | worktree 并发同步 | 串行链 01→02 的 worktree 是否看得到上游；03/04 是否并发（ADR-0042 / V-12） | 集成 |
| 6 | Merger | 按 outputs 归集、pr-style diff/整合分支、有没有乱合冲突 | 集成 |
| 7 | 收尾 | apply 批量后置（中途没真改 main）、给的是 candidate 等 /team accept | R-7 |
| 8 | `.agent-team/` | 跑完看 tasks/ index.md log.md decisions.md 是否如设计落盘 | R-1 |

### 7. 把过程贴回来
把主会话的完整过程（尤其 Scheduler 调度的每一轮、最终 Merger 的 candidate、`.agent-team/` 落了哪些文件）贴回。我据此判断 R-1/R-2 真实表现，决定是否要把调度内核抽成代码（ADR-0037 的"按需上代码"）。

---

## 重跑前重置
demo 项目是 git 仓库，跑完会产生改动 + worktree。重置回基线：
```bash
cd "demo/string-utils"
git worktree prune; rm -rf .claude/worktrees .agent-team
git reset --hard <baseline commit>   # 基线是 "string-utils baseline ..."
git clean -fd src test README.md      # 清掉 team 写入的改动（按需）
```
（baseline commit 见 `git log` 最早那条）

## 判定
- **跑通且上下文/调度可控** → C' 架构在真实规模成立，可进入 4 场景铺开 + 调度内核是否上代码的评估
- **上下文爆 / 调度跑偏** → 正是 demo 要暴露的；据此调整（强化落盘摘要 / 把 DAG 调度抽成脚本或 MCP，ADR-0037）

## 已知边界（首版 demo 不纠结）
- 仅 development 场景（ADR-0038）；content/research/office 待后续
- 调度是 prompt 驱动 + 自检（ADR-0037），非代码引擎——本 demo 就是来看它稳不稳
- strict hook 默认不拦（team-config 是 advisory）；想验 per-agent 拦截把 team-config 改 `files_scope_enforcement: strict`
- slash command（/team）：已通过 `~/.claude/commands/team.md` 正确注册（ADR-0045，follow-up #1 ✅）。Plugin 内的 commands/ 和 skills/team/ 不会注册用户可输入 slash command，需额外复制到 `~/.claude/commands/`（见步骤 1b）
