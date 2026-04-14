# Memory-Aware Child Skill Generation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `evo_skills` so generated child skills are not only documented as memory-aware, but also initialized with usable memory templates and lightweight runtime metadata.

**Architecture:** Keep the change focused on generation quality rather than full automation. Update the `evo_skills` contract to require memory-capable child skills, enrich generated `SKILL.md`, `README.md`, and `memory_schema.md`, initialize memory template files in the scaffold, and add a `memory_runtime` object to generated `meta.json` and registry entries.

**Tech Stack:** Markdown templates, Python builder, JSON metadata, conda `agent` environment for verification.

---

## File Structure

- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `docs/skill_spec_schema.md`
- Modify: `scripts/build/build_child_skill.py`
- Modify: `templates/child-skill-SKILL.template.md`
- Modify: `templates/child-skill-memory-schema.template.md`
- Modify: `templates/child-skill-meta.template.json`
- Verify: generated sample child skill under `examples/generated/`

### Task 1: Update the meta-skill contract

**Files:**
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `docs/skill_spec_schema.md`

- [ ] **Step 1: Define memory-capable child skill requirements**

State that generated child skills must include usage guidance, memory interaction guidance, initialized memory templates, and runtime metadata describing memory reads and writes.

- [ ] **Step 2: Extend schema expectations**

Document a lightweight `memory_runtime` structure in child skill metadata so future runtime logic can read, write, and locate memory consistently.

### Task 2: Upgrade child skill generation templates

**Files:**
- Modify: `templates/child-skill-SKILL.template.md`
- Modify: `templates/child-skill-memory-schema.template.md`
- Modify: `templates/child-skill-meta.template.json`

- [ ] **Step 1: Add memory interaction sections to the skill template**

- [ ] **Step 2: Add read/write/file-mapping sections to the memory schema template**

- [ ] **Step 3: Add `memory_runtime` placeholders to the child meta template**

### Task 3: Update the builder

**Files:**
- Modify: `scripts/build/build_child_skill.py`

- [ ] **Step 1: Generate richer `SKILL.md` and `README.md` content**

- [ ] **Step 2: Generate richer `memory_schema.md` content**

- [ ] **Step 3: Initialize memory template files inside `memory/<skill_id>/shared/` and `users/`**

- [ ] **Step 4: Add `memory_runtime` to generated `meta.json` and registry entries**

### Task 4: Verify sample output

**Files:**
- Verify: `examples/generated/skills/coach_clear_thinking_decision_review/*`
- Verify: `examples/generated/memory/coach.clear-thinking.decision-review.v1/*`

- [ ] **Step 1: Rebuild the sample child skill in the conda `agent` environment**

- [ ] **Step 2: Verify generated documents now explain memory usage**

- [ ] **Step 3: Verify memory template files exist and metadata contains `memory_runtime`**
