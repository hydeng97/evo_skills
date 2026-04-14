---
name: coach_clear_thinking_decision_review
description: |
  帮助用户理解并应用清晰思考进行决策复盘。

  Triggers when user mentions:
  - "帮我复盘这个决定"
  - "我总是判断失误"
---

# Clear Thinking 决策复盘教练

## Core Thesis

在行动前先澄清问题和偏差来源，可以提高长期决策质量。

## When to use

- 决策复盘
- 学习规划

## Not a fit when

- 不适合必须秒级反应的应急场景

## Supported Modes

teach, coach, reflect

## Mode behavior

- `teach`: explain the core concepts, examples, and misconceptions from this source.
- `coach`: apply the source framework to the user's real scenario and constraints.
- `reflect`: summarize patterns, changes, and recurring blind spots over time.
- `execute`: only available if execution is explicitly enabled for this skill.

## Execution Level

none

## Memory interaction

- `teach` reads: profile
- `coach` reads: profile, progress
- `reflect` reads: profile, progress, recent session summaries
- `execute` reads: profile
- Write back when: goal changes, stable patterns, progress summaries

## Memory paths

- Shared templates: `memory/coach.clear-thinking.decision-review.v1/shared/`
- User memories: `memory/coach.clear-thinking.decision-review.v1/users/<user_id>/`

## Article interaction

- `teach` reads: distilled.md, examples.md
- `coach` reads: distilled.md, coach_notes.md, examples.md
- `reflect` reads: distilled.md, coach_notes.md
- `execute` reads: none by default

## Article paths

- Distilled content: `articles/article_clear-thinking_sample/distilled.md`
- Examples: `articles/article_clear-thinking_sample/examples.md`
- Coach notes: `articles/article_clear-thinking_sample/coach_notes.md`

## Memory policy

- Store: 目标, 约束, 卡点
- Avoid: 密钥, 逐字隐私对话
