#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REQUIRED_TOP_LEVEL_KEYS = {
    "spec_version",
    "source_meta",
    "distillation",
    "examples",
    "skill_design",
    "mode_evaluation",
    "memory_design",
    "artifact_plan",
}


def fail(message: str) -> int:
    print(f"Build failed: {message}", file=sys.stderr)
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a child skill from skill_spec.json"
    )
    parser.add_argument("--spec", required=True, help="Path to skill_spec.json")
    parser.add_argument(
        "--root",
        default=".",
        help="Output root for generated files (defaults to current repository root)",
    )
    return parser.parse_args()


def load_spec(spec_path: Path) -> dict:
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    missing = sorted(REQUIRED_TOP_LEVEL_KEYS - set(data.keys()))
    if missing:
        raise ValueError(f"missing top-level keys: {', '.join(missing)}")

    source_meta = data["source_meta"]
    skill_design = data["skill_design"]
    mode_evaluation = data["mode_evaluation"]

    for required_path, value in {
        "source_meta.source_id": source_meta.get("source_id"),
        "source_meta.title": source_meta.get("title"),
        "skill_design.skill_id": skill_design.get("skill_id"),
        "skill_design.skill_folder_name": skill_design.get("skill_folder_name"),
        "skill_design.display_name": skill_design.get("display_name"),
        "skill_design.tags": skill_design.get("tags"),
        "skill_design.one_sentence_description": skill_design.get(
            "one_sentence_description"
        ),
        "mode_evaluation.supported_modes": mode_evaluation.get("supported_modes"),
        "mode_evaluation.execution_level": mode_evaluation.get("execution_level"),
    }.items():
        if value in (None, "", []):
            raise ValueError(f"missing required field: {required_path}")

    return data


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_parent(path)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    ensure_parent(path)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def render_distilled_md(spec: dict) -> str:
    d = spec["distillation"]
    key_concepts = d.get("key_concepts", [])
    concept_lines = (
        "\n".join(
            f"- **{item['name']}**：{item['definition']}（重要性：{item['importance']}）"
            for item in key_concepts
        )
        or "- 暂无"
    )
    mechanisms = "\n".join(f"- {item}" for item in d.get("mechanisms", [])) or "- 暂无"
    applicable = (
        "\n".join(f"- {item}" for item in d.get("applicable_scenarios", [])) or "- 暂无"
    )
    boundaries = "\n".join(f"- {item}" for item in d.get("boundaries", [])) or "- 暂无"
    misuses = "\n".join(f"- {item}" for item in d.get("common_misuses", [])) or "- 暂无"
    return f"""# Distilled Content

## Summary

{d.get("summary", "")}

## Core Thesis

{d.get("core_thesis", "")}

## Key Concepts

{concept_lines}

## Mechanisms

{mechanisms}

## Applicable Scenarios

{applicable}

## Boundaries

{boundaries}

## Common Misuses

{misuses}
"""


def render_examples_md(spec: dict) -> str:
    lines = ["# Examples", ""]
    for example in spec.get("examples", []):
        lines.extend(
            [
                f"## {example['title']}",
                "",
                f"- 场景：{example['scenario']}",
                f"- 分析：{example['analysis']}",
                f"- 启示：{example['lesson']}",
                f"- 标签：{', '.join(example.get('tags', []))}",
                "",
            ]
        )
    return "\n".join(lines)


def render_coach_notes_md(spec: dict) -> str:
    d = spec["distillation"]
    return f"""# Coach Notes

## Applicable Scenarios

{chr(10).join(f"- {item}" for item in d.get("applicable_scenarios", [])) or "- 暂无"}

## Boundaries

{chr(10).join(f"- {item}" for item in d.get("boundaries", [])) or "- 暂无"}

## Common Misuses

{chr(10).join(f"- {item}" for item in d.get("common_misuses", [])) or "- 暂无"}
"""


def render_skill_md(spec: dict) -> str:
    design = spec["skill_design"]
    modes = spec["mode_evaluation"]
    triggers = design.get("trigger_phrases", [])
    trigger_lines = "\n".join(f'  - "{item}"' for item in triggers)
    supported = ", ".join(modes.get("supported_modes", []))
    return f"""---
name: {design["skill_folder_name"]}
description: |
  {design["one_sentence_description"]}

  Triggers when user mentions:
{trigger_lines}
---

# {design["display_name"]}

## Core Thesis

{spec["distillation"].get("core_thesis", "")}

## Supported Modes

{supported}

## Execution Level

{modes.get("execution_level", "none")}
"""


def render_skill_readme(spec: dict) -> str:
    design = spec["skill_design"]
    tags = ", ".join(design.get("tags", [])) or "暂无"
    return f"""# {design["display_name"]}

{design["one_sentence_description"]}

## Tags

{tags}

## Target User Value

{chr(10).join(f"- {item}" for item in design.get("target_user_value", [])) or "- 暂无"}
"""


def render_memory_schema(spec: dict) -> str:
    memory = spec["memory_design"]
    store = memory.get("store", {})
    return f"""# Memory Schema

## Store

### teach
{chr(10).join(f"- {item}" for item in store.get("teach", [])) or "- 暂无"}

### coach
{chr(10).join(f"- {item}" for item in store.get("coach", [])) or "- 暂无"}

### reflect
{chr(10).join(f"- {item}" for item in store.get("reflect", [])) or "- 暂无"}

### execute
{chr(10).join(f"- {item}" for item in store.get("execute", [])) or "- 暂无"}

## Avoid

{chr(10).join(f"- {item}" for item in memory.get("avoid", [])) or "- 暂无"}

## Summary Policy

{memory.get("summary_policy", "")}
"""


def default_registry() -> dict:
    return {
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
        "tagging_note": "Tags are dynamic and should follow docs/dynamic_tagging_rule.md rather than a fixed category tree.",
        "skills": [],
    }


def refresh_summary(registry: dict, summary_path: Path) -> None:
    lines = [
        "# Managed Child Skills Summary",
        "",
        "This file is generated from `skills/registry.json`.",
        "",
        f"- registry version: {registry.get('registry_version', 'unknown')}",
        f"- managed by: {registry.get('managed_by', 'unknown')}",
        f"- execution posture: {registry.get('execution_posture', 'unknown')}",
        "",
    ]
    skills = registry.get("skills", [])
    if not skills:
        lines.append("No child skills have been registered yet.")
    else:
        lines.extend(["## Registered child skills", ""])
        for entry in skills:
            tags = ", ".join(entry.get("tags", [])) or "unknown"
            lines.extend(
                [
                    f"### {entry['display_name']}",
                    "",
                    f"- `skill_id`: `{entry['skill_id']}`",
                    f"- `source_id`: `{entry['source_id']}`",
                    f"- content type: `{entry['content_type']}`",
                    f"- tags: `{tags}`",
                    f"- supported modes: `{', '.join(entry['supported_modes'])}`",
                    f"- execution level: `{entry['execution_level']}`",
                    f"- status: `{entry['status']}`",
                    f"- exportable: `{entry['exportable']}`",
                    f"- entry path: `{entry['entry_path']}`",
                    "",
                ]
            )
    write_text(summary_path, "\n".join(lines))


def build(spec: dict, root: Path) -> list[Path]:
    created: list[Path] = []
    source_meta = spec["source_meta"]
    design = spec["skill_design"]
    memory = spec["memory_design"]
    modes = spec["mode_evaluation"]

    article_dir = root / "articles" / source_meta["source_id"]
    skill_dir = root / "skills" / design["skill_folder_name"]
    memory_dir = root / "memory" / design["skill_id"]
    registry_path = root / "skills" / "registry.json"
    summary_path = root / "skills" / "skill_summary.md"

    write_json(article_dir / "source_meta.json", source_meta)
    write_text(article_dir / "distilled.md", render_distilled_md(spec))
    write_text(article_dir / "examples.md", render_examples_md(spec))
    write_text(article_dir / "coach_notes.md", render_coach_notes_md(spec))
    created.extend(
        [
            article_dir / "source_meta.json",
            article_dir / "distilled.md",
            article_dir / "examples.md",
            article_dir / "coach_notes.md",
        ]
    )

    meta_payload = {
        "skill_id": design["skill_id"],
        "display_name": design["display_name"],
        "source_id": source_meta["source_id"],
        "content_type": design["content_type"],
        "one_sentence_description": design["one_sentence_description"],
        "tags": design["tags"],
        "supported_modes": modes["supported_modes"],
        "execution_level": modes["execution_level"],
        "status": "draft",
        "version": "v1",
        "memory_enabled": memory["memory_enabled"],
        "exportable": True,
        "entry_path": f"skills/{design['skill_folder_name']}/SKILL.md",
    }
    write_text(skill_dir / "SKILL.md", render_skill_md(spec))
    write_text(skill_dir / "README.md", render_skill_readme(spec))
    write_json(skill_dir / "meta.json", meta_payload)
    write_text(skill_dir / "memory_schema.md", render_memory_schema(spec))
    created.extend(
        [
            skill_dir / "SKILL.md",
            skill_dir / "README.md",
            skill_dir / "meta.json",
            skill_dir / "memory_schema.md",
        ]
    )

    (memory_dir / "shared").mkdir(parents=True, exist_ok=True)
    (memory_dir / "users").mkdir(parents=True, exist_ok=True)
    write_text(memory_dir / "shared" / ".gitkeep", "")
    write_text(memory_dir / "users" / ".gitkeep", "")
    created.extend(
        [
            memory_dir / "shared" / ".gitkeep",
            memory_dir / "users" / ".gitkeep",
        ]
    )

    if registry_path.exists():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    else:
        registry = default_registry()

    entry = {
        "skill_id": design["skill_id"],
        "display_name": design["display_name"],
        "source_id": source_meta["source_id"],
        "content_type": design["content_type"],
        "one_sentence_description": design["one_sentence_description"],
        "tags": design["tags"],
        "supported_modes": modes["supported_modes"],
        "execution_level": modes["execution_level"],
        "status": "draft",
        "version": "v1",
        "memory_enabled": memory["memory_enabled"],
        "exportable": True,
        "entry_path": f"skills/{design['skill_folder_name']}/SKILL.md",
    }
    skills = [
        item
        for item in registry.get("skills", [])
        if item.get("skill_id") != design["skill_id"]
    ]
    skills.append(entry)
    registry["skills"] = skills
    write_json(registry_path, registry)
    refresh_summary(registry, summary_path)
    created.extend([registry_path, summary_path])

    return created


def main() -> int:
    args = parse_args()
    spec_path = Path(args.spec).resolve()
    root = Path(args.root).resolve()

    if not spec_path.exists():
        return fail(f"spec file not found: {spec_path}")

    try:
        spec = load_spec(spec_path)
    except (json.JSONDecodeError, ValueError) as exc:
        return fail(str(exc))

    created = build(spec, root)
    print("Generated files:")
    for path in created:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
