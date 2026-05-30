# CHANGELOG

agent-team 插件版本历史。格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

---

## [0.1.13] — 2026-05-30

### Added（诚实复审方案二：fork 隔离运行时留痕）
- **`hooks/fork-evidence-guard.py`**（ADR-0054）：PreToolUse hook，写入 `.agent-team/forks/<fork>/` 时自动把 `{ts, agent_type, fork, file}` 追加到 `.agent-team/evidence/forks.jsonl`。证据独立于 forks/，accept 删 fork 也带不走——directory-fork 隔离从此事后可验证
- `test_fork_evidence_hook.py`：4 项真实自测（留痕/隔离可见/删 forks 后证据仍在/非 fork 不留痕）
- `verify_mechanism.py`：新增 fork 证据一节（自测 + 既有证据校验）；UNVERIFIABLE 从 {fork,worktree} 缩为 {worktree}

### Changed
- `skills/scheduler/SKILL.md`：content/research 分支注明隔离已自动留痕
- `commands/agent-team.md`：overlay 清理明确"只删 forks/，绝不 rm -rf .agent-team/"（保住 evidence/）

---

## [0.1.12] — 2026-05-29

### Fixed（诚实复审 item 3/4/5）
- **删装饰性机制**（ADR-0051）：retry 移除虚构的"指数退避 5/10/20s"（无计时器），改为"立即重派+附 last_error，可显式 Bash sleep 真实等待"；Wave"自检"降格为"派发纪律"（发出前指令，非发出后验证）
- **strict hook 修 worktree/子目录 fail-open**（ADR-0052）：`files-scope-guard.py` 新增 `find_project_root` 向上查找项目根，不再假设 cwd=项目根；strict 检测正则行首锚定（消化 P3-5）
- **Merger 加独立校验**（ADR-0053）：merger.md step 3 改为对整合结果真跑测试（development，退出码为准）/ outputs 存在性断言（content/research/office），不再全信 subagent 自报的 quality_gate

### Added
- `test_files_scope_hook.py`：strict hook 5 项真实自测（含 cwd=子目录用例锁定 ADR-0052 修复）
- 插件 README 顶部"诚实声明"段（item 2）：明确 prompt 驱动本质，区分提示词层与真实 hook 强制层

### Changed
- `verify_mechanism.py`：接入 files-scope hook 自测为第 2 层一节
- docs/16 进展表：item 1~6 全部完成

---

## [0.1.11] — 2026-05-29

### Fixed（诚实复审，Opus）
- **office 写前快照从 prompt 剧场改为真实 hook**（ADR-0049）：新增 `hooks/office-snapshot-guard.py`（PreToolUse 自动触发），覆盖既有文件前自动快照 + 记真实 ISO 时间戳，不再依赖 LLM 自觉。修复 v0.1.10 实测中"快照被报告成功却从未执行"（空目录 + 伪造时间戳 `20260526T000000`）
- `skills/scheduler/SKILL.md` office 分支：移除手写 mkdir/cp 指令，改为说明由 hook 自动完成

### Added
- **场景测试机器可验证化**（ADR-0050）：`pressure-test/verify/` 两层校验（`verify.py` 交付物+真跑 vitest / `verify_mechanism.py` 防叙述造假 / `test_office_snapshot_hook.py` hook 自测），`run-all.sh` 退出码裁决
- `docs/16-诚实复审报告-Opus.md`：取证式复审，区分"真实执行"与"LLM 叙述造假"

### Changed
- `docs/14-场景实测报告.md`：四场景 ✅ 按取证置信度重标（高/高/中/中），不再等同对待

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
