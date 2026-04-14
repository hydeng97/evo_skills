# Article-Runtime-Aware Child Skills Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the gap between generated child skills and their distilled article packages by adding a first-class `article_runtime` contract to child skill metadata and generated documentation.

**Architecture:** Keep the solution parallel to `memory_runtime`. Generated child skills should know both where article package files live and which article resources each mode should read. This contract belongs primarily in child metadata and child-skill docs, not only in registry-level summaries.

**Tech Stack:** Markdown docs, JSON metadata, Python builder, existing sample generated output for verification.

---

## File Structure

- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `docs/skill_spec_schema.md`
- Modify: `templates/child-skill-SKILL.template.md`
- Modify: `templates/child-skill-meta.template.json`
- Modify: `scripts/build/build_child_skill.py`

### Task 1: Update the meta-skill contract

**Files:**
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `docs/skill_spec_schema.md`

- [ ] **Step 1: Define article-runtime-aware child skill requirements**

- [ ] **Step 2: Document `article_runtime` metadata alongside `memory_runtime`**

### Task 2: Update templates and builder

**Files:**
- Modify: `templates/child-skill-SKILL.template.md`
- Modify: `templates/child-skill-meta.template.json`
- Modify: `scripts/build/build_child_skill.py`

- [ ] **Step 1: Add article interaction sections to generated skill docs**

- [ ] **Step 2: Add `article_runtime` metadata with `paths`, `read_by_mode`, and `required_by_mode`**

### Task 3: Verify sample output

**Files:**
- Verify: generated sample child skill metadata and docs

- [ ] **Step 1: Rebuild sample child skill**

- [ ] **Step 2: Confirm `article_runtime` appears in `meta.json`**

- [ ] **Step 3: Confirm child skill docs explain how article package files are used by mode**
