# scripts

This directory is for reusable automation helpers used by `evo_skills`.

Recommended subgroups:

- `ingest/`: import and normalize source materials
- `build/`: generate child skills from normalized article packages
- `registry/`: update `skill_summary.md` and `registry.json`
- `memory/`: summarize and compress long-term memory
- `export/`: build portable child-skill bundles
- `execute/`: shared helpers for technical child skills that support execution mode

Initial scaffold only documents the contract. Add scripts as the workflows are implemented.

## Current implementation status

The first implemented subgroup is `registry/`.

Use `registry/` for tasks such as:

- initializing `skills/registry.json`
- validating required registry fields
- refreshing `skills/skill_summary.md`
- checking for duplicate `skill_id` or `source_id` collisions
