# skills

This directory stores generated child skills managed by `evo_skills`.

Two top-level inventory files live here:

- `skill_summary.md`: human-readable overview of all child skills
- `registry.json`: machine-readable registry used for routing and governance
- `library_overview.md`: user-facing overview of the current skill library with summary stats, tag grouping, and per-skill descriptions

Each child skill registry entry should also be able to carry dynamic `tags` so routing can progressively narrow the candidate set without relying on a fixed category tree.

Each child skill should be exportable and contain at least:

- `SKILL.md`
- `README.md`
- `meta.json`
- `memory_schema.md`

Recommended metadata fields include:

- `skill_id`
- `display_name`
- `content_type`
- `one_sentence_description`
- `tags`
- `supported_modes`
- `execution_level`

Optional subdirectories:

- `cases/`
- `prompts/`

Child skills are managed here first, then copied or packaged into `exports/` when they need to be moved into another agent system.
