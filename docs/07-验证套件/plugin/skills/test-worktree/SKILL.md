---
name: test-worktree
description: 验证 V-4 —— 用 Agent 工具调用声明了 isolation:worktree 的 subagent，确认它在独立 git worktree 里运行。当用户说"测试隔离"、"test worktree"、"验证worktree"时触发。
---

# V-4 验证：subagent 在独立 worktree 里运行

你（**主会话**）现在被 `test-worktree` skill 加载。任务：**验证声明了 `isolation: worktree` 的项目级 subagent 真的跑在独立 git worktree 里**（开发场景隔离的基础）。

> 前提：test-project 必须是 git 仓库（套件已 git init）。若不是，worker-wt 会报 git 错误。

## 必须完成，原样报告（不解读、不兜底）

### 步骤 1：报告主会话自己的环境
用 Bash 跑：
```
pwd && git rev-parse --abbrev-ref HEAD 2>&1 && git worktree list 2>&1
```
原样贴。记下主会话的 **pwd** 和 **分支**。

### 步骤 2：调用 worker-wt
用 Agent 工具调用 `worker-wt`（subagent_type: "worker-wt"），它声明了 `isolation: worktree`。把它返回的完整环境报告原样贴出来。

### 步骤 3：对比结论
- **worker-wt 的 pwd 与主会话 pwd 相同还是不同？** 相同 / 不同（若不同，贴出 worker 的路径）
- **worker-wt 的分支与主会话相同还是不同？**
- **`git worktree list` 里有没有出现 worker 的那个 worktree？**
- **worker-wt 写的 wt-marker.txt 落在哪？**（在 worktree 里还是项目根）

## 判定
- worker-wt 的 pwd 是一个**独立 worktree 路径**（与主会话不同）+ 独立分支 → **V-4 通过**（worktree 隔离生效）
- worker-wt 的 pwd 与主会话**相同**（没隔离）→ V-4 不通过，记录"isolation:worktree 未生效"
- worker-wt 报 git 错误 → 说明 test-project 不是 git 仓库，先排查环境

## 禁止
- 不要自己 git worktree add 模拟 —— 要测的是 Agent 工具的 isolation 参数是否自动隔离
- 不要解读、不要美化
