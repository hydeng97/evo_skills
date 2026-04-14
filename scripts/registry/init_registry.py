#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "skills" / "registry.json"

DEFAULT_REGISTRY = {
    "registry_version": 1,
    "managed_by": "evo_skills",
    "execution_posture": "balanced",
    "mode_definitions": {
        "teach": "Explain key ideas, examples, and misconceptions.",
        "coach": "Apply source-derived strategies to the user's current scenario.",
        "reflect": "Summarize long-term changes, blind spots, and growth patterns.",
        "execute": "Perform concrete steps when a repeatable workflow has been approved for execution.",
    },
    "execution_levels": {
        "none": "No execution allowed.",
        "plan_only": "Plan steps but do not execute them.",
        "guided_execute": "Execute safe steps while explaining actions and assumptions.",
        "safe_execute": "Execute low-risk standard actions directly.",
    },
    "skills": [],
}


def main() -> int:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(
        json.dumps(DEFAULT_REGISTRY, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Initialized registry at {REGISTRY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
