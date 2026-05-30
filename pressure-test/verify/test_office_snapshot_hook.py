#!/usr/bin/env python3
"""
office 写前快照 hook 自测（诚实复审 item 6）。
用真实文件 + 真实 hook 子进程证明机制有效——不是叙述，是退出码。

测点：
  A 覆盖已存在文件 → 生成真实快照（内容正确 + MANIFEST 含真实时间戳，非 T000000）
  B 新建文件（无前态）→ 不快照（正确行为），仍放行
  C 非 office 项目 → hook 不动作
  D 目标在 .agent-team/ 内 → 跳过（不快照框架自身文件）
退出码：全过 0；任一失败 1。
"""
import sys, os, json, subprocess, tempfile, shutil, re

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "agent-team", "hooks", "office-snapshot-guard.py")
G, R, X = "\033[32m", "\033[31m", "\033[1m"
RST = "\033[0m"


def run_hook(payload):
    p = subprocess.run([sys.executable, HOOK], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=30)
    return p.returncode


def mk_project(office=True):
    d = tempfile.mkdtemp(prefix="snaptest_")
    cfg = "kind: office\nisolation: none\n" if office else "kind: development\nisolation: git-worktree\n"
    with open(os.path.join(d, "README.md"), "w") as f:
        f.write(f"# test\n\n## team-config\n```yaml\n{cfg}```\n")
    return d


def main():
    if not os.path.exists(HOOK):
        print(R + "FAIL" + RST + f" 找不到 hook: {HOOK}")
        return 1
    fails = []

    # ---- A: 覆盖已存在文件 ----
    d = mk_project(office=True)
    try:
        target = os.path.join(d, "onboard", "hr", "welcome.md")
        os.makedirs(os.path.dirname(target))
        with open(target, "w") as f:
            f.write("ORIGINAL_CONTENT_v1")
        rc = run_hook({
            "session_id": "sess-ABC123", "agent_type": "hr-assistant", "cwd": d,
            "tool_input": {"file_path": target},
        })
        snap = os.path.join(d, ".agent-team", "snapshots", "sess-ABC123", "onboard", "hr", "welcome.md")
        manifest = os.path.join(d, ".agent-team", "snapshots", "sess-ABC123", "MANIFEST.jsonl")
        if rc != 0:
            fails.append(f"A: hook 退出码 {rc} ≠ 0（应放行）")
        elif not os.path.isfile(snap):
            fails.append("A: 未生成快照文件")
        elif open(snap).read() != "ORIGINAL_CONTENT_v1":
            fails.append("A: 快照内容与原文件不符")
        elif not os.path.isfile(manifest):
            fails.append("A: 未写 MANIFEST")
        else:
            ts = json.loads(open(manifest).readline())["ts"]
            if re.search(r"T00:00:00$", ts) or "0000" in ts.replace("-", "").split("T")[1] if "T" in ts else False:
                fails.append(f"A: MANIFEST 时间戳可疑伪造: {ts}")
            elif not re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", ts):
                fails.append(f"A: MANIFEST 时间戳非真实 ISO: {ts}")
            else:
                print(G + "PASS" + RST + f" A 覆盖已存在文件 → 真实快照（内容正确, ts={ts}）")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # ---- B: 新建文件，无前态 ----
    d = mk_project(office=True)
    try:
        target = os.path.join(d, "onboard", "new.md")  # 不预先创建
        rc = run_hook({"session_id": "s2", "agent_type": "hr-assistant", "cwd": d,
                       "tool_input": {"file_path": target}})
        snaproot = os.path.join(d, ".agent-team", "snapshots")
        if rc != 0:
            fails.append(f"B: 退出码 {rc} ≠ 0")
        elif os.path.exists(snaproot) and any(os.scandir(snaproot)):
            fails.append("B: 新建文件不应产生快照，却产生了")
        else:
            print(G + "PASS" + RST + " B 新建文件 → 正确地不快照，放行")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # ---- C: 非 office 项目 ----
    d = mk_project(office=False)
    try:
        target = os.path.join(d, "src", "x.ts")
        os.makedirs(os.path.dirname(target)); open(target, "w").write("CODE")
        rc = run_hook({"session_id": "s3", "agent_type": "developer", "cwd": d,
                       "tool_input": {"file_path": target}})
        snaproot = os.path.join(d, ".agent-team", "snapshots")
        if rc != 0:
            fails.append(f"C: 退出码 {rc} ≠ 0")
        elif os.path.exists(snaproot):
            fails.append("C: 非 office 不应动作，却建了 snapshots/")
        else:
            print(G + "PASS" + RST + " C 非 office 项目 → hook 不干预")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # ---- D: 目标在 .agent-team/ 内 ----
    d = mk_project(office=True)
    try:
        target = os.path.join(d, ".agent-team", "tasks", "01.md")
        os.makedirs(os.path.dirname(target)); open(target, "w").write("TASK")
        rc = run_hook({"session_id": "s4", "agent_type": "hr-assistant", "cwd": d,
                       "tool_input": {"file_path": target}})
        snaproot = os.path.join(d, ".agent-team", "snapshots")
        if rc != 0:
            fails.append(f"D: 退出码 {rc} ≠ 0")
        elif os.path.exists(snaproot):
            fails.append("D: 不应快照 .agent-team/ 内部文件")
        else:
            print(G + "PASS" + RST + " D .agent-team/ 内部文件 → 正确跳过")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    print()
    if fails:
        for fl in fails:
            print(R + "FAIL" + RST + " " + fl)
        print(f"{R}{X}office 快照 hook 自测未通过（退出码 1）{RST}")
        return 1
    print(f"{G}{X}office 快照 hook 自测全过（退出码 0）—— 机制是真实代码，非叙述{RST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
