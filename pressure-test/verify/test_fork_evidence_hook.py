#!/usr/bin/env python3
"""
directory-fork 运行时证据 hook 自测（诚实复审方案二 / ADR-0054）。
用真实文件 + 真实子进程证明：写入 fork 会被自动留痕、且证据独立于 forks/ 目录而长存。

测点：
  A 写入 fork 内文件        → evidence/forks.jsonl 出现记录（agent/fork/file/真实时间戳）
  B 两个 agent 各写各的 fork → 两条记录，fork 字段不同（隔离边界可见）
  C 证据在 forks/ 删除后仍在 → 删掉 forks/，forks.jsonl 不受影响（accept 带不走证据）
  D 写主目录（非 fork）      → 不留痕（与本 hook 无关）
退出码：全过 0；任一失败 1。
"""
import sys, os, json, subprocess, tempfile, shutil, re

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "agent-team", "hooks", "fork-evidence-guard.py")
G, R, RST = "\033[32m", "\033[31m", "\033[0m"


def run(payload):
    p = subprocess.run([sys.executable, HOOK], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=30)
    return p.returncode


def read_evidence(proj):
    f = os.path.join(proj, ".agent-team", "evidence", "forks.jsonl")
    if not os.path.exists(f):
        return []
    return [json.loads(l) for l in open(f, encoding="utf-8") if l.strip()]


def main():
    if not os.path.exists(HOOK):
        print(R + "FAIL" + RST + f" 找不到 hook: {HOOK}"); return 1
    fails = []

    # A + B + C 共用一个项目
    proj = tempfile.mkdtemp(prefix="forkev_")
    try:
        # A: writer 写自己的 fork
        f1 = os.path.join(proj, ".agent-team", "forks", "writer-01-overview", "content", "drafts", "overview.md")
        os.makedirs(os.path.dirname(f1)); open(f1, "w").write("draft")
        rc = run({"agent_type": "writer", "session_id": "s1", "cwd": proj,
                  "tool_input": {"file_path": f1}})
        ev = read_evidence(proj)
        if rc != 0:
            fails.append(f"A: 退出码 {rc} ≠ 0")
        elif len(ev) != 1:
            fails.append(f"A: 期望 1 条证据，实得 {len(ev)}")
        elif ev[0]["fork"] != "writer-01-overview" or ev[0]["agent_type"] != "writer":
            fails.append(f"A: 证据字段不符: {ev[0]}")
        elif not re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", ev[0]["ts"]) or "T00:00:00" in ev[0]["ts"]:
            fails.append(f"A: 时间戳非真实/疑伪造: {ev[0]['ts']}")
        else:
            print(G + "PASS" + RST + f" A 写 fork → 自动留痕（fork={ev[0]['fork']}, ts={ev[0]['ts']}）")

        # B: 第二个 agent 写另一个 fork
        f2 = os.path.join(proj, ".agent-team", "forks", "editor-05-edit", "content", "final", "overview.md")
        os.makedirs(os.path.dirname(f2)); open(f2, "w").write("final")
        run({"agent_type": "editor", "session_id": "s1", "cwd": proj, "tool_input": {"file_path": f2}})
        ev = read_evidence(proj)
        forks = {r["fork"] for r in ev}
        if forks == {"writer-01-overview", "editor-05-edit"} and len(ev) == 2:
            print(G + "PASS" + RST + " B 两 agent 各写各 fork → 两条记录、fork 字段不同（隔离边界可见）")
        else:
            fails.append(f"B: 期望两个不同 fork 各一条，实得 {ev}")

        # C: 删掉 forks/，证据应仍在
        shutil.rmtree(os.path.join(proj, ".agent-team", "forks"))
        ev_after = read_evidence(proj)
        if len(ev_after) == 2:
            print(G + "PASS" + RST + " C 删除 forks/ 后 → 证据仍在（accept 清理带不走 evidence/）")
        else:
            fails.append(f"C: forks/ 删除后证据丢失，实得 {len(ev_after)} 条")
    finally:
        shutil.rmtree(proj, ignore_errors=True)

    # D: 写主目录（非 fork）不留痕
    proj = tempfile.mkdtemp(prefix="forkev_")
    try:
        fmain = os.path.join(proj, "content", "drafts", "overview.md")
        os.makedirs(os.path.dirname(fmain)); open(fmain, "w").write("x")
        run({"agent_type": "writer", "session_id": "s2", "cwd": proj, "tool_input": {"file_path": fmain}})
        if not read_evidence(proj):
            print(G + "PASS" + RST + " D 写主目录（非 fork）→ 正确地不留痕")
        else:
            fails.append("D: 非 fork 写入不应留痕")
    finally:
        shutil.rmtree(proj, ignore_errors=True)

    print()
    if fails:
        for fl in fails: print(R + "FAIL" + RST + " " + fl)
        print(R + "fork 证据 hook 自测未通过（退出码 1）" + RST); return 1
    print(G + "fork 证据 hook 自测全过（退出码 0）—— directory-fork 隔离现可后验" + RST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
