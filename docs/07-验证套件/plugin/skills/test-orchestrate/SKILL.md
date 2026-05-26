---
name: test-orchestrate
description: 验证主会话能否作为 Coordinator 扮演者动态调度项目级 subagent。当用户说"测试编排"、"test orchestrate"、"验证主会话编排"时触发。
---

# 主会话作为 Coordinator 的可行性验证

你现在被 skill 加载到**主会话**上下文里。本次任务是验证：**主会话视角下，能否动态读取项目 `.claude/agents/` 并通过 Agent 工具触达项目级 subagent**。

## 必须依次完成下列步骤，每步原样报告结果（不要解读、不要美化、不要兜底）

### 步骤 1：环境探查

用 Bash 跑：
```
pwd && ls -la .claude/agents/ 2>&1
```
原样贴输出。

### 步骤 2：读 frontmatter

用 Read 读取 `.claude/agents/hello-business.md`，把 frontmatter 部分（`---` 之间）贴出来。

### 步骤 3：列出你（主会话）当前能用的工具

直接回答：你现在的 tools 列表里**是否有 Agent 工具**？如果有，明确说"是"；没有就说"否"。

### 步骤 4：用 Agent 工具调用项目级 subagent

用 Agent 工具调用 `hello-business`（`subagent_type: "hello-business"`），让它执行默认动作。把它的返回原样贴出来。

### 步骤 5：结论

根据步骤 3 和 4 的实际结果，回答：

- **主会话能拿到 Agent 工具吗？** 是 / 否
- **主会话用 Agent 工具能成功调到项目级 subagent 吗？** 是 / 否 / 报错（贴报错原文）

如果都是"是" → "主会话作为 Coordinator" 路径可行
如果任一为"否" → 报告失败模式

## 禁止

- 不要派 subagent 来代你跑这些步骤（如果你派了 subagent，subagent 没有 Agent 工具，本次验证就失败了 —— 主会话必须自己跑）
- 不要解读、不要兜底、不要省略步骤
- 不要修改 hello-business 或自己模拟它的返回
