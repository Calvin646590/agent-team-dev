---
name: test-init-check
description: 验证 V-8 —— 缺 .claude/agents/ 时能否给出可操作的错误体验。当用户说"测试激活检查"、"test init check"、"验证缺agents"时触发。
---

# V-8 验证：缺 .claude/agents/ 的错误体验

你（**主会话**）现在被 `test-init-check` skill 加载。任务：**验证 Coordinator skill 检测项目配置时，能根据 `.claude/agents/` 是否存在给出恰当输出**——存在则报告可用角色，缺失则给可操作错误（N-4 易用性 / ADR-0023）。

本次一次演示两个分支：当前项目（应有 `.claude/agents/`）+ 一个故意不存在的路径。

## 必须完成，原样报告

### 分支 A：当前项目（应存在）
用 Bash 跑：
```
if [ -d .claude/agents ]; then echo "FOUND"; ls .claude/agents/; else echo "MISSING"; fi
```
- 若 FOUND → 输出："✅ 检测到 .claude/agents/，可用业务角色：<列出文件名>。team 可启动。"
- 若 MISSING → 走分支 B 的错误模板

### 分支 B：模拟缺失（故意指一个不存在的项目）
用 Bash 跑：
```
if [ -d /tmp/no-such-agent-team-project/.claude/agents ]; then echo "FOUND"; else echo "MISSING"; fi
```
应得 MISSING。然后**输出 Coordinator 规定的可操作错误**（照抄这个结构，验证错误体验质量）：

```
❌ TeamError(NoAgentsDir)
原因：当前项目没有 .claude/agents/ 目录，agent-team 需要至少一个业务 agent 才能协作。
你可以：
  1. 运行 /team init 自动生成 team-config + .claude/agents/ 角色骨架
  2. 或手动在 .claude/agents/ 下创建 <role>.md（参考 docs/08-README模板与init命令.md）
  3. 若只是想用单 agent，直接用普通 Claude Code 会话即可，无需 team
```

### 结论
- **存在分支：是否正确列出了可用角色？** 是 / 否
- **缺失分支：是否给出了含"下一步选项"的可操作错误（不是只丢一句 not found）？** 是 / 否

## 判定
- 两分支都按预期输出（存在→列角色；缺失→可操作错误含 /team init 提示） → **V-8 通过**（错误体验达标）
- 缺失分支只丢"目录不存在"没有下一步 → V-8 不通过，需改 Coordinator skill 的错误文案

## 禁止
- 不要真去创建 /tmp/no-such-agent-team-project（只用它演示 MISSING 分支）
- 不要解读、不要美化
