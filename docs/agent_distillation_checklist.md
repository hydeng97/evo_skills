# 一、文档目的

本文档定义 `evo_skills` 在 **agent-only** 工作流下的标准蒸馏检查清单。

它的目标不是替代 `skill_spec.json`，而是规定：

> 当前 agent 在把原始材料蒸馏成 `skill_spec.json` 之前、之中、之后，必须检查哪些内容，才能避免低质量 skill 被 build 进系统。

这份 checklist 应在每次正式生成 child skill 前使用。

# 二、使用时机

这份清单适用于以下场景：

- 用户希望把文章、书籍、教程、技术文档、笔记或转录材料蒸馏成 child skill
- 当前 agent 准备生成 `skill_spec.json`
- 当前 agent 准备进入 review gate

不适用场景：

- 单纯写读书笔记
- 只做普通摘要、不进入 skill build
- 只做项目 memory 记录而不产出 child skill

# 三、蒸馏前检查

## 1. 是否已经获得足够完整的来源材料

检查项：

- 是否有明确的原始内容或文件路径？
- 是否能判断材料边界，而不是只拿到零散残片？
- 是否知道作者、来源类型、上下文？

如果答案是否定的，应先补 source context，而不是直接蒸馏。

## 2. 是否已经判定材料类型

检查项：

- 这份内容更接近 `article`、`book`、`tutorial`、`reference`、`notes` 还是 `transcript`？

如果还未分类，不得继续进入正式 `skill_spec.json` 生成。

## 3. 是否已经判定目标产物类型

检查项：

- 这份材料更适合沉淀成：
  - 原则型 skill
  - 教练型 skill
  - 操作型 skill
  - 参考型 skill
  - memory / guardrail

如果不能判断目标产物类型，说明还不具备 build 前提。

# 四、蒸馏中检查

## 1. 是否完成 source map

至少应明确：

- 内容概览
- 主题分块
- 高价值段落
- 重复点
- 噪音 / 可忽略部分

如果没有 source map，后续很容易直接把原文情绪、修辞或重复内容误提炼成规则。

## 2. 是否提取了四类原子单元

每次蒸馏至少要尝试提取：

- `Concepts`
- `Procedures`
- `Rules`
- `Constraints`

检查标准：

- 至少有 1 个核心概念
- 至少能说明有没有操作步骤
- 至少能说明有哪些判断规则
- 至少能说明有哪些边界或限制

如果某类原子单元完全提不出来，应显式写明“该材料不包含该类结构”，而不是默默忽略。

## 3. 是否区分了“通用规则”和“具体例子”

检查项：

- 哪些内容是通用原则？
- 哪些只是文章中的例子、故事或个案？

如果不能区分，生成的 skill 会过拟合某个例子。

## 4. 是否提炼了不适用场景和误用方式

检查项：

- 什么时候不该用这份 skill？
- 如果用户误用，最可能错在哪里？

缺少这一步时，skill 很容易“看起来合理，但一用就过度泛化”。

# 五、`skill_spec.json` 完整性检查

在进入 review gate 前，至少检查以下字段是否明确：

## 1. `source_meta`

- `source_id`
- `source_type`
- `title`

## 2. `distillation`

- `core_thesis`
- `key_concepts`
- `applicable_scenarios`
- `boundaries`
- `common_misuses`

## 3. `examples`

- 是否至少有 1 个例子？
- 例子是否真的帮助理解或迁移，而不是只重复原文表述？

## 4. `skill_design`

- `skill_id`
- `display_name`
- `content_type`
- `one_sentence_description`
- `trigger_phrases`

## 5. `mode_evaluation`

- `supported_modes`
- `mode_reasoning`
- `execution_level`

## 6. `memory_design`

- `memory_enabled`
- `store`
- `avoid`
- `summary_policy`

## 7. `artifact_plan`

- article package 是否明确
- child skill package 是否明确
- memory package 是否明确
- registry update 是否明确

# 六、execute 判定检查

当材料可能支持 `execute` 时，必须额外检查：

## 1. 是否真的存在重复、稳定、可验证的流程

如果只是原则、建议、经验法则，而不是标准步骤，就不应启用 execute。

## 2. 是否存在明确输入与输出

如果 agent 无法判断输入条件和完成标准，就不应启用 execute。

## 3. 是否存在高风险动作

如果流程包含：

- 删除
- 远程部署
- 生产环境修改
- 高风险外部操作

则默认只能走 `plan_only` 或 `guided_execute`，不能直接 `safe_execute`。

## 4. 是否已经写明 approval-required actions

如果支持 execute，但没有写明哪些动作必须先征求用户确认，则说明 spec 尚不完整。

# 七、review gate 前检查

当前 agent 在向用户展示 spec 前，应确保下面这些内容可读、可判断：

- `display_name`
- `skill_id`
- `content_type`
- `supported_modes`
- `execution_level`
- `core_thesis`

并且要能用简洁的话解释：

- 为什么这样命名
- 为什么选这些 mode
- 为什么 execute 开或不开

# 八、build 后最小复查

虽然 build 后不属于纯蒸馏阶段，但建议在 checklist 中保留最小闭环要求：

- 生成的 `SKILL.md` 是否忠实表达 `skill_spec.json`
- `meta.json` 是否与 spec 一致
- `registry.json` 是否新增了正确 entry
- `skill_summary.md` 是否正确刷新

# 九、失败信号

如果出现以下情况，应停止 build，回到蒸馏阶段重做：

- 无法判断材料类型
- 无法判断目标产物类型
- 无法提取四类原子单元
- `core_thesis` 仍然模糊
- `supported_modes` 只是拍脑袋选的
- execute 判定没有依据
- trigger phrases 过于抽象，不像真实用户会说的话

# 十、结论

这份 checklist 的核心意义在于：

- 防止 `evo_skills` 退化成“随手总结 + 直接 build”
- 强制当前 agent 在 build 前完成必要的结构化判断
- 把蒸馏质量控制前置，而不是把问题留给后续脚本或运行时
