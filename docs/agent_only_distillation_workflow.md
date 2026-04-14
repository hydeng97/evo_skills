# 一、工作流定位

`evo_skills` 采用 **agent-only** 的内容提炼工作流。

这意味着：

- 不调用任何外部 LLM API。
- 不依赖额外的独立模型服务完成提炼。
- 由当前 agent 会话直接阅读用户提供的文章、书籍章节、笔记或教程内容。
- 由当前 agent 在交互中产出 `skill_spec.json`。
- 由本地脚本负责把批准后的 spec 落地成 child skill。

因此，`evo_skills` 的标准工作流是一个**交互式 agent + 明确阶段产物**流程。

# 二、标准流程

## 1. 用户提供来源内容

用户可以提供：

- 文件路径
- 粘贴的文章内容
- markdown 文档
- 书籍章节整理稿
- 教程说明文本

当前 agent 负责读取并理解这些内容。

## 2. 当前 agent 生成 `skill_spec.json`

当前 agent 在会话中完成以下工作：

- 提炼思想精髓
- 提炼或补充案例
- 设计 child skill 定位
- 判定 `teach`、`coach`、`reflect`、`execute`
- 判定 `execution_level`
- 设计长期记忆策略

输出结果是结构化的 `skill_spec.json`。

## 3. 用户审查关键字段

在正式 build 之前，至少应审查以下字段：

- `display_name`
- `skill_id`
- `content_type`
- `supported_modes`
- `execution_level`
- `core_thesis`

如果这些字段存在明显偏差，应先修正 spec，再进入 build。

## 4. 本地 builder 执行落地

在 spec 获得确认后，由当前 agent 调用本地脚本：

- `scripts/build/build_child_skill.py`

该脚本负责：

- 写入 article package
- 写入 child skill package
- 创建 memory scaffold
- 更新 `skills/registry.json`
- 刷新 `skills/skill_summary.md`

## 5. 当前 agent 做构建后复查

构建完成后，当前 agent 仍应复查：

- 生成的 `SKILL.md` 是否准确
- mode 是否符合原意
- `execute` 是否设置过宽
- registry entry 是否完整
- summary 是否正确反映新 skill

# 三、职责分工

## 1. 当前 agent 负责

- 阅读原始内容
- 进行思想提炼
- 进行 child skill 设计
- 与用户确认关键字段
- 调用本地脚本
- 复查生成结果

## 2. 本地脚本负责

- 目录创建
- 文件写入
- registry 更新
- summary 刷新
- memory scaffold 初始化

## 3. 用户负责

- 提供原始内容
- 审核关键 spec 字段
- 决定是否继续 build

# 四、关键规则

## 1. 不允许跳过 spec 阶段

不应直接从原始文章一步跳到最终 child skill 文件。

必须先有 `skill_spec.json`，再进行构建。

## 2. 不允许跳过 review gate

在 build 前至少要让用户确认关键设计字段。

## 3. 不允许把脚本当成提炼器

脚本只负责机械落地，不负责理解原文，不负责做思想判断。

## 4. 不允许使用外部 LLM API 替代当前 agent

整个提炼流程应由当前 agent 会话完成。

# 五、与 build 流程的关系

`build_child_skill.py` 不是提炼器，而是 `skill_spec.json` 的落地器。

推荐关系如下：

1. 当前 agent 读原文
2. 当前 agent 产出 `skill_spec.json`
3. 用户确认关键字段
4. `build_child_skill.py` 负责生成 child skill 结构

也就是说：

- **当前 agent 是大脑**
- **本地脚本是手和工具**

# 六、推荐后续扩展方向

当该工作流稳定后，后续应继续补齐：

- 更严格的 spec 校验
- 更完整的 child skill 渲染逻辑
- 更稳定的 memory 写回策略
- 运行时 routing 规则
- child skill 的长期维护与演化流程
