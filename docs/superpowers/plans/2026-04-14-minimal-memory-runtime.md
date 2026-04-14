# Minimal Memory Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a minimal but usable memory runtime for `evo_skills` so generated child skills can read, update, and compress long-term memory without depending on manual ad hoc filesystem edits.

**Architecture:** Keep the first runtime narrow and deterministic. Use a small script set under `scripts/memory/` to initialize a user memory directory from templates, read the effective memory context for a given mode, append a short session summary, and compress session-level data into progress/profile updates. Reuse the existing `memory_runtime` metadata structure rather than introducing a second competing contract.

**Tech Stack:** Python 3, Markdown files, JSON metadata, conda `agent` environment for verification.

---

## File Structure

- Create: `scripts/memory/README.md`
- Create: `scripts/memory/init_user_memory.py`
- Create: `scripts/memory/read_memory_context.py`
- Create: `scripts/memory/write_session_summary.py`
- Create: `scripts/memory/compress_memory.py`
- Modify: `docs/memory_runtime_rule.md`
- Modify: `README.md`

### Task 1: Define the minimal runtime contract

**Files:**
- Modify: `docs/memory_runtime_rule.md`
- Modify: `README.md`

- [ ] **Step 1: Document the minimal runtime operations**

Define the supported operations: initialize user memory, read memory context, write a session summary, compress summaries into durable memory.

- [ ] **Step 2: Keep the runtime aligned with generated `memory_runtime` metadata**

### Task 2: Implement runtime scripts

**Files:**
- Create: `scripts/memory/README.md`
- Create: `scripts/memory/init_user_memory.py`
- Create: `scripts/memory/read_memory_context.py`
- Create: `scripts/memory/write_session_summary.py`
- Create: `scripts/memory/compress_memory.py`

- [ ] **Step 1: Implement user memory initialization from shared templates**

- [ ] **Step 2: Implement mode-aware memory reads**

- [ ] **Step 3: Implement session summary writes**

- [ ] **Step 4: Implement a simple compression/update pass into `profile.md` and `progress.md`**

### Task 3: Verify the minimal runtime end to end

**Files:**
- Verify: `examples/generated/memory/coach.clear-thinking.decision-review.v1/`

- [ ] **Step 1: Initialize a sample user memory directory**

- [ ] **Step 2: Write a sample session summary**

- [ ] **Step 3: Read memory context for `coach` and `reflect` modes**

- [ ] **Step 4: Run compression and confirm durable files update**
