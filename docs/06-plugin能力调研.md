# Claude Code Plugin 能力调研报告

> 时间：2026-05-16 · 来源：claude-code-guide subagent 查证官方文档
> 目的：在动手编码前确认 plugin 路径技术可行性，对应 V-1~V-8 验证清单中的"代码前调研"部分

## 完整结论速览

| # | 能力 | 结论 | 影响 |
|---|------|------|------|
| 1 | plugin manifest 格式 | ✅ 仅 `name` 必需，其他可选 | 无障碍 |
| 2 | **动态派生未预定义 agent** | **❌ 不支持** | 🔴 **击穿原架构假设** |
| 3 | Agent 工具支持 `isolation: "worktree"` | ✅ 原生支持 | 无障碍 |
| 4 | PreToolUse / PostToolUse hooks | ✅ 支持，配置在 plugin.json 内联或 hooks/hooks.json | 无障碍 |
| 5 | Skill 触发机制 | ✅ 自动（description 命中）+ 手动两种 | 无障碍 |
| 6 | Plugin 加载时读 cwd | ❌ 加载时不行；运行时 agent 可用 Bash 读 | 需调整自动激活实现 |
| 7 | Plugin 分发 | ✅ 本地 `--plugin-dir` / 远程 zip / marketplace | 无障碍 |

## 详细结果

### 1. Plugin manifest 格式
- 必需：`name`
- 可选：`version, description, author, homepage, repository, license, keywords, skills, commands, agents, hooks, mcpServers, lspServers, outputStyles, userConfig, channels, dependencies`
- 文档：https://code.claude.com/docs/en/plugins-reference.md
- **⚠️ 调研漏报的关键细节（实测发现）**：`plugin.json` **必须放在 `.claude-plugin/` 子目录里**，不是 zip 根目录。zip 包结构必须是：
  ```
  .claude-plugin/plugin.json
  agents/<name>.md
  commands/...
  skills/...
  hooks/...
  ```
  根目录直接放 plugin.json 会报 `Invalid plugin: missing .claude-plugin/plugin.json`

### 2. 🔴 动态派生未预定义 agent —— 不支持
**官方说法**：plugin 内可调用的 agent 必须在 `agents/` 目录显式声明。
**变通方案**（调研给出）：
- A. plugin 加载时通过初始化脚本生成 agents/ 文件
- B. Coordinator 调 Bash 读项目里的 md 后委派给 plugin **预定义的通用 agent** 处理

**我们的第三种思路**（基于 Claude Code 项目级 subagent）：
- C. 业务 agent 走 Claude Code 项目级 `.claude/agents/` 机制（项目目录内可见，不需要走 plugin）；plugin 内的 Coordinator 通过 Agent 工具按 name 调用，Claude Code 自动找到项目级 subagent

> ⚠️ **第十轮实测修正（2026-05-17）**：方案 C 的"plugin 内 Coordinator（subagent）调项目级 subagent"**不可行** —— Claude Code 全局规则是 subagent 拿不到 Agent 工具（frontmatter 写 `tools: [Agent]` 也被 strip），任何 subagent 都不能派 subagent。
> **正确路径是方案 C'**：把 Coordinator 实现为 **skill**（加载到主会话，保留 Agent 工具），由主会话调项目级 subagent。已实测通过。详见 ADR-0032 与 [03-讨论记录/2026-05-16-第十轮-验证结论与形态调整.md](03-讨论记录/2026-05-16-第十轮-验证结论与形态调整.md)。
> 另：本表第 1 项的"`agents` 字段"实测有坑 —— `plugin.json` 写 `"agents": ["agents"]` 会让 plugin 静默不注册任何 agent，应**省略该字段**让其自动扫描 `agents/` 目录。

### 3. ✅ Agent + isolation: "worktree"
- 子 agent frontmatter 支持 `isolation: "worktree"` 字段
- 文档：https://code.claude.com/docs/en/sub-agents.md
- **✅ 第十四轮实测（2026-05-22）**：项目级 subagent 写 `isolation: worktree`，由主会话 Agent 工具调起后，确实跑在 `.claude/worktrees/agent-<id>/` 独立目录 + 独立分支 `worktree-agent-<id>`，`git worktree list` 可见，标记文件不污染主树。前提：项目是 git 仓库。

### 4. ✅ Hooks
- 配置位置：`plugin.json` 内联 `"hooks"` 或 `hooks/hooks.json`
- 支持事件：SessionStart, PreToolUse, PostToolUse 等全套
- 类型：command / http / mcp_tool / prompt
- 文档：https://code.claude.com/docs/en/plugins-reference.md（Hooks 部分）
- **✅ 第十四轮实测（2026-05-22）**：`hooks/hooks.json`（matcher: Bash + command 脚本）**自动发现**即生效，**无需在 plugin.json 显式声明 hooks 字段**；PreToolUse 能 deny 命令（返回 `permissionDecision: deny`）。脚本要 `chmod +x` 且权限随 zip 保留。→ 延续"manifest 少声明更稳"规律。

### 5. ✅ Skill
- SKILL.md 的 `description` 字段决定自动触发
- 也可手动 `/plugin-name:skill-name`
- 与 slash command 区别：skill 更新、支持目录与辅助文件、frontmatter 更丰富
- 文档：https://code.claude.com/docs/en/skills.md

### 6. ⚠️ Plugin 加载时不能读 cwd
- 限制：plugin 权限范围仅限 plugin 目录本身
- 变通：
  - 初始化脚本可访问 cwd
  - 运行时 skill/agent 可调 Bash 读
  - `--add-dir` 或 `userConfig` 让用户指定路径
- 影响：F-1"项目内自动激活"不能在 plugin 加载时检测 agents/，只能在 skill/command 被触发时检测

### 7. ✅ 分发
- 本地开发：`claude --plugin-dir ./my-plugin` + `/reload-plugins`
- 远程：`--plugin-url <zip-url>`
- 私有：Git 仓库 + 团队 marketplace
- 公开：Anthropic marketplace（提交审核）
