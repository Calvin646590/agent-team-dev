#!/usr/bin/env python3
"""
agent-team 场景产物机器校验器（诚实复审 item 1）。

目的：把场景测试的"✅"从 LLM 叙述改为**文件系统取证 + 退出码**。
原则：
- 不信 log.md、不信 candidate.md、不信任何 LLM 写的"通过"字样。
- 唯一真值源 = 各 task 文件里 owner 自己声明的 `outputs:` + 磁盘上文件是否真存在且非空。
- development 场景额外**真跑 vitest**，以退出码为准。

用法：
    python3 verify.py                 # 校验全部场景
    python3 verify.py office content  # 只校验指定场景
退出码：全部通过 0；任一失败 1；用法错误 2。

注意：本脚本校验的是「交付物是否真实存在」，**不**校验「编排机制（DAG/fork/snapshot）是否真执行」——
那是 verify_mechanism.py 的职责。两者刻意分开，避免又混成一个笼统的 ✅。
"""
import sys
import os
import re
import subprocess

# 仓库内 pressure-test 根目录（本脚本位于 pressure-test/verify/）
PT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 场景配置：name -> { dir, kind, run_tests }
SCENARIOS = {
    "development": {"dir": "shape-calc",     "kind": "development", "run_tests": True},
    "content":     {"dir": "travel-blog",    "kind": "content",     "run_tests": False},
    "research":    {"dir": "market-report",  "kind": "research",    "run_tests": False},
    "office":      {"dir": "team-onboard",   "kind": "office",      "run_tests": False},
}

# ANSI
G, R, Y, B, X = "\033[32m", "\033[31m", "\033[33m", "\033[1m", "\033[0m"


def ok(s):   return f"{G}PASS{X} {s}"
def bad(s):  return f"{R}FAIL{X} {s}"
def warn(s): return f"{Y}WARN{X} {s}"


def parse_task_outputs(task_path):
    """从一个 task md 的 frontmatter 抽 outputs 列表。支持两种 YAML 写法：
       inline:  outputs: [a, b]
       block:   outputs:\n  - a\n  - b
    """
    with open(task_path, "r", encoding="utf-8") as f:
        text = f.read()
    # 只取首个 frontmatter
    parts = text.split("---")
    front = parts[1] if len(parts) >= 3 else text

    # inline 形式
    m = re.search(r"^outputs:\s*\[([^\]]*)\]", front, re.MULTILINE)
    if m:
        items = [s.strip().strip("\"'") for s in m.group(1).split(",") if s.strip()]
        return items

    # block 形式：outputs: 后面紧跟若干 "- xxx" 行，直到出现下一个顶层键
    m = re.search(r"^outputs:\s*$\n((?:[ \t]+-[ \t]*.+\n?)+)", front, re.MULTILINE)
    if m:
        items = []
        for ln in m.group(1).splitlines():
            ln = ln.strip()
            if ln.startswith("-"):
                items.append(ln[1:].strip().strip("\"'"))
        return items
    return []


def resolve_output_path(declared, project_dir):
    """把声明的 output 路径解析为磁盘真实路径。
    content/research 用 overlay：声明路径形如 .agent-team/forks/<owner>-<id>/<rel>，
    accept 后 overlay 把 <rel> 写进项目根 —— 故剥掉 fork 前缀。
    """
    fork_m = re.match(r"^\.agent-team/forks/[^/]+/(.+)$", declared)
    rel = fork_m.group(1) if fork_m else declared
    return os.path.join(project_dir, rel), rel


def verify_artifacts(name, cfg):
    """校验一个场景声明的全部 outputs 是否真实存在且非空。返回 (pass_count, fail_list)。"""
    project_dir = os.path.join(PT_ROOT, cfg["dir"])
    tasks_dir = os.path.join(project_dir, ".agent-team", "tasks")
    if not os.path.isdir(tasks_dir):
        return 0, [f"缺 {cfg['dir']}/.agent-team/tasks/ —— 该场景没有可校验的任务记录"]

    declared = []  # (task_id, declared_path)
    for fn in sorted(os.listdir(tasks_dir)):
        if not fn.endswith(".md") or fn == "index.md":
            continue
        tp = os.path.join(tasks_dir, fn)
        for out in parse_task_outputs(tp):
            declared.append((fn[:-3], out))

    if not declared:
        return 0, [f"{cfg['dir']}: 任务文件里没有任何 outputs 声明 —— 无法校验交付物"]

    passed, failures = 0, []
    seen = set()
    for task_id, dp in declared:
        disk_path, rel = resolve_output_path(dp, project_dir)
        key = os.path.abspath(disk_path)
        if key in seen:
            continue
        seen.add(key)
        if not os.path.exists(disk_path):
            failures.append(f"[{task_id}] 缺文件: {rel}")
        elif os.path.getsize(disk_path) == 0:
            failures.append(f"[{task_id}] 空文件: {rel}")
        else:
            passed += 1
    return passed, failures


def run_dev_tests(cfg):
    """development 场景真跑 vitest，以退出码为准。返回 (ok_bool, detail)。"""
    project_dir = os.path.join(PT_ROOT, cfg["dir"])
    vitest = os.path.join(project_dir, "node_modules", ".bin", "vitest")
    if not os.path.exists(vitest):
        return None, f"node_modules/.bin/vitest 不存在（未 npm install）—— 跳过真跑，仅校验源码文件存在"
    try:
        r = subprocess.run([vitest, "run"], cwd=project_dir,
                           capture_output=True, text=True, timeout=180)
    except Exception as e:
        return False, f"vitest 执行异常: {e}"
    tail = r.stdout.strip().splitlines()
    summary = next((l for l in reversed(tail) if "Tests" in l or "passed" in l or "failed" in l), "")
    return (r.returncode == 0), f"vitest exit={r.returncode}  {summary.strip()}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    targets = args or list(SCENARIOS.keys())
    for t in targets:
        if t not in SCENARIOS:
            print(f"未知场景: {t}（可选: {', '.join(SCENARIOS)}）", file=sys.stderr)
            return 2

    print(f"{B}agent-team 场景产物机器校验{X}  (pressure-test/)\n")
    any_fail = False
    for name in targets:
        cfg = SCENARIOS[name]
        print(f"{B}■ {name}{X}  ({cfg['dir']}, kind={cfg['kind']})")

        tasks_dir = os.path.join(PT_ROOT, cfg["dir"], ".agent-team", "tasks")
        if not os.path.isdir(tasks_dir) and cfg["run_tests"]:
            # development：无 task 记录时以 vitest 为唯一门，交付物检查跳过
            print("  " + warn("交付物: 无 .agent-team/tasks/ 记录 —— development 以下方 vitest 退出码为准"))
        else:
            passed, failures = verify_artifacts(name, cfg)
            total = passed + len(failures)
            if failures:
                any_fail = True
                print(f"  交付物: {passed}/{total} 存在且非空")
                for fl in failures:
                    print("   " + bad(fl))
            else:
                print("  " + ok(f"交付物: {passed}/{total} 全部存在且非空"))

        if cfg["run_tests"]:
            res, detail = run_dev_tests(cfg)
            if res is True:
                print("  " + ok(f"测试: {detail}"))
            elif res is False:
                any_fail = True
                print("  " + bad(f"测试: {detail}"))
            else:
                print("  " + warn(f"测试: {detail}"))
        print()

    if any_fail:
        print(f"{R}{B}结果: 有场景未通过（退出码 1）{X}")
        return 1
    print(f"{G}{B}结果: 全部通过（退出码 0）{X}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
