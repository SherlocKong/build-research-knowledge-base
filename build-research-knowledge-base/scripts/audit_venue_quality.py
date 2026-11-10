#!/usr/bin/env python3
"""Audit venue-quality metadata without treating prestige as claim support."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TIERS = {"top", "high", "acceptable", "low", "unknown", "not_applicable"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

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

    errors: list[str] = []
    warnings: list[str] = []
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"sources[{index}] is not an object")
            continue
        label = source.get("id") or f"sources[{index}]"
        venue = source.get("venue_quality")
        if not isinstance(venue, dict):
            errors.append(f"{label}: missing venue_quality object")
            continue
        tier = venue.get("tier")
        if not isinstance(tier, str) or tier not in TIERS:
            errors.append(f"{label}: invalid tier {tier!r}")
            continue
        for field in (
            "venue_name",
            "venue_type",
            "ranking_systems",
            "verified_at",
            "admission_floor_passed",
            "assessment_note",
        ):
            if field not in venue:
                errors.append(f"{label}: venue_quality missing {field}")

        if tier in {"top", "high", "acceptable"}:
            if not venue.get("verified_at"):
                errors.append(f"{label}: admitted tier lacks verified_at")
            if not venue.get("ranking_systems"):
                warnings.append(f"{label}: admitted tier lacks ranking evidence")

        formal = source.get("claim_admissibility") in ("conclusion", "background_only")
        if formal and tier in {"low", "unknown"}:
            warnings.append(
                f"{label}: formal evidence has {tier} venue tier; "
                "check whether the task contract defines a venue floor"
            )

        if source.get("is_main_method") is True:
            if tier not in {"top", "high"}:
                warnings.append(f"{label}: main method is not top/high; verify configured venue policy")
            if source.get("source_type") != "peer_reviewed":
                warnings.append(f"{label}: main method is not peer reviewed; verify task policy")
            if source.get("evidence_grade") != "A":
                errors.append(f"{label}: main method evidence grade must be A")
            if source.get("claim_admissibility") != "conclusion":
                errors.append(f"{label}: main method must support conclusions")
            if source.get("asset_status") != "fulltext_parsed":
                errors.append(f"{label}: main method lacks parsed full text")
            for field in ("local_pdf", "source_card"):
                if not source.get(field):
                    errors.append(f"{label}: main method missing {field}")
            if not source.get("reader"):
                warnings.append(f"{label}: main method has no reader asset")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"Audited {len(sources)} sources; "
        f"{len(errors)} error(s), {len(warnings)} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
