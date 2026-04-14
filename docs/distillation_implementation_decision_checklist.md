# 一、文档目的

本文档用于把 `docs/distillation_workflow_research_report.md` 的研究结论压缩成一份 **可直接指导 `evo_skills` 实现的决策清单**。

它不是完整综述，也不是最终代码设计，而是回答下面这个问题：

> 如果现在要继续实现 `evo_skills` 的蒸馏层与运行层，哪些决策已经可以定死，哪些规则必须遵守？

这份清单应被视为后续实现时的工程判断基线。

# 二、已确认的总原则

## 1. 采用 agent-only 蒸馏流程

结论：

- 不接入任何外部 LLM API。
- 不依赖额外独立模型服务完成蒸馏。
- 由当前 agent 会话完成阅读、提炼、分类、mode 判断和 skill 设计。

工程含义：

- 代码与文档中不应再假设“外部 LLM 服务可用”。
- 后续实现重点应放在 workflow、checklist、templates、review gate，而不是模型 API 封装。

## 2. 采用交互式 agent + 明确阶段产物的 B 方案

结论：

- 当前 agent 先产出 `skill_spec.json`
- 用户确认关键字段
- 再调用 builder 落地

工程含义：

- 不能从原文直接一步跳到最终 child skill 文件。
- `skill_spec.json` 必须保持为一等中间产物。

## 3. 脚本只负责机械落地，不负责内容理解

结论：

- 脚本负责目录创建、文件写入、registry 更新、summary 刷新、memory scaffold。
- 当前 agent 负责思想提炼、材料分类、mode 判定、execute 判定、命名设计。

工程含义：

- 不应尝试把“文章理解”塞进 build 脚本。
- 后续脚本设计都应围绕 deterministic behavior 展开。

# 三、蒸馏前必须先做的判断

## 1. 必须先判断材料类型

结论：

每次蒸馏前，当前 agent 必须先判断来源材料属于哪类内容。

最少支持以下类型：

- `article`
- `book`
- `tutorial`
- `reference`
- `notes`
- `transcript`

工程含义：

- 后续应实现一个 **source-type classification step**。
- 该步骤是 distillation workflow 的前置动作，不可跳过。

## 2. 必须先判断目标产物类型

结论：

材料类型判定后，还要判断这份内容最终更适合沉淀成什么。

最少支持以下目标：

- 原则型 skill
- 教练型 skill
- 操作型 skill
- 参考型 skill
- memory / 约束型记录

工程含义：

- 不是所有材料都应该被 build 成正式 child skill。
- 有些内容只能进入 article package 或 memory，而不该直接生成公开 skill。

# 四、蒸馏过程必须采用的阶段

## 1. 先做 source map，不直接总结全文

结论：

当前 agent 在正式提炼前，应先产出 source map，至少包括：

- 内容概览
- 主题分块
- 高价值段落
- 重复点
- 明显噪音 / 可忽略部分

工程含义：

- 后续应实现一个 `source_map` 阶段或文档模板。
- 这一步可作为 build 前的早期质量门槛。

## 2. 必须提取四类原子单元

结论：

每次蒸馏至少要尝试从材料中提取：

- `Concepts`
- `Procedures`
- `Rules`
- `Constraints`

工程含义：

- 这四类原子单元应成为 distillation checklist 的核心部分。
- 如果材料无法稳定提取出这些结构，通常不应该继续 build 正式 skill。

## 3. 必须经过 review gate

结论：

在 build 之前，用户至少应确认以下字段：

- `display_name`
- `skill_id`
- `content_type`
- `supported_modes`
- `execution_level`
- `core_thesis`

工程含义：

- 后续实现应提供一个明确的 review 模板或 review 展示格式。
- build 流程默认应要求确认，而不是默默继续。

# 五、不同材料类型对应的默认蒸馏策略

## 1. 文章 / 博客 / 长文

默认策略：

- 优先提炼 thesis、规则、适用边界、误用
- 默认产出原则型或教练型 skill
- 默认不启用 execute

实现决策：

- 对 `article` 类型，后续 workflow 应优先走 `principle / coaching` 模式模板。

## 2. 书籍

默认策略：

- 优先提炼章节地图、核心模型、重复原则、反模式
- 默认产出框架型 / 教练型 / 反思型 skill
- 默认不启用 execute

实现决策：

- 对 `book` 类型，后续 workflow 不应按“逐段摘要”实现，而应按“模型抽取”实现。

## 3. 教程 / 操作指南

默认策略：

- 优先提炼前置条件、步骤、成功信号、排错分支、回滚方式
- 默认产出操作型 skill
- 默认作为 `execute` 候选

实现决策：

- 对 `tutorial` 类型，后续 workflow 应重点支持 `execute` 判定。

## 4. 技术文档 / 官方参考说明

默认策略：

- 先保留 reference 层，再做 task wrapper
- 默认产出参考型 skill 或混合型 skill
- execute 仅在明确任务包装后才评估

实现决策：

- 对 `reference` 类型，不能简单把全文变成步骤。

## 5. 笔记 / 摘录

默认策略：

- 先聚类去重，再抽取重复出现的判断标准
- 默认产出轻量 skill 或 memory

实现决策：

- 对 `notes` 类型，应优先实现聚类/归并逻辑，而不是直接 build。

## 6. 转录 / 会议纪要

默认策略：

- 优先提取决策、约束、禁忌、优先级
- 默认优先沉淀为 memory / guardrail，而不是公开通用 skill

实现决策：

- 对 `transcript` 类型，应谨慎 build 正式 child skill。

# 六、输出质量的硬性检查项

后续实现的每个新 child skill，在进入正式 registry 之前，建议都通过以下硬检查：

## 1. 可触发性

- 是否明确写出适用场景？
- 是否有真实用户会说的 trigger phrases？

## 2. 可执行性

- 如果支持 execute，步骤是否完整？
- 是否定义了输入、输出、停止条件、确认条件？

## 3. 可验证性

- 是否有完成标准或自查方式？

## 4. 可复用性

- 是否把具体例子与通用规则区分清楚？

## 5. 可追溯性

- 是否保留来源、版本、路径？

## 6. 边界清晰

- 是否说明不适用情况？
- 是否说明高风险误用？

## 7. 结构友好

- 是否可以快速扫描？
- 标题、列表、输出结构是否清楚？

实现决策：

- 后续应把这些检查项沉淀成一份 formal checklist，而不是只存在研究报告里。

# 七、当前最应优先实现的模块

基于当前仓库状态，后续优先级应如下：

## 优先级 1：distillation checklist

需要一个正式清单，明确当前 agent 蒸馏时必须完成的项目。

## 优先级 2：source-type decision rule

需要一套材料分类与目标产物判定规则。

## 优先级 3：review gate template

需要一套 build 前给用户确认的展示模板。

## 优先级 4：post-build trial rule

新 skill build 完后，应至少做一个最小试跑验证。

## 优先级 5：runtime routing rule

后续用户真实提问时，需要知道怎么从 registry 中选 child skill 并切 mode。

# 八、当前不应优先做的事情

基于本次研究，以下方向不应成为下一阶段优先级：

## 1. 不应优先增加更多外部集成

因为已明确采用 agent-only 流程。

## 2. 不应优先把 build 脚本做得过于复杂

builder 已经有 MVP，当前瓶颈不在 build，而在 distillation 质量控制。

## 3. 不应优先继续堆模板而缺少 decision rule

模板已经不少，真正缺的是：

- 何时用哪种蒸馏方式
- 何时允许 build
- 何时不该 build

# 九、可直接用于后续实现的结论

如果把本次研究压缩成一组可执行结论，那么 `evo_skills` 后续实现应遵守下面这些规则：

1. **先分类，再蒸馏。**
2. **先做 source map，再做 spec。**
3. **先抽 Concepts / Procedures / Rules / Constraints，再决定 skill 形态。**
4. **先 review gate，再 build。**
5. **先最小试跑，再正式纳入运行时。**
6. **不是所有材料都该生成 child skill。**
7. **教程优先考虑 execute，文章和书默认不启 execute。**
8. **转录与会议纪要默认优先做 memory / guardrail，不直接做通用 skill。**

# 十、结语

这份文档的作用不是替代完整研究报告，而是把研究结果收敛成工程决策。

后续继续实现 `evo_skills` 时，应优先以本文档为实现依据，再回到完整研究报告补充背景与论证。
