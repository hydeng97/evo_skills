# 一、文档目的

本文档定义 `evo_skills` 在 **agent-only** 工作流下的实际运行协议。

前面的文档已经分别定义了：

- 研究结论
- 工程决策
- 蒸馏 checklist
- 材料类型判定规则
- review gate 模板

而本文档的作用是把这些内容串成一个 **按顺序执行的 runtime protocol**。

也就是说，它回答的是：

> 当当前 agent 真的拿到一份原始文章、教程、文档或转录时，接下来应该一步一步怎么做？

# 二、适用范围

本文档适用于：

- 当前 agent 要把原始材料蒸馏成 `skill_spec.json`
- 当前 agent 要在 build 前完成 review gate
- 当前 agent 要在 build 后做最小复查

不适用于：

- 只做普通摘要
- 只做项目 memory 记录
- 不进入 child skill build 的临时对话分析

# 三、标准运行顺序

## 第 1 步：收集来源材料

当前 agent 首先应确认：

- 用户提供了什么内容
- 是文件路径、文本、markdown、章节整理稿还是教程片段
- 来源边界是否明确

输出要求：

- 明确 source input
- 明确是否足以进入类型判定

如果来源材料本身不完整，应先停在这里补上下文。

## 第 2 步：判定材料类型

当前 agent 必须使用 `docs/source_type_decision_rule.md` 进行材料类型判断。

最少从以下类型中选择：

- `article`
- `book`
- `tutorial`
- `reference`
- `notes`
- `transcript`

输出要求：

- 给出材料类型判断
- 用简短理由解释为什么这样分类

如果无法分类，不允许继续 build-oriented distillation。

## 第 3 步：判定目标产物类型

在材料类型判定后，当前 agent 需要继续判断：

- 这份材料更适合生成原则型 skill、教练型 skill、操作型 skill、参考型 skill，还是 memory / guardrail？

输出要求：

- 给出目标产物类型
- 给出理由

如果判断结果是 memory / guardrail，而不是正式 child skill，则应停止正式 build 流程。

## 第 4 步：生成 source map

当前 agent 不应直接从原文跳到 `skill_spec.json`，而应先做 source map。

source map 最少包括：

- 内容概览
- 主题分块
- 高价值段落
- 重复点
- 噪音 / 可忽略部分

输出要求：

- 用简洁结构描述 source map

这一步的作用是防止原文中的冗余、修辞、重复内容直接污染 spec。

## 第 5 步：提取四类原子单元

当前 agent 必须尝试提取：

- `Concepts`
- `Procedures`
- `Rules`
- `Constraints`

输出要求：

- 至少明确哪些原子单元存在
- 哪些不存在也要显式说明

这一步是后续 `skill_spec.json` 结构化质量的核心。

## 第 6 步：起草 `skill_spec.json`

当前 agent 根据前面的分析结果，按 `docs/skill_spec_schema.md` 生成 `skill_spec.json` 草案。

要求至少包括：

- `source_meta`
- `distillation`
- `examples`
- `skill_design`
- `mode_evaluation`
- `memory_design`
- `artifact_plan`

输出要求：

- spec 草案结构完整
- execute 判定有依据
- 命名清楚

## 第 7 步：执行蒸馏 checklist

当前 agent 在进入 review gate 前，必须使用 `docs/agent_distillation_checklist.md` 自查。

重点检查：

- 是否已经分类
- 是否有 source map
- 是否有四类原子单元
- spec 是否完整
- execute 判定是否站得住

如果 checklist 未通过，应回到前面相应步骤修正。

## 第 8 步：进入 review gate

当前 agent 使用 `docs/review_gate_template.md` 与用户确认关键字段。

最低确认项：

- `display_name`
- `skill_id`
- `content_type`
- `supported_modes`
- `execution_level`
- `core_thesis`

如果用户未明确确认，则不得自动 build。

## 第 9 步：调用 builder

只有在 review gate 通过后，当前 agent 才能调用本地 builder：

- `scripts/build/build_child_skill.py`

builder 负责：

- 写 article package
- 写 child skill package
- 写 memory scaffold
- 更新 registry
- 刷新 summary

## 第 10 步：执行 post-build trial

build 完后，不应立即宣称完成，而应执行最小试跑。

试跑规则由 `docs/post_build_trial_rule.md` 定义。

## 第 11 步：根据试跑结果决定去向

如果试跑通过：

- 该 child skill 可以进入正式 registry 视图与运行时使用

如果试跑失败：

- 回退到蒸馏阶段或 spec 阶段修正
- 不应带着明显问题进入正式运行态

# 四、运行时停机条件

出现以下任一情况，应暂停继续 build：

- 无法判断材料类型
- 无法判断目标产物类型
- source map 不完整
- 四类原子单元无法提炼
- execute 判定依据不足
- 用户没有通过 review gate

# 五、核心原则

整套 runtime protocol 的核心原则是：

1. 先分类，再提炼。
2. 先 source map，再写 spec。
3. 先 review，再 build。
4. 先试跑，再纳入运行态。

# 六、结论

本文档把 `evo_skills` 的蒸馏层从“有文档规则”提升为“有实际执行顺序”。

后续如果要把这个流程进一步产品化，可以围绕本文档继续沉淀：

- 统一显示模板
- 统一 checklist 渲染
- 统一试跑报告格式
