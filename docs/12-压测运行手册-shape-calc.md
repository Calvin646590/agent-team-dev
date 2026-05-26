# 压测运行手册 —— shape-calc 12 任务 DAG

> **目的**：在真实项目上验证 agent-team v0.1.8 的大任务 DAG 稳定性（ADR-0037）  
> **执行结果**：✅ 三场景全部通过（2026-05-25）  
> - 场景 A：12/12 done，46 tests passed，quality: passed，candidate.md 落盘  
> - 场景 B：死锁检测 → Mediator 升级报告 → retry 恢复，完整路径走通  
> - 场景 C：write-back 违约 → quality_unknowns → overall: failed 阻断，完整路径走通  
> **观察**：Wave 内并发未完全达设计上限（串行 dispatch），登记为技术债，详见 ADR-0047  
> **项目路径**：`pressure-test/shape-calc/`  
> **验证重点**：DAG 调度正确性 · 死锁检测 · write-back 合约 · Merger 收口质量  
> **预计用时**：首次全流程 ~30-60 分钟（含所有 subagent 执行时间）

---

## 一、DAG 结构

```
01-init
  └─► 02-point
        ├─► 03-line ──────────┐
        ├─► 04-circle ─────── ├─► 06-area ────┐
        ├─► 05-rectangle ─────┘               │    ├─► 09-test-line
        │                     ├─► 07-perimeter┤    ├─► 10-test-circle ──► 12-docs
        └─► 08-test-point(独立)               │    └─► 11-test-rect
                                              └─────► (09,10,11 全依赖 06+07)
```

| 层级 | 子任务 | 并发数 |
|------|--------|--------|
| L0 | 01-init | 1（串行） |
| L1 | 02-point | 1 |
| L2 | 03-line, 04-circle, 05-rectangle, 08-test-point | 4（并发） |
| L3 | 06-area, 07-perimeter | 2（并发，依赖 L2 三者） |
| L4 | 09-test-line, 10-test-circle, 11-test-rect | 3（并发） |
| L5 | 12-docs | 1（依赖全部测试通过） |

---

## 二、测试场景

### 场景 A：正常全流程（主路径）

**目标**：12 任务全部 done，DAG 调度正确，无依赖乱序，Merger 正常收口。

**启动命令**（在 shape-calc 目录下）：
```
/agent-team start 为 shape-calc 项目实现完整的 TypeScript 几何图形库，包含 Point/Line/Circle/Rectangle 类、area 和 perimeter 计算函数，以及对应的 Vitest 单元测试和 API 文档
```

**调度正确性验证点**（边跑边观察 `.agent-team/tasks/index.md`）：

| 检查点 | 预期行为 | 违规信号 |
|--------|---------|---------|
| L2 启动时机 | 02 done 后 03/04/05/08 才能同时派 | 02 还在 in_progress 时 03 已派出 |
| L3 启动时机 | 03+04+05 全 done 后 06+07 才同时派 | 任一 L2 未 done 时 06 已派 |
| L4 启动时机 | 06+07 全 done 后 09/10/11 才同时派 | 06 未 done 时 09 已派 |
| L5 启动时机 | 08+09+10+11 全 done 后 12 才派 | 08 还 pending 时 12 已派 |
| 无重复派发 | 每个 task_id 只被派一次 | index.md 中同 id 出现两次 in_progress |

**write-back 合约验证**（每个 task done 后检查其 `.md` 文件）：

```yaml
# 每个完成的 task 文件应包含：
outputs: ["src/geometry/point.ts"]    # 非空列表
quality_gate:
  status: passed                       # 非 pending
  notes: []
```

---

### 场景 B：死锁注入测试

**目标**：验证 v0.1.8 新增的死锁检测（L-6 修复）能正确触发并上报 mediator。

**触发方法**：在 05-rectangle 任务分发后，手动将其 task 文件 status 改为 `failed`（模拟代理失败且超出重试次数后的状态）：

```yaml
# .agent-team/tasks/05-rectangle.md
status: failed   # 手动注入
```

**预期行为**：
1. 06-area 和 07-perimeter 的 depends_on 含 05，status 永远不能从 pending 变 ready
2. Scheduler 下一轮循环：`ready 为空 且 无 in_progress` → 触发死锁检测
3. 上报 mediator，包含 `{reason: deadlock, blocked_tasks: [06-area, 07-perimeter, ...]}`
4. mediator 呈现可操作升级报告（skip 05 / user_takeover / retry）

**验证信号**：
- `.agent-team/log.md` 出现 `deadlock detected` 记录
- mediator 显示明确的 `blocked_tasks` 列表和处置选项

---

### 场景 C：write-back 违约测试

**目标**：验证当 subagent 未写回 `quality_gate` 时，Merger 的 `quality_unknowns` 路径（L-5 修复）正确触发。

**触发方法**：在某个 tester task（如 08-test-point）完成后，手动将其 `quality_gate.status` 保持 `pending`：

```yaml
# .agent-team/tasks/08-test-point.md
quality_gate:
  status: pending   # 模拟 subagent 未写回
  notes: []
```

**预期行为**：
1. Merger step 1 检测到 `pending` 状态
2. candidate.md 中出现 `quality_unknowns: [{task_id: "08-test-point"}]`
3. `quality` 字段按优先级规则升为 `unknown`（如无其他失败）
4. 主会话呈现 candidate 时注明"建议人工确认"

---

## 三、观察清单（全程追踪）

### 3.1 运行时文件检查（每隔几分钟刷新）

```bash
# 当前 DAG 状态
cat .agent-team/tasks/index.md

# 最新调度日志
tail -20 .agent-team/log.md

# 某子任务详情
cat .agent-team/tasks/06-area.md
```

### 3.2 Merger 产物检查（完成后）

```bash
# candidate 是否落盘
cat .agent-team/candidate.md

# 检查质量字段
grep "quality:" .agent-team/candidate.md

# 检查冲突
grep "conflicts:" -A 5 .agent-team/candidate.md
```

### 3.3 worktree 检查（development 场景）

```bash
# 列出所有 worktree
git worktree list

# 确认各 task 有独立 worktree
git worktree list | wc -l  # 应接近 12+1（主）
```

---

## 四、成功标准（全部满足即压测通过）

| # | 验证项 | 通过条件 |
|---|--------|---------|
| V-A1 | DAG 层级顺序 | 无任何下游在上游 done 前启动 |
| V-A2 | 并发正确性 | 同层无依赖任务在同一轮并发派出 |
| V-A3 | 无重复派发 | 每个 task_id 只出现一次 in_progress |
| V-A4 | write-back 合约 | 全部 done 任务的 outputs + quality_gate 均非空/非 pending |
| V-A5 | candidate 落盘 | `.agent-team/candidate.md` 存在且格式正确 |
| V-A6 | quality 正确 | 全 passed → quality=passed；有失败 → 按优先级规则 |
| V-B1 | 死锁检测触发 | 注入死锁后 mediator 收到 deadlock escalation | ✅ 通过 |
| V-B2 | Mediator 根因报告 | 下游影响链 + 4 选项呈现 | ✅ 通过 |
| V-B3 | retry 恢复执行 | attempts 清零 → 重跑 → DAG 解锁 | ✅ 通过 |
| V-C1 | write-back 违约检测 | outputs=[] ∩ quality_gate≠passed/failed → 标 unknown | ✅ 通过 |
| V-C2 | quality_unknowns 上报 | Merger 纳入 quality_unknowns 列表 | ✅ 通过 |
| V-C3 | 阻断 apply | overall: failed，apply_policy: blocked_by_quality_unknown | ✅ 通过 |

---

## 五、已知风险与预案

| 风险 | 可能性 | 预案 |
|------|--------|------|
| 主会话上下文溢出（12 任务 × 返回摘要） | 中 | 观察 scheduler 每轮只读 index.md 摘要，不吞全文；若溢出触发 ADR-0036 review |
| LLM 调度跑偏（ADR-0037 的核心风险） | 中 | 每层完成后人工核验 index.md 状态；发现异常立即记录 + 触发 R-2 后续处理 |
| worktree merge 冲突（同文件多 agent 写） | 低 | files_scope.write 已按 agent 分区（developer: src/*.ts / tester: *.test.ts）；意外冲突由 Merger 标 conflict: manual |
| npm install 失败（网络问题） | 低 | developer 在 01-init 中可选择不实际安装，只创建 package.json；vitest 运行时再装 |

---

## 六、压测后续 ADR 更新指引

压测通过后，在 `docs/04-决策日志.md` 追加：

```
ADR-0047：大任务 DAG 稳定性验证（12 任务，development 场景，v0.1.8）
- 状态：[已验证 / 部分通过 / 发现问题]
- 结论：[稳定 / 需引入代码状态机（ADR-0037 方案 B）]
- 观察：[记录实测的调度准确性、上下文增长、意外行为]
```
