# Library Overview and Interactive Distill Session Protocol Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a user-friendly skill library overview feature and continue formalizing the interactive distill session protocol.

**Architecture:** Keep the new overview feature separate from the low-level registry summary. A dedicated script should read registry data (and, when useful, child meta fields) to generate a human-facing `library_overview.md` with a top-level summary plus grouped skill entries. In parallel, document the end-to-end interactive distill session so the current agent can follow a repeatable dialogue protocol when turning raw materials into child skills.

**Tech Stack:** Python 3, Markdown, existing registry/build metadata, conda `agent` environment for script verification.

---

## File Structure

- Create: `scripts/registry/generate_skill_library_overview.py`
- Create: `skills/library_overview.md`
- Modify: `scripts/registry/README.md`
- Modify: `skills/README.md`
- Modify: `scripts/build/build_child_skill.py`
- Create: `docs/interactive_distill_session_protocol.md`

### Task 1: Add metadata support needed for overview generation

**Files:**
- Modify: `scripts/build/build_child_skill.py`

- [ ] **Step 1: Ensure generated metadata contains a short summary field**

Use `one_sentence_description` as the stable summary source in generated child skill metadata and registry entries.

### Task 2: Add a dedicated skill library overview generator

**Files:**
- Create: `scripts/registry/generate_skill_library_overview.py`
- Create: `skills/library_overview.md`
- Modify: `scripts/registry/README.md`
- Modify: `skills/README.md`

- [ ] **Step 1: Read registry data and compute overview statistics**

- [ ] **Step 2: Group skills by high-level tags for progressive disclosure**

- [ ] **Step 3: Include per-skill detail lines with name, tags, modes, status, execution level, and short summary**

### Task 3: Verify the overview script end to end

**Files:**
- Verify: `skills/library_overview.md`

- [ ] **Step 1: Run the overview generator in the conda `agent` environment**

- [ ] **Step 2: Confirm the generated document contains both summary and detailed sections**

### Task 4: Add the interactive distill session protocol

**Files:**
- Create: `docs/interactive_distill_session_protocol.md`

- [ ] **Step 1: Define the turn-by-turn interactive distill flow**

- [ ] **Step 2: Reference the existing source map, checklist, review gate, build, and trial templates**

### Task 5: Verify consistency

**Files:**
- Verify: `docs/interactive_distill_session_protocol.md`
- Verify: `docs/agent_distillation_runtime_protocol.md`
- Verify: `docs/review_gate_template.md`

- [ ] **Step 1: Confirm the session protocol does not contradict existing runtime rules**
