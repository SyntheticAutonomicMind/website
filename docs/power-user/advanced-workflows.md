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
3. [LoRA Training Workflows](#lora-training-workflows)
4. [Complex Project Templates](#complex-project-templates)
5. [Automation & Scripting](#automation--scripting)
6. [Performance Optimization](#performance-optimization)
7. [Advanced Tool Usage](#advanced-tool-usage)

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

## LoRA Training Workflows

### Advanced Training Strategies

Fine-tune local models with precision using advanced training techniques and parameter optimization.

**Requirements:**
- Local MLX model installed
- Training data in JSONL format
- macOS with Apple Silicon

### Parameter Tuning Guide

**Rank (4-128)**

Controls adapter capacity and file size:

| Rank | Use Case | File Size | Training Time |
|------|----------|-----------|---------------|
| 4-8 | Writing style, simple patterns | ~15-25MB | Fastest |
| 16-32 | Domain knowledge, terminology | ~30-60MB | Moderate |
| 64-128 | Complex reasoning, large datasets | ~100MB+ | Slower |

**Recommendations:**
- Start with rank 8, increase if model doesn't learn patterns
- Higher rank = more capacity but risk of overfitting
- Use lower rank for small datasets (<100 examples)
- Use higher rank for complex domains (medical, legal, technical)

**Learning Rate**

How fast the model learns:

| Rate | Use Case | Risk |
|------|----------|------|
| 0.00001-0.00005 | Fine-tuning pre-trained adapters | Slow progress |
| 0.0001 | **Default - most cases** | Balanced |
| 0.0005-0.001 | Quick experiments, small datasets | Instability |

**Recommendations:**
- Use default (0.0001) unless you have specific reasons
- Increase if loss plateaus early
- Decrease if loss becomes erratic or increases
- Monitor loss carefully when adjusting

**Epochs (1-50)**

Number of training passes through data:

| Epochs | Use Case | Risk |
|--------|----------|------|
| 1-3 | Quick experiments | Underfitting |
| 5-10 | **Most datasets** | Balanced |
| 15-30 | Large, diverse datasets | Some overfitting |
| 40-50 | Specialized, must memorize | High overfitting |

**Recommendations:**
- Start with 5 epochs
- Watch loss - stop when it plateaus
- More epochs needed for larger datasets
- Fewer epochs for small datasets to prevent memorization

**Batch Size (1-32)**

Examples processed simultaneously:

| Size | Memory | Speed | Use Case |
|------|--------|-------|----------|
| 1-2 | Low | Slower | Large models, limited RAM |
| 4-8 | Medium | **Balanced** | Most cases |
| 16-32 | High | Faster | Small models, ample RAM |

**Recommendations:**
- Start with 4
- Increase for faster training if you have RAM
- Decrease if you get out-of-memory errors
- Higher batch size can improve stability

### Training Data Best Practices

**Quality Over Quantity**

50 high-quality examples beat 500 mediocre ones:

✅ **Good Training Example:**
```jsonl
{"messages": [{"role": "user", "content": "What is our return policy for defective items?"}, {"role": "assistant", "content": "For defective items, we offer full refunds within 90 days of purchase. Contact support@company.com with your order number and photos of the defect. We'll arrange free return shipping and process your refund within 5 business days."}]}
```

❌ **Poor Training Example:**
```jsonl
{"messages": [{"role": "user", "content": "returns?"}, {"role": "assistant", "content": "yes"}]}
```

**Diversity and Coverage**

Cover different aspects of your domain:

**Example: Customer Support Bot**
```
✅ Include examples for:
- Product questions (features, specs, compatibility)
- Pricing and billing
- Shipping and delivery
- Returns and refunds
- Technical support
- Account management
```

**Consistent Formatting**

Use the same chat template throughout:

```bash
# Choose ONE template for all examples:
- Llama 3/4: For Llama models
- Qwen 2.5: For Qwen models
- Mistral: For Mistral/Mixtral models
- Gemma 2/3: For Gemma models
- Phi 3: For Phi models
- Custom: Generic markdown format
```

**PII Protection**

Enable redaction to keep sensitive data out:

**PII Types Detected:**
- Personal names
- Organization names  
- Place names
- Email addresses
- Phone numbers
- Credit card numbers
- Social security numbers
- IP addresses
- URLs

**Recommendation:** Always enable PII redaction unless training on purely public data.

### Document Chunking Strategies

Choose the right strategy for your content type:

**Semantic (Paragraphs)**

Best for: Articles, documentation, books

**How it works:**
- Splits on natural paragraph boundaries
- Preserves context and readability
- Variable chunk sizes

**When to use:**
- Well-structured documents
- Natural topic boundaries
- Readable, flowing text

**Fixed Size**

Best for: Consistent training, mixed content

**How it works:**
- Creates uniform token-sized chunks
- Overlap between chunks for context
- Predictable sizes

**When to use:**
- Mixed document types
- Need consistent chunk sizes
- Technical documentation with irregular formatting

**Page Aware (PDFs)**

Best for: PDF documents with page structure

**How it works:**
- Respects page boundaries
- Keeps page content together
- Useful for cited material

**When to use:**
- PDF documents with clear page structure
- Legal documents (cite by page)
- Academic papers
- Reports with page references

### Multi-Adapter Management

**Organizing Adapters**

Use descriptive names:
```
✅ Good names:
- "Customer Support - Products"
- "Medical Terminology - Cardiology"
- "Code Style - Python FastAPI"
- "Legal Writing - Contract Review"

❌ Poor names:
- "Adapter1"
- "test"
- "new_adapter_v2"
```

**Adapter Versioning**

Track versions in adapter names:
```
"Customer Support v1.0"  → Initial training
"Customer Support v1.1"  → Added FAQ data
"Customer Support v2.0"  → Complete retrain with new guidelines
```

**When to Retrain vs Create New**

**Retrain same adapter when:**
- Fixing mistakes in training data
- Adjusting parameters (rank, epochs)
- Adding more examples to existing domain

**Create new adapter when:**
- Different domain or use case
- Testing different approaches
- Experimental parameters
- Backup before major changes

**Comparing Adapter Performance**

**Method 1: Same Prompts**
```
Test prompt: "What is our warranty coverage?"

Base model: Generic response
Adapter v1: Company-specific, missing details
Adapter v2: Complete, accurate, on-brand
```

**Method 2: Loss Metrics**
```
Lower final loss = Better learning
Adapter A: Loss 1.85 ✅
Adapter B: Loss 2.42 ⚠️
```

**Method 3: Use Case Testing**
```
Create 10 test questions from your domain
Run through base model + each adapter
Score accuracy and style
```

### Advanced Training Workflows

**Iterative Refinement**

1. **Initial Training** (Rank 8, Epochs 5, 50 examples)
   - Train baseline adapter
   - Test with real prompts
   - Identify weaknesses

2. **Data Augmentation** (Add 50 examples targeting gaps)
   - Add examples for weak areas
   - Retrain with same parameters

3. **Parameter Optimization** (Rank 16, Epochs 10)
   - Increase capacity for better learning
   - Monitor loss for overfitting

4. **Final Validation** (Test suite)
   - Run comprehensive test suite
   - Compare to base model and previous versions
   - Deploy best-performing adapter

**Combining LoRA + RAG**

The hybrid approach for maximum effectiveness:

**Use Case: Medical Assistant**

**LoRA Adapter:**
- Trains on medical terminology
- Learns diagnostic reasoning patterns
- Internalizes treatment protocols
- Consistent medical writing style

**RAG (Memory/Documents):**
- Current research papers
- Drug databases (updated frequently)
- Patient guidelines
- Clinical trial results

**Result:** Fast, specialized medical reasoning with access to current information.

**Implementation:**
```
1. Train LoRA on medical textbooks and guidelines
2. Import current research papers as documents
3. Enable vector RAG in conversation
4. Select LoRA adapter in model picker
5. Ask medical questions

→ Model uses LoRA for reasoning + RAG for current facts
```

**Other Hybrid Use Cases:**

**Code Assistant:**
- LoRA: Team's coding style, architecture patterns
- RAG: API documentation, library references

**Customer Support:**
- LoRA: Company voice, common responses, workflow
- RAG: Current product specs, pricing, inventory

**Legal Research:**
- LoRA: Legal reasoning, citation format, writing style
- RAG: Case law database, recent rulings, statutes

### Troubleshooting Training Issues

**Symptom: Loss not decreasing**

**Diagnosis:**
```
Check training logs:
- Loss starts high (~3-5)
- Loss stays flat or increases
- No improvement after multiple epochs
```

**Solutions:**
1. Increase learning rate (0.0001 → 0.0005)
2. Increase epochs (5 → 10)
3. Increase rank (8 → 16)
4. Check data quality (remove duplicates, errors)
5. Add more diverse examples

**Symptom: Loss erratic/increasing**

**Diagnosis:**
```
Loss jumps around wildly
Loss increases instead of decreasing
Training unstable
```

**Solutions:**
1. Decrease learning rate (0.0001 → 0.00005)
2. Reduce batch size (8 → 4)
3. Check for corrupted data
4. Use smaller rank

**Symptom: Adapter memorizes verbatim**

**Diagnosis:**
```
Adapter repeats training examples exactly
No generalization to similar questions
Overfitting
```

**Solutions:**
1. Add more diverse examples
2. Reduce epochs (10 → 5)
3. Reduce rank (32 → 16)
4. Check for duplicate/near-duplicate examples

**Symptom: Out of memory**

**Diagnosis:**
```
Training crashes
"Out of memory" error
System becomes unresponsive
```

**Solutions:**
1. Reduce batch size (4 → 2 or 1)
2. Use smaller base model (7B → 3B)
3. Close other memory-intensive apps
4. Reduce rank (16 → 8)

### Best Practices Summary

**Do:**
✅ Start with conservative parameters (rank 8, epochs 5, LR 0.0001)  
✅ Validate data quality before training  
✅ Enable PII redaction for sensitive data  
✅ Test incrementally (small → larger datasets)  
✅ Compare adapters with same test prompts  
✅ Use descriptive adapter names with versions  
✅ Combine LoRA + RAG for best results  
✅ Monitor loss during training  

**Don't:**
❌ Train on low-quality or error-filled data  
❌ Use too high learning rate (causes instability)  
❌ Mix different chat templates in same dataset  
❌ Skip PII redaction for personal data  
❌ Expect perfect results from tiny datasets  
❌ Train when RAG would work better  
❌ Ignore loss metrics  
❌ Delete adapters without testing first  

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
