#!/usr/bin/env python3
"""Validate a research knowledge-base source manifest."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ENUMS = {
    "source_type": {
        "peer_reviewed",
        "thesis",
        "preprint",
        "standard",
        "official_documentation",
        "institutional_technical",
        "secondary",
    },
    "asset_status": {
        "fulltext_parsed",
        "fulltext_unparsed",
        "metadata_only",
        "pending_fulltext",
        "excluded",
    },
    "evidence_grade": {"A", "B", "C", "M"},
    "claim_admissibility": {
        "conclusion",
        "background_only",
        "candidate_only",
        "excluded",
    },
}
TIERS = {"top", "high", "acceptable", "low", "unknown", "not_applicable"}
REQUIRED_SOURCE_FIELDS = {
    "id",
    "title",
    "authors",
    "year",
    "doi",
    "source_type",
    "asset_status",
    "evidence_grade",
    "claim_admissibility",
    "venue_quality",
    "priority",
    "is_main_method",
    "source_url",
    "local_pdf",
    "local_text",
    "source_card",
    "reader",
    "sha256",
    "exclusion_reason",
    "notes",
}


def normalize_doi(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
    return re.sub(r"^doi:\s*", "", value)


def validate_venue(
    source: dict[str, Any], label: str, errors: list[str], warnings: list[str]
) -> str:
    venue = source.get("venue_quality")
    if not isinstance(venue, dict):
        errors.append(f"{label}: venue_quality must be an object")
        return "unknown"
    required = {
        "venue_name",
        "venue_type",
        "tier",
        "ranking_systems",
        "verified_at",
        "admission_floor_passed",
        "assessment_note",
    }
    missing = sorted(required - venue.keys())
    if missing:
        errors.append(f"{label}: venue_quality missing {', '.join(missing)}")
    tier = venue.get("tier", "unknown")
    if not isinstance(tier, str) or tier not in TIERS:
        errors.append(f"{label}: invalid venue tier {tier!r}")
        tier = "unknown"
    if not isinstance(venue.get("ranking_systems", []), list):
        errors.append(f"{label}: ranking_systems must be a list")
    if tier not in {"unknown", "not_applicable"} and not venue.get("verified_at"):
        errors.append(f"{label}: verified_at is required for tier {tier}")
    if tier in {"top", "high", "acceptable"} and not venue.get("ranking_systems"):
        warnings.append(f"{label}: admitted tier has no ranking-system evidence")
    return str(tier)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if not isinstance(data, dict):
        print("ERROR: manifest root must be an object")
        return 1
    sources = data.get("sources")
    if not isinstance(sources, list):
        print("ERROR: sources must be a list")
        return 1

    seen_ids: set[str] = set()
    seen_dois: dict[str, str] = {}
    for index, source in enumerate(sources):
        label = f"sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{label}: entry must be an object")
            continue
        missing = sorted(REQUIRED_SOURCE_FIELDS - source.keys())
        if missing:
            errors.append(f"{label}: missing {', '.join(missing)}")
        source_id = str(source.get("id", "")).strip()
        label = source_id or label
        if not source_id:
            errors.append(f"{label}: id is empty")
        elif source_id in seen_ids:
            errors.append(f"{label}: duplicate id")
        seen_ids.add(source_id)

        doi = normalize_doi(str(source.get("doi", "")))
        if doi:
            if doi in seen_dois:
                errors.append(f"{label}: duplicate DOI with {seen_dois[doi]}: {doi}")
            seen_dois[doi] = label

        for field, allowed in ENUMS.items():
            value = source.get(field)
            if not isinstance(value, str) or value not in allowed:
                errors.append(f"{label}: invalid {field} {value!r}")

        tier = validate_venue(source, label, errors, warnings)
        admissibility = source.get("claim_admissibility")
        if admissibility == "conclusion":
            if source.get("asset_status") != "fulltext_parsed":
                errors.append(f"{label}: conclusion source lacks parsed full text")
            if source.get("evidence_grade") not in ("A", "B"):
                errors.append(f"{label}: conclusion source has inadmissible evidence grade")
            if tier in {"low", "unknown"}:
                warnings.append(
                    f"{label}: conclusion source has {tier} venue tier; "
                    "review relevance, methods, validation, and any configured venue floor"
                )

        if source.get("is_main_method") is True:
            if source.get("source_type") != "peer_reviewed":
                warnings.append(f"{label}: main method is not peer reviewed; verify task policy")
            if tier not in {"top", "high"}:
                warnings.append(f"{label}: main method is not top/high; verify configured venue policy")
            if source.get("evidence_grade") != "A":
                errors.append(f"{label}: main method evidence grade must be A")
            if admissibility != "conclusion":
                errors.append(f"{label}: main method must be admissible for conclusions")
            if source.get("asset_status") != "fulltext_parsed":
                errors.append(f"{label}: main method lacks parsed full text")
            for field in ("local_pdf", "source_card"):
                if not str(source.get(field, "")).strip():
                    errors.append(f"{label}: main method missing {field}")
            if not str(source.get("reader", "")).strip():
                warnings.append(f"{label}: main method has no reader asset")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"Checked {len(sources)} sources; "
        f"{len(errors)} error(s), {len(warnings)} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
