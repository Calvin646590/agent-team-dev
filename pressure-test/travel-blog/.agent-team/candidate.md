# PublishCandidate
# generated_at: 2026-05-26T00:00:00Z
# merger: agent-team Merger
# scenario: travel-blog (content, directory-fork, overlay)

publish_strategy: overlay
apply_policy: require-review
quality: passed  # all 6 subtasks quality_gate=passed; all 13 source artifacts verified present

task_failures: []
integration_errors: []
quality_unknowns: []

artifacts:
  # --- drafts (from writer forks; editor's drafts/ copies intentionally ignored per overlay rule) ---
  - src: .agent-team/forks/writer-01-overview/content/drafts/overview.md
    dst: content/drafts/overview.md
    kind: external-action
    size_bytes: 4305
  - src: .agent-team/forks/writer-02-day1/content/drafts/day1.md
    dst: content/drafts/day1.md
    kind: external-action
    size_bytes: 8104
  - src: .agent-team/forks/writer-03-day2/content/drafts/day2.md
    dst: content/drafts/day2.md
    kind: external-action
    size_bytes: 7145
  - src: .agent-team/forks/writer-04-day3/content/drafts/day3.md
    dst: content/drafts/day3.md
    kind: external-action
    size_bytes: 8139

  # --- finals (from editor fork) ---
  - src: .agent-team/forks/editor-05-edit/content/final/overview.md
    dst: content/final/overview.md
    kind: external-action
    size_bytes: 4290
  - src: .agent-team/forks/editor-05-edit/content/final/day1.md
    dst: content/final/day1.md
    kind: external-action
    size_bytes: 8118
  - src: .agent-team/forks/editor-05-edit/content/final/day2.md
    dst: content/final/day2.md
    kind: external-action
    size_bytes: 7128
  - src: .agent-team/forks/editor-05-edit/content/final/day3.md
    dst: content/final/day3.md
    kind: external-action
    size_bytes: 8091
  - src: .agent-team/forks/editor-05-edit/content/seo/metadata.yaml
    dst: content/seo/metadata.yaml
    kind: external-action
    size_bytes: 1848

  # --- illustrations (from illustrator fork) ---
  - src: .agent-team/forks/illustrator-06-illustrations/content/illustrations/overview-prompts.md
    dst: content/illustrations/overview-prompts.md
    kind: external-action
    size_bytes: 1078
  - src: .agent-team/forks/illustrator-06-illustrations/content/illustrations/day1-prompts.md
    dst: content/illustrations/day1-prompts.md
    kind: external-action
    size_bytes: 1178
  - src: .agent-team/forks/illustrator-06-illustrations/content/illustrations/day2-prompts.md
    dst: content/illustrations/day2-prompts.md
    kind: external-action
    size_bytes: 1140
  - src: .agent-team/forks/illustrator-06-illustrations/content/illustrations/day3-prompts.md
    dst: content/illustrations/day3-prompts.md
    kind: external-action
    size_bytes: 1224

conflicts: []  # directory-fork: each fork writes a disjoint path set; no overlapping dst

rollback_hint: |
  删除 content/ 目录下对应文件即可回滚；原始内容保留在 .agent-team/forks/ 中。
  快速命令: rm -rf content/drafts content/final content/seo content/illustrations

task_rollback: .agent-team/snapshots/  # 若主会话在 apply 前已创建任务级快照，可一键回退到任务开始前
