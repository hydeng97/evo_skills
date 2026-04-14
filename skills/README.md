# skills

This directory stores generated child skills managed by `evo_skills`.

Two top-level inventory files live here:

- `skill_summary.md`: human-readable overview of all child skills
- `registry.json`: machine-readable registry used for routing and governance

Each child skill should be exportable and contain at least:

- `SKILL.md`
- `README.md`
- `meta.json`
- `memory_schema.md`

Optional subdirectories:

- `cases/`
- `prompts/`

Child skills are managed here first, then copied or packaged into `exports/` when they need to be moved into another agent system.
