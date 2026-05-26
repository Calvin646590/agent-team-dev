# Agent Team

一个**通用、可动态扩展、配置驱动**的 agent 团队，寄宿在 Claude Code Desktop 中运行。

## 当前状态

🟢 **端到端 demo 跑通（development）** · R-8 可治（强制显式入口下框架完整 engage：DAG/worktree/Merger/待审 diff 全真实生效）；R-1 中等任务可控、R-2 调度可靠（4 节点 DAG）。剩 slash command 注册 + plugin subagent 调用 2 个 follow-up，及大任务压测

**关键里程碑**：
- [x] 项目愿景与边界 (00)
- [x] 需求定义 v0.2 (01) —— 7 个用户故事 + 必备功能 + 跨 4 场景验收
- [x] 架构设计 v0.4 (02) —— **3 框架层 skill + 2 subagent** + 策略抽象 + DAG + skill 触发协议 + hello-world V-1~V-13 + office 实现细节 + connectors
- [x] 决策日志 43 条 (04) —— 历史 ADR 已加修订标注，可清晰回溯
- [x] 第八轮办公场景走查 —— 验证策略抽象立得住，发现 5 处补充设计（ADR-0027~0031）
- [x] 第十轮方案 C' 验证 —— 实测"subagent 不能派 subagent"，框架层改为"派人的当 skill"（ADR-0032），V-1/2/3/5/9 通过
- [x] 第十轮后文档总对齐 —— publish 拆 publish_strategy+apply_policy（ADR-0033）、决策缓存双 hash 失效（ADR-0034）、失败重试归 Scheduler（ADR-0035）、`.claude/agents/` 路径统一
- [x] 第十二轮 —— 内容场景 3 细节定稿 + research 场景走查确认与 content 同构
- [x] 框架层 5 组件草稿齐备 (05) —— coordinator/scheduler/mediator (skill) + requirement-gatherer/merger (subagent)
- [x] README 模板 + `/team init` 设计 (08)
- [x] 第十三轮 阶段二最高风险项实测 —— **V-11 skill 接力**（3 skill 形态确认）+ **V-10 并发收敛**（真并行，T3 命脉确证）
- [x] 第十四轮 编码门槛收尾 —— V-4 worktree / V-6 hook / V-7 共享文件 / V-8 错误体验 全部通过（**原语**全绿）
- [x] 高级审查 (09) —— 登记 R-1~R-7；R-2/R-4 拍板（单场景优先 + 状态机混合），R-1/R-5/R-6/R-7 落 ADR-0036~0041 + 文档修复
- [x] 第十五轮 集成验证 —— **V-12 worktree 并发+同步通过**（同步模型修正为"上游合 base→下游派生"，ADR-0042）+ **V-13 hook per-agent 身份通过**（payload 含 agent_type，ADR-0043）。R-3 消化，**V-1~V-13 全清**
- [x] 阶段三开工 —— **agent-team plugin**（agent-team/ → agent-team.zip：3 skill + 2 subagent + strict hook + `/team` command）+ **development demo 项目**（demo/string-utils）+ 运行手册 (10)
- [x] demo 首跑（自然语言入口）—— **暴露 R-8：框架被主会话绕过**（skill 自动触发不可靠，主会话直接并行派 agent，没进 Coordinator/Scheduler、撞依赖竞态）。已记入 09 风险册
- [x] R-8 应对 —— 加 `/team start` 强制入口（plugin v0.1.1）+ 换难任务 + demo 重置基线
- [x] 第十六轮 端到端 demo 跑通 —— Run1 自然语言被绕过（R-8）；Run2 **粘贴强制指令后框架完整跑通**：复杂度闸门→DAG（01→02→{03,04}）→worktree 同步→Merger→main 不动给待审 diff，9/9 绿。**R-8 可治（ADR-0044）**；R-1 主会话编排 ~20-30k 可控、R-2 调度可靠
- [x] 第十七轮 收尾审查 + follow-up #1 ✅ —— 5 项文档修复；/team slash command 通过 `~/.claude/commands/` 注册成功（ADR-0045）
- [ ] **下一步**：① 修 plugin subagent（merger/req-gatherer）bare-name 调用 ② 大任务压测 R-1/R-2 →（过了）4 场景铺开。详见 [docs/10](docs/10-单场景demo运行手册.md) follow-up

## 文档导航

| 文档 | 用途 |
|------|------|
| [docs/00-项目愿景.md](docs/00-项目愿景.md) | 我们要做什么、为什么做、不做什么 |
| [docs/01-需求定义.md](docs/01-需求定义.md) | 具体功能、使用场景、边界 |
| [docs/02-架构设计.md](docs/02-架构设计.md) | 技术选型、模块划分、协作协议 |
| [docs/03-讨论记录/](docs/03-讨论记录/) | 每次沟通的原始记录，按日期组织 |
| [docs/04-决策日志.md](docs/04-决策日志.md) | 关键决策及推导过程（ADR 风格） |
| [docs/05-框架agent草稿/](docs/05-框架agent草稿/) | 框架层组件（skill/subagent）的 prompt 草稿 |
| [docs/06-plugin能力调研.md](docs/06-plugin能力调研.md) | Claude Code Plugin 能力实测结论 |
| [docs/07-验证套件/](docs/07-验证套件/) | 方案 C/C' 实测套件 + 结论 |
| [docs/08-README模板与init命令.md](docs/08-README模板与init命令.md) | team-config 模板 + `.claude/agents/` 骨架 + `/team init` 设计 |
| [docs/09-高级审查与风险登记.md](docs/09-高级审查与风险登记.md) | 编码前资深复盘 + 风险登记 R-1~R-7 + 解决路线 |
| [docs/10-单场景demo运行手册.md](docs/10-单场景demo运行手册.md) | development demo 安装/触发/观察 R-1/R-2 指标 |
| [agent-team/](agent-team/) | **真 plugin 源码**（3 skill + 2 subagent + strict hook）→ 打包 `agent-team.zip` |
| [demo/string-utils/](demo/string-utils/) | development demo 目标项目（git + team-config + 业务 agent） |

## 工作方式

1. **讨论先于实现** —— 每个新方向先在对话里走一遍，再落到文档里
2. **结论 + 过程** —— 文档里既写"是什么"，也写"为什么这么选"
3. **可回溯** —— 讨论记录保留原始对话，方便事后追查
