# Runtime Orchestrator v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the first minimal runtime orchestrator for `evo_skills` so the system can produce structured routing and memory plans, and optionally perform low-risk memory actions.

**Architecture:** Keep orchestrator v1 narrow and explainable. A single script under `scripts/runtime/` will read registry data, inspect child skill metadata, classify a request into a likely mode, select a best matching skill using tags and supported modes, compute a memory plan from `memory_runtime`, and return a structured orchestration result. If explicitly allowed, it may also write a session summary through the existing memory runtime scripts.

**Tech Stack:** Python 3, JSON, registry metadata, child meta files, memory runtime scripts, conda `agent` environment for verification.

---

## File Structure

- Create: `scripts/runtime/README.md`
- Create: `scripts/runtime/orchestrate_runtime.py`
- Modify: `README.md`
- Modify: `docs/runtime_orchestrator_design.md`

### Task 1: Define the runtime entrypoint contract

**Files:**
- Create: `scripts/runtime/README.md`
- Modify: `README.md`

- [ ] **Step 1: Document v1 scope and inputs**

- [ ] **Step 2: Document what is not automated in v1**

### Task 2: Implement orchestrator v1

**Files:**
- Create: `scripts/runtime/orchestrate_runtime.py`

- [ ] **Step 1: Parse request, registry root, user id, and optional flags**

- [ ] **Step 2: Load registry and candidate child metadata**

- [ ] **Step 3: Choose a likely mode from the request**

- [ ] **Step 4: Score candidate skills using tags, content type, and supported modes**

- [ ] **Step 5: Build a memory plan from `memory_runtime`**

- [ ] **Step 6: Output a structured `orchestration_result`**

- [ ] **Step 7: Optionally write a session summary when explicitly enabled**

### Task 3: Verify v1 against sample data

**Files:**
- Verify: `examples/generated/skills/registry.json`
- Verify: `examples/generated/skills/coach_clear_thinking_decision_review/meta.json`

- [ ] **Step 1: Run orchestrator for a `coach`-like request**

- [ ] **Step 2: Verify selected skill, selected mode, and memory plan are correct**

- [ ] **Step 3: Verify optional session write mode works with sample memory directories**
