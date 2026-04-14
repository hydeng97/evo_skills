# memory

This directory stores long-term memory for generated child skills.

Recommended layout:

```text
memory/<skill_id>/
  shared/
  users/<user_id>/
    profile.md
    progress.md
    sessions/
```

- `shared/`: reusable, non-user-specific memory templates or stable observations
- `profile.md`: user background, goals, preferences, and constraints
- `progress.md`: summarized milestones, recurring patterns, and growth changes
- `sessions/`: session-level notes that can later be compressed into summaries

Do not store secrets or raw credentials here.
