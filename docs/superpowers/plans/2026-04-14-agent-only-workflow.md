# Agent-Only Workflow Alignment Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align `evo_skills` documentation and workflow definition with the approved agent-only design: the current agent performs distillation interactively, users review the resulting spec, and local scripts perform deterministic build and governance work.

**Architecture:** Keep the new workflow narrow and explicit. Documentation must stop implying that an external LLM service or separate LLM API is involved. The canonical flow becomes: source material -> current agent distills `skill_spec.json` -> user reviews key fields -> local builder writes artifacts -> registry and summary update.

**Tech Stack:** Markdown documentation, existing skill docs, existing build and registry scripts.

---

## File Structure

- Modify: `README.md`
- Modify: `SKILL.md`
- Modify: `docs/skill_spec_schema.md`
- Create: `docs/agent_only_distillation_workflow.md`

### Task 1: Update the repo-level workflow description

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace external-LLM wording**

Update the build workflow section so it clearly says the current agent produces `skill_spec.json`, not an external LLM API.

- [ ] **Step 2: Add the explicit review gate**

Document that the user should review key spec fields before `build_child_skill.py` is run.

### Task 2: Update the public skill contract

**Files:**
- Modify: `SKILL.md`

- [ ] **Step 1: Define the agent-only distillation responsibility**

State clearly that `evo_skills` itself performs source distillation interactively inside the current agent session.

- [ ] **Step 2: Define the spec-review-before-build rule**

Document that the agent should present the distilled spec summary to the user before invoking local build scripts.

### Task 3: Update the schema document to match the approved workflow

**Files:**
- Modify: `docs/skill_spec_schema.md`

- [ ] **Step 1: Replace “LLM produces spec” language with “current agent produces spec”**

- [ ] **Step 2: Clarify the separation of responsibilities**

State that the current agent handles understanding and distillation, while scripts only handle deterministic artifact generation and registry maintenance.

### Task 4: Add a dedicated workflow document

**Files:**
- Create: `docs/agent_only_distillation_workflow.md`

- [ ] **Step 1: Document the full approved workflow**

Cover: user supplies source, agent distills spec, user reviews key fields, builder writes artifacts, agent verifies generated output.

- [ ] **Step 2: Document the key approval fields**

List `display_name`, `skill_id`, `content_type`, `supported_modes`, `execution_level`, and `core_thesis` as the minimum review checkpoint.

### Task 5: Verify consistency

**Files:**
- Verify: `README.md`
- Verify: `SKILL.md`
- Verify: `docs/skill_spec_schema.md`
- Verify: `docs/agent_only_distillation_workflow.md`

- [ ] **Step 1: Read the updated docs and confirm consistent terminology**

- [ ] **Step 2: Confirm no document still implies external LLM API usage**
