#!/usr/bin/env python3
"""Audit structural evidence for required and recorded search channels."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CHANNELS = {
    "Codex built-in search": (r"Codex\s*内置搜索", r"built[- ]?in\s+(web\s+)?search"),
    "AnySearch": (r"AnySearch", r"anysearch"),
    "local repository": (r"本地仓库|仓库已有文献", r"local\s+repository"),
}
FAILURE_WORDS = re.compile(
    r"不可用|失败|未完成|缺失|额度|凭证|unavailable|failed|incomplete|missing",
    re.IGNORECASE,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("search_log", type=Path)
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Do not fail solely because a channel is explicitly incomplete",
    )
    parser.add_argument(
        "--require-anysearch",
        action="store_true",
        help="Require AnySearch because the task contract explicitly calls for it",
    )
    args = parser.parse_args()

    try:
        text = args.search_log.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: {exc}")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    complete_status = re.search(
        r"(?:检索状态|search\s+status)\s*[:：]\s*`?complete`?",
        text,
        re.IGNORECASE,
    )
    if not complete_status:
        message = "overall search status is not explicitly complete"
        if args.allow_partial:
            warnings.append(message)
        else:
            errors.append(message)
    required_channels = {"Codex built-in search", "local repository"}
    if args.require_anysearch:
        required_channels.add("AnySearch")
    checked_channels = 0
    for name, patterns in CHANNELS.items():
        matches = [
            match
            for pattern in patterns
            for match in re.finditer(pattern, text, re.IGNORECASE)
        ]
        if not matches:
            if name in required_channels:
                errors.append(f"missing required search channel: {name}")
            continue
        checked_channels += 1
        anchor = min(match.start() for match in matches)
        section_tail = text[anchor:]
        next_section = re.search(r"\n##\s+", section_tail)
        context = (
            section_tail[: next_section.start()]
            if next_section
            else section_tail[:2000]
        )
        if FAILURE_WORDS.search(context):
            message = f"{name} contains an incomplete/failure marker"
            if args.allow_partial or name not in required_channels:
                warnings.append(message)
            else:
                errors.append(message)
        if not re.search(r"查询|检索式|query", context, re.IGNORECASE):
            warnings.append(f"{name} has no nearby query record")
        if not re.search(r"\b20\d{2}[-/年]\d{1,2}|日期|date", context, re.IGNORECASE):
            warnings.append(f"{name} has no nearby date record")
        if not re.search(r"新增|重复|冲突|结果|new|duplicate|conflict|result", context, re.IGNORECASE):
            warnings.append(f"{name} has no nearby result/reconciliation record")

    if not re.search(r"合并|去重|merged|deduplicat", text, re.IGNORECASE):
        errors.append("missing merged/deduplicated search result")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"Checked {checked_channels} recorded channel(s); "
        f"{len(required_channels)} required; "
        f"{len(errors)} error(s), {len(warnings)} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
