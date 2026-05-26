---
id: 06-illustrations
title: 为定稿文章生成 AI 配图 Prompt
owner: illustrator
depends_on: [05-edit]
next_steps: []
status: done
attempts: 1
outputs:
  - .agent-team/forks/illustrator-06-illustrations/content/illustrations/overview-prompts.md
  - .agent-team/forks/illustrator-06-illustrations/content/illustrations/day1-prompts.md
  - .agent-team/forks/illustrator-06-illustrations/content/illustrations/day2-prompts.md
  - .agent-team/forks/illustrator-06-illustrations/content/illustrations/day3-prompts.md
quality_gate:
  status: passed
  notes: []
---

## 任务说明

读取 `content/final/` 下的定稿，为每篇生成 2-3 个 AI 绘图 prompt。

### 输入
`content/final/overview.md`、`day1.md`、`day2.md`、`day3.md`

### Prompt 格式
```markdown
# Overview 配图

## 封面图
> A panoramic view of Bangkok skyline at dusk, ...

## 城市特色图
> ...
```

- 英文 prompt，适配 Midjourney/DALL-E 风格
- 每篇至少 2 个 prompt，不超过 3 个
- prompt 要体现文章的核心场景和氛围

### 输出路径（工作区内）
- `content/illustrations/overview-prompts.md`
- `content/illustrations/day1-prompts.md`
- `content/illustrations/day2-prompts.md`
- `content/illustrations/day3-prompts.md`
