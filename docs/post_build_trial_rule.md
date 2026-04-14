# 一、文档目的

本文档用于定义 `evo_skills` 在 child skill build 完成后的 **最小试跑规则**。

其目标是避免以下问题：

- skill build 完就直接进入正式运行态
- registry 已更新，但 skill 实际一用就误触发或边界不清
- execute 已开启，但没有真实试跑过

因此，post-build trial 是 build 之后、正式接入运行态之前的最后一道质量门。

# 二、为什么必须做 post-build trial

build 成功只能说明：

- 文件写出来了
- registry 更新了
- summary 刷新了

但并不能说明：

- 这个 skill 真能用
- 这个 skill 不会误导 agent
- execute 判定真的合适

所以，每个新生成的 child skill 都至少应有一个最小试跑。

# 三、试跑目标

post-build trial 至少要验证以下问题：

## 1. 触发是否合理

- 这个 skill 在目标场景下是否会被合理触发？

## 2. 输出是否符合定位

- teach 型 skill 是否真的在解释，而不是乱执行？
- coach 型 skill 是否真的在做情境分析，而不是只复述原文？
- reference 型 skill 是否清楚边界，而不是硬给步骤？

## 3. execute 是否过宽或过窄

- 如果启用了 execute，当前 skill 是否真的具备稳定步骤？
- 如果没启 execute，是否其实遗漏了可操作流程？

## 4. 边界是否清晰

- 是否明确了不适用场景？
- 是否会在高风险场景中给出过于自信的指令？

# 四、最小试跑规则

## 1. 每个新 skill 至少跑 1 个正例

正例要求：

- 与该 skill 的目标场景高度匹配
- 能清楚检验 skill 的主要用途

例如：

- 对教练型 skill：给一个真实但简短的用户场景
- 对操作型 skill：给一个最小流程任务
- 对参考型 skill：给一个边界明确的查询或判断任务

## 2. 高风险或 execute 型 skill 至少跑 1 个反例

反例要求：

- 明显不适合这个 skill 的场景
- 或可能诱发误用的场景

目的：

- 检查 skill 会不会过度适用
- 检查 execute 会不会被错误开启

## 3. 每次试跑必须记录结论

最少记录：

- 试跑输入是什么
- 预期行为是什么
- 实际表现如何
- 是否通过
- 如果不通过，问题出在：
  - 触发
  - spec
  - mode 判定
  - execute 判定
  - 文本表达

# 五、按 skill 类型的最小试跑要求

## 1. 原则型 / 教练型 skill

至少验证：

- 是否能给出与原始思想一致的分析
- 是否能把概念迁移到用户场景
- 是否不会直接越界给出机械执行

## 2. 操作型 skill

至少验证：

- 步骤顺序是否完整
- 前置条件是否清楚
- 完成标准是否明确
- 出错时是否能停下来或给出排错建议

## 3. 参考型 skill

至少验证：

- 是否能准确引用能力边界
- 是否不会把参考说明误改成绝对步骤

## 4. memory / guardrail 型产物

至少验证：

- 是否准确反映约束
- 是否没有把临时讨论误写成长期规则

# 六、试跑失败后的回退规则

## 1. 触发不对

回退到：

- `skill_design.trigger_phrases`
- `content_type`

## 2. 输出方向不对

回退到：

- `mode_evaluation`
- `distillation.core_thesis`

## 3. execute 判定不对

回退到：

- `mode_evaluation.execution_level`
- `execution_scope`
- `approval_required_actions`

## 4. 内容本身提炼不对

回退到：

- source map
- 四类原子单元提取
- `distillation`

# 七、试跑报告建议格式

推荐当前 agent 用下面这种最小格式记录试跑结果：

```text
Trial Input:
<试跑输入>

Expected Behavior:
<预期行为>

Observed Behavior:
<实际行为>

Result:
PASS / FAIL

If FAIL, likely issue layer:
trigger / distillation / mode / execute / rendering
```

# 八、什么情况下可以视为“可进入运行态”

至少满足：

- build 成功
- 至少 1 个正例试跑通过
- 如果是 execute 候选或高风险 skill，至少 1 个反例试跑通过
- 没有明显越界风险

只有满足以上条件，才建议把它作为正式 child skill 使用。

# 九、结论

post-build trial 的核心意义不是追求复杂测试体系，而是给每个新 child skill 一个最小现实检验。

对 `evo_skills` 来说，这一步是防止低质量蒸馏结果直接进入运行态的关键保险。
