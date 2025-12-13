# SAM Tools Reference

**16 tools. 49+ operations. Infinite possibilities.**

This is how SAM gets things done. While most AI assistants just talk, SAM takes action: reading your files, executing commands, searching the web, managing git, generating images, and more. All through the Model Context Protocol (MCP).

**You don't call tools directly.** Just describe what you need in natural language, and SAM automatically invokes the right tools. Say "read that config file" and SAM uses `file_operations`. Ask "what did we discuss about auth?" and SAM searches memory.

**This reference covers:**
- All 16 tools with every operation documented
- Real-world examples and parameter details
- When to use each tool (and when not to)
- Security model and authorization

**Who needs this:**
- Power users pushing SAM's limits
- Developers integrating SAM via API
- System prompt authors designing workflows
- Anyone curious about what's possible

---

## Overview

SAM provides MCP tools that enable the AI to perform complex operations. Tools are invoked automatically - you don't call them directly.

**Tool Categories:**
- **Core Tools** (4): think, increase_max_iterations, read_tool_result, user_collaboration
- **File & Terminal** (2): file_operations (16 ops), terminal_operations (11 ops)
- **Memory & Planning** (2): memory_operations (4 ops), todo_operations (4 ops)
- **Build & VCS** (1): build_and_version_control (5 ops)
- **Web & Documents** (2): web_operations (6 ops), document_operations (3 ops)
- **Context Recall** (1): recall_history (search archived conversation context)
- **Image Generation** (1): image_generation (requires Stable Diffusion models)
- **Subagent & Discovery** (3): run_subagent, list_system_prompts, list_mini_prompts

For an authoritative, up-to-date inventory and availability details, see the repository `user-docs/TOOLS_REFERENCE.md` (this document provides usage examples, parameters, and workflows).

**Security Note:** All tools implement proper authorization. Operations outside the working directory require user approval.

---

## Core Tools

### 1. think

**Purpose:** Strategic planning and problem decomposition

**Description:**  
Enables the AI to think through complex problems, plan multi-step solutions, and organize its approach before taking action. Implements the thinking pattern from VS Code Copilot.

**When to use:**
- Planning complex multi-step workflows
- Clarifying approach when uncertain
- Breaking down large or ambiguous requests
- Analyzing errors or unexpected results

**When NOT to use:**
- Simple, single-step tasks
- Repeated planning without action
- Todo list management (use todo_operations instead)

**Parameters:**
- `thoughts` (string, required): Planning, analysis, or reasoning process
- `requested_tools` (array[string], optional): List of tool names for subsequent iterations

**Example:**
```json
{
  "name": "think",
  "arguments": {
    "thoughts": "To refactor the authentication system: 1) Analyze current implementation 2) Design new architecture 3) Implement changes 4) Test thoroughly",
    "requested_tools": ["file_operations", "terminal_operations"]
  }
}
```

**Critical Rule:** Think once, then execute. Do NOT get stuck in thinking loops.

---

### 2. increase_max_iterations

**Purpose:** Request more iterations for complex tasks

**Description:**  
Allows agents to request additional iterations when approaching the limit. Requires Dynamic Iterations to be enabled in conversation settings.

**When to use:**
- Approaching iteration limit
- Complex task requires more iterations than initially allocated
- Making steady progress but need more time to complete

**Requirements:**
- Dynamic Iterations must be ENABLED in conversation settings
- Specify total iterations needed (not additional iterations)
- Provide clear reason explaining the need

**Parameters:**
- `requested_iterations` (integer, required): Total iterations needed (must be greater than current max)
- `reason` (string, required): Clear explanation of why more iterations are needed

**Example:**
```json
{
  "name": "increase_max_iterations",
  "arguments": {
    "requested_iterations": 500,
    "reason": "Need more iterations to complete refactoring of remaining files. Making steady progress."
  }
}
```

---

### 3. read_tool_result

**Purpose:** Retrieve large tool results in chunks

**Description:**  
Large tool results are automatically saved to disk to avoid provider errors. This tool reads those saved results in manageable chunks.

**When to use:**
- Tool response contains `[TOOL_RESULT_STORED]` marker
- Tool response includes `toolCallId` and `totalLength` metadata
- Need to access large web scraping or research results

**Chunked Retrieval:**
- Configurable chunk sizes for efficient reading
- Use `offset` + `length` to paginate through large results

**Parameters:**
- `toolCallId` (string, required): Tool call ID from stored result message
- `offset` (integer, optional): Character offset to start reading from (default: 0)
- `length` (integer, optional): Number of characters to read

**Example:**
```json
{
  "name": "read_tool_result",
  "arguments": {
    "toolCallId": "call_abc123",
    "offset": 0,
    "length": 8192
  }
}
```

**Example Workflow:**
1. Tool returns: "Preview: ... [TOOL_RESULT_STORED: toolCallId=abc123, totalLength=150000]"
2. Read first chunk: `read_tool_result(toolCallId: "abc123", offset: 0, length: 8192)`
3. Read next chunk: `read_tool_result(toolCallId: "abc123", offset: 8192, length: 8192)`
4. Continue until `hasMore=false`

---

### 4. user_collaboration

**Purpose:** Request user input during task execution

**Description:**  
Enables SAM to request user input, clarification, or decisions mid-stream without breaking conversation flow. Blocks execution until user responds.

**Critical Rule:** Ask questions HERE, not in chat responses. If you have a question, call this tool.

**When to use:**
- Ambiguous requests needing clarification
- Multiple valid approaches - user should choose
- Confirmation before destructive operations
- Information only user knows (API keys, credentials, paths)

**When NOT to use:**
- Questions answerable with other tools (use memory_operations, file_operations instead)
- Optional confirmations (proceed unless operation is destructive)
- Information already available in the conversation context

**Parameters:**
- `prompt` (string, required): Question or request to show user
- `context` (string, optional): Context explaining why you're asking
- `authorize_operation` (string, optional): Tool operation to authorize if user approves (format: 'tool_name.operation')

**Example:**
```json
{
  "name": "user_collaboration",
  "arguments": {
    "prompt": "Found 500 files matching pattern. Rename all with timestamp prefix?",
    "context": "This will modify all .log files in the directory permanently",
    "authorize_operation": "file_operations.rename_file"
  }
}
```

**Security:** Blocks execution indefinitely until user responds. User has full control.

---

## File & Terminal Operations

### 5. file_operations

**Purpose:** Read, write, search, and manage files

**Description:**  
Comprehensive file system operations including reading, writing, searching (glob, regex, semantic), and file management. **16 operations total.**

**Authorization:**
- Inside working directory: AUTO-APPROVED ✅
- Outside working directory: Requires user approval ⚠️
- Relative paths: Auto-resolve to working directory

**READ Operations (4):**

#### read_file
Read file contents with optional line range.

**Parameters:**
- `operation`: `"read_file"` (required)
- `filePath` (string, required): Absolute path to file
- `limit` (number, optional): Max lines to read
- `offset` (number, optional): Starting line (1-indexed)

**Example:**
```json
{
  "name": "file_operations",
  "arguments": {
    "operation": "read_file",
    "filePath": "/Users/andrew/project/src/main.swift",
    "limit": 100,
    "offset": 1
  }
}
```

#### list_dir
List directory contents.

**Parameters:**
- `operation`: `"list_dir"` (required)
- `path` (string, required): Directory path

#### get_errors
Retrieve compilation or linting errors.

**Parameters:**
- `operation`: `"get_errors"` (required)
- `filePaths` (array, optional): Specific files to check

#### get_search_results
Fetch workspace search view results.

**Parameters:**
- `operation`: `"get_search_results"` (required)

**SEARCH Operations (5):**

#### file_search
Search for files by glob pattern.

**Parameters:**
- `operation`: `"file_search"` (required)
- `query` (string, required): Glob pattern (e.g., `"**/*.swift"`)
- `maxResults` (number, optional): Limit results

**Example:**
```json
{
  "name": "file_operations",
  "arguments": {
    "operation": "file_search",
    "query": "**/*.{js,ts}",
    "maxResults": 50
  }
}
```

#### grep_search
Search file contents using regex.

**Parameters:**
- `operation`: `"grep_search"` (required)
- `query` (string, required): Search pattern
- `isRegexp` (boolean, required): true for regex
- `includePattern` (string, optional): File pattern to search within
- `maxResults` (number, optional): Limit results

**Example:**
```json
{
  "name": "file_operations",
  "arguments": {
    "operation": "grep_search",
    "query": "class\\s+\\w+Controller",
    "isRegexp": true,
    "includePattern": "src/**/*.swift"
  }
}
```

#### semantic_search
AI-powered code/text search across workspace.

**Parameters:**
- `operation`: `"semantic_search"` (required)
- `query` (string, required): Natural language query

**Example:**
```json
{
  "name": "file_operations",
  "arguments": {
    "operation": "semantic_search",
    "query": "function that validates email addresses"
  }
}
```

#### list_usages
Find all references to a symbol (variable, function, class).

**Parameters:**
- `operation`: `"list_usages"` (required)
- `symbolName` (string, required): Symbol to find
- `filePaths` (array, optional): Files to search within

#### search_index
Search working directory file index for fast file discovery by name, path, or extension.

**WRITE Operations (7):**

#### create_file
Create new file with content.

**Parameters:**
- `operation`: `"create_file"` (required)
- `filePath` (string, required): Absolute path for new file
- `content` (string, required): File content

**Example:**
```json
{
  "name": "file_operations",
  "arguments": {
    "operation": "create_file",
    "filePath": "/Users/andrew/project/README.md",
    "content": "# My Project\n\nDescription here..."
  }
}
```

#### replace_string
Replace text in file (single occurrence).

**Parameters:**
- `operation`: `"replace_string"` (required)
- `filePath` (string, required): File to modify
- `oldString` (string, required): Exact text to replace (include context lines!)
- `newString` (string, required): Replacement text

**Important:** Include 3-5 lines of context before/after to ensure unique match.

#### multi_replace_string
Multiple string replacements in one operation.

**Parameters:**
- `operation`: `"multi_replace_string"` (required)
- `filePath` (string, required): File to modify
- `replacements` (array, required): Array of `{oldString, newString}` objects

#### insert_edit
Insert or replace text at specific line.

**Parameters:**
- `operation`: `"insert_edit"` (required)
- `filePath` (string, required): File to modify
- `lineNumber` (number, required): Line number (1-indexed)
- `newText` (string, required): Text to insert/replace
- `insertOperation` (string, required): `"insert"` or `"replace"`

#### rename_file
Rename or move file.

**Parameters:**
- `operation`: `"rename_file"` (required)
- `oldPath` (string, required): Current file path
- `newPath` (string, required): New file path

#### delete_file
Delete file.

**Parameters:**
- `operation`: `"delete_file"` (required)
- `filePath` (string, required): File to delete

#### apply_patch
Apply unified diff patch to file.

**Parameters:**
- `operation`: `"apply_patch"` (required)
- `filePath` (string, required): File to patch
- `patchContent` (string, required): Unified diff format patch

**Note on Working Directories:**

File operations use the conversation's effective working directory:

**Without Shared Topic:**
- Working Directory: `~/SAM/{conversation-uuid}/`
- Creates: `~/SAM/{conversation-uuid}/file.txt`

**With Shared Topic "myproject":**
- Working Directory: `~/SAM/myproject/`
- Creates: `~/SAM/myproject/file.txt`

**Benefits:**
- Multiple conversations share same workspace
- Human-readable directory names
- Easy to find files in Finder

See [Shared Topics Documentation](../end-user/shared-topics.md) for details.

---

### 6. terminal_operations

**Purpose:** Execute shell commands and manage terminal sessions

**Description:**  
Execute terminal commands and manage persistent PTY (pseudo-terminal) sessions. **11 operations total.**

**Command Execution (6):**
- `run_command` - Execute shell command
- `get_terminal_output` - Get output from background process
- `get_terminal_buffer` - Get current visible terminal contents
- `get_last_command` - Get last executed command
- `get_terminal_selection` - Get selected terminal text
- `create_directory` - Create directory recursively

**PTY Session Management (5):**
- `create_session` - Start new persistent terminal session
- `send_input` - Send command to existing session
- `get_output` - Read session output
- `get_history` - Get full session history
- `close_session` - Close terminal session

**Critical: send_input Requirements:**
- Shell commands MUST end with `\r\n` (carriage return + newline)
- Interactive keystrokes send as-is WITHOUT `\r\n`
- Examples:
  - Shell command: `{"input": "ls -la\r\n"}`
  - Vim keystroke: `{"input": ":wq\r"}` or `{"input": "\u001b"}` (escape)

**Common Parameters:**
- `operation` (string, required): Terminal operation to perform
- `command` (string): Shell command to execute
- `explanation` (string): What command does
- `isBackground` (boolean): Run as background process (USE SPARINGLY)
- `session_id` (string): PTY session ID

**Example:**
```json
{
  "name": "terminal_operations",
  "arguments": {
    "operation": "run_command",
    "command": "npm install",
    "explanation": "Install Node.js dependencies",
    "isBackground": false
  }
}
```

```json
{
  "name": "terminal_operations",
  "arguments": {
    "operation": "create_session",
    "working_directory": "/Users/andrew/project"
  }
}
```

```json
{
  "name": "terminal_operations",
  "arguments": {
    "operation": "send_input",
    "session_id": "conv-uuid",
    "input": "git status\r\n"
  }
}
```

**Critical: isBackground Usage**
- ✓ Long-running servers (web servers, dev servers)
- ✓ Watch mode processes (file watchers, auto-rebuild)
- ✗ SSH commands (must wait for response)
- ✗ File operations (must confirm completion)
- ✗ Installation commands (must verify success)
- ✗ ANY command where you need the output

**System Context Awareness:**
- ALWAYS verify current system before SSH operations
- Use `echo $HOSTNAME` to confirm current system
- NEVER SSH from a system to itself
- Best practice: Check hostname before every SSH command

**Security:** Command authorization based on working directory. PTY sessions scoped to conversation.

---

## Memory & RAG Tools

### 7. memory_operations

**Purpose:** Search, store conversation memory and manage todo lists

**Description:**  
Consolidated tool for semantic search across stored memories, persistent storage, and task management. **4 operations total.**

**Operations:**

#### search_memory
Semantic search across stored memories.

**Parameters:**
- `operation`: `"search_memory"` (required)
- `query` (string, required): Search query
- `similarity_threshold` (string, optional): Minimum similarity (0.0-1.0, default: 0.3)
- `limit` (integer, optional): Maximum results

**Similarity Threshold Guide:**
- Document/RAG: 0.15-0.25 (embeddings produce lower scores)
- Conversation memory: 0.3-0.5
- No results? Lower threshold incrementally (0.3→0.2→0.15)

**Example:**
```json
{
  "name": "memory_operations",
  "arguments": {
    "operation": "search_memory",
    "query": "previous API keys",
    "similarity_threshold": "0.3"
  }
}
```

#### store_memory
Save information to memory.

**Parameters:**
- `operation`: `"store_memory"` (required)
- `content` (string, required): Content to store
- `content_type` (string, optional): Type categorization

**Example:**
```json
{
  "name": "memory_operations",
  "arguments": {
    "operation": "store_memory",
    "content": "User prefers JSON format for API responses",
    "content_type": "preference"
  }
}
```

#### list_collections
View memory statistics.

**Parameters:**
- `operation`: `"list_collections"` (required)

**Security:** Memory scoped to conversation or shared topic.

---

### 8. todo_operations

**Purpose:** Track progress and plan tasks through structured todo lists

**Description:**  
Dedicated tool for managing todo lists during multi-step workflows. Use VERY frequently to ensure task visibility and proper planning. Separated from memory_operations for clearer usage.

**When to Use:**
- Complex multi-step work requiring planning and tracking
- User provides multiple tasks or requests (numbered/comma-separated)
- After receiving new instructions requiring multiple steps
- BEFORE starting work on any todo (mark as in-progress)
- IMMEDIATELY after completing each todo (mark completed individually)
- When user requests more work after completing initial tasks (use `add` operation)

**When NOT to Use:**
- Single, trivial tasks completable in one step
- Purely conversational/informational requests
- Simple code samples or explanations

**Operations (4):**
- `read` - Get current todo list
- `write` - Create/replace todo list (requires todoList array)
- `update` - Partial update (requires todoUpdates array)
- `add` - Append new todos while preserving existing ones (requires newTodos array)

**Parameters:**
- `operation` (string, required): 'read', 'write', 'update', or 'add'
- `todoList` (array[object]): Complete todo array for write operation
- `todoUpdates` (array[object]): Partial updates for update operation
- `newTodos` (array[object]): New todos to add (for add operation)

**Todo Item Structure:**
```json
{
  "id": 1,
  "title": "Implement authentication",
  "description": "Add JWT-based auth to API endpoints",
  "status": "in-progress",
  "priority": "high",
  "dependencies": [],
  "canRunParallel": false,
  "progress": "0.5"
}
```

**Status Values:** `not-started` | `in-progress` (max 1 at a time) | `completed` | `blocked`

**Critical Workflow:**
1. Plan tasks by writing todo list with specific, actionable items
2. Mark ONE todo as `in-progress` BEFORE starting work
3. Complete the work for that specific todo
4. Mark that todo as `completed` IMMEDIATELY after finishing
5. Move to next todo and repeat

**Example - Create Todo List:**
```json
{
  "name": "todo_operations",
  "arguments": {
    "operation": "write",
    "todoList": [
      {
        "id": 1,
        "title": "Research options",
        "description": "Explore available authentication libraries",
        "status": "not-started"
      },
      {
        "id": 2,
        "title": "Implement solution",
        "description": "Add chosen auth library to the project",
        "status": "not-started"
      }
    ]
  }
}
```

**Example - Update Status:**
```json
{
  "name": "todo_operations",
  "arguments": {
    "operation": "update",
    "todoUpdates": [
      {"id": 1, "status": "completed"},
      {"id": 2, "status": "in-progress"}
    ]
  }
}
```

**Example - Add New Tasks (after completing initial list):**
```json
{
  "name": "todo_operations",
  "arguments": {
    "operation": "add",
    "newTodos": [
      {"title": "Additional task", "description": "New work requested by user"},
      {"title": "Another task", "description": "More details here"}
    ]
  }
}
```

The `add` operation automatically:
- Preserves all existing todos (including completed ones)
- Assigns IDs starting after the highest existing ID
- Defaults to `not-started` status

**Important:** Describing progress in your response is NOT the same as updating - you MUST call this tool to update todo status.

---

## Version Control


### 8. build_and_version_control

**Purpose:** Build tasks and version control operations

**Description:**  
Consolidated tool for creating/running build tasks and git operations. **5 operations total.**

**Task Management (3):**
- `create_and_run_task` - Create and execute SAM task
- `run_task` - Run existing SAM task by label
- `get_task_output` - Get task execution output

**Git Operations (2):**
- `git_commit` - Commit changes to repository
- `get_changed_files` - Get changed files in repo

**Common Parameters:**
- `operation` (string, required): Build/VCS operation to perform
- `task` (object): Task definition for create_and_run_task
- `label` (string): Task label for run_task
- `message` (string): Commit message for git_commit
- `files` (array[string]): Files to commit

**Example:**
```json
{
  "name": "build_and_version_control",
  "arguments": {
    "operation": "create_and_run_task",
    "task": {
      "label": "Build Debug",
      "type": "shell",
      "command": "make build-debug"
    },
    "workspaceFolder": "/Users/andrew/project"
  }
}
```

```json
{
  "name": "build_and_version_control",
  "arguments": {
    "operation": "git_commit",
    "message": "feat: Add authentication system",
    "files": ["Sources/Auth.swift", "Tests/AuthTests.swift"]
  }
}
```

```json
{
  "name": "build_and_version_control",
  "arguments": {
    "operation": "get_changed_files",
    "sourceControlState": ["staged", "unstaged"]
  }
}
```

**Security:** Git operations require authorization. Task output captured and retrievable.

---

## Context Recall

### 9. recall_history

**Purpose:** Search and retrieve archived conversation context

**Description:**
When YaRN compression archives older messages to fit model context limits, this tool allows agents to recall that archived context when needed. Also supports topic-wide search across multiple agent conversations in shared topics.

**When to use:**
- You need context from earlier in a long conversation
- The user references something discussed previously
- You see "[Memory Status]" indicating archived context exists
- You need to remember decisions or information from earlier
- You want to see what other agents discussed in a shared topic

**When NOT to use:**
- Recent context still in the conversation window
- Information stored via memory_operations (use search_memory instead)
- Current conversation is short and complete

**Parameters:**
- `query` (string, required): Search term or topic to find relevant history
- `topic_id` (string, optional): UUID of shared topic to search across ALL conversations in the topic
- `time_hint` (string, optional): 'recent' for latest archived, 'early' for oldest, or leave empty for relevance-based search
- `limit` (integer, optional): Number of chunks to retrieve (1-10, default: 3)

**Example - Single Conversation:**
```json
{
  "name": "recall_history",
  "arguments": {
    "query": "database schema decisions",
    "limit": 3
  }
}
```

**Example - Topic-Wide Search:**
```json
{
  "name": "recall_history",
  "arguments": {
    "query": "authentication implementation",
    "topic_id": "550e8400-e29b-41d4-a716-446655440000",
    "limit": 5
  }
}
```

**Example - Time-Based Retrieval:**
```json
{
  "name": "recall_history",
  "arguments": {
    "query": "project setup",
    "time_hint": "early",
    "limit": 2
  }
}
```

**Output Format:**
```
# Recalled History for: "database schema"

Found 2 relevant archive chunks.

---
## Chunk 1: 10:30-11:15

**Summary:** Discussed database schema for user management system.

**Key Topics:** PostgreSQL, foreign keys, indexes, user table

**Messages (5):**
[User - 10:32] What database should we use?
[Assistant - 10:33] I recommend PostgreSQL for relational data...
```

**Topic-Wide Benefits:**
- Search history from ALL agents in a shared topic
- Find what specialized agents (frontend, backend, testing) discussed
- Maintain continuity across agent handoffs
- Get full project context from multiple perspectives

**Security:** Archived context scoped to conversation or shared topic. Cannot access archives from other conversations/topics.

---

## Web & Documents

### 10. web_operations

**Purpose:** Web research, search, scraping, and content retrieval

**Description:**  
Comprehensive web operations tool combining research, search, scraping, and content extraction. Includes professional search via SerpAPI when configured.

**Supported Operations:**
- `research` - Comprehensive multi-source research + memory storage
- `retrieve` - Access previously stored research from memory
- `web_search` - Quick web search for top results
- `serpapi` - Professional search via SerpAPI (Google, Bing, Amazon, etc.) [if enabled]
- `scrape` - Extract content from websites (WebKit rendering with JavaScript)
- `fetch` - Retrieve main content from webpage (basic HTTP, faster)

**When to use:**
- Current events, news, live information
- Documentation lookup
- Multi-source research synthesis
- Shopping/product research (serpapi with engine=amazon/ebay/walmart)

**When NOT to use:**
- Information already in context
- Questions answerable from conversation history
- Local file content (use file_operations)

**Parameters:**
- `operation` (string, required): Operation type (research, retrieve, web_search, serpapi, scrape, fetch)
- `query` (string): Search query or research question
- `url` (string): Target URL for scrape/fetch operations (MUST use HTTPS)
- `depth` (string): Research depth - shallow/standard/comprehensive
- `engine` (string): Search engine for serpapi - google/bing/amazon/ebay/walmart
- `location` (string): Search location for serpapi (optional)

**Examples:**
```json
{
  "name": "web_operations",
  "arguments": {
    "operation": "research",
    "query": "Latest developments in quantum computing",
    "depth": "comprehensive"
  }
}
```

```json
{
  "name": "web_operations",
  "arguments": {
    "operation": "serpapi",
    "query": "best laptops 2025",
    "engine": "amazon"
  }
}
```

**Important:** All URLs must use HTTPS. Research operation stores results in memory for later retrieval via retrieve operation.

---


### 11. document_operations

**Purpose:** Import documents, create formatted files, and get document info

**Description:**  
Comprehensive document handling for importing PDFs/DOCX/TXT/MD/XLSX into memory and creating formatted documents.

**Supported Operations:**
- `document_import` - Import PDF/DOCX/TXT/MD/XLSX into conversation memory
- `document_create` - Create formatted DOCX/PDF/TXT/Markdown files
- `get_doc_info` - List imported documents in current conversation

**Supported Import Formats:**
- PDF files (text extraction)
- Word documents (.docx)
- Excel spreadsheets (.xlsx) - New in December 2025
- Text files (.txt, .md, .rtf)
- Code files (all programming languages)

**When to use:**
- Extract content from PDFs, Word docs, Excel spreadsheets, text files
- Generate formatted reports or documents
- Track what documents were imported

**When NOT to use:**
- Plain text file reading (use file_operations)
- Web content (use web_operations)
- Simple text creation (use file_operations write)

**Parameters:**
- `operation` (string, required): Operation type (document_import, document_create, get_doc_info)
- `path` (string): File path to import (for document_import) - must be valid file:// URL or absolute path
- `tags` (array[string]): Tags to associate with imported document
- `content` (string): Document content (for document_create)
- `format` (string): Output format - docx/pdf/txt/markdown
- `output_path` (string): Path where to save created document

**File URL Handling:**
- Malformed `file://` URLs are automatically recovered using working directory
- Both absolute paths and `file://` URLs accepted
- URLs validated before import attempt

**Examples:**
```json
{
  "name": "document_operations",
  "arguments": {
    "operation": "document_import",
    "path": "/Users/andrew/Documents/report.pdf",
    "tags": ["research", "Q1-2025"]
  }
}
```

```json
{
  "name": "document_operations",
  "arguments": {
    "operation": "document_create",
    "content": "# Project Report\n\nFindings...",
    "format": "docx",
    "output_path": "project_report.docx"
  }
}
```

---

### 12. image_generation

**Purpose:** Generate images from text using Stable Diffusion

**Description:**  
Creates high-quality AI-generated images based on detailed text prompts using Stable Diffusion models. SAM supports both LLM-assisted generation (via this tool) and Direct SD Mode for instant image creation.

**Two Generation Methods:**

**LLM-Assisted (via image_generation tool):**
- SAM enhances your prompt with artistic details
- Automatically adds appropriate negative prompts
- Optimizes parameters for best quality
- Use for natural language requests

**Direct SD Mode (no LLM):**
- Select SD model without LLM in model picker
- Your exact prompt goes directly to Stable Diffusion
- Faster generation (bypasses LLM processing)
- Purple send button indicates Direct Mode
- Perfect when you know exactly what you want

**Image Size Limitations:**
- SD 1.5 models: 512×512 (default), 512×768, or 768×512
- SDXL models: 1024×1024
- Cannot generate arbitrary sizes - use model's native resolution

**Scheduler Options:**
- `dpm++` (default, recommended): DPM-Solver++ with Karras timestep spacing
- `euler`: Euler method - simple and effective
- `euler_a`: Euler ancestral - more variation
- `pndm`: PLMS method - sometimes more stable

**Model Sources:**
- Manual: Place CoreML models in local models directory
- CivitAI: Browse and download community models via Preferences → CivitAI
  - Search thousands of specialized models
  - One-click download with auto-convert to CoreML
  - Filter by style, type, and rating
- ALICE: Remote GPU server for Stable Diffusion
  - Configure in Preferences → Stable Diffusion → Settings
  - Models appear with "ALICE" location in picker
  - Useful for AMD GPU hardware (Steam Deck, Linux servers)

**Engine Selection:**
- `coreml` (default): Apple Silicon optimized, fastest local inference
- `python`: Full feature support, LoRA compatible
- `alice`: Remote generation via ALICE server (when configured)

**LoRA Support:**
- Available with `python` engine only (not CoreML)
- Browse and download LoRAs via Preferences → Image Generation → LoRA Browser
- Reference LoRAs by filename in your prompt
- Use `list_loras` operation to discover available LoRAs with trigger words
- SAM automatically resolves paths and applies LoRAs

**Limitations:**
- LoRA not supported by Apple's CoreML framework
- Safety filter always enabled

**Operations:**
- **generate**: Create images from text prompts
- **list_loras**: List all available LoRAs with compatibility info and trigger words

**Parameters (generate):**
- `prompt` (string, required): Detailed text description of image to generate
- `negative_prompt` (string, optional): Things to avoid in image
- `steps` (integer, optional): Inference steps (20-100, default: 25)
- `guidance_scale` (integer, optional): How closely to follow prompt (1-20, default: 8)
- `seed` (integer, optional): Random seed (-1 for random, default: -1)
- `image_count` (integer, optional): Number of images (1-4, default: 1)
- `model` (string, optional): Model name (uses first available if not specified)
- `scheduler` (string, optional): Sampling algorithm ('dpm++', 'euler', 'euler_a', 'pndm')
- `use_karras` (boolean, optional): Use Karras timestep spacing for DPM++ (default: true)

**Example:**
```json
{
  "name": "image_generation",
  "arguments": {
    "prompt": "a serene mountain landscape at sunset with snow-capped peaks and a calm lake reflecting the orange sky, photorealistic style",
    "negative_prompt": "blurry, low quality, distorted, ugly",
    "steps": 30,
    "guidance_scale": 8,
    "seed": 42,
    "image_count": 2,
    "scheduler": "dpm++",
    "use_karras": true
  }
}
```

**Display Generated Images:**
After generation, use markdown to display in chat:
```markdown
![Generated image](file:///absolute/path/to/image.png)
```
MUST use absolute `file://` paths from tool result!

**Security:** Model loading requires file system access. Images saved to working directory. Safety filter prevents inappropriate content.

---

## Subagent Tools

### 13. run_subagent

**Purpose:** Spawn isolated subagent workflows

**Description:**  
Delegate subtasks to specialized subagents for research, parallel work, or chunking large tasks. Subagents run in isolated conversations with fresh iteration budgets.

**Subagent Characteristics:**
- Runs in isolated conversation (no context pollution)
- Fresh iteration budget (doesn't burn main agent's iterations)
- Returns summary only (not full transcript)
- Cannot spawn more subagents (recursion prevented)

**Use Cases:**
- Processing large documents (chunk into groups)
- Research before implementation
- Parallel work streams (multiple focused subagents)
- Complex workflows needing decomposition

**Example: 32-Chapter Book Review**
- Main agent: Plan chunking strategy
- Subagent 1: Review chapters 1-5 (returns summary)
- Subagent 2: Review chapters 6-10 (returns summary)
- Continue for all groups
- Main agent: Synthesize all summaries

**Parameters:**
- `task` (string, required): Brief task description
- `instructions` (string, optional): Detailed instructions for subagent
- `model` (string, optional): Model to use (default: parent's model)
- `maxIterations` (integer, optional): Iteration limit (default: 15)
- `temperature` (string, optional): Sampling temperature (0.0-2.0)
- `topP` (string, optional): Top-p sampling (0.0-1.0)
- `enableTerminalAccess` (boolean, optional): Allow terminal commands (default: false)
- `enableReasoning` (boolean, optional): Enable chain-of-thought (default: parent's setting)
- `systemPromptId` (string, optional): System prompt UUID (default: parent's prompt)
- `enableWorkflowMode` (boolean, optional): Allow nested workflows (default: false)
- `sharedTopicId` (string, optional): Shared topic UUID (default: isolated)

**Example:**
```json
{
  "name": "run_subagent",
  "arguments": {
    "task": "Review chapters 1-5 of programming book",
    "instructions": "Analyze code examples, identify patterns, note any errors, create summary of key concepts",
    "maxIterations": 20,
    "enableTerminalAccess": false,
    "systemPromptId": "research-analyst-uuid"
  }
}
```

**Security:** Terminal access disabled by default. Workflow mode disabled to prevent recursion. Isolated conversation prevents context pollution.

---

### 14. list_system_prompts

**Purpose:** Discover available system prompts

**Description:**  
List all available system prompts with IDs, names, and descriptions. Enables agents to discover prompts for use with run_subagent tool.

**Use Case:**
- Discover available prompts before creating subagents
- Find appropriate prompt for specialized tasks
- Get prompt IDs for run_subagent systemPromptId parameter

**Workflow:**
1. Agent: "What system prompts are available?"
2. Uses list_system_prompts tool
3. Gets list with IDs and descriptions
4. Agent: "Create subagent with [prompt name]"
5. Uses run_subagent with systemPromptId from discovery

**Parameters:**
- None (no parameters required)

**Example:**
```json
{
  "name": "list_system_prompts",
  "arguments": {}
}
```

**Example Output:**
```
Available System Prompts:

ID: 550E8400-E29B-41D4-A716-446655440000
Name: Code Reviewer
Description: Specialized in code review and quality analysis

ID: 6BA7B810-9DAD-11D1-80B4-00C04FD430C8
Name: Research Analyst
Description: Focused on information gathering and synthesis
```

---

### 15. list_mini_prompts

**Purpose:** Discover available mini-prompts

**Description:**  
List all available mini-prompts with IDs, names, and content. Mini-prompts are reusable contextual information snippets that can be enabled per-conversation.

**What Are Mini-Prompts:**
Mini-prompts contain:
- Personal info (location, system specs)
- Project details (tech stack, architecture)
- Code preferences (style, patterns)
- Technical specs (hardware, software)

**Use Case:**
- Discover contextual information available
- Learn about user preferences and project details
- Understand conversation context

**Parameters:**
- None (no parameters required)

**Example:**
```json
{
  "name": "list_mini_prompts",
  "arguments": {}
}
```

**Example Output:**
```
Available Mini-Prompts:

ID: 123E4567-E89B-12D3-A456-426614174000
Name: Personal Context
Content: Based in Orlando, FL. Uses macOS with M1 Pro. Prefers Swift for system tools.

---

ID: 987F6543-E21C-32F1-B654-426614174001
Name: SAM Project
Content: Working on SAM, a Swift/SwiftUI AI assistant. Architecture: MCP tools, streaming API, conversation management.
```

---

## Multi-Tool Execution

### multi_tool_use.parallel

**Purpose:** Execute multiple tools simultaneously

**Description:**  
GitHub Copilot's parallel tool execution feature. Allows calling multiple tools in a single turn for efficiency. Automatically handled by the AI.

**Example Scenario:**  
Read 3 files simultaneously instead of sequentially, reducing latency from 3 round-trips to 1.

**Usage:** Automatically handled - you don't invoke this directly.

---

## Tool Invocation Format

Tools are invoked using JSON format. GitHub Copilot and OpenAI use slightly different formats:

### GitHub Copilot Format
```json
{
  "finish_reason": "tool_calls",
  "message": {
    "role": "assistant",
    "content": "",
    "tool_calls": [{
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "file_operations",
        "arguments": "{\"operation\":\"read_file\",\"filePath\":\"/path/to/file.txt\"}"
      }
    }]
  }
}
```

### OpenAI Format
```json
{
  "finish_reason": "tool_calls",
  "message": {
    "role": "assistant",
    "tool_calls": [{
      "id": "call_xyz789",
      "type": "function",
      "function": {
        "name": "memory_operations",
        "arguments": "{\"operation\":\"search_memory\",\"query\":\"authentication\"}"
      }
    }]
  }
}
```

Tool results are returned as:
```json
{
  "role": "tool",
  "tool_call_id": "call_abc123",
  "content": "{\"success\":true,\"output\":{\"content\":\"...\",\"mimeType\":\"text/plain\"}}"
}
```

---

## Best Practices

### DO:
- Use `think` for complex multi-step tasks before taking action
- Use `semantic_search` when you need "code that does X" (not exact text match)
- Use `grep_search` for exact text or regex patterns
- Include context lines (3-5) when using `replace_string`
- Tag memories for better retrieval
- Use appropriate similarity thresholds for memory search

### DON'T:
- Use file_operations for web content
- Forget to commit changes with descriptive messages
- Use isBackground=true for commands where you need output
- Get stuck in thinking loops without taking action
- Spawn subagents for simple tasks

---

## Summary

SAM provides 16 comprehensive MCP tools:

| Tool                         | Operations | Category           |
|------------------------------|------------|--------------------|
| think                        | 1          | Core               |
| increase_max_iterations      | 1          | Core               |
| read_tool_result             | 1          | Core               |
| user_collaboration           | 1          | Core               |
| file_operations              | 16         | File & Terminal    |
| terminal_operations          | 11         | File & Terminal    |
| memory_operations            | 4          | Memory & RAG       |
| todo_operations              | 4          | Memory & Planning  |
| recall_history               | 1          | Context Recall     |
| build_and_version_control    | 5          | Version Control    |
| web_operations               | 6          | Web & Documents    |
| document_operations          | 3          | Web & Documents    |
| image_generation             | 1          | Image Generation   |
| run_subagent                 | 1          | Subagent           |
| list_system_prompts          | 1          | Subagent           |
| list_mini_prompts            | 1          | Subagent           |

**Total:** 57 operations across 16 tools

For additional help:
- [API Reference](../developer/api-reference.md) - REST API documentation
- [Getting Started](../end-user/getting-started.md) - Usage tutorials
- [Architecture](../developer/architecture.md) - Technical details

