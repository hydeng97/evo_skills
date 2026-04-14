---
name: {{skill_folder_name}}
description: |
  {{one_sentence_description}}

  Triggers when user mentions:
  - "{{trigger_phrase_1}}"
  - "{{trigger_phrase_2}}"
  - "{{trigger_phrase_3}}"
---

# {{display_name}}

## Core thesis

{{core_thesis}}

## Supported modes

- `teach`: {{teach_mode_behavior}}
- `coach`: {{coach_mode_behavior}}
- `reflect`: {{reflect_mode_behavior}}
- `execute`: {{execute_mode_behavior_or_not_supported}}

## When to use

- {{use_case_1}}
- {{use_case_2}}

## Memory interaction

- `teach` reads: {{teach_memory_reads}}
- `coach` reads: {{coach_memory_reads}}
- `reflect` reads: {{reflect_memory_reads}}
- `execute` reads: {{execute_memory_reads}}
- Write back when: {{memory_write_triggers}}

## Memory paths

- Shared templates: `memory/{{skill_id}}/shared/`
- User memories: `memory/{{skill_id}}/users/<user_id>/`

## Execution boundary

- `execution_level`: `{{execution_level}}`
- Allowed actions: {{allowed_actions}}
- Approval required: {{approval_required_actions}}

## Examples

- {{example_1}}
- {{example_2}}

## Memory policy

- Store: {{memory_store_rules}}
- Avoid: {{memory_avoid_rules}}

## Export notes

This child skill should remain useful when copied into another agent system with its local metadata files.
