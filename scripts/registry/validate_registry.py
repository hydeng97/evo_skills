#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "skills" / "registry.json"

TOP_LEVEL_KEYS = {
    "registry_version",
    "managed_by",
    "execution_posture",
    "mode_definitions",
    "execution_levels",
    "skills",
}

ENTRY_REQUIRED_KEYS = {
    "skill_id",
    "display_name",
    "source_id",
    "content_type",
    "supported_modes",
    "execution_level",
    "status",
    "version",
    "memory_enabled",
    "exportable",
    "entry_path",
}


def fail(message: str) -> int:
    print(f"Registry validation failed: {message}", file=sys.stderr)
    return 1


def main() -> int:
    if not REGISTRY_PATH.exists():
        return fail(f"missing registry file at {REGISTRY_PATH}")

    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON ({exc})")

    missing_top_level = sorted(TOP_LEVEL_KEYS - set(data.keys()))
    if missing_top_level:
        return fail(f"missing top-level keys: {', '.join(missing_top_level)}")

    skills = data.get("skills")
    if not isinstance(skills, list):
        return fail("'skills' must be a list")

    seen_skill_ids: set[str] = set()

    for index, entry in enumerate(skills):
        if not isinstance(entry, dict):
            return fail(f"skills[{index}] must be an object")

        missing_entry_keys = sorted(ENTRY_REQUIRED_KEYS - set(entry.keys()))
        if missing_entry_keys:
            return fail(
                f"skills[{index}] missing keys: {', '.join(missing_entry_keys)}"
            )

        skill_id = entry["skill_id"]
        if skill_id in seen_skill_ids:
            return fail(f"duplicate skill_id: {skill_id}")
        seen_skill_ids.add(skill_id)

        supported_modes = entry["supported_modes"]
        if not isinstance(supported_modes, list) or not supported_modes:
            return fail(f"skills[{index}].supported_modes must be a non-empty list")

        entry_path = ROOT / entry["entry_path"]
        if not str(entry["entry_path"]).endswith("SKILL.md"):
            return fail(f"skills[{index}].entry_path must point to SKILL.md")

        if entry_path.exists() and not entry_path.is_file():
            return fail(f"skills[{index}].entry_path exists but is not a file")

    print("Registry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
