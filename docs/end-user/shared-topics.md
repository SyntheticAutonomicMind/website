# Shared Topics Guide

**Your project. Multiple AI experts. One shared brain.**

Building something big? Imagine having a team of AI specialists: one handling your backend, another perfecting your frontend, a third writing tests. All sharing the same codebase, the same memory, the same context. That's exactly what Shared Topics delivers.

With most AI tools, every conversation starts from scratch. With SAM, conversations *collaborate*. Decisions made in one conversation are instantly available to others. Files created by one agent are visible to all. Knowledge compounds over time.

**This guide covers:**
- How Shared Topics transform complex project work
- When to use them (and when regular conversations work better)
- Step-by-step setup for your first shared workspace
- Real-world workflows that become simpler with shared context

Let's build something big together.

---

## Table of Contents

1. [What Are Shared Topics?](#what-are-shared-topics)
2. [When to Use Shared Topics](#when-to-use-shared-topics)
3. [Creating a Shared Topic](#creating-a-shared-topic)
4. [Using Shared Topics](#using-shared-topics)
5. [Real-World Examples](#real-world-examples)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## What Are Shared Topics?

**Shared Topics** are named workspaces where multiple conversations collaborate on the same project.

**The Core Idea**:
Instead of each conversation having its own isolated workspace, shared topics create a common workspace that multiple conversations can access together.

**What Gets Shared**:
- 📁 **Files**: All conversations see the same directory (`~/SAM/{topic-name}/`)
- 🧠 **Memory**: Memories stored by one conversation accessible to all
- 💻 **Terminal Sessions**: Working directory shared across conversations
- 📄 **Documents**: RAG documents imported once, searchable by all

**What Stays Separate**:
- Conversation history (messages)
- Model selection
- System prompts
- Advanced parameters

---

## When to Use Shared Topics

### Perfect For:

✅ **Complex Projects with Multiple Aspects**
```
Example: Web Application Development
- One conversation handles frontend
- Another handles backend
- Another handles database
- Another handles testing
All working in the same ~/SAM/My Web App/ directory
```

✅ **Team-Like Collaboration**
```
Example: Research Project
- Literature review conversation
- Data analysis conversation
- Writing conversation
All accessing the same papers and findings
```

✅ **Specialized Workflows**
```
Example: Content Creation
- Research conversation gathers information
- Writing conversation creates content
- Editing conversation refines output
All sharing source materials and drafts
```

### Not Ideal For:

❌ **Unrelated Projects**
```
Personal notes + Work project = Use separate conversations
```

❌ **Privacy-Sensitive Work**
```
Different clients' projects = Keep isolated
```

❌ **Temporary Explorations**
```
Quick experiments = Use regular conversation
```

---

## Creating a Shared Topic

### Step 1: Open Preferences

- Click **SAM** menu → **Preferences** (or press ⌘,)
- Navigate to **Shared Topics** tab

### Step 2: Create Topic

In the **Shared Topics** section:
1. Enter a descriptive name in the **"Topic name"** field:
   - ✅ Good: "My Web Application", "Research Project 2025"
   - ❌ Avoid: "Project1", "Stuff", "Test"
2. Add description in the **"Description (optional)"** field:
   - Example: "Full-stack web app with React frontend and Flask backend"
3. Click the **Create** button

### Step 3: Verify Creation

After creation:
- Topic appears in list
- Directory created at `~/SAM/{topic-name}/`
- Topic available for selection in conversations

**Verify in Terminal**:
```bash
ls ~/SAM/
# You should see your topic directory
```

---

## Using Shared Topics

### Enable in Conversation

**Step 1: Enable Shared Topic Toggle**
- In the conversation toolbar, find the **"Shared Topic"** toggle
- Turn it ON

**Step 2: Select Your Topic**
- When enabled, a topic picker dropdown appears next to the toggle
- Select your topic from the dropdown
- If no topics exist, click the orange **"No Topics - Create One"** link to open Preferences

**Step 3: Verify**
- Working directory should show: `~/SAM/{topic-name}/`
- Memory scope changes to topic scope

### Working Directory Changes

**Before (Regular Conversation)**:
```
Working Directory: ~/SAM/My Conversation/
└── Files isolated to this conversation
```

**After (Shared Topic Enabled)**:
```
Working Directory: ~/SAM/My Web Application/
└── Files shared across all conversations using this topic
```

### Create Multiple Conversations

**Scenario**: Building a web application

**Setup**:
1. Create shared topic "My Web Application"
2. Create conversations:
   - "Backend API Development"
   - "Frontend React UI"
   - "Database Design"
   - "Testing & QA"
3. Enable shared topic in each conversation
4. Select "My Web Application" from dropdown

**Result**:
All conversations now work in `~/SAM/My Web Application/`

---

## Real-World Examples

### Example 1: Full-Stack Web Development

**Goal**: Build a complete web application

**Setup**:
```
Shared Topic: "E-Commerce Platform"

Conversations:
1. "Backend API" - Handles server-side logic
2. "Frontend React" - Builds user interface
3. "Database Schema" - Designs data models
4. "API Documentation" - Documents endpoints
5. "Testing" - Writes tests for all components
```

**Workflow**:

**Day 1 - Backend Conversation**:
```
You: Create a Flask API with user authentication
SAM: Created in ~/SAM/E-Commerce Platform/backend/
- app.py
- models.py
- auth.py
```

**Day 2 - Frontend Conversation**:
```
You: Read the backend API endpoints and create React components
SAM: [Reads backend/app.py from shared workspace]
Found endpoints: /login, /register, /products
Creating React components...
```

**Day 3 - Testing Conversation**:
```
You: Write integration tests for the API
SAM: [Accesses both backend and frontend code]
Creating tests in ~/SAM/E-Commerce Platform/tests/
```

**Benefits**:
- Each conversation specialized in its domain
- No manual file copying between conversations
- All see latest code changes
- Shared memory of architecture decisions

### Example 2: Research & Writing

**Goal**: Write a research paper

**Setup**:
```
Shared Topic: "AI Safety Research"

Conversations:
1. "Literature Review" - Reads and summarizes papers
2. "Data Analysis" - Analyzes research data
3. "Writing" - Drafts paper sections
4. "Citations" - Manages references
```

**Workflow**:

**Literature Review Conversation**:
```
You: Import these 15 research papers
SAM: Imported to ~/SAM/AI Safety Research/papers/
All indexed for semantic search

You: Summarize key themes across papers
SAM: [Analyzes all papers]
Key themes: 1) Alignment problem 2) Value learning...
[Stores summary in shared memory]
```

**Writing Conversation**:
```
You: Write introduction section using the literature review
SAM: [Retrieves summaries from shared memory]
[Reads paper summaries from shared directory]
Drafting introduction...
```

**Citations Conversation**:
```
You: Generate bibliography from all cited papers
SAM: [Scans papers/ directory and writing/ drafts]
Creating bibliography.bib...
```

### Example 3: Software Refactoring

**Goal**: Refactor a large codebase

**Setup**:
```
Shared Topic: "Legacy Code Refactor"

Conversations:
1. "Code Analysis" - Understands existing code
2. "Architecture Design" - Plans new structure
3. "Implementation" - Writes refactored code
4. "Testing" - Ensures behavior unchanged
```

**Workflow**:

**Code Analysis**:
```
You: Analyze this codebase and identify code smells
SAM: Analyzing ~/SAM/Legacy Code Refactor/src/...
Found issues:
- God objects in user_manager.py
- Circular dependencies
- Missing error handling
[Stores analysis in memory]
```

**Architecture Design**:
```
You: Design new architecture addressing the code smells
SAM: [Retrieves analysis from shared memory]
Proposed architecture:
- Separate user service
- Dependency injection
[Saves design doc to shared workspace]
```

**Implementation**:
```
You: Implement the new user service
SAM: [Reads design doc from shared workspace]
[Reads existing code]
Creating refactored user_service.py...
```

**Testing**:
```
You: Write tests to ensure refactor preserves behavior
SAM: [Reads old and new code]
Creating comprehensive test suite...
```

---

## Best Practices

### Naming Topics

**Good Names** (descriptive and specific):
- "Customer Portal Project"
- "AI Chatbot MVP"
- "Q1 2025 Website Redesign"

**Bad Names** (avoid these):
- Generic: "Project", "Work", "Stuff"
- Vague: "Project1", "Test", "New"
- Too long: "The complete redesign of our customer-facing..."

### Organizing Conversations

**Use Clear, Descriptive Names**:
```
✅ Good:
- "Backend API Development"
- "Frontend Components"
- "Database Schema Design"

❌ Avoid:
- "Conversation 1"
- "Work"
- "Main"
```

**Find the Right Level of Specialization**:
```
Too Broad:
❌ One conversation trying to do everything

Too Narrow:
❌ Separate conversation for each tiny file

Just Right:
✅ One conversation per major component or aspect
```

### File Organization

**Create Clear Structure**:
```
~/SAM/My Project/
├── backend/
│   ├── api/
│   ├── models/
│   └── tests/
├── frontend/
│   ├── components/
│   ├── pages/
│   └── styles/
├── docs/
└── scripts/
```

**Benefits**:
- Easy to navigate
- Clear ownership
- Prevents conflicts

### Memory Management

**Store Project Decisions**:
```
Backend conversation:
"Remember: We chose PostgreSQL over MySQL for better JSON support"

Later in Frontend conversation:
"What database are we using and why?"
→ SAM retrieves from shared memory
```

**Tag Appropriately**:
```
Store with tags:
- "architecture"
- "database"
- "decision"

Easy to find later across conversations
```

### Cleaning Up

**When Your Project is Complete**:
1. Export important conversations to save them
2. Backup the workspace directory
3. Delete the shared topic (if you no longer need it)
4. Or keep the topic but disable it in conversations to isolate them

**⚠️ WARNING**: Deleting a topic deletes ALL shared memories for that topic!

---

## Troubleshooting

### Files Not Appearing

**Problem**: Files created in one conversation don't appear in another

**Solutions**:
1. **Verify Both Use Same Topic**: Check settings in both conversations
2. **Refresh**: Close and reopen conversation
3. **Check Directory**: Verify files actually in ~/SAM/{topic-name}/
4. **Case Sensitivity**: macOS is case-insensitive but preserves case

### Memory Not Shared

**Problem**: Information stored in one conversation not retrievable in another

**Solutions**:
1. **Both Must Use Topic**: Enable shared topics in both conversations
2. **Same Topic Selected**: Verify topic name matches exactly
3. **Wait for Sync**: Memory operations may take a moment
4. **Check Threshold**: Lower similarity threshold when searching

### Working Directory Confusion

**Problem**: Not sure which directory SAM is using

**Solutions**:
1. **Check Settings Panel**: Working directory shown clearly
2. **Ask SAM**: "What's my current working directory?"
3. **List Files**: "List files in current directory"
4. **Use Reveal in Finder**: Click folder icon in toolbar

### Accidentally Modified Wrong Files

**Problem**: Changed files in wrong topic workspace

**Solutions**:
1. **Check Git History**: If using version control, revert
2. **Restore from Backup**: If you have backups
3. **Review Changes**: Ask SAM to show recent file modifications
4. **Be Careful**: Always verify working directory before operations

### Topic Name Conflicts

**Problem**: Multiple topics with similar names

**Solutions**:
1. **Rename Topics**: Give more descriptive names
2. **Add Dates**: "Project Alpha - 2025", "Project Alpha - 2024"
3. **Delete Unused**: Remove old topics to avoid confusion

---

## Advanced Patterns

### Subagents + Shared Topics

**A Powerful Combination**:
Enable a shared topic, then spawn subagents. All subagents automatically work in the same workspace.

```
Main Conversation: "My App" shared topic enabled

Spawn subagents that collaborate:
├── "API Development" subagent → works in ~/SAM/My App/api/
├── "UI Design" subagent → works in ~/SAM/My App/ui/
└── "Testing" subagent → reads both api/ and ui/

All subagents share the same workspace and knowledge!
```

### Topic Hierarchies (Manual)

Create organized structure:
```
~/SAM/
├── Client A - Project 1/
├── Client A - Project 2/
├── Client B - Project 1/
└── Personal - Research/
```

Each is separate topic, but organized by prefix.

### Switching Contexts

Easily switch between different project contexts by enabling/disabling shared topics:

```
One Conversation: "Architecture Design"

Context 1: Personal Project
- Enable shared topics
- Select "Personal Web App" topic
- Work on your personal code

Context 2: Work Project
- Enable shared topics
- Select "Client XYZ App" topic
- Work on client code

Context 3: Isolated Experiment
- Disable shared topics
- Work in isolated ~/SAM/Architecture Design/ directory
```

---

## Next Steps

**Learn More**:
- **[Memory & RAG](memory-and-rag.md)** - Understanding shared memory
- **[Advanced Workflows](../power-user/advanced-workflows.md)** - Complex patterns
- **[Features Overview](features-overview.md)** - All SAM capabilities

**Try It Out**:
1. Create your first shared topic
2. Set up 2-3 specialized conversations
3. Work on a small project together
4. Experience the collaboration power!

---

**Unlock SAM's full collaborative potential with Shared Topics!**
