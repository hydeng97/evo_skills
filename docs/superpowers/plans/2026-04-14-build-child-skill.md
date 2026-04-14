# Build Child Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a minimal `build_child_skill.py` flow that converts a valid `skill_spec.json` into article artifacts, a child skill package, memory directories, and registry updates.

**Architecture:** Keep the first version narrow and deterministic. A single Python script under `scripts/build/` will read a spec file, materialize the expected directory structure, write the first set of markdown/json artifacts, append or replace the registry entry for the generated skill, and refresh the human-readable skill summary. Verification will use a fixture spec plus direct file checks.

**Tech Stack:** Python 3, JSON, Markdown, existing registry scripts.

---

## File Structure

- Create: `scripts/build/build_child_skill.py`
- Create: `scripts/build/README.md`
- Create: `examples/specs/sample_skill_spec.json`
- Create: `examples/generated/.gitkeep`
- Modify: `README.md`
- Modify: `skills/registry.json`
- Modify: `skills/skill_summary.md`

### Task 1: Add a sample spec fixture for TDD verification

**Files:**
- Create: `examples/specs/sample_skill_spec.json`

- [ ] **Step 1: Write a minimal but valid sample skill spec**

Include one example, one key concept, a coaching-style child skill identity, `supported_modes` with `teach`, `coach`, `reflect`, and `execution_level` set to `none`.

- [ ] **Step 2: Use the sample spec as the canonical verification input**

The sample file should be rich enough that generated markdown files can be checked for expected text.

### Task 2: Implement the first build script

**Files:**
- Create: `scripts/build/build_child_skill.py`
- Create: `scripts/build/README.md`

- [ ] **Step 1: Implement argument parsing**

Support at least `--spec <path>` and optional `--root <path>` for writing output somewhere other than the repository root.

- [ ] **Step 2: Implement spec loading and required-key validation**

Fail clearly if the spec is missing required top-level keys or core identity fields.

- [ ] **Step 3: Implement article artifact generation**

Write `source_meta.json`, `distilled.md`, `examples.md`, and `coach_notes.md` under `articles/<source_id>/`.

- [ ] **Step 4: Implement child-skill package generation**

Write `SKILL.md`, `README.md`, `meta.json`, and `memory_schema.md` under `skills/<skill_folder_name>/`.

- [ ] **Step 5: Implement memory scaffold generation**

Create `memory/<skill_id>/shared/` and `memory/<skill_id>/users/` with `.gitkeep` placeholders.

- [ ] **Step 6: Implement registry update and summary refresh**

Add or replace the generated skill entry in `skills/registry.json`, then call the existing summary refresh script or equivalent in-process logic.

### Task 3: Verify the end-to-end build flow

**Files:**
- Verify: `examples/specs/sample_skill_spec.json`
- Verify: generated output tree under a temporary root

- [ ] **Step 1: Run the builder against the sample spec**

Run:

```bash
python3 "scripts/build/build_child_skill.py" --spec "examples/specs/sample_skill_spec.json" --root "examples/generated"
```

Expected: the script prints the generated paths and exits successfully.

- [ ] **Step 2: Verify expected files exist**

Check that the article package, child skill package, memory directories, registry file, and summary file are all created under `examples/generated`.

- [ ] **Step 3: Verify registry remains valid**

Run the registry validator against the generated root or reuse the same logic to confirm the generated registry shape is still valid.

### Task 4: Document usage and repo workflow

**Files:**
- Modify: `README.md`
- Create: `scripts/build/README.md`

- [ ] **Step 1: Document what the builder does**

Explain that LLM produces `skill_spec.json`, then the builder turns it into the actual managed child skill structure.

- [ ] **Step 2: Document the minimal build command**

Show how to run the builder with the sample spec and what directories it creates.
