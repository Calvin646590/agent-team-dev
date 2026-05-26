# string-utils

一个极小的字符串工具库，作为 **agent-team development 单场景 demo** 的目标项目。

## API

- `capitalize(s)` —— 首字母大写
- `truncate(s, n)` —— 截断到至多 n 个字符，超出加省略号
- `slugify(s)` —— 将字符串转为 URL 友好的 slug：转小写、空格替换为连字符、去除非 `[a-z0-9-]` 字符
- `slugifyUnique(strs)` —— 对字符串数组每项调用 `slugify`，重复结果依次加 `-2`、`-3` 等后缀以保证唯一

## 测试

```bash
npm test    # 等价 node --test
```

---

## team-config

```yaml
kind: development                  # development | content | research | office
mode_default: observer             # commander | observer
scheduling: dag                    # dag | parallel-force
files_scope_enforcement: advisory  # advisory | strict（改 strict 可激活 per-agent 写权限硬约束）

retry:
  max_attempts: 3
  base_seconds: 5
  timeout_minutes: 10

derivation_rules:
  - pattern: "实现|函数|功能|feature|逻辑"
    roles: [developer]
  - pattern: "测试|test|用例"
    roles: [tester]
  - pattern: "文档|README|说明|API 列表"
    roles: [doc-writer]
  - pattern: ".*"
    fallback: coordinator
```

> 这是 agent-team 的项目级配置。业务角色定义在 `.claude/agents/`（developer / tester / doc-writer）。
> 用法：以本目录为根打开 Claude Code 会话，安装 agent-team plugin 后，对团队下达任务即可。
