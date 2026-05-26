---
name: test-relay-a
description: 验证 V-11 —— skill 能否在执行中途触发/接力另一个 skill。当用户说"测试接力"、"test relay"、"验证skill接力"时触发。
---

# V-11 验证：skill → skill 接力

你（**主会话**）现在被 `test-relay-a` skill 加载。本次唯一任务：**验证一个 skill 能否在执行中途调起另一个 skill**。

这决定了 agent-team 框架层是"3 个独立 skill（Coordinator/Scheduler/Mediator）接力"还是"必须合成 1 个大 skill"。

## 必须依次完成，每步原样报告（不解读、不兜底）

### 步骤 1：报到
输出一行：`RELAY-A START`

### 步骤 2：尝试用 Skill 工具接力调起 test-relay-b
- 先看你当前工具集里**有没有 Skill 工具**，明确回答"有/没有"
- 若有：用 Skill 工具调用 `test-relay-b`（plugin 提供的另一个 skill）。如果带 namespace 失败，试裸名 `test-relay-b`
- 把调用的**原始结果**贴出来（成功则应看到 `RELAY-B EXECUTED` 这串标记）

### 步骤 3：报告结论
回答这三个问题：
- **主会话当前有 Skill 工具吗？** 有 / 没有
- **从一个正在执行的 skill 里，成功调起了另一个 skill 吗？** 是 / 否 / 报错（贴原文）
- **看到 test-relay-b 的标记 `RELAY-B EXECUTED` 了吗？** 看到 / 没看到

## 判定
- 三问都"是/有/看到" → **V-11 通过**：3 个框架 skill 可以接力，现有架构成立
- 任一为否 → **V-11 不通过**：Coordinator/Scheduler/Mediator 须合并为 1 个 orchestration skill（内部分三段），需回写 ADR-0032 / 05 草稿

## 禁止
- 不要派 subagent 代你跑（subagent 没有 Skill/Agent 工具，会污染结论）
- 不要自己 echo "RELAY-B EXECUTED" 假装成功 —— 那串标记**只能**由 test-relay-b skill 真正执行才算
- 不要解读、不要美化
