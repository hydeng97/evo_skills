# 一、文档目的

本文档定义 `evo_skills` 在 **child skill 已经存在之后**，如何在运行时结合动态标签、mode 和 memory 选择合适的 skill。

它解决的问题是：

- 用户提出一个问题时，应该调用哪个 child skill？
- 如果多个 skill 都相关，应该怎么排序？
- 动态标签应该如何参与候选集收缩？
- 是用 `teach`、`coach`、`reflect` 还是 `execute`？
- 什么时候根本不该调用已有 skill，而应该重新蒸馏或重新设计？

# 二、routing 的基本原则

## 1. 先判断是否需要 routing

并不是所有用户请求都应该进入 child skill routing。

下列情况通常应先考虑 routing：

- 用户在问一个明确主题问题
- 用户希望基于某种书、文章、方法论得到解释或建议
- 用户的场景与已有 skill 的主题高度相关
- 用户希望做复盘、决策、教练式分析或按流程执行

下列情况通常不应直接走已有 skill：

- 用户只是提供新材料准备蒸馏
- 用户的问题与现有 skill 主题无明显关联
- 用户在要求修改 `evo_skills` 本身

## 2. 先用 tags 收缩候选集，再看主题和 mode

runtime routing 不能只看关键词命中，也不能只看 skill 名称。

在已有 dynamic tags 的前提下，默认应先用 tags 做一轮后台收缩，再进入更细的判断。

应按以下顺序判断：

1. 用户问题是否能映射到一组候选 tags
2. 这些 tags 下有哪些相关 skill
3. 该 skill 的 `supported_modes` 是否包含当前所需模式
4. 如果支持 execute，当前场景是否适合 execute
5. 是否存在更高优先级的用户长期 memory 需要优先使用

## 3. tags 是 routing 的前置筛选层，不是唯一决策层

dynamic tags 的作用是：

- 先缩小 skill 搜索空间
- 在候选很多时支持渐进式披露

但 tags 不应单独决定最终调用。最终仍要结合：

- 用户意图
- mode 兼容性
- execute 风险
- memory 关联度

# 三、推荐的 routing 判断流程

## 第 1 步：识别用户意图类型

至少应先判断用户当前请求更接近哪类意图：

- `teach`：想理解概念、思想、框架
- `coach`：想分析自己的场景、获得建议
- `reflect`：想做复盘、成长回顾、长期变化总结
- `execute`：想按某个已知流程让 agent 动手执行

如果意图本身不清晰，默认优先按 `teach` 或 `coach` 理解，而不是直接进入 `execute`。

## 第 2 步：优先识别候选 tags

在筛 skill 之前，应先尝试从用户问题中识别更合适的候选 tags。

识别来源可以包括：

- 用户明确提到的领域或主题
- skill 现有 `tags`
- 用户长期 memory 中的稳定主题偏好

如果问题可以明显映射到一个或几个 tags，则应先按 tag 收缩候选集。

如果 tags 无法明显判断，则允许退回到更粗粒度的主题匹配。

## 第 3 步：从 tags 过滤后的集合中筛选 skill

筛选时至少参考：

- `display_name`
- `skill_id`
- `source_id`
- `content_type`
- `tags`
- `supported_modes`

如果没有明显匹配项：

- 不应勉强调用无关 skill
- 应考虑是否需要创建新 child skill 或退回普通对话分析

## 第 4 步：检查 mode 兼容性

对于候选 skill，继续检查：

- 用户当前意图是否在其 `supported_modes` 内
- 如果不在，则该 skill 不应作为首选

例如：

- 用户要求“帮我执行这套流程”，但该 skill 不支持 `execute`，则不能强行进入执行模式

## 第 5 步：检查 execute 风险

如果候选 skill 支持 `execute`，必须继续检查：

- 当前任务是否真的符合其 `execution_scope`
- 是否包含需要用户确认的动作
- 当前情境是否高风险或模糊

如有风险，默认降级到：

- `plan_only`
- 或 `coach`

## 第 6 步：决定是否加载 memory

如果用户是长期互动对象，且该 skill 有 memory，则应加载：

- 相关 `profile`
- `progress`
- 最近有效的长期摘要

如果是首次互动或无 memory，则直接按 skill 本体运行。

# 四、当多个 skill 都相关时如何排序

推荐排序因素如下：

## 1. tag 匹配度

优先选择 tags 与当前问题最接近的 skill。

## 2. 主题匹配度

优先选择主题最接近用户问题的 skill。

## 3. mode 匹配度

在主题都接近时，优先选择能自然支持当前意图 mode 的 skill。

## 4. 近期 memory 关联度

如果某个 skill 与用户近期长期互动强相关，可以提高优先级。

## 5. execute 风险等级

在 execute 场景下，如果两个 skill 都能做，优先选择边界更清楚、风险更低的那个。

# 五、渐进式披露规则

## 1. 默认后台静默使用 tags

在大多数情况下，tags 应只在后台用于候选收缩，用户不需要看到它们。

## 2. 候选仍然过多时，再向用户展示标签层

如果后台筛选后仍有较多候选，不应直接给用户完整 skill 列表，而应先展示更高层的 tag 选择。

例如：

- 这更像“心理学 / 决策”还是“经济学 / 风险判断”？

## 3. 在标签层确认后，再展示 skill 层

这样可以实现：

- 第一层：标签
- 第二层：skill

而不是一开始就摊开完整总表。

# 六、mode 选择规则

## 1. teach

适用：

- 用户在理解概念
- 用户想听文章/书的思想精髓
- 用户要求案例与解释

## 2. coach

适用：

- 用户带着自己的真实场景来问
- 用户需要建议、分析、提问引导
- 用户要把思想迁移到现实问题中

## 3. reflect

适用：

- 用户在做复盘
- 用户想看长期变化、成长模式、重复偏差

## 4. execute

适用：

- skill 明确支持 execute
- 当前任务确实符合 skill 的流程边界
- 风险可控，或必要确认已经完成

# 七、什么情况下不应使用已有 child skill

遇到以下情况时，应停止 routing，转而考虑重新蒸馏或普通分析：

- registry 中没有明显相关 skill
- 相关 skill 都不支持当前 mode
- execute 风险过高且无法降级
- 用户问题已经明显超出已有 skill 边界

# 八、结论

runtime routing 的核心不是“命中一个 skill”，而是：

- 先用 tags 缩小候选空间
- 选对 skill
- 选对 mode
- 在必要时带上 memory
- 在不适合时敢于不调用任何已有 skill
