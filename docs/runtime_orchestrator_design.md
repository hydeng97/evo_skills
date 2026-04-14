# 一、文档目的

本文档定义 `evo_skills` 的 **runtime orchestrator** 设计。

在当前系统中，已经存在：

- child skill registry
- dynamic tags
- runtime routing 规则
- memory runtime 规则
- child skill `memory_runtime` 元数据
- memory runtime 脚本

但这些能力仍然主要分散在文档、模板和独立脚本中。缺少一个统一调度层去把它们真正串成一次运行流程。

runtime orchestrator 的目标，就是解决这个问题。

# 二、核心定义

runtime orchestrator 可以理解为：

> 把 routing、mode 选择、memory 读取、child skill 调用前准备、session 写回、压缩建议等步骤组织成统一运行流程的调度层。

它不是新的 child skill，也不是新的 LLM；它是 `evo_skills` 的运行时控制器。

# 三、为什么需要 runtime orchestrator

当前 `evo_skills` 已经具备较完整的设计闭环，但仍缺少一个统一调度入口。

具体表现为：

- routing 有规则，但主要停留在文档层
- memory runtime 有最小可运行脚本，但主要靠手工串接
- child skill invocation 缺少统一决策结果和自动衔接

因此，runtime orchestrator 的作用是把：

- 规则
- 元数据
- 脚本
- child skill 本体

真正连接成运行时链路。

# 四、设计目标

第一版 runtime orchestrator 的目标不是“全自动代替所有流程”，而是：

1. **可解释**：先输出结构化决策结果。
2. **可渐进自动化**：在低风险场景自动做后续动作。
3. **低风险**：不自动放大 execute 权限。
4. **可扩展**：未来可继续接 routing tooling 和 memory automation。

# 五、采用方案

本设计采用 **混合型 orchestrator（方案 C）**。

即：

- 默认先产出结构化 orchestration result
- 在低风险且条件充分时，自动执行部分后续动作

而不是：

- 完全只做建议（太弱）
- 完全黑箱自动执行（太激进）

# 六、职责边界

第一版 runtime orchestrator 负责：

## 1. 判断是否进入 child skill routing

不是所有用户请求都应该走 child skill。

## 2. 选择最合适的 child skill

依据：

- 用户意图
- tags
- registry
- `content_type`
- `supported_modes`

## 3. 选择 mode

在 `teach` / `coach` / `reflect` / `execute` 中选择最合适模式。

## 4. 规划 memory 动作

依据 child skill `meta.json` 中的 `memory_runtime`：

- 是否需要读取 memory
- 读哪些层
- 是否应写 session summary
- 是否建议或触发 compress

## 5. 输出结构化 orchestration result

输出应可读、可审计、可复核。

## 6. 在低风险条件下自动执行部分动作

例如：

- memory context 读取
- session summary 写入
- 简单压缩建议

# 七、第一版不负责的事情

第一版 orchestrator 不应承担：

## 1. 不自动越权执行高风险 execute

即使 skill 支持 `execute`，也仍然受原有风险边界与确认要求约束。

## 2. 不替代 child skill 本体推理

orchestrator 负责调度，不负责代替 child skill 的具体内容输出。

## 3. 不做复杂多 skill 混合编排

第一版优先只选一个主 skill，最多一个备选。

## 4. 不做复杂智能压缩系统

第一版只支持最小 memory runtime 动作，不做重度自动总结系统。

# 八、输入设计

建议第一版统一输入包含：

```json
{
  "user_request": "...",
  "user_id": "...",
  "registry": "...",
  "optional_context": {
    "preferred_mode": null,
    "allow_auto_memory_write": true,
    "allow_auto_compress": false
  }
}
```

实际来源包括：

- 当前用户请求
- `skills/registry.json`
- child skill `meta.json`
- 用户 memory 路径

# 九、输出设计

建议第一版输出统一的 `orchestration_result`，至少包含：

```json
{
  "should_route": true,
  "reason": "...",
  "selected_skill_id": "...",
  "selected_mode": "coach",
  "candidate_tags": ["psychology", "psychology.decision-making"],
  "memory_plan": {
    "should_read": true,
    "read_layers": ["profile", "progress"],
    "should_write_session": true,
    "should_compress": false
  },
  "execution_plan": {
    "auto_actions": [
      "read_memory_context",
      "write_session_summary"
    ],
    "manual_actions": [
      "invoke_child_skill_response_generation"
    ]
  }
}
```

这个输出的意义在于：

- 当前 agent 可解释自己的选择
- 用户可审查
- 后续脚本可消费

# 十、内部步骤设计

为了保持边界清晰，runtime orchestrator 建议拆成以下步骤：

## 1. Request Classifier

回答：

- 当前请求要不要进入 child skill routing？
- 当前请求更像 `teach` / `coach` / `reflect` / `execute`？

## 2. Skill Selector

回答：

- 哪些 tags 最相关？
- 哪个 skill 是最佳候选？
- 是否需要标签层渐进式披露？

## 3. Memory Planner

回答：

- 这个 skill 当前 mode 要读哪些 memory？
- 是否应该写 session summary？
- 是否建议 compress？

## 4. Result Builder

把以上结果组合成结构化 `orchestration_result`。

## 5. Optional Action Runner

在低风险条件下自动执行：

- read memory context
- write session summary
- 可选 compress

# 十一、自动执行边界

第一版建议默认自动执行：

## 可以自动执行

- routing 决策
- memory read
- session summary 写入

## 不建议默认自动执行

- 高风险 execute
- 多 skill 混合编排
- 重度 memory 压缩

compression 建议默认先作为：

- 建议动作
- 或在非常明确的低风险场景才自动执行

# 十二、与现有文档和脚本的关系

runtime orchestrator 不是替代现有规则，而是整合它们。

它应建立在这些现有文档和组件之上：

- `docs/runtime_routing_rule.md`
- `docs/memory_runtime_rule.md`
- child skill `meta.json`
- `scripts/memory/init_user_memory.py`
- `scripts/memory/read_memory_context.py`
- `scripts/memory/write_session_summary.py`
- `scripts/memory/compress_memory.py`

# 十三、第一版实现建议

建议下一步实现为：

- 一个设计文档
- 一个实现计划
- 一个最小入口脚本，例如：
  - `scripts/runtime/orchestrate_runtime.py`

这个脚本第一版可以只做到：

1. 读取 registry
2. 选择 skill + mode
3. 读取 memory context
4. 输出 orchestration result
5. 可选写 session summary

# 十四、结论

runtime orchestrator 的核心意义，不是增加一个新概念，而是把 `evo_skills` 已经存在的：

- routing 规则
- memory runtime
- child skill metadata
- child skill 本体

真正组织成一个统一运行入口。

在当前系统阶段，采用 **混合型 orchestrator（方案 C）** 是最稳妥也最符合现状的路径。
