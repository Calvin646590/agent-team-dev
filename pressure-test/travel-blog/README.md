# travel-blog

旅行博客内容项目（agent-team content 场景测试专用）。

## 功能目标

为"东京 3 日旅行攻略"生成一套完整的博客内容：文案（中文）、配图描述、SEO 元数据，多角色协作产出。

## 角色分工

- **writer**：写正文（Day 1/2/3 三篇 + 总览页），Markdown 格式
- **editor**：审校 writer 产出，修正事实/语法/风格，补充 SEO 元数据
- **illustrator**：为每篇生成配图描述（prompt-style，供后续 AI 绘图使用）

---

## team-config

```yaml
kind: content
mode_default: commander
isolation: directory-fork
publish_strategy: overlay
apply_policy: require-review
files_scope_enforcement: strict

derivation_rules:
  - pattern: "write|draft|create.*article"
    roles: [writer]
  - pattern: "edit|review|proofread|seo"
    roles: [editor]
  - pattern: "illustrat|image|visual|picture"
    roles: [illustrator]
  - fallback: coordinator

retry:
  max_attempts: 3
  backoff: exponential

agents:
  writer:
    capabilities: [markdown, chinese-writing, travel-knowledge]
    files_scope:
      write: ["content/drafts/**/*.md"]
      read: ["content/**", "README.md"]
  editor:
    capabilities: [editing, seo, fact-check, chinese-writing]
    files_scope:
      write: ["content/final/**/*.md", "content/seo/**"]
      read: ["content/**", "README.md"]
  illustrator:
    capabilities: [prompt-writing, visual-description]
    files_scope:
      write: ["content/illustrations/**"]
      read: ["content/**", "README.md"]
```

---

## DAG 设计（6 子任务）

```
01-overview ──► 02-day1 ──► 05-edit ──► 06-illustrations
                02-day2 ──►    ▲
                02-day3 ──►    │
                03-day2 ──────┘
                04-day3 ──────┘
```

简化版：

| 子任务 | owner | depends_on |
|--------|-------|------------|
| 01-overview | writer | -- |
| 02-day1 | writer | 01 |
| 03-day2 | writer | 01 |
| 04-day3 | writer | 01 |
| 05-edit | editor | 02, 03, 04 |
| 06-illustrations | illustrator | 05 |

## 项目结构（目标）

```
content/
  drafts/
    overview.md
    day1.md
    day2.md
    day3.md
  final/
    overview.md
    day1.md
    day2.md
    day3.md
  seo/
    metadata.yaml
  illustrations/
    day1-prompts.md
    day2-prompts.md
    day3-prompts.md
```
