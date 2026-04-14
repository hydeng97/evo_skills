#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "skills" / "registry.json"
SUMMARY_PATH = ROOT / "skills" / "skill_summary.md"


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
        lines.extend(
            [
                f"### {entry.get('display_name', 'Unnamed skill')}",
                "",
                f"- `skill_id`: `{entry.get('skill_id', 'unknown')}`",
                f"- `source_id`: `{entry.get('source_id', 'unknown')}`",
                f"- content type: `{entry.get('content_type', 'unknown')}`",
                f"- supported modes: `{supported_modes}`",
                f"- execution level: `{entry.get('execution_level', 'unknown')}`",
                f"- status: `{entry.get('status', 'unknown')}`",
                f"- exportable: `{entry.get('exportable', 'unknown')}`",
                f"- entry path: `{entry.get('entry_path', 'unknown')}`",
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
    print(f"Refreshed skill summary at {SUMMARY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
