#!/usr/bin/env python3
"""Check local Markdown links under a research knowledge-base root."""

from __future__ import annotations

import argparse
import re
import urllib.parse
from pathlib import Path


LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#", "doi:")


def extract_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    if re.search(r'\s+["\']', target):
        target = re.split(r'\s+["\']', target, maxsplit=1)[0]
    return target


def markdown_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix.lower() == ".md" else []
    return sorted(
        path
        for path in root.rglob("*.md")
        if ".git" not in path.relative_to(root).parts
        and "tmp" not in path.relative_to(root).parts
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.exists():
        print(f"ERROR: audit root does not exist: {root}")
        return 1
    files = markdown_files(root)
    errors: list[str] = []
    warnings: list[str] = []
    checked = 0

    for markdown in files:
        try:
            lines = markdown.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            errors.append(f"{markdown}: {exc}")
            continue
        in_fence = False
        for line_number, line in enumerate(lines, start=1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in LINK_RE.finditer(line):
                target = extract_target(match.group(1))
                if not target or target.lower().startswith(SKIP_PREFIXES):
                    continue
                checked += 1
                decoded = urllib.parse.unquote(target)
                decoded = decoded.split("#", 1)[0]
                if not decoded:
                    continue
                path = Path(decoded).expanduser()
                if path.is_absolute():
                    warnings.append(
                        f"{markdown}:{line_number}: absolute local link {target!r}"
                    )
                    candidate = path
                else:
                    candidate = (markdown.parent / path).resolve()
                if not candidate.exists():
                    errors.append(
                        f"{markdown}:{line_number}: missing local target {target!r}"
                    )

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"Checked {checked} local link(s) in {len(files)} Markdown file(s); "
        f"{len(errors)} error(s), {len(warnings)} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
