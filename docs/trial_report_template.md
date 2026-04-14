# 一、文档目的

本文档提供 `evo_skills` 在 build 完成后进行最小试跑时使用的 **trial report 模板**。

它的目标是让试跑结果可读、可复查、可回退，而不是停留在“感觉这个 skill 可以用”。

# 二、推荐模板

```md
# Trial Report

## 1. Skill 基本信息

- display_name: <display_name>
- skill_id: <skill_id>
- content_type: <content_type>
- supported_modes: <supported_modes>
- execution_level: <execution_level>

## 2. Trial 类型

- trial_type: <positive / negative>
- trial_goal: <本次试跑要验证什么>

## 3. Trial 输入

<试跑输入>

## 4. Expected Behavior

<预期行为>

## 5. Observed Behavior

<实际行为>

## 6. Result

- PASS / FAIL

## 7. If FAIL, likely issue layer

- trigger
- distillation
- mode
- execute
- rendering
- memory

## 8. Follow-up Action

- 无需修改 / 回到 spec / 回到 mode 判定 / 回到 execute 判定 / 回到 source map
```

# 三、使用规则

## 1. 每个新 skill 至少应有一个正例报告

如果 skill 已 build，但没有至少一份正例 trial report，不应视为完成。

## 2. execute 候选 skill 应尽量补一个反例报告

这样才能检查是否存在过度执行风险。

## 3. FAIL 时必须标明故障层

不能只写“失败了”，而要尽量定位是：

- 触发问题
- 蒸馏问题
- mode 问题
- execute 问题
- 渲染问题
- memory 问题

# 四、与回退规则的关系

trial report 不只是记录结果，也用于指导回退。

例如：

- trigger 问题 -> 回到 `skill_design.trigger_phrases`
- execute 问题 -> 回到 `mode_evaluation`
- distillation 问题 -> 回到 source map 和四类原子单元提取

# 五、结论

trial report 的核心意义是：把“试跑过”变成可复查、可修正、可积累的质量证据。
