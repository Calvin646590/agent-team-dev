# shape-calc

TypeScript 几何图形计算库（agent-team 大任务压测专用项目）。

## 功能目标

提供 `Point`、`Line`、`Circle`、`Rectangle` 四种几何基元，以及各自的 `area()` / `perimeter()` 方法，附带完整单测和 API 文档。

## 技术栈

- TypeScript 5.x
- Vitest（单元测试）
- Node.js 18+

---

## team-config

```yaml
kind: development
mode_default: commander
isolation: git-worktree
publish_strategy: pr-style
apply_policy: require-review
files_scope_enforcement: strict

derivation_rules:
  - pattern: "impl|implement|add|create.*class"
    roles: [developer]
  - pattern: "test|spec|verify"
    roles: [tester]
  - pattern: "doc|readme|document"
    roles: [doc-writer]
  - fallback: coordinator

retry:
  max_attempts: 3
  backoff: exponential

agents:
  developer:
    capabilities: [typescript, node, file-write]
    files_scope:
      write: ["src/**/*.ts"]
      read: ["src/**", "package.json", "tsconfig.json"]
  tester:
    capabilities: [typescript, vitest, test-run]
    files_scope:
      write: ["src/**/*.test.ts", "src/**/*.spec.ts"]
      read: ["src/**", "package.json"]
  doc-writer:
    capabilities: [markdown, documentation]
    files_scope:
      write: ["docs/**", "README.md"]
      read: ["src/**", "package.json"]
```

---

## 压测 DAG 设计（12 子任务）

```
01-init ──► 02-point ──► 03-line ─────────────► 06-area ──► 09-test-line
                    │                        │          │
                    ├──► 04-circle ──────────┤          ├──► 10-test-circle
                    │                        │          │
                    └──► 05-rectangle ───────┘          └──► 11-test-rect ──► 12-docs
                              │                                   ▲
                              └──────────────────► 07-perimeter ──┘
                                                        ▲
                    └──────────── 08-test-point ──► (独立，不阻塞 12)
```

**依赖矩阵：**

| 子任务 | owner | depends_on |
|--------|-------|------------|
| 01-init | developer | — |
| 02-point | developer | 01 |
| 03-line | developer | 02 |
| 04-circle | developer | 02 |
| 05-rectangle | developer | 02 |
| 06-area | developer | 03, 04, 05 |
| 07-perimeter | developer | 03, 04, 05 |
| 08-test-point | tester | 02 |
| 09-test-line | tester | 06, 07 |
| 10-test-circle | tester | 06, 07 |
| 11-test-rect | tester | 06, 07 |
| 12-docs | doc-writer | 08, 09, 10, 11 |

**死锁测试开关**（压测时可选注入）：
- 将 `05-rectangle` 的 task 文件 status 手动置为 `blocked`，则 06/07 永远无法 ready → 触发死锁检测路径

## 项目结构（目标）

```
src/
  geometry/
    point.ts
    line.ts
    circle.ts
    rectangle.ts
    area.ts
    perimeter.ts
  __tests__/
    point.test.ts
    line.test.ts
    circle.test.ts
    rectangle.test.ts
docs/
  API.md
package.json
tsconfig.json
vitest.config.ts
```
