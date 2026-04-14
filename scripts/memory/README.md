# memory scripts

This directory contains the minimal memory runtime helpers for `evo_skills`.

## Supported operations

- `init_user_memory.py`: initialize a user directory from shared templates
- `read_memory_context.py`: read the effective memory context for a given mode
- `write_session_summary.py`: write a short session summary file
- `compress_memory.py`: compress session summaries into durable memory files

## Notes

- These scripts operate on generated child-skill memory directories.
- They are designed to work with the `memory_runtime` metadata stored in child-skill `meta.json`.
