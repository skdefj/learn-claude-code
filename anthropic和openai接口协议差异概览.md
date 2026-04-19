###  核心差异概览

| 特性 | OpenAI (Chat Completions) | Anthropic (Messages API) |
| :--- | :--- | :--- |
| **设计理念** | 灵活、通用，消息列表包含所有指令 | 结构化、安全优先，系统提示词独立 |
| **端点** | `/v1/chat/completions` | `/v1/messages` |
| **系统提示词** | 放在 `messages` 数组中 (`role: system`) | 独立的顶层参数 `system` (字符串) |
| **消息角色** | `system`, `user`, `assistant`, `tool` | `user`, `assistant` (系统提示词独立) |
| **工具调用** | `tools` 参数，模型返回 `tool_calls` | `tools` 参数，模型返回 `content` 块 |
| **推理/思考** | 通过 `reasoning_effort` 或特定模型支持 | 通过 `thinking` 参数启用扩展思考 |

---

###  场景一：基础聊天与多轮对话

#### OpenAI 协议
OpenAI 将对话历史视为一个线性的消息列表。`system` 角色只是列表中的一个特殊消息，通常放在开头。

**请求报文：**
```json
POST /v1/chat/completions
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "system",
      "content": "你是一个乐于助人的助手。"
    },
    {
      "role": "user",
      "content": "你好，我叫小明。"
    },
    {
      "role": "assistant",
      "content": "你好小明，很高兴认识你！"
    },
    {
      "role": "user",
      "content": "我叫什么名字？"
    }
  ]
}
```

**响应报文：**
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "你叫小明。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": { "prompt_tokens": 20, "completion_tokens": 5, "total_tokens": 25 }
}
```

#### Anthropic 协议
Anthropic 严格区分“系统指令”和“对话内容”。`system` 是顶层字段，`messages` 数组中只包含 `user` 和 `assistant` 的交替对话。

**请求报文：**
```json
POST /v1/messages
{
  "model": "claude-3-5-sonnet-20241022",
  "system": "你是一个乐于助人的助手。",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": "你好，我叫小明。"
    },
    {
      "role": "assistant",
      "content": "你好小明，很高兴认识你！"
    },
    {
      "role": "user",
      "content": "我叫什么名字？"
    }
  ]
}
```

**响应报文：**
```json
{
  "id": "msg_01234567890",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "你叫小明。"
    }
  ],
  "model": "claude-3-5-sonnet-20241022",
  "stop_reason": "end_turn",
  "usage": { "input_tokens": 20, "output_tokens": 5 }
}
```

> **关键点：** Anthropic 的 `content` 是一个数组，这为后续支持多模态和工具调用留下了扩展空间，而 OpenAI 早期是直接的字符串，现在也转为支持多种内容块。

---

### ️ 场景二：工具调用

这是两者差异最大的地方。OpenAI 倾向于将工具调用作为消息的一部分，而 Anthropic 将其视为内容块的一种。

#### OpenAI 协议
你需要定义 `tools`，模型会在响应中返回 `tool_calls`。你需要执行代码后，再把结果以 `role: tool` 的形式发回去。

**请求 (定义工具)：**
```json
{
  "model": "gpt-4o",
  "messages": [{"role": "user", "content": "北京天气怎么样？"}],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气",
        "parameters": {
          "type": "object",
          "properties": {
            "city": {"type": "string"}
          },
          "required": ["city"]
        }
      }
    }
  ]
}
```

**响应 (模型决定调用)：**
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_abc123",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"city\": \"北京\"}"
            }
          }
        ]
      }
    }
  ]
}
```

**下一轮请求 (回传结果)：**
```json
{
  "messages": [
    // ... 之前的对话 ...
    {"role": "assistant", "tool_calls": [...]}, 
    {
      "role": "tool",
      "tool_call_id": "call_abc123",
      "content": "晴朗，25度"
    }
  ]
}
```

#### Anthropic 协议
Anthropic 将工具调用视为一种特殊的内容块 (`type: tool_use`)。回传结果时，是作为用户的输入 (`type: tool_result`)。

**请求 (定义工具)：**
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "system": "你是一个助手，可以使用工具。",
  "tools": [
    {
      "name": "get_weather",
      "description": "获取指定城市的天气",
      "input_schema": {
        "type": "object",
        "properties": {
          "city": {"type": "string"}
        },
        "required": ["city"]
      }
    }
  ],
  "max_tokens": 1024,
  "messages": [
    {"role": "user", "content": "北京天气怎么样？"}
  ]
}
```

**响应 (模型决定调用)：**
```json
{
  "content": [
    {
      "type": "tool_use",
      "id": "toolu_01A2B3C4",
      "name": "get_weather",
      "input": {
        "city": "北京"
      }
    }
  ]
}
```

**下一轮请求 (回传结果)：**
```json
{
  "messages": [
    // ... 之前的对话 ...
    {"role": "assistant", "content": [{"type": "tool_use", ...}]},
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01A2B3C4",
          "content": "晴朗，25度"
        }
      ]
    }
  ]
}
```

> **关键点：** Anthropic 的 `tool_result` 是放在 `user` 角色的 `content` 数组里的，这符合其“一切皆内容”的设计哲学。

---

###  场景三：推理与思考

这是较新的功能，用于让模型展示其“思维链”。

#### OpenAI 协议
OpenAI 通过 `reasoning_effort` 参数或在 Responses API 中使用 `include: ["reasoning.encrypted_content"]` 来控制。

**请求报文：**
```json
{
  "model": "o1-preview",
  "messages": [{"role": "user", "content": "一个复杂的问题..."}],
  "reasoning_effort": "medium"
}
```

#### Anthropic 协议
Anthropic 通过 `thinking` 参数来启用扩展思考，模型会在响应中返回包含思考过程的 `content` 块。

**请求报文：**
```json
{
  "model": "claude-3-7-sonnet-20250219",
  "messages": [{"role": "user", "content": "一个复杂的问题..."}],
  "thinking": {
    "type": "enabled",
    "budget_tokens": 2048
  },
  "max_tokens": 4096
}
```

**响应报文：**
```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "让我来分析这个问题...",
      "signature": "..."
    },
    {
      "type": "text",
      "text": "这是最终的答案..."
    }
  ]
}
```

---

###  总结

| 场景 | OpenAI 特点 | Anthropic 特点 |
| :--- | :--- | :--- |
| **聊天** | 消息列表扁平化，`system` 也是消息 | 结构清晰，`system` 独立，`messages` 纯净 |
| **工具调用** | 角色驱动 (`tool`, `assistant`)，逻辑清晰 | 内容块驱动 (`tool_use`, `tool_result`)，高度统一 |
| **推理** | 参数控制 (`reasoning_effort`) | 显式启用 (`thinking`)，返回思考过程块 |

总的来说，OpenAI 的协议更灵活、更通用，而 Anthropic 的协议更结构化、更强调安全和一致性。理解这些差异有助于你更好地为不同的模型编写代码。

