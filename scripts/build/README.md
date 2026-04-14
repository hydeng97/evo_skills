# build scripts

This directory contains scripts that turn a validated `skill_spec.json` into a concrete managed child skill package.

## Current files

- `build_child_skill.py`: generate article artifacts, child skill files, memory scaffolding, and registry updates from a spec

## Minimal usage

Run Python scripts in the conda `agent` environment.

```bash
source ~/.zshrc >/dev/null 2>&1
conda activate agent
python "scripts/build/build_child_skill.py" --spec "examples/specs/sample_skill_spec.json" --root "examples/generated"
```

This command creates a full generated tree under `examples/generated/` without modifying the main repository runtime.
