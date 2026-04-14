# Tags Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add first-class dynamic tag support to the `evo_skills` schema, templates, and registry conventions without hardcoding a fixed category tree.

**Architecture:** Keep tags flexible and rule-driven. Introduce `tags` as a first-class field in `skill_spec.json`, child-skill metadata templates, and registry entry expectations. Tags remain dynamically created and managed by the current agent according to `docs/dynamic_tagging_rule.md`, rather than coming from a predefined taxonomy.

**Tech Stack:** Markdown docs, JSON templates, registry conventions.

---

## File Structure

- Modify: `docs/skill_spec_schema.md`
- Modify: `templates/skill-spec.template.json`
- Modify: `templates/child-skill-meta.template.json`
- Modify: `skills/README.md`
- Modify: `skills/registry.json`
- Modify: `scripts/registry/README.md`

### Task 1: Update schema documentation

**Files:**
- Modify: `docs/skill_spec_schema.md`

- [ ] **Step 1: Add `tags` to the formal schema description**

Document `tags` as a first-class field in `skill_design` or equivalent recommended output location, and explain that tags are dynamic, not pre-enumerated.

- [ ] **Step 2: Explain tag semantics**

State that tags can represent domain, topic, or function, but are stored in a unified list unless later split by implementation needs.

### Task 2: Update generation templates

**Files:**
- Modify: `templates/skill-spec.template.json`
- Modify: `templates/child-skill-meta.template.json`

- [ ] **Step 1: Add `tags` to the skill spec template**

Include placeholder tag values that demonstrate unified tag storage.

- [ ] **Step 2: Add `tags` to the child meta template**

Ensure generated child-skill metadata has a stable place to store tags for future routing use.

### Task 3: Update registry conventions

**Files:**
- Modify: `skills/README.md`
- Modify: `skills/registry.json`
- Modify: `scripts/registry/README.md`

- [ ] **Step 1: Add tags to the documented registry entry shape**

- [ ] **Step 2: Extend the example registry structure to show tag support**

- [ ] **Step 3: Update registry script docs to mention tags validation expectations for future work**

### Task 4: Verify consistency

**Files:**
- Verify: `docs/skill_spec_schema.md`
- Verify: `templates/skill-spec.template.json`
- Verify: `templates/child-skill-meta.template.json`
- Verify: `skills/registry.json`

- [ ] **Step 1: Read all updated files and confirm `tags` uses the same meaning everywhere**

- [ ] **Step 2: Validate JSON templates remain syntactically valid**
