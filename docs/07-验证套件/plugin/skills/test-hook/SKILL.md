---
name: test-hook
description: 验证 V-6 —— plugin 注册的 PreToolUse hook 能否拦截工具调用。当用户说"测试钩子"、"test hook"、"验证hook"时触发。
---

# V-6 验证：PreToolUse hook 拦截

你（**主会话**）现在被 `test-hook` skill 加载。任务：**验证 plugin 注册的 PreToolUse hook 真的会触发并能拦截 Bash 调用**（strict 模式 files_scope 强制的基础，ADR-0019）。

plugin v0.0.5 注册了一个 PreToolUse hook（matcher: Bash）：命令里含 `STRICT_TRIPWIRE` 就 deny，其余放行。

## 必须完成，原样报告（不解读、不兜底）

### 步骤 1：先证明普通 Bash 能跑（hook 不误伤）
用 Bash 跑：
```
echo "normal command ok"
```
应正常返回 `normal command ok`。原样贴。

### 步骤 2：触发 tripwire，看是否被拦截
用 Bash 跑：
```
echo "STRICT_TRIPWIRE should be blocked"
```
**关注**：这条命令是被 hook 拦下了（你会收到 deny / block + 含 "V-6 HOOK FIRED" 的理由），还是正常执行打印了那行字？

### 步骤 3：结论
- **普通命令正常跑了吗？** 是 / 否
- **含 STRICT_TRIPWIRE 的命令被拦截了吗？** 拦截了（贴 deny 理由原文）/ 没拦截（正常打印了）
- **看到 "V-6 HOOK FIRED" 字样了吗？** 看到 / 没看到

## 判定
- 普通命令通 + tripwire 被拦 + 看到 "V-6 HOOK FIRED" → **V-6 通过**（PreToolUse hook 可注册可拦截，strict 模式可行）
- tripwire 没被拦（正常打印） → V-6 不通过（hook 没注册或没生效），需排查 hooks/hooks.json 是否被加载（可能要在 plugin.json 显式声明 hooks 字段）

## 禁止
- 不要派 subagent 代跑（hook 作用于主会话的工具调用）
- 不要因为命令"看起来危险"就跳过步骤 2 —— 那行 echo 无害，就是用来触发 hook 的
- 不要解读、不要美化
