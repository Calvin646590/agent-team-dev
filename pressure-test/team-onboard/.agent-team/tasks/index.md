# agent-team task index

**任务**: 为新员工张三准备完整入职材料  
**kind**: office | **mode**: commander | **isolation**: none | **concurrency**: serial  
**started**: 2026-05-26

## DAG

```
01-welcome ──► 02-checklist ──► 05-schedule
03-devices ──► 04-permissions ──►
```

> none_concurrency=serial：即使 01 和 03 无依赖，也串行执行（id 小者优先）

## 子任务状态

| id | title | owner | depends_on | status |
|----|-------|-------|------------|--------|
| 01-welcome | 撰写欢迎信 | hr-assistant | — | ✅ done |
| 02-checklist | 撰写入职清单 | hr-assistant | 01 | ✅ done |
| 03-devices | 准备设备清单 | it-assistant | — | ✅ done |
| 04-permissions | 准备权限申请表 | it-assistant | 03 | ✅ done |
| 05-schedule | 安排第一周日程 | scheduler | 02, 04 | ✅ done |

## 当前 Ready

**全部完成 ✅** — PublishCandidate 已生成，等待 `/agent-team accept`

## 执行历史

| 轮次 | dispatched | status |
|------|-----------|--------|
| 1 | 01-welcome | ✅ done |
| 2 | 02-checklist | ✅ done |
| 3 | 03-devices | ✅ done |
| 4 | 04-permissions | ✅ done |
| 5 | 05-schedule | ✅ done |
| 6 | Merger | ✅ candidate.md 生成 |
