#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "skills" / "registry.json"
SUMMARY_PATH = ROOT / "skills" / "skill_summary.md"
OVERVIEW_PATH = ROOT / "skills" / "library_overview.md"


def fail(message: str) -> int:
    print(f"Summary refresh failed: {message}", file=sys.stderr)
    return 1


def build_summary(data: dict) -> str:
    lines = [
        "# Managed Child Skills Summary",
        "",
        "This file is generated from `skills/registry.json`.",
        "",
        f"- registry version: {data.get('registry_version', 'unknown')}",
        f"- managed by: {data.get('managed_by', 'unknown')}",
        f"- execution posture: {data.get('execution_posture', 'unknown')}",
        "",
    ]

    skills = data.get("skills", [])
    if not skills:
        lines.append("No child skills have been registered yet.")
        lines.append("")
        return "\n".join(lines)

    lines.extend(["## Registered child skills", ""])

    for entry in skills:
        supported_modes = ", ".join(entry.get("supported_modes", [])) or "unknown"
        tags = ", ".join(entry.get("tags", [])) or "unknown"
        lines.extend(
            [
                f"### {entry.get('display_name', 'Unnamed skill')}",
                "",
                f"- `skill_id`: `{entry.get('skill_id', 'unknown')}`",
                f"- `source_id`: `{entry.get('source_id', 'unknown')}`",
                f"- content type: `{entry.get('content_type', 'unknown')}`",
                f"- tags: `{tags}`",
                f"- supported modes: `{supported_modes}`",
                f"- execution level: `{entry.get('execution_level', 'unknown')}`",
                f"- status: `{entry.get('status', 'unknown')}`",
                f"- exportable: `{entry.get('exportable', 'unknown')}`",
                f"- entry path: `{entry.get('entry_path', 'unknown')}`",
                "",
            ]
        )

    return "\n".join(lines)


def build_overview(data: dict) -> str:
    skills = data.get("skills", [])
    active_count = sum(1 for entry in skills if entry.get("status") == "active")
    draft_count = sum(1 for entry in skills if entry.get("status") == "draft")
    deprecated_count = sum(
        1 for entry in skills if entry.get("status") in {"deprecated", "merged"}
    )
    execute_count = sum(
        1 for entry in skills if entry.get("execution_level", "none") != "none"
    )

    tag_groups: dict[str, list[dict]] = {}
    tag_counts: dict[str, int] = {}

    for entry in skills:
        tags = entry.get("tags", [])
        primary_tag = tags[0].split(".")[0] if tags else "uncategorized"
        tag_groups.setdefault(primary_tag, []).append(entry)
        for tag in tags or ["uncategorized"]:
            top = tag.split(".")[0]
            tag_counts[top] = tag_counts.get(top, 0) + 1

    lines = [
        "# Skill Library Overview",
        "",
        "This file is generated from `skills/registry.json`.",
        "",
        "## Overview",
        "",
        f"- Total skills: {len(skills)}",
        f"- Active skills: {active_count}",
        f"- Draft skills: {draft_count}",
        f"- Deprecated or merged skills: {deprecated_count}",
        f"- Execute-capable skills: {execute_count}",
        "",
        "## Top Tag Groups",
        "",
    ]

    if tag_counts:
        for tag, count in sorted(
            tag_counts.items(), key=lambda item: (-item[1], item[0])
        ):
            lines.append(f"- {tag} ({count})")
    else:
        lines.append("- No registered tags yet")

    lines.extend(["", "## Skills by Tag Group", ""])

    if not skills:
        lines.append("No child skills have been registered yet.")
        return "\n".join(lines)

    for group in sorted(tag_groups.keys()):
        lines.extend([f"### {group}", ""])
        for entry in sorted(
            tag_groups[group], key=lambda item: item.get("display_name", "")
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
    if not REGISTRY_PATH.exists():
        return fail(f"missing registry file at {REGISTRY_PATH}")

    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON ({exc})")

    SUMMARY_PATH.write_text(build_summary(data), encoding="utf-8")
    OVERVIEW_PATH.write_text(build_overview(data), encoding="utf-8")
    print(f"Refreshed skill summary at {SUMMARY_PATH}")
    print(f"Refreshed skill library overview at {OVERVIEW_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
