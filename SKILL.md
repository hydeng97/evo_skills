---
name: evo_skills
description: |
  Build, manage, and route a library of article-derived child skills with long-term memory and optional execution support.

  Triggers when user mentions:
  - "文章转 skill"
  - "从书里提炼 skill"
  - "统一管理多个 skill"
---

# evo_skills

`evo_skills` is the exposed meta skill for this workspace. It is discoverable by the agent system directly and acts as the control layer for managed child skills created from books, articles, tutorials, and other learning materials.

## What evo_skills does

`evo_skills` owns five responsibilities:

1. **Source distillation** — the current agent reads user-provided source material and distills it into a structured `skill_spec.json` plus normalized article packages under `articles/`.
2. **Child-skill generation** — create standalone-friendly child skills under `skills/` using the shared templates in `templates/`.
3. **Skill routing** — pick the most relevant child skill for a user request and decide which mode to use.
4. **Memory orchestration** — keep long-term memory in `memory/` using a per-skill and per-user structure.
5. **Governance and export** — maintain `skills/skill_summary.md`, `skills/registry.json`, and prepare portable exports under `exports/`.

## Agent-only distillation rule

`evo_skills` should not rely on any external LLM API for content distillation. The current agent session must do the actual reading, synthesis, mode evaluation, and child-skill design work.

The normal sequence is:

1. Read the user-supplied source material.
2. Distill a `skill_spec.json` candidate in the current session.
3. Present the key design fields for user review.
4. Only after approval, invoke local build scripts to materialize files and registry updates.

The detailed operating documents for this workflow are:

- `docs/source_type_decision_rule.md`
- `docs/agent_distillation_checklist.md`
- `docs/review_gate_template.md`
- `docs/agent_distillation_runtime_protocol.md`
- `docs/post_build_trial_rule.md`

The minimum review gate before build should cover:

- `display_name`
- `skill_id`
- `content_type`
- `supported_modes`
- `execution_level`
- `core_thesis`

## Child-skill modes

Every generated child skill should support one or more of these modes:

- `teach`: explain key ideas, examples, mechanisms, and misconceptions
- `coach`: analyze the user's scenario, suggest strategies, ask guiding questions, and adapt to constraints
- `reflect`: summarize growth, persistent blind spots, and behavior changes from long-term memory
- `execute`: perform concrete steps when the source material describes a repeatable, low-to-medium-risk workflow

## Execution-mode rule

`execute` is **optional**. It is enabled only when the child skill passes an execution-eligibility review.

Enable `execute` only if the source material has:

1. a repeatable step-by-step workflow
2. actions the agent can realistically map to tools
3. outputs that can be validated
4. risk low enough for the balanced execution posture

Execution levels:

- `none`: no execution allowed
- `plan_only`: provide steps but do not execute
- `guided_execute`: execute safe steps while explaining what is happening
- `safe_execute`: execute low-risk standard actions directly

Balanced posture:

- Safe reads, analysis, generation, indexing, and tests may run automatically when clearly within scope.
- Any destructive, production-impacting, remote, credential-sensitive, or ambiguous action requires explicit user approval first.

## Long-term memory policy

Memory is organized by skill and then by user.

Recommended layout:

```text
memory/<skill_id>/
  shared/
  users/<user_id>/
    profile.md
    progress.md
    sessions/
```

Memory should store summarized, durable observations such as goals, recurring obstacles, preferred explanation style, effective interventions, and growth milestones.

Do **not** commit raw secrets, access tokens, or verbatim private memory into repo files. Store only safe summaries, schemas, and stable pointers.

## Registry and naming rules

Use stable IDs:

- `source_id`: source-material identifier, such as `article_clear-thinking_2026-04`
- `skill_id`: child-skill identifier, such as `coach.clear-thinking.decision-review.v1`
- `display_name`: human-readable title, such as `Clear Thinking 决策复盘教练`

`skills/registry.json` is the machine-readable inventory.

`skills/skill_summary.md` is the human-readable overview.

## Child-skill standard

Each generated child skill should be portable and contain at least:

- `SKILL.md`
- `README.md`
- `meta.json`
- `memory_schema.md`
- optional `cases/` and `prompts/`

Memory-capable child skills should additionally include:

- initialized memory scaffold templates under `memory/<skill_id>/shared/`
- a documented memory interaction section in `SKILL.md`
- a documented memory usage section in `README.md`
- lightweight `memory_runtime` metadata describing read-by-mode, write triggers, and memory paths

Generated child skills should work outside `evo_skills` as much as possible. `evo_skills` improves routing, governance, and memory orchestration, but should not make child skills unusable elsewhere.

## Quick usage

Use `evo_skills` when the user wants to:

- turn source material into reusable skills
- manage many child skills consistently
- route a user problem to the right child skill
- maintain long-term growth memory per skill and per user
- decide whether a tutorial-like child skill should expose execution mode
- perform the entire distill -> review -> build workflow inside the current agent session

## Runtime use after build

After child skills exist, `evo_skills` should also manage:

1. **Routing** — choose the most relevant child skill from registry metadata and user intent.
2. **Mode selection** — decide whether the selected skill should operate in `teach`, `coach`, `reflect`, or `execute` mode.
3. **Memory loading** — read the relevant user and skill memory before generating a response.
4. **Memory write-back** — update durable summaries after useful interactions.

Supporting documents for this runtime layer:

- `docs/runtime_routing_rule.md`
- `docs/memory_runtime_rule.md`

## Internal directories

- `articles/` stores normalized content packages derived from source materials
- `skills/` stores managed child skills plus summary and registry files
- `memory/` stores long-term memory for child skills and their users
- `scripts/` stores automation helpers
- `templates/` stores child-skill generation templates
- `exports/` stores portable child-skill bundles
- `archive/` stores retired or superseded child skills
