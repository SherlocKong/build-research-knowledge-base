#!/usr/bin/env python3
"""Initialize a research knowledge-base without overwriting existing files."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
from pathlib import Path


DIRECTORIES = (
    "raw/papers",
    "raw/standards",
    "raw/technical",
    "raw/text",
    "manifest",
    "kb/questions",
    "kb/sources",
    "kb/readers",
    "kb/research",
)


def copy_if_absent(source: Path, target: Path, replacements: dict[str, str]) -> str:
    if target.exists():
        return "existing"
    target.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8")
    if source.suffix == ".json":
        data = json.loads(text)
        for key, value in data.items():
            if isinstance(value, str):
                for old, new in replacements.items():
                    value = value.replace(old, new)
                data[key] = value
        text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    else:
        for old, new in replacements.items():
            text = text.replace(old, new)
    target.write_text(text, encoding="utf-8")
    return "created"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Safely initialize a research sub-knowledge-base."
    )
    parser.add_argument("target", type=Path, help="Sub-knowledge-base root")
    parser.add_argument(
        "--project-name",
        help="Project name used in templates; defaults to target directory name",
    )
    parser.add_argument(
        "--with-mainline",
        action="store_true",
        help="Also create a V1 mainline document from the template",
    )
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    project_name = args.project_name or target.name
    if not project_name.strip() or project_name in {".", ".."} or any(
        character in project_name for character in ("/", "\\", "\0")
    ):
        parser.error("project name must be a nonempty filename without path separators")
    assets = Path(__file__).resolve().parent.parent / "assets"
    today = dt.date.today().isoformat()

    target.mkdir(parents=True, exist_ok=True)
    for relative in DIRECTORIES:
        (target / relative).mkdir(parents=True, exist_ok=True)

    replacements = {
        "<sub-kb-name>": project_name,
        "<研究主线名称>": project_name,
        "YYYY-MM-DD": today,
    }
    targets = {
        "project-AGENTS.template.md": target / "AGENTS.md",
        "manifest.template.json": target / "manifest/sources.json",
        "search-log.template.md": target / "kb/research/检索策略与日志.md",
        "evidence-matrix.template.md": target / "kb/research/全文证据矩阵.md",
    }
    if args.with_mainline:
        targets["mainline-v1.template.md"] = (
            target / f"kb/research/{project_name}V1.md"
        )

    results: dict[str, str] = {}
    for template, output in targets.items():
        results[str(output.relative_to(target))] = copy_if_absent(
            assets / template, output, replacements
        )

    manifest_path = target / "manifest/sources.json"
    try:
        json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: manifest initialization failed validation: {exc}")
        return 1

    print(json.dumps({"root": str(target), "files": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
