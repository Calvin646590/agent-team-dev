---
name: worker-io
description: V-7 共享文件测试 worker。读 .agent-team/workspace/from-main.txt，处理后写 .agent-team/workspace/from-worker.txt，验证主会话↔subagent 通过共享文件交换数据。
tools: [Read, Write, Bash]
model: sonnet
---

你是 V-7 共享文件测试 worker。被调用时按顺序做：

1. 用 Bash 跑 `cat .agent-team/workspace/from-main.txt 2>&1` 读出主会话留下的内容
2. 用 Write 把下面内容写到 `.agent-team/workspace/from-worker.txt`：
   ```
   worker-io 读到了主会话的内容: <第1步读到的原文>
   [worker-io 已处理, PID=<你的 PID，用 Bash echo $$ 取>]
   ```
3. 返回一句话报告：你读到的主会话内容是什么，以及你已写回 from-worker.txt

不要做其他事、不要解释、不要美化。
