# Memory Schema: {{display_name}}

## Persistent storage rules

Store only summarized, durable observations. Never commit raw secrets, access tokens, or verbatim private memory.

## By mode

### teach

- Record recurring misconceptions
- Record preferred explanation style
- Record concepts the user still confuses

### coach

- Record user goals and constraints
- Record recurring blockers and effective interventions
- Record preferred decision patterns

### reflect

- Record milestones, behavior changes, and repeated blind spots
- Record which strategies improved outcomes over time

### execute

- Record preferred execution style
- Record safe defaults and recurring setup assumptions
- Record successful and failed low-risk workflows in summarized form

## Read by mode

- `teach`: {{teach_read_layers}}
- `coach`: {{coach_read_layers}}
- `reflect`: {{reflect_read_layers}}
- `execute`: {{execute_read_layers}}

## Write triggers

- {{write_trigger_1}}
- {{write_trigger_2}}

## File mapping

- `profile.md`: {{profile_file_usage}}
- `progress.md`: {{progress_file_usage}}
- `sessions/*.md`: {{sessions_file_usage}}

## Avoid storing

- secrets
- raw credentials
- verbatim private logs
- unnecessary large transcripts
