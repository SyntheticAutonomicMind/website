# Advanced Workflows

**Build systems, not just prompts.**

SAM isn't limited to single conversations. With subagents, shared topics, and MCP tools, you can orchestrate entire projects. Specialized agents working in parallel, sharing knowledge, building on each other's work.

**This guide shows you how to:**
- Spawn subagents that handle complex subtasks autonomously
- Design multi-conversation patterns for large projects
- Automate workflows with SAM's REST API
- Optimize performance for enterprise-scale work

**Real-world results:**
- Research projects spanning hundreds of sources
- Full-stack development from planning to deployment
- Document analysis across massive corpora
- Automated pipelines that run while you sleep

**Who this is for:** Users who've mastered the basics and want to push SAM to its limits. Build systems that use SAM's full capabilities.

---

## Table of Contents

1. [Subagent Workflows](#subagent-workflows)
2. [Multi-Conversation Patterns](#multi-conversation-patterns)
3. [Complex Project Templates](#complex-project-templates)
4. [Automation & Scripting](#automation--scripting)
5. [Performance Optimization](#performance-optimization)
6. [Advanced Tool Usage](#advanced-tool-usage)

---

## Subagent Workflows

### What Are Subagents?

**Subagents** are specialized AI agents spawned by the main conversation to handle specific subtasks.

**Benefits**:
- **Fresh iteration budget** for each subagent
- **Isolated context** for focused, specialized work
- **Parallel execution** of multiple tasks simultaneously
- **Specialized expertise** - each subagent focuses on one aspect

### When to Use Subagents

✅ **Complex Multi-Part Tasks**:
```
Main: "Build a full-stack web application"
├── Subagent 1: Design database schema
├── Subagent 2: Implement REST API
├── Subagent 3: Build React frontend
└── Subagent 4: Write comprehensive tests
```

✅ **Code Review**:
```
Main: "Review this codebase"
├── Subagent 1: Security analysis
├── Subagent 2: Performance audit
├── Subagent 3: Code style review
└── Subagent 4: Test coverage analysis
```

✅ **Research**:
```
Main: "Research AI safety"
├── Subagent 1: Literature review
├── Subagent 2: Current developments
├── Subagent 3: Expert opinions
└── Subagent 4: Synthesis and summary
```

### Subagent Best Practices

**Clear Instructions**:
```
❌ Bad: "Help with the frontend"
✅ Good: "Build React components for user authentication with form validation, 
         error handling, and loading states. Use TypeScript and follow our 
         component structure in src/components/."
```

**Shared Topic Integration**:
```
1. Enable shared topic in your main conversation
2. Spawn subagents - they automatically inherit the topic workspace
3. All subagents collaborate in the same directory
4. Results persist and are available to the main conversation
```

**Iteration Budgeting**:
- Each subagent gets fresh iteration budget
- Can request increases via increase_max_iterations
- Main conversation tracks overall progress

---

## Multi-Conversation Patterns

### Pattern 1: Specialist Team

**Concept**: Multiple persistent conversations, each specialized in one area

```
Shared Topic: "E-Commerce Platform"

Conversations:
├── "Backend Engineer" (Python/Flask expert)
├── "Frontend Developer" (React specialist)
├── "Database Architect" (PostgreSQL expert)
├── "DevOps Engineer" (CI/CD, deployment)
└── "QA Tester" (Test automation)
```

**Workflow**:
1. Start with Backend Engineer for API design
2. Switch to Database Architect for schema
3. Frontend Developer builds UI using API
4. DevOps sets up deployment
5. QA tests everything

**Benefits**:
- Deep specialization per conversation
- Context maintained per domain
- All access shared workspace

### Pattern 2: Pipeline Processing

**Setup**: Sequential conversations for workflow stages

```
Shared Topic: "Content Pipeline"

Pipeline:
"Research" → "Drafting" → "Editing" → "Publishing"
```

**Workflow**:
```
Research Conversation:
- Gathers information
- Stores findings in shared memory
- Saves sources to shared workspace

Drafting Conversation:
- Retrieves research from memory
- Reads source documents
- Creates draft in shared workspace

Editing Conversation:
- Reads draft
- Refines content
- Applies style guidelines

Publishing Conversation:
- Reads final draft
- Formats for publication
- Handles deployment
```

### Pattern 3: Review & Iterate

**Setup**: Primary + Review conversations

```
Shared Topic: "Code Project"

Conversations:
├── "Implementation" (primary development)
└── "Code Review" (analysis and feedback)
```

**Workflow**:
```
Implementation:
1. Writes code
2. Commits to shared workspace
3. Requests review

Code Review:
1. Reads code from workspace
2. Analyzes for issues
3. Stores feedback in memory

Implementation:
1. Retrieves feedback from memory
2. Implements improvements
3. Cycle repeats
```

---

## Complex Project Templates

### Full-Stack Web Application

**Shared Topic Setup**:
```
Topic: "My Web App"

Directory Structure:
~/SAM/My Web App/
├── backend/
├── frontend/
├── tests/
├── docs/
└── deployment/
```

**Conversations**:
1. **"API Development"**
   - System Prompt: Backend expert
   - Model: GPT-4 (complex logic)
   - Working Dir: backend/

2. **"UI Components"**
   - System Prompt: Frontend expert
   - Model: Claude 3.5 Sonnet (creative UI)
   - Working Dir: frontend/

3. **"Database Design"**
   - System Prompt: Database architect
   - Model: GPT-4
   - Working Dir: backend/models/

4. **"Integration Testing"**
   - System Prompt: QA expert
   - Model: GPT-3.5-turbo (sufficient for tests)
   - Working Dir: tests/

**Workflow**:
```
Week 1:
- Database Design: Schema definition
- API Development: CRUD endpoints

Week 2:
- UI Components: Component library
- API Development: Business logic

Week 3:
- Integration Testing: Test all endpoints
- UI Components: Wire up to API

Week 4:
- All conversations: Bug fixes, polish
```

### Research & Writing Project

**Setup**:
```
Topic: "Research Paper on AI Ethics"

Conversations:
1. "Literature Review"
2. "Data Collection"
3. "Analysis"
4. "Writing"
5. "Citations"
```

**Advanced Pattern**:
```
Literature Review:
- Imports multiple PDFs
- Uses Vector RAG for semantic search
- Stores summaries in shared memory
- Tags: "methodology", "findings", "critique"

Data Collection (spawns subagents):
├── Subagent: Web research (latest developments)
├── Subagent: Expert interviews (contact info)
└── Subagent: Dataset analysis

Writing (uses all previous work):
- Retrieves summaries from memory
- Accesses imported papers
- References data collection results
- Synthesizes into coherent paper

Citations:
- Scans all references in paper
- Generates bibliography
- Verifies citation format
```

---

## Automation & Scripting

### API-Based Workflows

**Use SAM's REST API for automation**:

```bash
#!/bin/bash
# Automated code review script

# Start conversation
CONV_ID=$(curl -X POST http://localhost:8080/v1/conversations \
  -H "Content-Type: application/json" \
  -d '{"title":"Automated Review"}' \
  | jq -r '.id')

# Submit code for review
curl -X POST http://localhost:8080/api/chat/completions \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"gpt-4\",
    \"conversationId\": \"$CONV_ID\",
    \"messages\": [{
      \"role\": \"user\",
      \"content\": \"Review this PR for security and performance issues\"
    }]
  }"
```

### Scheduled Workflows

**Daily Summary**:
```bash
# cron: 0 18 * * * /path/to/daily_summary.sh

#!/bin/bash
# Generate daily summary of project progress

curl -X POST http://localhost:8080/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "conversationId": "'$PROJECT_CONV_ID'",
    "messages": [{
      "role": "user",
      "content": "Review git commits from today and summarize progress"
    }]
  }' > ~/daily-summary.txt
```

### Batch Processing

**Process Multiple Files**:
```python
import requests

files = ['file1.py', 'file2.py', 'file3.py']
endpoint = 'http://localhost:8080/api/chat/completions'

for file in files:
    response = requests.post(endpoint, json={
        'model': 'gpt-4',
        'conversationId': conv_id,
        'messages': [{
            'role': 'user',
            'content': f'Analyze {file} for code quality issues'
        }]
    })
    print(f"Results for {file}:", response.json())
```

---

## Performance Optimization

### Context Management

**YaRN Profile Selection**:
```
Small Tasks       → Default (low scaling)
Long Conversations → Extended (medium scaling)
Document Analysis  → Universal (high scaling, default)
Enterprise Docs    → Mega (enterprise scaling)
```

**How to Set**: Click the **Parameters** button in the toolbar to expand Advanced Parameters, then select Context Size.

**Manual Context Pruning**:
```
When context fills:
1. Clear less important messages
2. Summarize earlier parts
3. Store summaries in memory
4. Continue with clean context
```

### Memory Optimization

**Regular Cleanup**:
```
Every few weeks:
1. Review memory statistics
2. Clear low-importance memories (< 0.4)
3. Remove duplicate entries
4. Archive completed project memories
```

**Efficient Storage**:
```
❌ Don't store everything
✅ Store decisions, requirements, and critical information

❌ Don't duplicate across conversations
✅ Use shared topics for related work

❌ Don't use high similarity thresholds for documents
✅ Lower threshold for document search (0.15-0.25)
```

### Model Selection Strategy

**By Task Type**:
```
Quick Q&A          → GPT-3.5-turbo (fast, cheap)
Complex Logic      → GPT-4 (best reasoning)
Creative Writing   → Claude 3.5 Sonnet (creative)
Code Generation    → GitHub Copilot GPT-4 (code-optimized)
Privacy-Critical   → Local MLX/GGUF models (offline)
```

**Cost Optimization**:
```
1. Use cheaper models (GPT-3.5-turbo) for initial drafts
2. Refine with expensive models (GPT-4) when needed
3. Use local models for sensitive or privacy-critical data
4. Enable streaming for better user experience
```

---

## Advanced Tool Usage

### Chaining Multiple Tools

**Pattern**: Research → Store → Retrieve → Create

```
Step 1: Web Research
Tool: web_operations (research)
Result: Stores findings in memory

Step 2: Memory Retrieval
Tool: memory_operations (search_memory)
Result: Retrieves relevant research

Step 3: Document Creation
Tool: document_operations (create)
Result: Creates final document with citations
```

### Terminal Workflows

**Complex Build Pipeline**:
```
Session 1: "build"
- run_command: "make clean"
- run_command: "make build"
- get_output: Check for errors

Session 2: "test"
- run_command: "pytest tests/"
- get_output: Verify all passed

Session 3: "deploy"
- run_command: "docker build ."
- run_command: "docker push ..."
```

**Persistent Sessions**:
```
Main conversation maintains multiple sessions:
- "backend-server": Running Flask app
- "frontend-dev": React dev server
- "database": PostgreSQL instance
- "monitoring": Logs tail

Switch between sessions as needed
```

### File Operation Optimization

**Bulk Operations**:
```
Instead of:
- create_file (10 times)

Use:
- multi_replace_string (one operation)
- Apply templates efficiently
```

**Smart Search**:
```
Semantic: Find by meaning
"functions that validate user input"

Regex: Find by pattern  
"def.*validate.*\(.*\):"

Glob: Find by filename
"**/test_*.py"
```

---

## Example: Complete Full-Stack Project

**Setup** (Day 1):
```
1. Create shared topic "Task Manager App"
2. Create conversations:
   - "Backend API"
   - "React Frontend"  
   - "Database Schema"
   - "API Tests"
3. Enable shared topic in all conversations
```

**Week 1** (Backend):
```
Backend API conversation:
- Design REST API structure
- Implement user authentication
- Create task CRUD endpoints
- Store API design in shared memory

Database Schema conversation:
- Design tables
- Create migrations
- Document relationships
- Commit schema to shared workspace
```

**Week 2** (Frontend):
```
React Frontend conversation:
- Read API endpoints from shared memory
- Build component library
- Implement routing
- Connect to backend API
- Store component patterns in memory

API Tests conversation:
- Read API from shared workspace
- Write integration tests
- Test all endpoints
- Document test coverage
```

**Week 3** (Polish):
```
All conversations:
- Bug fixes using shared memory of known issues
- Performance optimization
- Documentation
- Deployment preparation

Spawn subagents for:
- Security audit
- Performance testing
- Documentation generation
```

**Result**: Complete application with:
- Fully tested backend
- Polished frontend
- Comprehensive tests
- Complete documentation
- All in shared workspace
- Memory of all decisions

---

## Troubleshooting Advanced Workflows

**Subagents Not Finishing**:
- Increase max iterations in settings
- Break large tasks into smaller, focused subtasks
- Check for circular dependencies in the workflow

**Memory Conflicts**:
- Use clear, distinct tags for different project aspects
- Assign higher importance to critical information
- Review and remove duplicate memories regularly

**Context Overflow**:
- Switch to a higher YaRN profile (Extended, Universal, or Mega)
- Clear less important messages from the conversation
- Summarize old context and store summaries in memory

**Performance Issues**:
- Use appropriate models for each task type
- Optimize context size settings
- Clear terminal session history periodically
- Remove old files from the workspace

---

## Next Steps

- **[Tools Reference](tools-reference.md)** - Master SAM's complete toolset
- **[Configuration](configuration.md)** - Optimize settings
- **[Troubleshooting](troubleshooting.md)** - Fix common issues

**Related**:
- **[Memory & RAG](../end-user/memory-and-rag.md)** - Memory mastery
- **[Shared Topics](../end-user/shared-topics.md)** - Collaboration basics

---

**Level up your SAM workflows and build complex projects efficiently!**
