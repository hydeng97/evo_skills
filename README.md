# evo_skills

`evo_skills` is an exposed OpenCode meta skill for turning books, articles, and tutorials into managed child skills.

It owns four responsibilities:

1. Normalize source material into reusable distilled article packages.
2. Generate child skills that can teach, coach, reflect, and optionally execute.
3. Maintain a registry and summary of all managed child skills.
4. Store long-term memory in a structured per-skill and per-user layout.

This skill is intentionally designed so generated child skills can be exported and installed into other agent systems without depending completely on `evo_skills`.

## Runtime layout

- `articles/`: normalized source-material packages
- `skills/`: generated child skills plus registry files
- `memory/`: long-term memory grouped by skill and user
- `scripts/`: automation helpers for ingest, generation, registry, memory, and export flows
- `templates/`: standard generation templates for child skills
- `exports/`: standalone child-skill bundles ready for migration
- `archive/`: retired or superseded skill versions

## Current build workflow

The intended workflow is:

1. Use the current agent to read source material and distill a `skill_spec.json` that follows `docs/skill_spec_schema.md`.
2. Review key spec fields with the user before building, especially `display_name`, `skill_id`, `content_type`, `supported_modes`, `execution_level`, and `core_thesis`.
3. Use `scripts/build/build_child_skill.py` to convert the approved spec into article artifacts, a child skill package, memory scaffolding, and registry updates.
4. Use the registry tools to validate and refresh summary views as needed.

## Skill library visibility

`evo_skills` now maintains two human-facing views of the skill library:

1. `skills/skill_summary.md` — compact registry-oriented summary
2. `skills/library_overview.md` — user-facing overview with overall stats, tag grouping, and per-skill descriptions

Use the registry refresh flow to keep these views synchronized.

Example build command:

```bash
source ~/.zshrc >/dev/null 2>&1
conda activate agent
python "scripts/build/build_child_skill.py" --spec "examples/specs/sample_skill_spec.json" --root "examples/generated"
```

## Agent-only rule

`evo_skills` does not depend on any separate LLM API for distillation. The current agent session is responsible for understanding source material, proposing the child skill design, and producing the intermediate `skill_spec.json`. Local scripts only perform deterministic filesystem, registry, and summary work.

## Core protocol entry points

The most important workflow documents for continuing implementation and day-to-day use are:

- `docs/interactive_distill_session_protocol.md`
- `docs/agent_distillation_runtime_protocol.md`
- `docs/runtime_routing_rule.md`
- `docs/memory_runtime_rule.md`
- `docs/dynamic_tagging_rule.md`
