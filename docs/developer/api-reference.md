# API Reference

**Complete REST API documentation for integrating with SAM.**

SAM provides a built-in REST API that's compatible with OpenAI's format, making it easy to integrate SAM into your applications, scripts, and workflows. Whether you're building a custom UI, automating tasks, or integrating SAM into larger systems, this API gives you programmatic access to all of SAM's capabilities.

**What's covered:**
- Complete endpoint reference with examples
- OpenAI-compatible chat completions API
- Conversation management endpoints
- Memory and RAG API endpoints
- Streaming responses with SSE
- Error handling and best practices

**Why use the API:**
- Build custom frontends and UIs
- Integrate SAM into existing applications
- Automate workflows with scripts
- Create specialized tools and interfaces
- Access SAM from other programming languages

**Prerequisites:**
- Basic understanding of REST APIs
- Familiarity with JSON
- Knowledge of HTTP methods (GET, POST, DELETE)
- Optional: Understanding of Server-Sent Events (SSE) for streaming

---

## Base URL

```
http://localhost:8080
```

Default port: `8080` (configurable in preferences)

---

## Authentication

Currently no authentication required for localhost.  
For remote access, configure authentication in SAM preferences.

---

## Endpoints

### POST /api/chat/completions

Send a chat message and receive a response.

**Request Body**:
```json
{
  "model": "gpt-4",
  "messages": [
    {"role": "user", "content": "Hello"}
  ],
  "temperature": 0.7,
  "max_tokens": 2000,
  "stream": false,
  "tools": []
}
```

**Response** (non-streaming):
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1699123456,
  "model": "gpt-4",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hello! How can I help you?"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 28,
    "total_tokens": 43
  },
  "sam_metadata": {
    "provider": {
      "type": "openai",
      "name": "OpenAI",
      "is_local": false,
      "base_url": "api.openai.com"
    },
    "model_info": {
      "context_window": 8192,
      "max_output_tokens": 8192,
      "supports_tools": true,
      "supports_vision": false,
      "supports_streaming": true,
      "family": "gpt-4"
    },
    "workflow": {
      "iterations": 1,
      "max_iterations": 300,
      "tool_call_count": 0,
      "tools_used": [],
      "duration_seconds": 2.5,
      "completion_reason": "workflow_complete",
      "had_errors": false
    },
    "cost_estimate": {
      "estimated_cost_usd": 0.0012,
      "prompt_cost_per_1k": 0.03,
      "completion_cost_per_1k": 0.06,
      "currency": "USD",
      "note": "Estimated based on published pricing"
    }
  }
}
```

### SAM Enhanced Metadata

SAM enriches API responses with comprehensive metadata in the `sam_metadata` field:

| Field | Description |
|-------|-------------|
| `provider` | Provider info: type, name, local/remote status, base URL |
| `model_info` | Model capabilities: context window, output limits, tool/vision/streaming support |
| `workflow` | Execution details: iterations, tool calls, duration, completion reason |
| `cost_estimate` | USD cost estimate with per-1K token rates |

**Provider Types**: `openai`, `anthropic`, `github_copilot`, `deepseek`, `mlx`, `gguf`, `custom`

**Completion Reasons**: `workflow_complete`, `max_iterations_reached`, `cancelled`, `error`, `tool_execution_failed`

**Response** (streaming with `stream: true`):
```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1699123456,"model":"gpt-4","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1699123456,"model":"gpt-4","choices":[{"index":0,"delta":{"content":"Hello"},"finish_reason":null}]}

data: [DONE]
```

### GET /api/models

List available models.

**Response**:
```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4",
      "object": "model",
      "owned_by": "openai"
    },
    {
      "id": "mlx-qwen-7b",
      "object": "model",
      "owned_by": "local"
    }
  ]
}
```

### Common Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `model` | string | Model to use | Required |
| `messages` | array | Conversation messages | Required |
| `temperature` | number | Randomness (0.0-2.0) | 0.7 |
| `max_tokens` | integer | Max response length | 2000 |
| `top_p` | number | Nucleus sampling | 1.0 |
| `stream` | boolean | Enable streaming | false |
| `tools` | array | Available tools | [] |

### Message Format

```json
{
  "role": "user|assistant|system|tool",
  "content": "Message content",
  "tool_calls": [] // For assistant messages with tool calls
}
```


### POST /api/chat/tool-response

Submit user response for blocked tool execution (User Collaboration Protocol).

**Request Body**:
```json
{
  "toolCallId": "call_abc123",
  "userResponse": "yes",
  "conversationId": "uuid-here"
}
```

---

### POST /api/chat/autonomous

Multi-step autonomous workflow endpoint with agent orchestration.

**Request Body**:
```json
{
  "model": "gpt-4",
  "messages": [{"role": "user", "content": "Build a todo app"}],
  "maxIterations": 50
}
```

---

### GET /v1/conversations

List all conversations.

**Response**:
```json
{
  "conversations": [
    {
      "id": "uuid",
      "title": "My Conversation",
      "messageCount": 42
    }
  ]
}
```

---

### GET /v1/conversations/:conversationId

Get specific conversation details.

---

### GET /api/prompts/system

List available system prompts.

---

### GET /api/prompts/mini

List available mini prompts.

---

### POST /api/models/download

Download Stable Diffusion model.

---

### GET /api/models/download/:downloadId/status

Check download status.

---

### DELETE /api/models/download/:downloadId

Cancel ongoing download.

---

### GET /api/tool_result

Retrieve large persisted tool results (>16KB auto-persist).

**Query Parameters**:
- `resultId` (string): Tool result ID

---

---

## Tool Calling

SAM provides MCP (Model Context Protocol) tools that the AI can automatically invoke to complete tasks. For complete tool documentation, see [Tools Reference](../power-user/tools-reference.md).

### Available Tools

SAM includes the following consolidated tools:

| Tool | Operations | Status | Description |
|------|------------|--------|-------------|
| `think` | 1 | ✓ Enabled | Planning and structured reasoning |
| `increase_max_iterations` | 1 | ✓ Enabled | Request more iterations for complex tasks |
| `read_tool_result` | 1 | ✓ Enabled | Retrieve large persisted tool results |
| `user_collaboration` | 1 | ✗ Disabled | Request user input mid-task |
| `file_operations` | 16 | ✓ Enabled | Read, search, write, and manage workspace files |
| `terminal_operations` | 11 | ✗ Disabled | Execute commands and manage persistent PTY sessions |
| `memory_operations` | 4 | ✓ Enabled | Search conversation history, store information |
| `todo_operations` | 4 | ✓ Enabled | Track progress and plan tasks through todo lists |
| `recall_history` | 1 | ✓ Enabled | Search archived YaRN-compressed conversation context |
| `build_and_version_control` | 5 | ✓ Enabled | Build tasks and git operations |
| `web_operations` | 6 | ✓ Enabled | Web research, scraping, content retrieval, SerpAPI |
| `document_operations` | 3 | ✓ Enabled | Import PDFs/DOCX, create formatted documents |
| `image_generation` | 1 | ✗ Conditional | Stable Diffusion image generation (requires models) |
| `run_subagent` | 1 | ✗ Disabled | Delegate subtasks to isolated agents |
| `list_system_prompts` | 1 | ✓ Enabled | List available system prompts |
| `list_mini_prompts` | 1 | ✓ Enabled | List available mini prompts |

**Note:** SAM provides 16 total tools (57 operations total). Core tools are automatically available to the AI. Advanced tools (terminal, collaboration, subagent) are disabled by default for security and can be enabled via API or UI preferences.

### Tool Invocation Format

Tools are invoked using OpenAI's function calling format. For consolidated tools, include the `operation` parameter:

**Request with tools:**
```json
{
  "model": "gpt-4",
  "messages": [
    {"role": "user", "content": "Read the README file"}
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "file_operations",
        "description": "File operations: read, search, write, and manage workspace files",
        "parameters": {
          "type": "object",
          "properties": {
            "operation": {
              "type": "string",
              "description": "File operation to perform",
              "enum": ["read_file", "list_dir", "create_file", "replace_string", ...]
            },
            "filePath": {
              "type": "string",
              "description": "File path for read/write operations"
            }
          },
          "required": ["operation"]
        }
      }
    }
  ]
}
```

**Model's tool call:**
```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [{
    "id": "call_abc123",
    "type": "function",
    "function": {
      "name": "file_operations",
      "arguments": "{\"operation\":\"read_file\",\"filePath\":\"/path/to/README.md\"}"
    }
  }]
}
```

**Tool result response:**
```json
{
  "role": "tool",
  "tool_call_id": "call_abc123",
  "name": "file_operations",
  "content": "{\"success\":true,\"content\":\"# README\\n\\nThis is the README file...\"}"
}
```

### Common Tool Calling Patterns

**Read a file:**
```json
{
  "name": "file_operations",
  "arguments": {
    "operation": "read_file",
    "filePath": "/project/src/main.swift"
  }
}
```

**Search code:**
```json
{
  "name": "file_operations",
  "arguments": {
    "operation": "grep_search",
    "query": "func.*authenticate",
    "isRegexp": true,
    "includePattern": "**/*.swift"
  }
}
```

**Execute terminal command:**
```json
{
  "name": "terminal_operations",
  "arguments": {
    "operation": "run_command",
    "command": "npm install",
    "explanation": "Install project dependencies"
  }
}
```

**Search conversation memory:**
```json
{
  "name": "memory_operations",
  "arguments": {
    "operation": "search_memory",
    "query": "API configuration",
    "similarity_threshold": "0.3"
  }
}
```

**Git commit:**
```json
{
  "name": "build_and_version_control",
  "arguments": {
    "operation": "git_commit",
    "message": "feat: Add authentication module",
    "files": ["src/auth.swift", "tests/auth_test.swift"]
  }
}
```

### Tool Response Format

Tool results are returned as JSON strings in the `content` field:

**Success response:**
```json
{
  "success": true,
  "data": "Tool execution result",
  "message": "Operation completed successfully"
}
```

**Error response:**
```json
{
  "success": false,
  "error": "Error message",
  "message": "Operation failed"
}
```

### Multi-Turn Tool Calling

Complex tasks may require multiple tool calls. The conversation continues with tool results:

```json
// Turn 1: User request
{"role": "user", "content": "Find and update the version number"}

// Turn 2: AI calls search tool
{"role": "assistant", "tool_calls": [{"function": {"name": "file_operations", "arguments": "{\"operation\":\"grep_search\",\"query\":\"version\"}"}}]}

// Turn 3: Tool result
{"role": "tool", "content": "Found in config.json: \"version\": \"1.0.0\""}

// Turn 4: AI calls edit tool
{"role": "assistant", "tool_calls": [{"function": {"name": "file_operations", "arguments": "{\"operation\":\"replace_string\",\"filePath\":\"config.json\",\"oldString\":\"\\\"version\\\": \\\"1.0.0\\\"\",\"newString\":\"\\\"version\\\": \\\"1.1.0\\\"\"}"}}]}

// Turn 5: Tool result
{"role": "tool", "content": "{\"success\": true}"}

// Turn 6: AI response
{"role": "assistant", "content": "Version number updated from 1.0.0 to 1.1.0"}
```

### Tool Authorization

Some operations require user authorization:

- **Auto-approved:** Read operations, write operations inside working directory
- **Require approval:** Write operations outside working directory, destructive operations

When authorization is required, the AI can use the `user_collaboration` tool:

```json
{
  "name": "user_collaboration",
  "arguments": {
    "prompt": "May I delete the old backup files?",
    "authorize_operation": "file_operations.delete_file"
  }
}
```

---

## Examples

### Simple Chat

```bash
curl -X POST http://localhost:8080/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "What is 2+2?"}
    ]
  }'
```

### Streaming Response

```bash
curl -N -X POST http://localhost:8080/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "Write a poem"}
    ],
    "stream": true
  }'
```

### With SAM Tools

**Note:** SAM's built-in tools are automatically available. This example shows how to use them via the API:

```bash
curl -X POST http://localhost:8080/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "Read the package.json file"}
    ]
  }'
```

The AI will automatically invoke `file_operations` with `operation: read_file`.

**For custom tool integrations:**

```bash
curl -X POST http://localhost:8080/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "Search for authentication code"}
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "file_operations",
          "description": "File operations",
          "parameters": {
            "type": "object",
            "properties": {
              "operation": {"type": "string", "enum": ["grep_search"]},
              "query": {"type": "string"},
              "isRegexp": {"type": "boolean"}
            },
            "required": ["operation"]
          }
        }
      }
    ]
  }'
```

---

## Error Handling

**Error Response Format**:
```json
{
  "error": {
    "message": "Invalid API key",
    "type": "invalid_request_error",
    "code": "invalid_api_key"
  }
}
```

**Common Error Codes**:
- `invalid_request_error` - Malformed request
- `authentication_error` - Invalid API key
- `rate_limit_error` - Too many requests
- `server_error` - Internal server error

---

## Rate Limits

SAM does not impose rate limits for localhost access.  
For remote access, configure rate limits in preferences.

---

## SDK Examples

### Python

```python
import openai

openai.api_base = "http://localhost:8080/api"
openai.api_key = "not-needed-for-local"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)

print(response.choices[0].message.content)
```

### JavaScript

```javascript
const response = await fetch('http://localhost:8080/api/chat/completions', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    model: 'gpt-4',
    messages: [{role: 'user', content: 'Hello'}]
  })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

---

For more examples, see [Developer's Guide](developers-guide.md).
