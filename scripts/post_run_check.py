#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


REQUIRED_PHRASES = {
    "Q3 never defaults to no": "Q3 永不代答",
    "human approval guardrail": "Human Approval + Guardrail",
    "strategy change rule": "同一錯誤連續 2 次無進展",
    "fixed escalation conditions": "固定三條",
    "output self-check gate": "輸出前自檢閘門",
    "approval gates in prompt": "Approval Gates",
    "memory pollution guard": "Memory Pollution",
    "tool whitelist guard": "工具白名單",
}


def main() -> int:
    text = SKILL.read_text(encoding="utf-8")
    results: list[tuple[str, bool, str]] = []

    def record(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, ok, detail))

    record("skill file exists", SKILL.exists())
    for name, phrase in REQUIRED_PHRASES.items():
        record(name, phrase in text, f"missing phrase: {phrase}")

    pattern_names = [
        "Test-Repair Loop",
        "Evaluator-Optimizer",
        "Research-Synthesis Loop",
        "Generate-Critique-Revise",
        "Human Approval Loop",
    ]
    record("five main patterns present", all(name in text for name in pattern_names))

    required_sections = ["區塊 1:設計摘要", "區塊 2:Loop Agent 規格書", "區塊 3:可直接複製的 Loop Prompt", "區塊 4:上線前檢查表"]
    record("four output blocks present", all(section in text for section in required_sections))

    yaml = re.search(r"^---\nname:\s*loop-setup-wizard\ndescription:.+?\n---", text, re.S | re.M)
    record("frontmatter valid", yaml is not None)

    failed = [row for row in results if not row[1]]
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'} {name}{' - ' + detail if detail and not ok else ''}")
    if failed:
        print(f"post-run check failed: {len(failed)} issue(s)", file=sys.stderr)
        return 1
    print("post-run check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
