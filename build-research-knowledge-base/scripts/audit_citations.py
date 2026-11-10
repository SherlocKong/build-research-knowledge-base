#!/usr/bin/env python3
"""Audit structural consistency of numeric Markdown citations and references."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REFERENCE_HEADING = re.compile(
    r"^#{1,6}\s*(参考文献|References|Bibliography)\s*$", re.IGNORECASE | re.MULTILINE
)
CITATION = re.compile(r"(?<!\!)\[(\d+(?:\s*[-–,，;；]\s*\d+)*)\]")
FULLWIDTH_CITATION = re.compile(r"［(\d+(?:\s*[-–,，;；]\s*\d+)*)］")
REFERENCE_ENTRY = re.compile(r"^\s*(?:\[(\d+)\]|(\d+)[.)、])\s+", re.MULTILINE)


def expand_numbers(content: str) -> set[int]:
    numbers: set[int] = set()
    for part in re.split(r"[,，;；]\s*", content):
        part = part.strip()
        range_match = re.fullmatch(r"(\d+)\s*[-–]\s*(\d+)", part)
        if range_match:
            start, end = map(int, range_match.groups())
            if start <= end and end - start <= 1000:
                numbers.update(range(start, end + 1))
        elif part.isdigit():
            numbers.add(int(part))
    return numbers


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    args = parser.parse_args()

    try:
        text = args.document.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: {exc}")
        return 1

    heading = REFERENCE_HEADING.search(text)
    body = text[: heading.start()] if heading else text
    bibliography = text[heading.end() :] if heading else ""

    cited: set[int] = set()
    for pattern in (CITATION, FULLWIDTH_CITATION):
        for match in pattern.finditer(body):
            cited.update(expand_numbers(match.group(1)))

    referenced: set[int] = set()
    for match in REFERENCE_ENTRY.finditer(bibliography):
        referenced.add(int(match.group(1) or match.group(2)))

    errors: list[str] = []
    warnings: list[str] = []
    if cited and not heading:
        errors.append("numeric citations exist but no reference heading was found")
    if heading and not referenced:
        errors.append("reference heading exists but no numbered entries were found")

    missing = sorted(cited - referenced)
    uncited = sorted(referenced - cited)
    if missing:
        errors.append(f"citations missing reference entries: {missing}")
    if uncited:
        warnings.append(f"reference entries not cited in body: {uncited}")

    duplicates = [
        number
        for number in referenced
        if len(
            re.findall(
                rf"^\s*(?:\[{number}\]|{number}[.)、])\s+",
                bibliography,
                re.MULTILINE,
            )
        )
        > 1
    ]
    if duplicates:
        errors.append(f"duplicate reference numbers: {sorted(duplicates)}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"Found {len(cited)} cited number(s) and {len(referenced)} reference entry/entries; "
        f"{len(errors)} error(s), {len(warnings)} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
