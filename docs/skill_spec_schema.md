# 一、`skill_spec.json` 概述

`skill_spec.json` 是 `evo_skills` 中用于连接“当前 agent 的内容提炼”与“child skill 工程落地”的标准中间格式。

它的职责不是直接替代最终的 `SKILL.md`、`meta.json` 或 `memory_schema.md`，而是先把一次内容提炼的结果稳定地表达出来，让后续脚本和流程能够可靠消费。

这份 schema 解决的核心问题有四个：

1. 统一表达不同来源内容的提炼结果。
2. 统一表达 child skill 的设计决策。
3. 统一表达 mode 判定与 execute 判定。
4. 统一表达长期记忆与落地文件计划。

因此，`skill_spec.json` 应被视为 child skill 生成流程中的**正式中间产物**。

# 二、设计原则

`skill_spec.json` 的设计遵循以下原则：

1. **当前 agent 负责理解与提炼**。思想精髓、案例、适用边界、mode 判定应由当前 agent 会话产出。
2. **脚本负责机械落地**。目录创建、文件写入、registry 更新与 summary 刷新由脚本承担。
3. **先有 spec，再有文件**。不建议让 agent 直接一步到位生成所有最终文件，而应先产出结构化 spec。
4. **可迁移**。schema 不能过度依赖某个单一工作区结构，字段设计应支持迁移与导出。
5. **可演进**。通过 `spec_version` 支持未来扩展。

# 三、顶层结构

`skill_spec.json` 顶层固定包含以下字段：

```json
{
  "spec_version": "1.0",
  "source_meta": {},
  "distillation": {},
  "examples": [],
  "skill_design": {},
  "mode_evaluation": {},
  "memory_design": {},
  "artifact_plan": {}
}
```

字段含义如下：

- `spec_version`：schema 版本号。
- `source_meta`：来源材料的元信息。
- `distillation`：对内容本身的核心提炼。
- `examples`：用于 teach 与 coach 的示例集合。
- `skill_design`：该内容将被设计成什么 child skill。
- `mode_evaluation`：支持哪些 mode，以及 execute 是否开启。
- `memory_design`：长期记忆的设计规则。
- `artifact_plan`：后续落地成目录与文件的计划。

# 四、`spec_version`

该字段用于声明当前 spec 使用的 schema 版本。

示例：

```json
{
  "spec_version": "1.0"
}
```

建议规则：

- `1.0`：初始稳定版。
- `1.x`：小幅增强，不破坏原有结构。
- `2.0`：发生结构级不兼容变化。

# 五、`source_meta`

该对象描述来源材料的身份信息。

建议字段：

```json
{
  "source_id": "article_clear-thinking_2026_04",
  "source_type": "article",
  "title": "Clear Thinking",
  "author": "Example Author",
  "language": "zh",
  "source_path": "articles/article_clear-thinking_2026_04/raw.md",
  "topic_tags": [
    "thinking",
    "decision-making",
    "cognition"
  ],
  "rights_note": "Derived summary for skill generation"
}
```

字段说明：

- `source_id`：来源唯一标识，必填。
- `source_type`：来源类型，建议值包括 `article`、`book`、`chapter`、`tutorial`、`note`。
- `title`：来源标题，必填。
- `author`：作者，可选。
- `language`：原始语言。
- `source_path`：原始材料或整理材料路径。
- `topic_tags`：主题标签列表。
- `rights_note`：版权或用途说明。

# 六、`distillation`

该对象承载对内容本身的核心提炼，是 `skill_spec.json` 中最重要的部分之一。

建议结构：

```json
{
  "summary": "一句话总结这份内容的核心主张。",
  "core_thesis": "该内容真正想帮助人解决的问题是什么，以及它给出的核心方法是什么。",
  "key_concepts": [
    {
      "name": "清晰思考",
      "definition": "在行动和判断之前识别偏差与噪声。",
      "importance": "这是全文的中心支点。"
    }
  ],
  "mechanisms": [
    "为什么这种方法有效",
    "它通过什么机制改善判断"
  ],
  "applicable_scenarios": [
    "决策复盘",
    "日常工作判断",
    "长期成长反思"
  ],
  "boundaries": [
    "不适用于必须秒级决策的场景"
  ],
  "common_misuses": [
    "把清晰思考误解成过度犹豫"
  ],
  "related_concepts": [
    {
      "name": "批判性思维",
      "relation": "相近但更偏分析框架"
    }
  ]
}
```

设计要求：

- `core_thesis` 必填。
- `key_concepts` 至少包含一个核心概念。
- `applicable_scenarios`、`boundaries`、`common_misuses` 建议都填写，避免 skill 过于抽象或过度泛化。

# 七、`examples`

该字段是案例数组，用于支撑 `teach` 和 `coach` 模式。

建议结构：

```json
[
  {
    "example_id": "ex_decision_review_01",
    "title": "工作决策复盘案例",
    "scenario": "某用户在没有澄清目标的情况下匆忙做了团队选择。",
    "analysis": "按文章思想来看，问题不在执行力，而在判断前缺少清晰问题定义。",
    "lesson": "先定义决策问题，再比较选项，而不是情绪先行。",
    "tags": ["work", "decision"]
  }
]
```

建议规则：

- 至少提供两个案例。
- 至少一个案例面向日常/成长场景。
- 至少一个案例面向工作/项目场景。

# 八、`skill_design`

该对象用于表达“如何把提炼内容变成 child skill”。

建议结构：

```json
{
  "skill_id": "coach.clear-thinking.decision-review.v1",
  "skill_folder_name": "coach_clear_thinking_decision_review",
  "display_name": "Clear Thinking 决策复盘教练",
  "content_type": "coaching",
  "tags": [
    "psychology",
    "psychology.decision-making",
    "coaching"
  ],
  "one_sentence_description": "基于清晰思考方法帮助用户做决策分析、复盘与偏差修正。",
  "target_user_value": [
    "帮助用户理解文章精髓",
    "帮助用户把思想迁移到现实场景",
    "帮助用户形成长期判断改进"
  ],
  "trigger_phrases": [
    "帮我复盘这个决定",
    "我感觉自己总判断失误",
    "用 clear thinking 分析一下"
  ],
  "tone_style": [
    "clarifying",
    "practical",
    "coach-like"
  ]
}
```

字段说明：

- `skill_id`：逻辑上的唯一 skill 标识，必填。
- `skill_folder_name`：文件系统目录名，建议使用安全、扁平命名。
- `display_name`：人类可读名，必填。
- `content_type`：建议值为 `insight`、`coaching`、`tutorial`、`technical`。
- `tags`：动态标签列表，用于 routing 与渐进式披露。标签不应来自预设固定分类树，而应根据 `docs/dynamic_tagging_rule.md` 动态创建、复用、合并或拆分。
- `one_sentence_description`：一句话定位，必填。
- `trigger_phrases`：用于帮助系统理解触发场景，建议至少两个。
- `tone_style`：对输出风格的软性建议。

# 九、`mode_evaluation`

该对象用于明确 child skill 支持哪些 mode，以及 `execute` 是否被允许。

建议结构：

```json
{
  "supported_modes": ["teach", "coach", "reflect"],
  "mode_reasoning": {
    "teach": "内容具有清晰概念框架和解释价值。",
    "coach": "可迁移到用户真实决策和复盘场景。",
    "reflect": "适合用于长期行为总结与偏差复盘。",
    "execute": "不适合，因为缺乏明确、可验证的操作流程。"
  },
  "execution_level": "none",
  "execution_scope": [],
  "approval_required_actions": []
}
```

允许的 mode：

- `teach`
- `coach`
- `reflect`
- `execute`

允许的 `execution_level`：

- `none`
- `plan_only`
- `guided_execute`
- `safe_execute`

规则要求：

- `supported_modes` 必填。
- `execution_level` 必填。
- 如果不支持 `execute`，`execution_level` 必须为 `none`。
- 如果支持 `execute`，应补充 `execution_scope` 与 `approval_required_actions`。

# 十、`memory_design`

该对象用于定义长期记忆的策略。

建议结构：

```json
{
  "memory_enabled": true,
  "store": {
    "teach": [
      "用户容易混淆的概念",
      "偏好的解释风格"
    ],
    "coach": [
      "用户目标",
      "现实约束",
      "重复出现的卡点"
    ],
    "reflect": [
      "阶段性成长变化",
      "常见行为偏差",
      "策略迭代历史"
    ],
    "execute": [
      "偏好的执行方式",
      "常用安全默认项"
    ]
  },
  "avoid": [
    "密钥",
    "敏感凭证",
    "逐字隐私对话",
    "不必要的大段原始日志"
  ],
  "summary_policy": "session_to_periodic_to_long_term",
  "progress_dimensions": [
    "理解深度",
    "应用频率",
    "稳定行为变化"
  ]
}
```

规则要求：

- `memory_enabled` 必填。
- `avoid` 建议始终填写。
- `summary_policy` 应明确从 session 到长期画像的压缩路径。

# 十一、`artifact_plan`

该对象描述后续要生成哪些目录与文件。

建议结构：

```json
{
  "article_package": {
    "folder": "articles/article_clear-thinking_2026_04",
    "files": [
      "source_meta.json",
      "distilled.md",
      "examples.md",
      "coach_notes.md"
    ]
  },
  "child_skill_package": {
    "folder": "skills/coach_clear_thinking_decision_review",
    "files": [
      "SKILL.md",
      "README.md",
      "meta.json",
      "memory_schema.md"
    ]
  },
  "memory_package": {
    "folder": "memory/coach.clear-thinking.decision-review.v1",
    "subfolders": [
      "shared",
      "users"
    ]
  },
  "registry_updates": {
    "append_registry_entry": true,
    "refresh_summary": true
  }
}
```

该对象的意义在于：

- 指导后续脚本创建目录。
- 指导后续脚本写入哪些文件。
- 指导 registry 是否需要更新。

# 十二、必填字段与可选字段

## 1. 必填字段

以下字段建议作为 schema v1 的最低要求：

- `spec_version`
- `source_meta.source_id`
- `source_meta.source_type`
- `source_meta.title`
- `distillation.core_thesis`
- `distillation.key_concepts`
- `skill_design.skill_id`
- `skill_design.display_name`
- `skill_design.content_type`
- `skill_design.tags`
- `skill_design.one_sentence_description`
- `mode_evaluation.supported_modes`
- `mode_evaluation.execution_level`
- `memory_design.memory_enabled`
- `artifact_plan`

## 2. 推荐必填字段

- `examples`
- `skill_design.trigger_phrases`
- `mode_evaluation.mode_reasoning`
- `memory_design.avoid`
- `memory_design.summary_policy`

## 3. 可选字段

- `source_meta.author`
- `source_meta.rights_note`
- `distillation.related_concepts`
- `skill_design.tone_style`
- `mode_evaluation.execution_scope`
- `mode_evaluation.approval_required_actions`

# 十三、完整示例

下面给出一个压缩但完整的示例：

```json
{
  "spec_version": "1.0",
  "source_meta": {
    "source_id": "article_clear-thinking_2026_04",
    "source_type": "article",
    "title": "Clear Thinking",
    "author": "Example Author",
    "language": "zh",
    "source_path": "articles/article_clear-thinking_2026_04/raw.md",
    "topic_tags": ["thinking", "decision-making"]
  },
  "distillation": {
    "summary": "帮助用户减少判断噪声，提升决策清晰度。",
    "core_thesis": "在行动前先澄清问题和偏差来源，可以显著提高长期决策质量。",
    "key_concepts": [
      {
        "name": "清晰思考",
        "definition": "在行动前识别偏差与误判来源。",
        "importance": "是全文的核心方法。"
      }
    ],
    "mechanisms": [
      "延迟冲动判断",
      "明确判断标准"
    ],
    "applicable_scenarios": [
      "决策复盘",
      "学习规划"
    ],
    "boundaries": [
      "不适合秒级紧急场景"
    ],
    "common_misuses": [
      "把它变成拖延分析"
    ],
    "related_concepts": [
      {
        "name": "批判性思维",
        "relation": "相近但不完全等同"
      }
    ]
  },
  "examples": [
    {
      "example_id": "ex1",
      "title": "工作决策复盘案例",
      "scenario": "用户匆忙决定加入某项目",
      "analysis": "未先定义判断标准",
      "lesson": "先定义问题，再比较选项",
      "tags": ["work", "decision"]
    }
  ],
  "skill_design": {
    "skill_id": "coach.clear-thinking.decision-review.v1",
    "skill_folder_name": "coach_clear_thinking_decision_review",
    "display_name": "Clear Thinking 决策复盘教练",
    "content_type": "coaching",
    "tags": [
      "psychology",
      "psychology.decision-making",
      "coaching"
    ],
    "one_sentence_description": "帮助用户理解并应用清晰思考进行决策复盘。",
    "target_user_value": [
      "理解思想",
      "迁移应用",
      "长期改进"
    ],
    "trigger_phrases": [
      "帮我复盘这个决定",
      "我总是判断失误"
    ],
    "tone_style": ["clarifying", "practical"]
  },
  "mode_evaluation": {
    "supported_modes": ["teach", "coach", "reflect"],
    "mode_reasoning": {
      "teach": "概念框架完整",
      "coach": "适合分析现实场景",
      "reflect": "适合长期复盘",
      "execute": "不适合，缺乏标准操作流程"
    },
    "execution_level": "none",
    "execution_scope": [],
    "approval_required_actions": []
  },
  "memory_design": {
    "memory_enabled": true,
    "store": {
      "teach": ["概念误解", "偏好解释方式"],
      "coach": ["目标", "约束", "卡点"],
      "reflect": ["成长变化", "重复偏差"],
      "execute": []
    },
    "avoid": ["密钥", "逐字隐私对话"],
    "summary_policy": "session_to_periodic_to_long_term",
    "progress_dimensions": ["理解深度", "应用频率"]
  },
  "artifact_plan": {
    "article_package": {
      "folder": "articles/article_clear-thinking_2026_04",
      "files": ["source_meta.json", "distilled.md", "examples.md", "coach_notes.md"]
    },
    "child_skill_package": {
      "folder": "skills/coach_clear_thinking_decision_review",
      "files": ["SKILL.md", "README.md", "meta.json", "memory_schema.md"]
    },
    "memory_package": {
      "folder": "memory/coach.clear-thinking.decision-review.v1",
      "subfolders": ["shared", "users"]
    },
    "registry_updates": {
      "append_registry_entry": true,
      "refresh_summary": true
    }
  }
}
```

# 十四、实现建议

在 `evo_skills` 中，推荐遵循以下工作流：

1. 由当前 agent 根据原始材料生成 `skill_spec.json`。
2. 在 build 前由用户审查关键 spec 字段，尤其是 `display_name`、`skill_id`、`content_type`、`supported_modes`、`execution_level` 和 `core_thesis`。
3. 使用脚本根据批准后的 `skill_spec.json` 生成 child skill 文件、memory 目录和 registry 更新。

该流程的核心原则是：**当前 agent 负责提炼，脚本负责落地；先生成结构化 spec，再生成最终文件。**
