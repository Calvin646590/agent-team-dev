# agent-team task index — 曼谷旅行博客

**任务**：写一篇关于曼谷的目的地旅行博客（总览 + Day1/2/3）
**kind**: content | **mode**: commander | **isolation**: directory-fork

## DAG

```
01-overview ──► 02-day1 ──┐
             ├► 03-day2 ──┼──► 05-edit ──► 06-illustrations
             └► 04-day3 ──┘
```

## 子任务状态

| ID | 标题 | Owner | 依赖 | 状态 |
|----|------|-------|------|------|
| 01-overview | 总览页 | writer | — | ✅ done |
| 02-day1 | Day 1 大皇宫与湄南河 | writer | 01 | ✅ done |
| 03-day2 | Day 2 都市购物美食 | writer | 01 | ✅ done |
| 04-day3 | Day 3 寺庙深度游 | writer | 01 | ✅ done |
| 05-edit | 审校 + SEO | editor | 02,03,04 | ✅ done |
| 06-illustrations | 配图 Prompt | illustrator | 05 | ✅ done |

## 当前 Ready
- **全部完成** ✅ → 派发 Merger
