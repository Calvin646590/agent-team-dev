---
name: test-hook-identity
description: 验证 V-13 —— PreToolUse hook 的 payload 能否识别"当前是哪个 subagent 在调用工具"（决定 strict 模式 per-agent files_scope 是否可行）。当用户说"测试钩子身份"、"test hook identity"、"验证hook身份"时触发。
---

# V-13 验证：hook 能否识别当前 subagent 身份

你（**主会话**）现在被加载。任务：探明 **PreToolUse hook 收到的 payload 里，有没有字段能区分"这次工具调用是主会话发的，还是某个 subagent 发的、是哪个 subagent"**。

这决定 strict 模式能否做 **per-agent files_scope**（按当前是哪个 agent 应用它的写权限边界，ADR-0019）。V-6 只验了全局 tripwire，没验身份。

plugin v0.0.6 的 hook 会把每次 Bash 调用的完整 payload dump 到 `.agent-team/hook-payloads.jsonl`。

## 必须依次完成，原样贴输出

### 步骤 0：清空旧 dump（避免干扰）
```
mkdir -p .agent-team && : > .agent-team/hook-payloads.jsonl && echo "cleared"
```

### 步骤 1：主会话自己发一个带标记的 Bash 调用
```
echo "V13-MAIN-CALL from main session"
```
（这次调用会被 hook dump）

### 步骤 2：让 subagent 发一个带标记的 Bash 调用
用 Agent 工具调用 `worker-hook`（subagent_type: "worker-hook"）。它内部会跑一个含 `V13-SUBAGENT-CALL` 的 Bash。把它的返回贴出来。
**同时关注**：worker-hook 的 Bash 调用**有没有触发 hook**（即有没有被 dump 下来）——这本身是关键问题之一（hook 对 subagent 的工具调用生不生效）。

### 步骤 3：读出 dump，逐条分析
```
echo "=== payload 条数 ===" && wc -l .agent-team/hook-payloads.jsonl
echo "=== 全部 payload ===" && cat .agent-team/hook-payloads.jsonl
```
对照看两次调用（V13-MAIN-CALL vs V13-SUBAGENT-CALL）的 payload：
- 两条都在吗？（hook 对 subagent 调用是否也触发）
- 每条 payload 有哪些字段？（列出 key）
- **有没有任何字段能标识"是哪个 agent / subagent"**？比如 agent 名、subagent_type、不同的 session_id、不同的 cwd（subagent 在 worktree 时 cwd 可能不同）等

### 步骤 4：结论
- **hook 对 subagent 的工具调用也触发吗？** 是 / 否（若否，strict 模式根本管不到 subagent —— 重大发现）
- **payload 里有没有直接的 agent 身份字段？** 有（贴字段名）/ 没有
- **有没有可间接区分的信号？**（如 cwd 不同、session 不同）有（说明）/ 没有
- **per-agent files_scope 可行吗？** 可行（直接靠身份字段）/ 勉强（靠 cwd 等间接信号）/ 不可行（hook 拿不到任何区分信息）

## 禁止
- 不要让 worker-hook 跳过 Bash 直接 return —— 必须真发 Bash 调用才会触发 hook
- 不要解读美化，把 payload 原文贴出来由事实说话
