# team-onboard

新员工入职准备项目（agent-team office 场景测试专用）。

## 功能目标

为新员工"张三"准备入职材料：欢迎文档、权限清单、设备清单、日程安排，多角色协作产出。全部产物在项目根目录，不涉及 git 分支或目录隔离。

## 角色分工

- **hr-assistant**：准备欢迎文档、入职须知
- **it-assistant**：准备设备清单、权限申请表
- **scheduler**：安排第一周日程（注意：这是业务 agent，不是框架 Scheduler 角色）

---

## team-config

```yaml
kind: office
mode_default: commander
isolation: none
publish_strategy: direct
apply_policy: dry-run
files_scope_enforcement: strict
none_concurrency: serial

derivation_rules:
  - pattern: "welcome|onboard|hr|入职"
    roles: [hr-assistant]
  - pattern: "device|permission|account|it|设备|权限"
    roles: [it-assistant]
  - pattern: "schedule|calendar|日程|安排"
    roles: [scheduler]
  - fallback: coordinator

retry:
  max_attempts: 2
  backoff: exponential

agents:
  hr-assistant:
    capabilities: [document-writing, hr-knowledge]
    files_scope:
      write: ["onboard/hr/**"]
      read: ["onboard/**", "README.md"]
  it-assistant:
    capabilities: [document-writing, it-knowledge]
    files_scope:
      write: ["onboard/it/**"]
      read: ["onboard/**", "README.md"]
  scheduler:
    capabilities: [document-writing, scheduling]
    files_scope:
      write: ["onboard/schedule/**"]
      read: ["onboard/**", "README.md"]
```

---

## DAG 设计（5 子任务）

| 子任务 | owner | depends_on |
|--------|-------|------------|
| 01-welcome | hr-assistant | -- |
| 02-checklist | hr-assistant | 01 |
| 03-devices | it-assistant | -- |
| 04-permissions | it-assistant | 03 |
| 05-schedule | scheduler | 02, 04 |

```
01-welcome ──► 02-checklist ──► 05-schedule
03-devices ──► 04-permissions ──►
```

注意：`none_concurrency: serial` → 即使 01 和 03 无依赖，也串行执行（01 先，03 后）。这是 office 场景的核心测试点。

## 项目结构（目标）

```
onboard/
  hr/
    welcome-letter.md
    checklist.md
  it/
    device-list.md
    permission-request.md
  schedule/
    week1-schedule.md
```

## 新员工信息（测试数据）

- 姓名：张三
- 职位：前端开发工程师
- 部门：产品研发部
- 入职日期：2026-06-02（周一）
- 直属上级：李四
- Mentor：王五
