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
