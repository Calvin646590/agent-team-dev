---
name: test-worktree-sync
description: 验证 V-12 —— 多个 isolation:worktree subagent 并发 + 跨 worktree 同步是否可行（开发场景 T3 核心）。当用户说"测试worktree同步"、"test wt sync"、"验证隔离同步"时触发。
---

# V-12 验证：worktree 并发 + 跨 worktree 同步

你（**主会话**）现在被加载。任务：探明**开发场景 T3 的核心机制**到底怎么落地——多个 subagent 各自在 worktree 并发干活、完成后上游产物怎么到下游。这是 V-10（并发）+ V-4（worktree）的组合，外加同步，**之前从没合在一起测过**。

> 这是探索性验证，不是简单 pass/fail。如实报告每一步观察，结论我来下。

## 必须依次完成，每步原样贴输出

### 步骤 1：并发 + worktree（V-10 × V-4 组合）
**在同一条消息里并发**调用 `worker-wt-a` 和 `worker-wt-b`（两个都 isolation:worktree，各自产出并提交一个文件）。
贴出两者返回。关注：
- 两个是否都在**各自独立的 worktree 路径 + 独立分支**
- 两个是否都成功 commit（各自 git log -1）
- 是否真并发（两个调用一条消息发出）

### 步骤 2：上游产物能否被主会话回收（collect_artifacts 可行性）
worker-wt-a/b 返回后，在主会话（项目根 worktree）跑：
```
git worktree list && echo "--- branches ---" && git branch -a && echo "--- all commits ---" && git log --oneline --all -10
```
观察：A、B 的分支和 commit 是否从主会话可见。
然后**尝试把 A、B 的分支合并到 main**（模拟 Scheduler 收集上游产物）：
```
git merge --no-edit <worker-A 的分支名> <worker-B 的分支名> 2>&1 || echo "MERGE FAILED"
ls -la out-a.txt out-b.txt 2>&1
```
（分支名用步骤 1 里报告的实际名字）贴出结果：合并成功吗？out-a.txt / out-b.txt 现在在 main 里了吗？

### 步骤 3：下游能否看到上游（sync 模型可行性）
**在步骤 2 把 A/B 合进 main 之后**，调用 `worker-wt-c`（isolation:worktree）。
观察 C 的返回：它的 worktree（应从更新后的 main 派生）**能不能看到 out-a.txt 和 out-b.txt**？

### 步骤 4：结论
- **Q1 并发+worktree**：多个 worktree subagent 能并发且各自隔离吗？ 能 / 不能
- **Q2 回收**：上游分支能从主会话合并回 main 吗（= Scheduler 能收集上游产物）？ 能 / 不能（贴失败原因）
- **Q3 下游可见**：把上游合进 main 后，新起的下游 worktree subagent 能看到上游产物吗？ 能 / 不能
- **如果 Q3 不能**：记录——git rebase 同步模型不可行，跨 agent 交接应改用 `.agent-team/workspace/` 共享文件（V-7 已证可行）

## 禁止
- 不要自己 git worktree add 模拟 worker —— 要测 Agent 工具的 isolation 真实行为
- 不要因为命令多就跳步；每步都要真实跑 + 原样贴
- 不要解读美化，事实优先
