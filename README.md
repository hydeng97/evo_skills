# evo_skills

`evo_skills` 是一个面向长期演化的元 skill 系统，用于把文章、书籍、教程、技术文档、笔记和转录材料蒸馏成可复用的 child skills，并在后续对话中持续调用、管理和记忆这些技能。

它不是一个单纯的“摘要工具”，而是一个围绕 **知识蒸馏、skill 生成、运行时路由、长期记忆、标签治理** 设计的工作流系统。

## 核心定位

`evo_skills` 的目标是解决这样一类问题：

- 如何把大量来源各异的内容沉淀为可重复复用的 agent skill
- 如何让这些 skill 在后续真实问题中被智能调用，而不是只停留在文档层
- 如何在长期互动中积累用户背景、偏好、目标和成长变化
- 如何在 skill 数量越来越多时，仍然保持可管理、可检索、可扩展

## 核心能力

### 1. Source Distillation

把用户提供的原始材料转换为结构化中间产物，而不是直接把原文压缩成普通摘要。

系统强调：

- 材料类型判断
- source map
- 四类原子单元提取
- `skill_spec.json` 生成
- review gate

这使得蒸馏过程更可解释、更可审查，也更适合长期维护。

### 2. Child Skill Generation

基于 `skill_spec.json` 生成标准化 child skills，包括：

- `SKILL.md`
- `README.md`
- `meta.json`
- `memory_schema.md`

生成出的 child skill 既能被 `evo_skills` 统一管理，也尽可能保持可移植、可独立导出。

### 3. Runtime Routing

当用户在真实对话中提出问题时，`evo_skills` 不会简单遍历 skill 总表，而是通过：

- 用户意图判断
- 动态标签过滤
- mode 兼容性判断
- execute 风险判断
- memory 关联排序

来选择最合适的 child skill。

### 4. Long-Term Memory

系统将 memory 视为长期交互中的稳定摘要，而不是原始对话存档。

memory 可用于：

- 更贴合用户背景的解释
- 更有针对性的教练分析
- 更连续的长期反思
- 更一致的执行偏好控制

### 5. Governance and Evolution

`evo_skills` 不只是生成 skill，还负责：

- registry 管理
- summary / overview 生成
- 动态标签治理
- child skill 演化与维护

这让系统可以从少量 skill 平滑扩展到更大的 skill 库，而不会快速失控。

## Child Skill Modes

每个 child skill 可以支持一个或多个运行模式：

- `teach`：讲解关键思想、概念、案例和误区
- `coach`：结合用户场景做分析、建议和提问引导
- `reflect`：做复盘、总结成长模式和长期变化
- `execute`：在流程稳定、边界清晰时执行具体步骤

其中 `execute` 是可选能力，只有在流程明确、结果可验证、风险可控时才会开启。

## Agent-Only Workflow

`evo_skills` 采用 **agent-only** 的蒸馏与构建流程。

这意味着：

- 不依赖外部 LLM API 完成核心蒸馏
- 由当前 agent 负责阅读、提炼、分类、判定和设计
- 由本地脚本负责 deterministic 的落地、registry 更新和 overview 刷新

这种设计让系统既保留智能判断能力，又保留工程化的稳定输出。

## Dynamic Tagging System

随着 skill 数量增加，固定分类树会越来越僵化。因此 `evo_skills` 不采用预定义死板分类体系，而采用 **动态标签系统**。

动态标签系统支持：

- 标签新建
- 标签复用
- 标签合并
- 标签拆分
- 基于标签的渐进式披露

这使得 skill 库可以在不断扩张的同时，仍然保持可路由、可导航、可理解。

## Skill Library Views

系统维护两个不同层级的人类可读视图：

### `skills/skill_summary.md`

偏 registry-oriented 的紧凑摘要，适合快速查看每个 skill 的核心元信息。

### `skills/library_overview.md`

偏用户浏览的总览页，提供：

- 技能库总体统计
- 标签分组
- 每个 skill 的名称、标签、模式、状态、功能摘要

这使得用户无需直接面对完整 skill 总表，就能先建立对 skill 库的大致认识。

## 适用场景

`evo_skills` 适合以下场景：

- 从文章或书籍中提炼长期可复用的认知型 skill
- 从教程或工作流中提炼可执行的操作型 skill
- 为大型 skill 库提供统一治理、标签、summary 和 overview
- 让 agent 在长期对话中基于已有技能与记忆持续陪伴用户

## 仓库结构

- `articles/`：蒸馏后的来源材料包
- `skills/`：child skill、registry、summary、overview
- `memory/`：长期记忆结构
- `scripts/`：构建、registry、overview 等自动化脚本
- `templates/`：skill spec、review gate、source map、trial report 等模板
- `docs/`：工作流协议、蒸馏规则、运行规则、治理规则
- `exports/`：导出后的可移植 child skill 包
- `archive/`：废弃或替换后的 skill 版本

## 当前特点

这个仓库目前已经具备：

- `skill_spec.json` 驱动的 build 流程
- 动态标签支持
- registry / summary / overview 生成
- interactive distill session protocol
- runtime routing 规则
- memory runtime 规则
- post-build trial 规则

换句话说，`evo_skills` 已经不是一个零散脚本集合，而是一个逐步成型的 **元 skill operating system**。
