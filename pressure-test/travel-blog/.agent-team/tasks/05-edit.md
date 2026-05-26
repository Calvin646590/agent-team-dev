---
id: 05-edit
title: 审校全部草稿 + 生成 SEO 元数据
owner: editor
depends_on: [02-day1, 03-day2, 04-day3]
next_steps: []
status: done
attempts: 1
outputs:
  - .agent-team/forks/editor-05-edit/content/final/overview.md
  - .agent-team/forks/editor-05-edit/content/final/day1.md
  - .agent-team/forks/editor-05-edit/content/final/day2.md
  - .agent-team/forks/editor-05-edit/content/final/day3.md
  - .agent-team/forks/editor-05-edit/content/seo/metadata.yaml
quality_gate:
  status: passed
  notes: []
---

## 任务说明

审校 writer 产出的四篇草稿，输出定稿并生成 SEO 元数据。

### 输入
`content/drafts/overview.md`、`day1.md`、`day2.md`、`day3.md`

### 工作内容
1. 逐篇审校：事实准确性、语法、风格一致性、可读性
2. 输出定稿到 `content/final/`（保留原文件名）
3. 生成 `content/seo/metadata.yaml`，格式：

```yaml
pages:
  - slug: overview
    title: "曼谷3日旅行攻略 - 完整指南"
    description: "..."
    keywords: [曼谷, 旅行, 攻略, ...]
  - slug: day1
    ...
  - slug: day2
    ...
  - slug: day3
    ...
```

### 输出路径（工作区内）
- `content/final/overview.md`
- `content/final/day1.md`
- `content/final/day2.md`
- `content/final/day3.md`
- `content/seo/metadata.yaml`
