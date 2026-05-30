#!/usr/bin/env python3
"""
agent-team 编排机制完整性校验器（诚实复审 item 1 · 防欺骗层）。

verify.py 只证明「交付物存在」——但一个 LLM 完全可以一次性把所有文件写出来、
再编一段 log 谎称"DAG 调度 + fork 隔离 + 快照"都跑过。本脚本专门抓这种叙述造假：
检查编排机制是否在磁盘上留下了**真实、不可伪造**的痕迹。

可后验校验的机制（留痕，本脚本检查）：
  - office 写前快照：snapshots/<id>-<timestamp>/，时间戳必须是真实 date 输出
  - log.md 时间戳真实性：真跑会调用 date，造假常留裸日期/占位符

无法后验校验的机制（痕迹会被 accept 清理，只能在运行当时取证）：
  - content/research 的 directory-fork：overlay accept 后 forks/ 被删，事后无据
  - development 的 worktree：accept 后清理
  → 这些场景必须在「运行当时」保留证据，本脚本会明确标注 UNVERIFIABLE，绝不假装通过。

退出码：全部通过/仅有不可校验项 0；发现造假或机制缺失 1。
"""
import sys
import os
import re
import subprocess

PT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(PT_ROOT)
HOOK = os.path.join(REPO_ROOT, "agent-team", "hooks", "office-snapshot-guard.py")
HOOKS_JSON = os.path.join(REPO_ROOT, "agent-team", "hooks", "hooks.json")
HOOK_SELFTEST = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "test_office_snapshot_hook.py")
G, R, Y, B, X = "\033[32m", "\033[31m", "\033[33m", "\033[1m", "\033[0m"


def ok(s):     return f"{G}PASS{X} {s}"
def bad(s):    return f"{R}FAIL{X} {s}"
def warn(s):   return f"{Y}WARN{X} {s}"
def unver(s):  return f"{Y}UNVERIFIABLE{X} {s}"


def is_fabricated_timestamp(ts):
    """判断快照目录名里的时间戳是否是 LLM 编的占位符而非真实 date 输出。
    真实: 20260526T213355 ；造假典型: 20260526T000000 / TIMESTAMP / <timestamp>
    """
    m = re.search(r"T(\d{6})$", ts)
    if not m:
        return True  # 根本没有合法时分秒结构
    return m.group(1) == "000000"  # 全零 = date 永不产出，必为手打占位符


def check_office_snapshots():
    """office 写前快照机制取证（item 6 后：机制已从 prompt 剧场改为真实 hook 代码）。

    正确语义：快照只针对「覆盖已存在文件」。office 测试若全是新建文件，
    零快照是**正确**结果，不应判负。因此本检查不再数"应有几个快照"，而是验证：
      1. 真实 hook 代码存在且已在 hooks.json 注册
      2. hook 自测通过（真覆盖→真快照→真时间戳），以退出码为准
      3. 任何遗留快照目录都不得是伪造时间戳（保留旧造假探测）
    返回 (fail_bool, lines)。
    """
    lines, fail = [], False

    # 1. hook 存在 + 注册
    if not os.path.isfile(HOOK):
        return True, [bad(f"office 快照 hook 不存在: {os.path.relpath(HOOK, REPO_ROOT)}")]
    lines.append("  " + ok(f"真实 hook 存在: agent-team/hooks/office-snapshot-guard.py"))
    try:
        registered = "office-snapshot-guard.py" in open(HOOKS_JSON, encoding="utf-8").read()
    except Exception:
        registered = False
    if registered:
        lines.append("  " + ok("已在 hooks.json 的 PreToolUse 注册（写操作自动触发，不靠 LLM 自觉）"))
    else:
        fail = True
        lines.append("  " + bad("hook 未在 hooks.json 注册 —— 不会被运行时触发"))

    # 2. hook 自测（真实文件 + 真实子进程 + 真实时间戳）
    if os.path.isfile(HOOK_SELFTEST):
        try:
            r = subprocess.run([sys.executable, HOOK_SELFTEST],
                               capture_output=True, text=True, timeout=60)
            if r.returncode == 0:
                lines.append("  " + ok("hook 自测通过：真覆盖→真快照→真 ISO 时间戳（test_office_snapshot_hook.py exit 0）"))
            else:
                fail = True
                lines.append("  " + bad(f"hook 自测失败 exit={r.returncode}：\n{r.stdout.strip()}"))
        except Exception as e:
            fail = True
            lines.append("  " + bad(f"hook 自测无法运行: {e}"))
    else:
        fail = True
        lines.append("  " + bad("缺 test_office_snapshot_hook.py 自测"))

    # 3. 遗留快照造假探测（任何 pressure-test 项目里残留的伪造时间戳目录）
    for proj in ("team-onboard", "travel-blog", "market-report"):
        snap_root = os.path.join(PT_ROOT, proj, ".agent-team", "snapshots")
        if not os.path.isdir(snap_root):
            continue
        for d in sorted(os.listdir(snap_root)):
            full = os.path.join(snap_root, d)
            if os.path.isdir(full) and is_fabricated_timestamp(d):
                fail = True
                lines.append("  " + bad(f"残留伪造时间戳快照: {proj}/.agent-team/snapshots/{d}"))
    return fail, lines


def check_log_authenticity(scenario, project_dir):
    """log.md 时间戳真实性启发式：真跑会调 date 留下 HH:MM:SS；造假常留裸日期。
    仅作 WARN（启发式，不作判负的硬依据）。"""
    log = os.path.join(project_dir, ".agent-team", "log.md")
    if not os.path.exists(log):
        return [warn(f"{scenario}: 无 log.md")]
    with open(log, encoding="utf-8") as f:
        text = f.read()
    content_lines = [l for l in text.splitlines()
                     if l.strip() and not l.lstrip().startswith("#")
                     and re.search(r"\d", l)]
    real_ts = sum(1 for l in content_lines if re.search(r"\d{2}:\d{2}:\d{2}", l))
    if content_lines and real_ts == 0:
        return [warn(f"{scenario}: log.md 全部 {len(content_lines)} 条记录都无秒级时间戳 —— "
                     f"疑似未真实调用 date，编排过程可能是事后叙述")]
    return [ok(f"{scenario}: log.md 含 {real_ts} 条真实秒级时间戳")]


def run_selftest(path, label):
    """跑一个 hook 自测脚本，返回 (fail_bool, line)。"""
    if not os.path.isfile(path):
        return True, bad(f"{label}: 缺自测脚本 {os.path.basename(path)}")
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=60)
    except Exception as e:
        return True, bad(f"{label}: 自测无法运行: {e}")
    if r.returncode == 0:
        return False, ok(f"{label}: 自测通过（exit 0）")
    return True, bad(f"{label}: 自测失败 exit={r.returncode}\n{r.stdout.strip()}")


SCOPE_SELFTEST = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "test_files_scope_hook.py")


def main():
    print(f"{B}agent-team 编排机制完整性校验（防叙述造假）{X}\n")
    any_fail = False

    print(f"{B}■ office 写前快照机制{X}")
    fail, lines = check_office_snapshots()
    for l in lines:
        print(l)
    any_fail = any_fail or fail
    print()

    print(f"{B}■ strict 文件域强制（真实 hook 代码，含 worktree/子目录 fail-open 修复）{X}")
    fail, line = run_selftest(SCOPE_SELFTEST, "files-scope-guard")
    print("  " + line)
    any_fail = any_fail or fail
    print()

    print(f"{B}■ log.md 时间戳真实性（启发式 WARN）{X}")
    for name, d in [("content", "travel-blog"), ("research", "market-report"),
                    ("office", "team-onboard")]:
        for l in check_log_authenticity(name, os.path.join(PT_ROOT, d)):
            print("  " + l)
    print()

    print(f"{B}■ 运行时机制（accept 后痕迹已清，无法后验）{X}")
    print("  " + unver("content/research directory-fork：overlay accept 已删 forks/，事后无据可查"))
    print("  " + unver("development worktree：accept 已清理 worktree，事后无据可查"))
    print("  → 这些场景如需可信证据，必须在运行当时归档 forks// worktree 列表，不能事后补证")
    print()

    if any_fail:
        print(f"{R}{B}结果: 发现机制造假或缺失（退出码 1）{X}")
        return 1
    print(f"{G}{B}结果: 可后验的机制均通过（退出码 0）{X}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
