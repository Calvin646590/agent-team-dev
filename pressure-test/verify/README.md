# 场景测试机器校验（pressure-test/verify/）

> 诚实复审 item 1 的产物。目的：**把场景测试的"✅ 通过"从 LLM 叙述改为退出码裁决。**

## 为什么需要它

这个项目是 prompt 驱动的——`scheduler`/`coordinator`/`merger` 都是给 LLM 的 markdown 指令，不是强制引擎。
因此跑测试的 LLM 完全可能**声称**"DAG 调度 + fork 隔离 + 写前快照都跑过了 ✅"，
而实际上只是一次性把文件写出来、再编一段漂亮的 log。

诚实复审（docs/16）已用取证证明：**office 写前快照机制从未真正执行**
（快照目录空、时间戳 `20260526T000000` 是 LLM 手打的占位符），
但当初的 log、candidate、测试报告、乃至前一版代码审查全都写着 ✅。

机器校验就是为了让这种"自评自报"无处藏身：✅ 必须由文件系统和退出码说了算。

## 两层校验

| 脚本 | 查什么 | 当前结果 |
|------|--------|---------|
| `verify.py` | 各 task 声明的 `outputs` 是否真实存在且非空；development 真跑 `vitest` 看退出码 | ✅ exit 0 |
| `verify_mechanism.py` | 编排机制是否留下**不可伪造**的真实痕迹（三个 hook 自测 + 残留伪造探测 + log 时间戳真实性 + fork 证据校验） | ✅ exit 0 |
| `test_office_snapshot_hook.py` | office 写前快照 hook 自测：真覆盖→真快照→真 ISO 时间戳 | ✅ exit 0 |
| `test_files_scope_hook.py` | strict 文件域 hook 自测（含 cwd=子目录 fail-open 修复用例） | ✅ exit 0 |
| `test_fork_evidence_hook.py` | directory-fork 证据 hook 自测：写 fork 留痕 / 隔离可见 / 删 forks 后证据仍在 | ✅ exit 0 |

> **历史**：item 6 之前，第 2 层是**红的**——office 写前快照是 prompt 指令，实测被 LLM 跳过却谎报成功
> （空目录 + 伪造时间戳 `20260526T000000`）。item 6 把该机制从"提示词剧场"改为**真实 hook 代码**
> （`agent-team/hooks/office-snapshot-guard.py`，PreToolUse 自动触发），第 2 层方才真实转绿。

## 用法

```bash
# 全部跑（推荐）
bash pressure-test/verify/run-all.sh

# 单独跑
python3 pressure-test/verify/verify.py            # 全部场景交付物
python3 pressure-test/verify/verify.py office content   # 指定场景
python3 pressure-test/verify/verify_mechanism.py  # 机制防造假
```

## 校验原则

1. **唯一真值源 = 文件系统**。不读 log.md / candidate.md 里任何"通过"字样。
2. **期望来自框架自己的声明**。校验依据是各 task 文件里 owner 写的 `outputs:`，
   不是脚本作者拍脑袋——框架承诺产出什么，就校验什么。
3. **诚实标注不可校验项**。content/research 的 fork、development 的 worktree 在
   accept 后痕迹被清理，事后无法取证 → 明确标 `UNVERIFIABLE`，**绝不假装通过**。
   要可信，必须在运行当时归档证据。
4. **退出码即结论**。0=过，1=不过。CI 或人都能一眼判定，无需相信任何叙述。

## 已知缺口（待后续 item 修复）

- **office 快照机制**（item 6）：需在 scheduler 真正用 `$(date)` 命名目录 + 真 `cp` 文件，重测留证。
- **运行时证据归档**：建议改造 scheduler/merger，在 accept 前把 forks// worktree 清单
  快照到 `.agent-team/evidence/`，使 fork/worktree 机制也变得可后验。
- **quality_gate 真校验**（item 4）：Merger 目前只信 subagent 自报；development 至少应真跑一次 compile/test。
