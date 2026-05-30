#!/usr/bin/env python3
"""
files-scope strict hook 自测（诚实复审 item 5）。
重点验证 ADR-0052 修复：cwd 是子目录/worktree 路径时，hook 仍能向上找到项目根并正确强制，
不再静默 fail-open。用真实文件 + 真实子进程 + 输出断言，不靠叙述。

测点：
  A strict + 越界写            → deny
  B strict + 范围内写          → allow
  C strict + cwd 是子目录(bug) → 仍 deny（向上找到根，修复前会误放行）
  D advisory(无 strict)        → allow（即便越界）
  E 主会话(无 agent_type)      → allow
退出码：全过 0；任一失败 1。
"""
import sys, os, json, subprocess, tempfile, shutil

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "agent-team", "hooks", "files-scope-guard.py")
G, R, RST = "\033[32m", "\033[31m", "\033[0m"


def run(payload):
    p = subprocess.run([sys.executable, HOOK], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=30)
    denied = "deny" in p.stdout
    return denied, p.returncode


def mk_project(strict=True):
    d = tempfile.mkdtemp(prefix="scopetest_")
    enf = "files_scope_enforcement: strict\n" if strict else ""
    with open(os.path.join(d, "README.md"), "w") as f:
        f.write(f"# proj\n\n## team-config\n```yaml\nkind: development\n{enf}```\n")
    ag = os.path.join(d, ".claude", "agents")
    os.makedirs(ag)
    with open(os.path.join(ag, "developer.md"), "w") as f:
        f.write("---\nname: developer\nfiles_scope:\n  write: [\"src/**/*.ts\"]\n---\n你是开发者\n")
    return d


def main():
    if not os.path.exists(HOOK):
        print(R + "FAIL" + RST + f" 找不到 hook: {HOOK}"); return 1
    fails = []

    # A strict + 越界
    d = mk_project(strict=True)
    try:
        denied, rc = run({"agent_type": "developer", "cwd": d,
                          "tool_input": {"file_path": os.path.join(d, "secrets/key.txt")}})
        if denied: print(G + "PASS" + RST + " A strict + 越界写 → deny")
        else: fails.append("A: 越界写未被拦截")
    finally: shutil.rmtree(d, ignore_errors=True)

    # B strict + 范围内
    d = mk_project(strict=True)
    try:
        denied, rc = run({"agent_type": "developer", "cwd": d,
                          "tool_input": {"file_path": os.path.join(d, "src/app.ts")}})
        if not denied: print(G + "PASS" + RST + " B strict + 范围内写 → allow")
        else: fails.append("B: 范围内写被误拦")
    finally: shutil.rmtree(d, ignore_errors=True)

    # C strict + cwd 是子目录（ADR-0052 修复点）
    d = mk_project(strict=True)
    try:
        subdir = os.path.join(d, "src", "deep", "nested")
        os.makedirs(subdir)
        denied, rc = run({"agent_type": "developer", "cwd": subdir,
                          "tool_input": {"file_path": os.path.join(d, "config/prod.yaml")}})
        if denied: print(G + "PASS" + RST + " C strict + cwd=子目录 + 越界写 → 仍 deny（向上找到项目根）")
        else: fails.append("C: cwd 为子目录时越界写未被拦截（worktree/子目录 fail-open 未修复）")
    finally: shutil.rmtree(d, ignore_errors=True)

    # D advisory（无 strict）
    d = mk_project(strict=False)
    try:
        denied, rc = run({"agent_type": "developer", "cwd": d,
                          "tool_input": {"file_path": os.path.join(d, "secrets/key.txt")}})
        if not denied: print(G + "PASS" + RST + " D advisory（无 strict）→ allow（即便越界）")
        else: fails.append("D: advisory 模式不应拦截")
    finally: shutil.rmtree(d, ignore_errors=True)

    # E 主会话（无 agent_type）
    d = mk_project(strict=True)
    try:
        denied, rc = run({"cwd": d, "tool_input": {"file_path": os.path.join(d, "secrets/key.txt")}})
        if not denied: print(G + "PASS" + RST + " E 主会话（无 agent_type）→ allow")
        else: fails.append("E: 主会话不应受 per-agent scope 约束")
    finally: shutil.rmtree(d, ignore_errors=True)

    print()
    if fails:
        for fl in fails: print(R + "FAIL" + RST + " " + fl)
        print(R + "files-scope hook 自测未通过（退出码 1）" + RST); return 1
    print(G + "files-scope hook 自测全过（退出码 0）—— 含 worktree/子目录 fail-open 修复" + RST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
