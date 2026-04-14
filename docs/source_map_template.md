# 一、文档目的

本文档提供 `evo_skills` 在正式蒸馏前使用的 **source map 模板**。

它的目标是帮助当前 agent 在读取原始材料后，不直接跳到 `skill_spec.json`，而是先做一层结构化整理，明确：

- 这份材料在讲什么
- 哪些部分最重要
- 哪些部分重复
- 哪些部分可以忽略

这个模板应在正式生成 `skill_spec.json` 前使用。

# 二、推荐模板

```md
# Source Map

## 1. 来源信息

- source_type: <article / book / tutorial / reference / notes / transcript>
- title: <标题>
- source_id: <来源标识>
- author_or_origin: <作者或来源>

## 2. 内容概览

- 这份材料主要在解决什么问题：<一句话>
- 它更偏 explanation / tutorial / reference / record 中的哪一种：<判断>
- 为什么这样判断：<简短理由>

## 3. 主题分块

### Block A
- 主题：<主题名>
- 内容摘要：<简述>
- 重要性：高 / 中 / 低

### Block B
- 主题：<主题名>
- 内容摘要：<简述>
- 重要性：高 / 中 / 低

## 4. 高价值段落 / 片段

- 片段 1：<为什么高价值>
- 片段 2：<为什么高价值>

## 5. 重复点

- 哪些观点、步骤或模式在材料中重复出现：<列表>

## 6. 噪音 / 可忽略部分

- 哪些部分更像修辞、铺垫、冗余案例或低价值重复：<列表>

## 7. 初步蒸馏方向判断

- 候选目标产物：<原则型 / 教练型 / 操作型 / 参考型 / memory>
- execute 候选：是 / 否
- 初步理由：<简述>
```

# 三、使用规则

## 1. source map 不是摘要全文

不要把 source map 写成普通总结。

source map 的重点是：

- 分块
- 识别高价值内容
- 标记重复与噪音
- 为后续蒸馏提供导航

## 2. source map 不要求写得很长

只要结构清晰、能支持下一步提炼即可。

## 3. source map 必须包含“噪音 / 可忽略部分”

这是为了避免后续把冗余内容误写进 skill。

# 四、与后续流程的关系

source map 完成后，当前 agent 才应继续：

1. 提取四类原子单元
2. 起草 `skill_spec.json`
3. 进入 review gate

# 五、结论

source map 的核心意义不是“再写一遍总结”，而是给蒸馏过程做一张工作地图。
