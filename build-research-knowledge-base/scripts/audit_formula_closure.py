#!/usr/bin/env python3
"""Find Markdown display equations that likely lack an adjacent symbol explanation."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DISPLAY_PATTERNS = (
    re.compile(r"\$\$(.+?)\$\$", re.DOTALL),
    re.compile(r"\\\[(.+?)\\\]", re.DOTALL),
    re.compile(
        r"\\begin\{(?:equation\*?|align\*?|gather\*?)\}(.+?)"
        r"\\end\{(?:equation\*?|align\*?|gather\*?)\}",
        re.DOTALL,
    ),
)
CLOSURE_RE = re.compile(
    r"式中|其中[，,:：]|符号(?:说明|表)|where[,:]|\|\s*符号\s*\|",
    re.IGNORECASE,
)


def strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.DOTALL)


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
    parser.add_argument(
        "--window",
        type=int,
        default=900,
        help="Characters after a display equation searched for closure text",
    )
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.exists():
        print(f"ERROR: audit root does not exist: {root}")
        return 1
    files = markdown_files(root)
    errors: list[str] = []
    equations = 0
    for markdown in files:
        try:
            text = strip_fenced_code(markdown.read_text(encoding="utf-8"))
        except OSError as exc:
            errors.append(f"{markdown}: {exc}")
            continue
        matches = [
            match
            for pattern in DISPLAY_PATTERNS
            for match in pattern.finditer(text)
        ]
        for match in sorted(matches, key=lambda item: item.start()):
            equations += 1
            after = text[match.end() : match.end() + args.window]
            next_heading = re.search(r"\n#{1,6}\s", after)
            if next_heading:
                after = after[: next_heading.start()]
            if not CLOSURE_RE.search(after):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(
                    f"{markdown}:{line}: display equation lacks nearby 式中/symbol table"
                )

    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"Checked {equations} display equation(s) in {len(files)} Markdown file(s); "
        f"{len(errors)} error(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
