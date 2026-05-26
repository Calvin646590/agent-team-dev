#!/usr/bin/env bash
# V-6 验证：PreToolUse hook（matcher: Bash）。
# 读 stdin 的 JSON，若 Bash 命令里含 STRICT_TRIPWIRE，则 deny（证明 hook 能注册 + 能拦截 = strict 模式可行）。
# 其余命令一律放行，不影响其他测试。

input=$(cat)

# V-13: best-effort dump 完整 payload，供"hook 能否识别当前 subagent 身份"检查。
# 写到项目 .agent-team/hook-payloads.jsonl（每行一条），失败不影响放行。
dump_dir="${CLAUDE_PROJECT_DIR:-$PWD}/.agent-team"
mkdir -p "$dump_dir" 2>/dev/null && printf '%s\n' "$input" >> "$dump_dir/hook-payloads.jsonl" 2>/dev/null || true

if echo "$input" | grep -q "STRICT_TRIPWIRE"; then
  # 现代格式：hookSpecificOutput.permissionDecision
  cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"V-6 HOOK FIRED: agent-team PreToolUse 拦截了含 STRICT_TRIPWIRE 的命令（strict 模式可行性已证）"},"decision":"block","reason":"V-6 HOOK FIRED: blocked STRICT_TRIPWIRE"}
JSON
  exit 0
fi

# 放行
exit 0
