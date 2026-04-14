#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a user-facing overview of the skill library"
    )
    parser.add_argument(
        "--root",
        default=str(DEFAULT_ROOT),
        help="Root directory containing skills/registry.json",
    )
    return parser.parse_args()


def load_registry(root: Path) -> dict:
    return json.loads((root / "skills" / "registry.json").read_text(encoding="utf-8"))


def top_level_tag(tag: str) -> str:
    return tag.split(".")[0]


def build_overview(registry: dict) -> str:
    skills = registry.get("skills", [])
    total = len(skills)
    status_counter = Counter(entry.get("status", "unknown") for entry in skills)
    execute_count = sum(
        1 for entry in skills if entry.get("execution_level", "none") != "none"
    )

    top_tags = Counter()
    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in skills:
        tags = entry.get("tags", [])
        if tags:
            primary = top_level_tag(tags[0])
            grouped[primary].append(entry)
            for tag in tags:
                top_tags[top_level_tag(tag)] += 1
        else:
            grouped["uncategorized"].append(entry)
            top_tags["uncategorized"] += 1

    lines = [
        "# Skill Library Overview",
        "",
        "This file is generated from `skills/registry.json`.",
        "",
        "## Overview",
        "",
        f"- Total skills: {total}",
        f"- Active skills: {status_counter.get('active', 0)}",
        f"- Draft skills: {status_counter.get('draft', 0)}",
        f"- Deprecated or merged skills: {status_counter.get('deprecated', 0) + status_counter.get('merged', 0)}",
        f"- Execute-capable skills: {execute_count}",
        "",
        "## Top Tag Groups",
        "",
    ]

    if top_tags:
        for tag, count in top_tags.most_common():
            lines.append(f"- {tag} ({count})")
    else:
        lines.append("- No registered tags yet")

    lines.extend(["", "## Skills by Tag Group", ""])

    if not skills:
        lines.append("No child skills have been registered yet.")
        return "\n".join(lines)

    for group in sorted(grouped.keys()):
        lines.extend([f"### {group}", ""])
        for entry in sorted(
            grouped[group], key=lambda item: item.get("display_name", "")
        ):
            tags = ", ".join(entry.get("tags", [])) or "none"
            modes = ", ".join(entry.get("supported_modes", [])) or "none"
            summary = entry.get("one_sentence_description", "No summary available.")
            lines.extend(
                [
                    f"#### {entry.get('display_name', 'Unnamed skill')}",
                    "",
                    f"- skill_id: `{entry.get('skill_id', 'unknown')}`",
                    f"- content type: `{entry.get('content_type', 'unknown')}`",
                    f"- tags: `{tags}`",
                    f"- modes: `{modes}`",
                    f"- execution level: `{entry.get('execution_level', 'unknown')}`",
                    f"- status: `{entry.get('status', 'unknown')}`",
                    f"- summary: {summary}",
                    "",
                ]
            )

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    output_path = root / "skills" / "library_overview.md"
    registry = load_registry(root)
    output_path.write_text(build_overview(registry).rstrip() + "\n", encoding="utf-8")
    print(f"Generated skill library overview at {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
