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

PT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G, R, Y, B, X = "\033[32m", "\033[31m", "\033[33m", "\033[1m", "\033[0m"


def ok(s):     return f"{G}PASS{X} {s}"
def bad(s):    return f"{R}FAIL{X} {s}"
def warn(s):   return f"{Y}WARN{X} {s}"
def unver(s):  return f"{Y}UNVERIFIABLE{X} {s}"


def count_write_tasks(project_dir):
    """统计有 outputs 声明（即会写文件）的任务数。"""
    tasks_dir = os.path.join(project_dir, ".agent-team", "tasks")
    if not os.path.isdir(tasks_dir):
        return 0
    n = 0
    for fn in sorted(os.listdir(tasks_dir)):
        if not fn.endswith(".md") or fn == "index.md":
            continue
        with open(os.path.join(tasks_dir, fn), encoding="utf-8") as f:
            if re.search(r"^outputs:\s*(\[.*\S.*\]|\s*$\n[ \t]+-)", f.read(), re.MULTILINE):
                n += 1
    return n


def is_fabricated_timestamp(ts):
    """判断快照目录名里的时间戳是否是 LLM 编的占位符而非真实 date 输出。
    真实: 20260526T213355 ；造假典型: 20260526T000000 / TIMESTAMP / <timestamp>
    """
    m = re.search(r"T(\d{6})$", ts)
    if not m:
        return True  # 根本没有合法时分秒结构
    return m.group(1) == "000000"  # 全零 = date 永不产出，必为手打占位符


def check_office_snapshots():
    """office 写前快照机制取证。返回 (fail_bool, lines)。"""
    proj = os.path.join(PT_ROOT, "team-onboard")
    snap_root = os.path.join(proj, ".agent-team", "snapshots")
    lines, fail = [], False

    expected = count_write_tasks(proj)
    if not os.path.isdir(snap_root):
        return True, [bad(f"office: 无 snapshots/ 目录 —— 写前快照机制完全未运行（应有 ≈{expected} 个）")]

    subdirs = [d for d in sorted(os.listdir(snap_root))
               if os.path.isdir(os.path.join(snap_root, d))]
    lines.append(f"  期望快照数 ≈ {expected}（office 写任务数），实际目录数 = {len(subdirs)}")

    if len(subdirs) < expected:
        fail = True
        lines.append("   " + bad(f"快照数量不足：{len(subdirs)}/{expected} —— 多数写任务未在写前快照"))

    for d in subdirs:
        ts_fake = is_fabricated_timestamp(d)
        nfiles = len(os.listdir(os.path.join(snap_root, d)))
        if ts_fake:
            fail = True
            lines.append("   " + bad(f"伪造时间戳: {d} —— date 永不输出此值，证明目录名是手打占位符（机制被叙述而非执行）"))
        else:
            note = "（空：若全为新建文件可接受）" if nfiles == 0 else f"（{nfiles} 个文件）"
            lines.append("   " + ok(f"快照 {d} 时间戳真实 {note}"))
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


def main():
    print(f"{B}agent-team 编排机制完整性校验（防叙述造假）{X}\n")
    any_fail = False

    print(f"{B}■ office 写前快照机制{X}")
    fail, lines = check_office_snapshots()
    for l in lines:
        print(l)
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
