# 一、文档目的

本文档定义 `evo_skills` 在真实对话中执行蒸馏任务时的 **interactive distill session protocol**。

它解决的问题是：

- 当用户说“把这篇文章做成一个 skill”时，当前 agent 应该先做什么、后做什么？
- 在什么节点必须停下来问用户？
- 在什么节点可以自动继续？
- source map、review gate、build、trial 这些环节在对话里如何衔接？

这份协议的作用不是替代已有文档，而是把已有规则串成一个 **可实际执行的会话流程**。

# 二、适用范围

适用于：

- 用户要求从文章、书籍、教程、技术文档、笔记、转录中蒸馏 child skill
- 当前 agent 要从原始内容进入 `skill_spec.json`
- 当前 agent 要继续经过 review gate、build 与 trial

不适用于：

- 普通问答
- 不进入 skill build 的临时分析
- 只记录项目 memory 而不生成 child skill

# 三、会话总流程

一个完整的 interactive distill session 建议按以下顺序执行：

1. 接收来源材料
2. 判定材料类型
3. 判定目标产物类型
4. 产出 source map
5. 抽取四类原子单元
6. 起草 `skill_spec.json`
7. 执行蒸馏 checklist
8. 进入 review gate
9. 调用 builder
10. 执行 post-build trial
11. 根据结果决定是否正式纳入运行态

这个顺序不应随意跳步。

# 四、每一阶段的对话协议

## 阶段 1：接收来源材料

目标：

- 确认用户给了什么材料
- 判断材料边界是否足够清晰

当前 agent 的动作：

- 读取文件或文本
- 明确来源类型候选
- 如有缺口，先补 source context

输出要求：

- 简洁说明已接收到什么材料
- 如果材料不完整，提出具体缺口

何时暂停：

- 材料边界不清
- 只拿到局部残片，无法判断整体

## 阶段 2：判定材料类型

应使用：

- `docs/source_type_decision_rule.md`

目标：

- 明确来源材料属于哪一类

输出要求：

- 给出材料类型判断
- 给出简短理由

何时暂停：

- 如果材料在两个类型之间摇摆严重，且这会影响后续策略，应先向用户解释再继续

## 阶段 3：判定目标产物类型

目标：

- 明确这份材料是更适合成为原则型、教练型、操作型、参考型 skill，还是 memory / guardrail

输出要求：

- 给出目标产物判断
- 解释为什么

何时暂停：

- 如果判断结果更适合 memory / guardrail，而不是 child skill，应向用户说明并请用户确认是否仍要继续 skill 化

## 阶段 4：产出 source map

应使用：

- `docs/source_map_template.md`
- `templates/source-map.template.md`

目标：

- 对原始内容做第一次结构化整理

输出要求：

- 内容概览
- 主题分块
- 高价值片段
- 重复点
- 噪音 / 可忽略部分
- 初步蒸馏方向判断

何时暂停：

- 如果 source map 还无法清楚识别高价值内容与噪音，不应继续进入 spec 阶段

## 阶段 5：抽取四类原子单元

目标：

- 提取：
  - Concepts
  - Procedures
  - Rules
  - Constraints

输出要求：

- 每类尽量提炼出稳定内容
- 不存在的类型也要显式说明

何时暂停：

- 如果四类原子单元大面积提不出来，说明材料还不适合 build 正式 skill

## 阶段 6：起草 `skill_spec.json`

应使用：

- `docs/skill_spec_schema.md`
- `templates/skill-spec.template.json`

目标：

- 把前面的结构化结果转成正式中间产物

输出要求：

- spec 草案完整
- mode 判定清楚
- execute 判定有依据
- tags 初步合理

## 阶段 7：执行蒸馏 checklist

应使用：

- `docs/agent_distillation_checklist.md`

目标：

- 在进入 review gate 前先自查

输出要求：

- 确认 checklist 是否通过
- 若未通过，应说明缺口在哪

## 阶段 8：进入 review gate

应使用：

- `docs/review_gate_template.md`
- `templates/review-gate.template.md`

目标：

- 让用户确认关键设计字段

最低确认字段：

- `display_name`
- `skill_id`
- `content_type`
- `supported_modes`
- `execution_level`
- `core_thesis`

何时暂停：

- 用户未明确通过 review gate
- 用户提出修改意见

## 阶段 9：调用 builder

应使用：

- `scripts/build/build_child_skill.py`

目标：

- 把批准后的 `skill_spec.json` 落盘成正式 child skill 结构

输出要求：

- article package
- child skill package
- memory scaffold
- registry 更新
- summary 更新

## 阶段 10：执行 post-build trial

应使用：

- `docs/post_build_trial_rule.md`
- `docs/trial_report_template.md`
- `templates/trial-report.template.md`

目标：

- 给新 skill 一个最小现实检验

最低要求：

- 至少 1 个正例
- execute 候选或高风险 skill，尽量至少 1 个反例

## 阶段 11：决定去向

如果 trial 通过：

- 该 skill 可以作为正式 child skill 使用

如果 trial 失败：

- 不应直接进入正式运行态
- 应回退到 trigger / distillation / mode / execute / source map 中的问题层修正

# 五、当前 agent 在会话中的默认行为

## 1. 默认可以自动继续的部分

在没有明显风险和歧义时，当前 agent 可以自动继续：

- 材料类型判断
- source map 起草
- 原子单元提取
- spec 草案生成
- checklist 自查

## 2. 默认必须停下来确认的部分

以下节点默认应停下来：

- 目标产物类型明显有歧义时
- execute 风险判断存在不确定性时
- review gate
- memory / guardrail 与正式 skill 边界不清时

## 3. 默认不应自动越过的节点

- 不应绕过 review gate 直接 build
- 不应绕过 trial 直接宣布完成

# 六、协议与现有文档的关系

本协议依赖以下文档：

- `docs/source_type_decision_rule.md`
- `docs/agent_distillation_checklist.md`
- `docs/source_map_template.md`
- `docs/review_gate_template.md`
- `docs/skill_spec_schema.md`
- `docs/post_build_trial_rule.md`
- `docs/trial_report_template.md`

这意味着它是一个 **总协议文档**，而不是替代这些文档的内容。

# 七、结论

interactive distill session protocol 的核心价值在于：

- 把 `evo_skills` 的蒸馏过程变成一套可重复执行的会话流程
- 明确什么时候可以自动继续，什么时候必须停下来让用户确认
- 把 source map、spec、review、build、trial 串成一条真正可运行的链路
