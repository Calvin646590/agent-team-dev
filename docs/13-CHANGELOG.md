# CHANGELOG

agent-team 插件版本历史。格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

---

## [0.1.10] — 2026-05-26

### Added
- **Wave 并发强制规则**（ADR-0047）：Scheduler step 3 新增 ❌/✅ 反模式对比 + 批量派发硬约束 + Wave 自检机制（`wave_underutilized` 警告）
- **4 场景完整代码路径**（ADR-0048）：
  - Scheduler：directory-fork 工作区创建（rsync 基线）、office 写前快照、none_concurrency serial 串行约束
  - Mediator abort：三场景分支清理（worktree / forks / snapshot 回滚）
  - Command accept/reject：overlay（+history 备份）、direct（+dry-run 行为）、pr-style 各详细化
- 初始化目录扩展：`mkdir -p .agent-team/tasks .agent-team/forks .agent-team/snapshots`

### Fixed
- Wave 内串行派发退化为已知技术债后彻底修复

### Verified
- content 场景（travel-blog，6 任务）：directory-fork + overlay + resume 全流程 ✅
- office 场景（team-onboard，5 任务）：serial 串行 + dry-run + snapshots ✅
- research 场景（market-report，7 任务）：Wave 3+2 并发 + Merger 产物拦截 + retry ✅
- Commander/Observer 模式切换：state.md 写入 + log 记录 ✅
- **首版验收标准全部通过** ✅

---

## [0.1.9] — 2026-05-25

### Fixed（P2 × 11，代码审查第 3 批）
- C-4：context 字段完整枚举（coordinator step 7）
- ST-3：swap_agent attempts 不清零（仅 retry 清零）
- ST-4：worktree checkpoint 写入 state.md
- ST-1：新增 `resume` 命令（断点恢复）
- S-4：candidate schema 在 accept/reject 双向引用 merger.md
- ST-5：timeout 建议性声明（prompt 驱动无系统计时器）
- E-1：Merger fast-path（全 passed 时跳过逐条展开）
- E-2：external-action 类子任务跳过 git merge/diff
- E-3：index.md 局部更新优先（任务数 ≤5 时可全量重写）
- E-4：mediator 直接使用 context.team_config，不重读 README
- L-3：coordinator source 枚举（natural / slash / api）

### Verified
- 压测场景 A：shape-calc 12 任务全流程，46 Vitest tests passed（ADR-0047）
- 压测场景 B：死锁注入 → 检测 → Mediator 升级 → retry 恢复
- 压测场景 C：write-back 违约 → quality_unknowns → apply 阻断

---

## [0.1.8] — 2026-05-25

### Fixed（P0 × 5 + P1 × 8，代码审查第 1-2 批）
**P0 Critical**
- C-1：Step 0 初始化 `mkdir -p .agent-team/tasks`（幂等）
- L-4：write-back 合约写入派发 prompt（不可省略）
- C-2：coordinator context 完整字段透传 Merger
- L-5：Merger step 1 显式处理 quality_gate: pending 任务
- L-8：candidate.md 持久化（Merger 写盘，accept 读取）

**P1 Design**
- L-6：DAG 死锁检测（ready=∅ ∧ in_progress=∅ → mediator escalate）
- L-7：`status: failed` 先写回再调 mediator
- S-5/L-9：quality 优先级规则（integration-failed > failed > unknown > passed）+ task_failures/integration_errors/quality_unknowns 三字段拆分
- S-1：task schema 补 quality_gate 字段（done ≠ quality passed，ADR-0046）
- S-2：requirement-gatherer still_ambiguous 三选项协议
- S-6：Merger step 3 集成验证覆盖全部 kind
- C-3：mediator escalate 携带 files_scope + context 字段
- S-3（ADR-0045）：follow-up #1 结案，local-upload slash command 注册限制记录

---

## [0.1.7] — 2026-05-24

### Added
- 代码审查报告（docs/11-代码审查报告-v0.1.7.md），共识别 29 项技术问题
- done ≠ quality 原则确立（ADR-0046，Follow-up #3）

---

## [0.1.6] — 2026-05-24

### Added
- 正式编码阶段首版
- 与官方插件结构对齐（plugin.json、hooks.json、命名规则）
- Follow-up #1 结案（ADR-0045：slash command 注册限制）
- Follow-up #2 结案（subagent_type namespaced 格式）

---

## [0.1.x] — 2026-05-23 及以前（探索阶段）

### 里程碑
- V-1~V-13 验证套件全部通过（2026-05-23）
- 端到端 demo 跑通（development 场景，2026-05-23，ADR-0044）
- R-1~R-8 高级审查风险决策完成（ADR-0036~0044；最终验证在 v0.1.9/0.1.10 压测与 4 场景实测后关闭）
- 框架架构收敛：Coordinator / Scheduler / Mediator（skill）+ Merger / requirement-gatherer（subagent）

---

> 完整决策历史见 [docs/04-决策日志.md](04-决策日志.md)（ADR-0001~0048）
