# registry scripts

This directory contains registry-maintenance helpers for `evo_skills`.

## Responsibilities

- initialize the machine-readable registry
- validate registry structure and required keys
- detect duplicate `skill_id` values
- detect obvious entry-path mismatches
- later refresh the human-readable `skills/skill_summary.md`

## Current files

- `validate_registry.py`: minimal registry validator for the initial scaffold

## Expected registry entry shape

Each child skill entry in `skills/registry.json` should eventually include:

- `skill_id`
- `display_name`
- `source_id`
- `content_type`
- `supported_modes`
- `execution_level`
- `status`
- `version`
- `memory_enabled`
- `exportable`
- `entry_path`

## Usage

Run from the `evo_skills` root or any directory:

```bash
python3 ".opencode/skills/evo_skills/scripts/registry/validate_registry.py"
```

Expected success output:

```text
Registry validation passed.
```
