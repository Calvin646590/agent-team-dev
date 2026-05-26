---
name: test-shared-file
description: 验证 V-7 —— 主会话与子 subagent 通过共享文件 .agent-team/workspace/ 双向交换数据。当用户说"测试共享文件"、"test shared"、"验证共享文件"时触发。
---

# V-7 验证：主会话 ↔ subagent 共享文件往返

你（**主会话**）现在被 `test-shared-file` skill 加载。任务：**验证主会话写一个文件、subagent 读它再写回、主会话再读到**这条共享文件链路（ADR-0008 通信机制的基础）。

## 必须完成，原样报告（不解读、不兜底）

### 步骤 1：主会话写入
用 Bash 跑：
```
mkdir -p .agent-team/workspace && echo "MAIN-MARKER-$(date +%s) 来自主会话" > .agent-team/workspace/from-main.txt && cat .agent-team/workspace/from-main.txt
```
记下写入的 MAIN-MARKER 内容，原样贴。

### 步骤 2：调用 worker-io
用 Agent 工具调用 `worker-io`（subagent_type: "worker-io"）。它会读 from-main.txt、写 from-worker.txt。把它的返回原样贴出来。

### 步骤 3：主会话读回
用 Bash 跑：
```
cat .agent-team/workspace/from-worker.txt 2>&1
```
原样贴。

### 步骤 4：结论
- **worker-io 读到主会话写的 MAIN-MARKER 了吗？**（看它返回里有没有那串 marker）是 / 否
- **主会话读回的 from-worker.txt 里有 worker 写的 `[worker-io 已处理]` 吗？** 是 / 否
- **双向往返完整吗？**（主→worker→主，数据没丢） 完整 / 有问题（说明）

## 判定
- worker 读到了主会话的 marker + 主会话读到了 worker 的回写 → **V-7 通过**（共享文件双向通）
- 任一方向断 → V-7 不通过，记录断在哪一环

## 禁止
- 不要让 worker 把内容直接 return 而跳过写文件 —— 必须经 `.agent-team/workspace/` 文件中转
- 不要解读、不要美化
