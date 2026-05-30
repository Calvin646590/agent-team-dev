#!/usr/bin/env python3
"""
git-worktree 运行时证据 hook 自测（诚实复审方案二·收尾 / ADR-0055）。
用**真实 git worktree** + 真实子进程证明：写入 worktree 会被自动留痕（含分支名），
证据写到主仓库且 worktree 删除后仍在。

测点：
  A 写入 worktree 内文件   → 主仓库 evidence/worktrees.jsonl 出现记录（branch/worktree/真实ts）
  B 写主工作树（非 worktree）→ 不留痕（.git 是目录，非 worktree）
  C `git worktree remove` 后 → 证据仍在主仓库（accept 清理带不走）
退出码：全过 0；任一失败 1；无 git 时跳过（exit 0，标注 SKIP）。
"""
import sys, os, json, subprocess, tempfile, shutil, re

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "agent-team", "hooks", "worktree-evidence-guard.py")
G, R, Y, RST = "\033[32m", "\033[31m", "\033[33m", "\033[0m"


def git(args, cwd):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)


def run_hook(payload):
    p = subprocess.run([sys.executable, HOOK], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=30)
    return p.returncode


def read_ev(main_root):
    f = os.path.join(main_root, ".agent-team", "evidence", "worktrees.jsonl")
    if not os.path.exists(f):
        return []
    return [json.loads(l) for l in open(f, encoding="utf-8") if l.strip()]


def main():
    if not os.path.exists(HOOK):
        print(R + "FAIL" + RST + f" 找不到 hook: {HOOK}"); return 1
    if shutil.which("git") is None:
        print(Y + "SKIP" + RST + " 环境无 git，跳过 worktree 自测"); return 0

    fails = []
    main_root = tempfile.mkdtemp(prefix="wtev_main_")
    wt = tempfile.mkdtemp(prefix="wtev_wt_"); os.rmdir(wt)  # git worktree add 需目标不存在
    try:
        # 建主仓库 + 初始提交
        git(["init", "-q"], main_root)
        git(["config", "user.email", "t@t.t"], main_root)
        git(["config", "user.name", "t"], main_root)
        open(os.path.join(main_root, "seed.txt"), "w").write("seed")
        git(["add", "-A"], main_root); git(["commit", "-qm", "init"], main_root)
        # 加一个 worktree（独立分支）
        r = git(["worktree", "add", "-q", "-b", "agent-team/dev-x", wt], main_root)
        if r.returncode != 0:
            print(R + "FAIL" + RST + f" 无法创建 worktree: {r.stderr.strip()}"); return 1

        # A: 在 worktree 内写文件
        f1 = os.path.join(wt, "src", "feature.ts")
        os.makedirs(os.path.dirname(f1)); open(f1, "w").write("code")
        rc = run_hook({"agent_type": "developer", "session_id": "s1", "cwd": wt,
                       "tool_input": {"file_path": f1}})
        ev = read_ev(main_root)
        if rc != 0:
            fails.append(f"A: 退出码 {rc} ≠ 0")
        elif len(ev) != 1:
            fails.append(f"A: 期望 1 条证据，实得 {len(ev)}: {ev}")
        elif ev[0]["branch"] != "agent-team/dev-x" or ev[0]["agent_type"] != "developer":
            fails.append(f"A: 证据字段不符: {ev[0]}")
        elif "T00:00:00" in ev[0]["ts"] or not re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", ev[0]["ts"]):
            fails.append(f"A: 时间戳非真实/疑伪造: {ev[0]['ts']}")
        else:
            print(G + "PASS" + RST + f" A 写 worktree → 留痕（branch={ev[0]['branch']}, ts={ev[0]['ts']}）")

        # B: 写主工作树（.git 是目录，非 worktree）→ 不留痕
        f2 = os.path.join(main_root, "main_file.txt")
        open(f2, "w").write("x")
        run_hook({"agent_type": "developer", "session_id": "s1", "cwd": main_root,
                  "tool_input": {"file_path": f2}})
        if len(read_ev(main_root)) == 1:  # 仍只有 A 那一条
            print(G + "PASS" + RST + " B 写主工作树（非 worktree）→ 正确地不留痕")
        else:
            fails.append("B: 主工作树写入不应留痕")

        # C: 移除 worktree 后，证据仍在主仓库
        git(["worktree", "remove", "--force", wt], main_root)
        if len(read_ev(main_root)) == 1 and not os.path.exists(wt):
            print(G + "PASS" + RST + " C git worktree remove 后 → 证据仍在主仓库（清理带不走）")
        else:
            fails.append("C: worktree 移除后证据丢失")
    finally:
        shutil.rmtree(main_root, ignore_errors=True)
        shutil.rmtree(wt, ignore_errors=True)

    print()
    if fails:
        for fl in fails: print(R + "FAIL" + RST + " " + fl)
        print(R + "worktree 证据 hook 自测未通过（退出码 1）" + RST); return 1
    print(G + "worktree 证据 hook 自测全过（退出码 0）—— git-worktree 隔离现可后验" + RST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
