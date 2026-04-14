# 一、文档目的

本文档定义 `evo_skills` 在 build 前给用户展示的 **review gate 模板**。

它的目标是把“用户确认关键字段”这件事标准化，避免当前 agent 每次自由发挥，导致：

- 有时确认了命名，却没确认 mode
- 有时确认了 thesis，却忘了 execute
- 有时直接 build，没有正式 review gate

这份模板应在每次正式 build child skill 前使用。

# 二、最小 review gate 要确认什么

在进入 build 前，至少必须让用户确认以下字段：

- `display_name`
- `skill_id`
- `content_type`
- `supported_modes`
- `execution_level`
- `core_thesis`

这 6 项是最低门槛，不应跳过。

# 三、推荐展示模板

当前 agent 在展示 review gate 时，建议用下面这个结构：

## 1. 来源摘要

- 来源类型：`<source_type>`
- 来源标题：`<title>`
- 来源标识：`<source_id>`

## 2. 核心提炼

- 核心主张：`<core_thesis>`
- 核心概念：`<key_concepts summary>`
- 适用场景：`<applicable_scenarios summary>`
- 不适用场景：`<boundaries summary>`

## 3. child skill 设计

- `display_name`: `<display_name>`
- `skill_id`: `<skill_id>`
- `content_type`: `<content_type>`
- 触发语示例：`<trigger_phrases summary>`

## 4. mode 判定

- `supported_modes`: `<supported_modes>`
- `execution_level`: `<execution_level>`
- execute 判定理由：`<execute reasoning>`

## 5. memory 设计摘要

- 是否启用 memory：`<memory_enabled>`
- 重点记录什么：`<memory store summary>`
- 明确不记录什么：`<memory avoid summary>`

## 6. 确认问题

最后明确问用户：

> 这版 spec 是否可以进入 build？如果要改，请优先指出：命名、mode、execute 判定或核心主张是否需要调整。

# 四、推荐对话模板

可以直接参考下面的表达方式：

```text
我已经完成这份材料的第一版蒸馏，准备进入 build 之前，先请你确认 6 个关键字段：

1. display_name: <display_name>
2. skill_id: <skill_id>
3. content_type: <content_type>
4. supported_modes: <supported_modes>
5. execution_level: <execution_level>
6. core_thesis: <core_thesis>

补充说明：
- 这份材料被我判断为 <source_type>
- 我建议它主要做成 <target product type>
- execute 之所以设为 <execution_level>，是因为 <reason>

如果你认可，我再继续 build；如果不认可，我会先改 spec。
```

# 五、什么情况下不能通过 review gate

只要出现以下任一情况，就不应继续 build：

## 1. 用户明确表示命名不合适

例如：

- `display_name` 过抽象
- `skill_id` 不稳定或不符合命名规范

## 2. 用户不认可 content_type

例如：

- 用户认为它不是教练型，而是参考型
- 用户认为它不该做正式 skill，而应做 memory

## 3. mode 判定存在重大疑问

例如：

- 用户认为不该开 execute
- 用户认为缺了某个 mode

## 4. `core_thesis` 仍然模糊

如果当前 agent 还不能用简洁、准确的话解释“这份材料真正想帮助解决什么问题”，那说明蒸馏尚未完成。

# 六、review gate 后的动作规则

## 1. 用户通过

如果用户明确同意，则进入 build。

## 2. 用户要求修改

如果用户提出修改意见，则必须先修正 `skill_spec.json`，再重新进入 review gate。

## 3. 用户没有明确表态

如果用户没有明确确认，而只是继续追问内容细节，应优先视为还在 review 阶段，不应默认自动 build。

# 七、与后续实现的关系

这份模板后续可以演化为：

- 一个正式 review checklist
- 一个固定展示函数 / 渲染器
- 一个命令式 review gate 输出格式

但在当前阶段，它首先是一个人工与 agent 协作的统一模板。

# 八、结论

review gate 的核心意义在于：

- 把 build 前的用户确认标准化
- 防止当前 agent 在未经确认时直接落盘
- 把高风险判断（尤其是 execute）放在 build 之前解决
