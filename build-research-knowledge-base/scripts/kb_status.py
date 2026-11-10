#!/usr/bin/env python3
"""Summarize structural research knowledge-base status conservatively."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def has_required_search_channels(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace").lower()
    return (
        declared_search_status(path) == "complete"
        and "codex 内置搜索" in text
        and ("本地仓库" in text or "仓库已有文献" in text)
        and ("合并" in text or "去重" in text)
    )


def declared_search_status(path: Path) -> str:
    if not path.exists():
        return "missing"
    text = path.read_text(encoding="utf-8", errors="replace").lower()
    for status in ("complete", "partial", "draft"):
        if (
            f"检索状态：`{status}`" in text
            or f"检索状态: `{status}`" in text
            or f"检索状态：{status}" in text
            or f"检索状态: {status}" in text
            or f"search status: {status}" in text
        ):
            return status
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    manifest_path = root / "manifest/sources.json"
    if not manifest_path.exists():
        print(json.dumps({"root": str(root), "error": "manifest missing"}, ensure_ascii=False, indent=2))
        return 1
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"root": str(root), "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    if not isinstance(data, dict):
        print(json.dumps({"root": str(root), "error": "manifest root must be an object"}, ensure_ascii=False, indent=2))
        return 1
    sources = data.get("sources")
    if not isinstance(sources, list):
        print(json.dumps({"root": str(root), "error": "sources is not a list"}, ensure_ascii=False, indent=2))
        return 1

    if any(not isinstance(source, dict) for source in sources):
        print(json.dumps({"root": str(root), "error": "source entries must be objects"}, ensure_ascii=False, indent=2))
        return 1
    if any(not isinstance(source.get("venue_quality", {}), dict) for source in sources):
        print(json.dumps({"root": str(root), "error": "venue_quality must be an object"}, ensure_ascii=False, indent=2))
        return 1

    asset_counts = Counter(str(source.get("asset_status", "missing")) for source in sources)
    tier_counts = Counter(
        str(source.get("venue_quality", {}).get("tier", "missing"))
        for source in sources
        if isinstance(source, dict)
    )
    admissibility_counts = Counter(
        str(source.get("claim_admissibility", "missing")) for source in sources
    )
    main_methods = [source for source in sources if source.get("is_main_method") is True]

    priority_open = [
        source.get("id")
        for source in sources
        if source.get("priority") == 0
        and source.get("asset_status") != "fulltext_parsed"
    ]
    formal_uncertain_tier = [
        source.get("id")
        for source in sources
        if source.get("claim_admissibility") in {"conclusion", "background_only"}
        and source.get("venue_quality", {}).get("tier") in {"low", "unknown"}
    ]
    main_method_failures: list[str] = []
    for source in main_methods:
        tier = source.get("venue_quality", {}).get("tier")
        required_paths = all(bool(source.get(field)) for field in ("local_pdf", "source_card"))
        if (
            source.get("asset_status") != "fulltext_parsed"
            or not required_paths
        ):
            main_method_failures.append(str(source.get("id")))

    research = root / "kb/research"
    search_log = research / "检索策略与日志.md"
    matrix = research / "全文证据矩阵.md"
    synthesis = research / "统一总结与结论.md"
    mainlines = sorted(research.glob("*V[0-9]*.md")) if research.exists() else []
    search_status = declared_search_status(search_log)

    state = "draft"
    if (
        bool(sources)
        and has_required_search_channels(search_log)
        and matrix.exists()
        and not priority_open
    ):
        state = "evidence-complete"
        if synthesis.exists():
            state = "synthesis-ready"
            if mainlines and main_methods and not main_method_failures:
                state = "mainline-ready"
    elif search_status == "partial":
        state = "partial"

    report = {
        "root": str(root),
        "structural_candidate_state": state,
        "semantic_review_required": True,
        "source_count": len(sources),
        "asset_status": dict(asset_counts),
        "venue_tiers": dict(tier_counts),
        "claim_admissibility": dict(admissibility_counts),
        "main_method_count": len(main_methods),
        "open_priority_0": priority_open,
        "formal_low_or_unknown_warning": formal_uncertain_tier,
        "main_method_failures": main_method_failures,
        "files": {
            "search_log": search_log.exists(),
            "declared_search_status": search_status,
            "evidence_matrix": matrix.exists(),
            "unified_conclusion": synthesis.exists(),
            "mainline_documents": [str(path.relative_to(root)) for path in mainlines],
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
