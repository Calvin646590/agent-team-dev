# PublishCandidate

<!-- generated: 2026-05-26 by Merger -->

## quality
passed

## task_failures
[]

## integration_errors
[]

## quality_unknowns
[]

## artifacts
- path: onboard/hr/welcome-letter.md
  task: 01-welcome
  owner: hr-assistant
  quality: passed
  summary: 入职欢迎信（致张三），含公司寄语、入职准备与联系人信息
- path: onboard/hr/checklist.md
  task: 02-checklist
  owner: hr-assistant
  quality: passed
  summary: 新员工入职清单（张三），覆盖材料、合同、培训等流程项
- path: onboard/it/device-list.md
  task: 03-devices
  owner: it-assistant
  quality: passed
  summary: IT 设备清单（张三），列出笔记本、外设、配件型号与领取项
- path: onboard/it/permission-request.md
  task: 04-permissions
  owner: it-assistant
  quality: passed
  summary: 权限申请表（张三），覆盖账号、系统、邮箱、VPN 等访问授权
- path: onboard/schedule/week1-schedule.md
  task: 05-schedule
  owner: scheduler
  quality: passed
  summary: 第一周入职日程安排（张三），按天列出培训、会议与对接任务

## conflicts
[]

## publish_strategy
direct

## apply_policy
dry-run

## rollback_hint
当前为 dry-run 模式，未对工作区执行任何 publish 动作；candidate 仅作呈现。
如需回到任务开始前状态，可使用 .agent-team/snapshots/ 下的快照（ADR-0041）。
isolation_strategy=none，无独立分支或 fork 需清理。

## external_actions
[]
