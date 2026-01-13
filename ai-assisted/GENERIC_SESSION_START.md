# Generic Session Start - SAM Website Documentation

**Purpose:** This document provides complete context for starting a brand new website documentation session when no prior session context is available.

**Date:** January 13, 2026  
**Status:** Template for new contributors or fresh starts

---

## 🎯 YOUR FIRST ACTION

**MANDATORY:** Your very first tool call MUST be:

```bash
cd /Users/andrew/repositories/fewtarius/website
nohup python3 -m http.server 8000 --bind 0.0.0.0 > /dev/null 2>&1 &
```

Then immediately use the collaboration tool:

```bash
scripts/user_collaboration.sh "Session started.

✅ Read THE_UNBROKEN_METHOD.md: yes
✅ Read copilot-instructions: yes
📋 Continuation context: Generic session start (no prior context)
🎯 User request: [Waiting for user to describe tasks]

Web server running at http://localhost:8000

I am ready to collaborate on documentation tasks.

What would you like to work on today? Press Enter:"
```

**WAIT for user response.** They will describe what they need you to work on.

---

## 📋 SESSION INITIALIZATION CHECKLIST

Before starting work, complete these steps:

### 1. Read The Unbroken Method
```bash
cat ai-assisted/THE_UNBROKEN_METHOD.md
```

This is the foundational methodology. The Seven Pillars govern all work:
1. **Continuous Context** - Never break the conversation
2. **Complete Ownership** - Fix every bug you find
3. **Investigation First** - Understand before changing
4. **Root Cause Focus** - Fix problems, not symptoms
5. **Complete Deliverables** - No partial solutions
6. **Structured Handoffs** - Perfect context transfer
7. **Learning from Failure** - Document anti-patterns

### 2. Read Copilot Instructions
```bash
cat .github/copilot-instructions.md
```

This contains website-specific documentation practices, anti-AI writing policy, and workflow.

### 3. Start Web Server (Background)
```bash
cd /Users/andrew/repositories/fewtarius/website
nohup python3 -m http.server 8000 --bind 0.0.0.0 > /dev/null 2>&1 &
```

**CRITICAL**: Use `nohup` and `&` so collaboration tool can block for user input.

### 4. Check Recent Context
```bash
# Recent commits
git log --oneline -10

# Current status
git status

# Look for recent session handoffs
ls -lt project-docs/ | head -20

# Check for uncommitted work
git diff
```

### 5. Use Collaboration Tool (see YOUR FIRST ACTION above)

Wait for user to provide tasks and priorities.

---

## 📚 PROJECT CONTEXT

### What is This Website?

The SAM website (syntheticautonomicmind.org) is a documentation and marketing site for SAM (Synthetic Autonomic Mind), a native macOS AI assistant.

**Purpose:**
- **End-User Documentation** - Getting started, features, use cases
- **Power-User Guides** - Configuration, tools, advanced workflows
- **Developer Documentation** - Architecture, API, building from source
- **Marketing** - Convert visitors into SAM users

**Technology Stack:**
- **Frontend:** Static HTML, CSS, JavaScript
- **Markdown:** Documentation content in `docs/`
- **Viewer:** Custom markdown renderer (`viewer.html`)
- **Hosting:** GitHub Pages (syntheticautonomicmind.org)

### Architecture

```
syntheticautonomicmind.org/
│
├── index.html          # Landing page (marketing)
├── viewer.html         # Markdown documentation viewer
│
├── docs/               # All documentation
│   ├── README.md       # Documentation index
│   ├── end-user/       # Getting started, features, memory
│   ├── power-user/     # Configuration, tools, workflows
│   └── developer/      # Architecture, API, contributing
│
├── css/                # Styles
│   ├── styles.css      # Landing page styles
│   └── markdown.css    # Documentation rendering
│
└── js/                 # JavaScript
    └── main.js         # Viewer logic, link rewriting
```

### Content Organization

**User-First Hierarchy:**

1. **End-User Documentation** (highest priority)
   - `getting-started.md` - Installation, first conversation
   - `features-overview.md` - What SAM can do
   - `memory-and-rag.md` - Memory system guide
   - `shared-topics.md` - Multi-conversation workflows
   - `use-cases.md` - Real-world scenarios

2. **Power-User Documentation**
   - `configuration.md` - Complete settings reference
   - `tools-reference.md` - MCP tools reference
   - `advanced-workflows.md` - Subagents, complex projects
   - `troubleshooting.md` - Common issues

3. **Developer Documentation**
   - `developers-guide.md` - Complete developer guide
   - `the-unbroken-method.md` - AI collaboration methodology
   - `architecture.md` - System design
   - `api-reference.md` - REST API
   - `contributing.md` - How to contribute
   - `building.md` - Build instructions
   - `templates/` - Prompts, handoffs, tools

---

## 🔧 ESSENTIAL COMMANDS

### Web Server
```bash
# Start server (background, MANDATORY for collaboration)
cd /Users/andrew/repositories/fewtarius/website
nohup python3 -m http.server 8000 --bind 0.0.0.0 > /dev/null 2>&1 &

# Open in browser
open http://localhost:8000
open "http://localhost:8000/viewer.html?file=docs/README.md"
```

### Source Code Verification
```bash
# SAM source code is at ../SAM-dist/Sources/
# ALWAYS verify documentation against source

# Example: Verify tool count
cat ../SAM-dist/Sources/MCPFramework/Tools/ToolRegistry.swift | grep "case "

# Example: Verify personality count
cat ../SAM-dist/Sources/ConfigurationSystem/PersonalityManager.swift | grep "Personality("

# Example: Read HelpView for UI workflows
cat ../SAM-dist/Sources/UserInterface/Help/HelpView.swift
```

### Content Search
```bash
# Search documentation
git grep "pattern" docs/

# Search specific file types
git grep "pattern" -- "*.md"

# Search with context
git grep -n -C 3 "pattern" docs/

# Global find and replace (PREFERRED for bulk operations)
git grep -l 'old_text' | xargs sed -i '' 's~old_text~new_text~g'
```

### Anti-AI Writing Detection
```bash
# Find em/en dashes
git grep -E '—|–' -- '*.md' '*.html'

# Find fancy quotes
git grep -E '"|"' -- '*.md' '*.html'

# Find forbidden phrases
git grep -iE "let's dive in|leverage|utilize|seamlessly" docs/
```

### Collaboration (MANDATORY)
```bash
# Use at key checkpoints
scripts/user_collaboration.sh "message"
```

### Git Workflow
```bash
# Commit with clear message
git add -A && git commit -m "docs: description

**Changes:**
- [what changed]

**Testing:**
✅ Links tested in browser
✅ Content verified against source code
✅ Anti-AI writing policy followed"
```

---

## 📂 FILE LOCATIONS

| Purpose | Path |
|---------|------|
| Landing page | `index.html` |
| Documentation viewer | `viewer.html` |
| Documentation | `docs/` |
| End-user guides | `docs/end-user/` |
| Power-user guides | `docs/power-user/` |
| Developer docs | `docs/developer/` |
| Templates | `docs/developer/templates/` |
| Styles | `css/` |
| Scripts | `js/` |
| Collaboration tool | `scripts/user_collaboration.sh` |
| Session handoffs | `project-docs/YYYY-MM-DD/HHMM/` |
| SAM source code | `../SAM-dist/Sources/` |

---

## 📖 KEY DOCUMENTATION

Read these as needed for your work:

### Methodology & Process (MUST READ)
- `ai-assisted/THE_UNBROKEN_METHOD.md` - **Core methodology**
- `.github/copilot-instructions.md` - **Website documentation practices**

### Session Handoffs
- Look in `project-docs/YYYY-MM-DD/HHMM/` for recent work context
- Most recent session will have the latest continuation prompt

### External References
- SAM source code: `../SAM-dist/Sources/`
- HelpView.swift: Primary reference for UI workflows, shortcuts

---

## 🚨 CRITICAL RULES

### Process
1. **Always use collaboration tool** at session start, before implementation, after testing, at session end
2. **Read documentation before changing it** - Investigation first (Pillar 3)
3. **Verify against source code** - Facts must be accurate
4. **Fix all issues you find** - Complete ownership (Pillar 2)
5. **No partial solutions** - Complete deliverables (Pillar 5)

### Writing
1. **No em/en dashes** - Use periods, commas, "and", regular hyphens
2. **No fancy quotes** - Use straight quotes only
3. **No AI phrases** - "Let's dive in", "leverage", "seamlessly", etc.
4. **No arbitrary counts** - "15 tools", "26 personalities" become outdated
5. **No marketing fluff** - "Amazing", "revolutionary", "game-changer"
6. **No changelog content** - Document current state, not version history

### Technical Accuracy
1. **Verify against source** - Read actual code before documenting
2. **Use exact UI labels** - Check SwiftUI source for button text
3. **Document UI paths** - Describe menu paths, not file paths
4. **Test all links** - Links must work in browser
5. **No assumptions** - Verify every fact

### Web Server
1. **Background mode** - Use `nohup ... > /dev/null 2>&1 &`
2. **Collaboration blocks** - Use `isBackground: false` for collaboration tool
3. **Test in browser** - Open http://localhost:8000 to verify changes

---

## ⚠️ ANTI-PATTERNS (DO NOT DO THESE)

❌ Skip session start collaboration checkpoint  
❌ Start web server in foreground (blocks collaboration)  
❌ Use em dashes (—), en dashes (–), fancy quotes (" ")  
❌ Write "let's dive in", "leverage", "seamlessly"  
❌ Add arbitrary feature counts ("15 tools with 54 operations")  
❌ Document features without reading source code  
❌ Label issues as "out of scope" (you own them)  
❌ Create partial implementations ("TODO for later")  
❌ Assume how features work (investigate first)  
❌ End session without user approval  
❌ Commit without testing links  

---

## 🎯 WORKFLOW PATTERN

For each documentation task:

1. **INVESTIGATE**
   - Read existing documentation
   - Verify against SAM source code: `cat ../SAM-dist/Sources/Path/File.swift`
   - Search for patterns: `git grep "pattern" docs/`
   - Understand WHY it's documented this way

2. **CHECKPOINT** (collaboration tool)
   - Share findings
   - Propose changes
   - WAIT for approval

3. **IMPLEMENT**
   - Make exact changes from approved plan
   - Follow anti-AI writing policy
   - Use exact UI labels from source

4. **TEST**
   - Test links in browser: http://localhost:8000
   - Verify rendering in viewer.html
   - Check for broken links
   - Validate against source code

5. **CHECKPOINT** (collaboration tool)
   - Show test results
   - WAIT for approval

6. **COMMIT**
   - Clear commit message with testing details

7. **CONTINUE**
   - Move to next task
   - Keep working until ALL issues resolved

---

## 🤝 COLLABORATION IS MANDATORY

You are working **WITH** a human partner, not **FOR** a human.

- Use `scripts/user_collaboration.sh` at all key points
- WAIT for user response at each checkpoint
- User may approve, request changes, or reject
- This is a conversation, not a command stream

**The methodology works. Follow it exactly.**

---

## 💡 COMMON DOCUMENTATION TASKS

### Adding a New Documentation Page

1. Create file in appropriate directory (`docs/end-user/`, etc.)
2. Write content following anti-AI writing policy
3. Verify all facts against SAM source code
4. Test in viewer.html
5. Add link from `docs/README.md`
6. Add link from `index.html` if user-facing
7. Test all links in browser
8. Commit with clear message

### Fixing Inaccurate Documentation

1. Search for similar inaccuracies: `git grep "pattern" docs/`
2. Read SAM source code to understand truth
3. Fix root cause (not just symptoms)
4. Check for similar errors elsewhere (you own them all)
5. Test in browser
6. Update related documentation if needed
7. Commit with explanation

### Improving Readability

1. Read entire document first
2. Identify awkward phrasing, AI patterns
3. Rewrite for clarity without changing facts
4. Remove em/en dashes, fancy quotes
5. Replace AI phrases with direct language
6. Test in browser
7. Verify technical accuracy unchanged
8. Commit with "Polish" description

### Verifying Button Labels

1. Find relevant SwiftUI View file in `../SAM-dist/Sources/UserInterface/`
2. Search for `Button(` to find button definitions
3. Copy EXACT text from button label
4. Update documentation with exact label
5. Example: `Button("New Personality")` → document as **"New Personality"**

### Checking Link Integrity

1. Start web server: `nohup python3 -m http.server 8000 ... &`
2. Open http://localhost:8000
3. Click through main pages
4. Test at least 5 random documentation links
5. Search for markdown links: `git grep -E '\[.*\]\(.*\.md\)' docs/`
6. Fix broken links immediately (Complete Ownership)

---

## 🔍 SOURCE CODE VERIFICATION

**CRITICAL**: Documentation must match reality. Verify against source code.

### Key Source Directories

| Documentation Topic | Primary Source Files |
|---------------------|---------------------|
| Keyboard shortcuts | `../SAM-dist/Sources/UserInterface/Help/HelpView.swift` |
| Tool parameters | `../SAM-dist/Sources/MCPFramework/Tools/*.swift` |
| Memory/embeddings | `../SAM-dist/Sources/ConversationEngine/VectorDatabase.swift` |
| Providers | `../SAM-dist/Sources/APIFramework/ProviderType.swift` |
| Personalities | `../SAM-dist/Sources/ConfigurationSystem/PersonalityManager.swift` |
| YaRN profiles | `../SAM-dist/Sources/ConversationEngine/YarnConfig.swift` |
| Settings | `../SAM-dist/Sources/UserInterface/Settings/` |

### Verification Checklist

Before committing documentation changes:

- [ ] Technical specifications verified against source
- [ ] Feature descriptions match actual behavior
- [ ] Workflows tested (mentally traced through code)
- [ ] Code examples verified for syntax and correctness
- [ ] API parameters checked against implementations
- [ ] Model/provider lists verified against enums
- [ ] Default values verified against source
- [ ] File paths verified (if mentioned)
- [ ] External links tested
- [ ] Cross-references verified (features/docs exist)

---

## 📊 WEBSITE STRUCTURE

### Landing Page (index.html)

**Purpose:** Convert visitors into users

**Sections:**
- Hero: Main value proposition
- Features: Key capabilities
- Quick Start: Installation steps
- Documentation: Link to docs
- Community: Support and contribution

**Style:** Marketing-focused, benefit-driven, action-oriented

### Documentation Viewer (viewer.html)

**Purpose:** Render markdown documentation

**Features:**
- Automatic link rewriting (markdown → viewer URLs)
- Syntax highlighting
- Responsive design
- Navigation breadcrumbs

**Link Format:** `/viewer.html?file=docs/category/filename.md`

### Documentation Index (docs/README.md)

**Purpose:** Central navigation hub

**Sections:**
- Quick navigation by user type
- At-a-glance feature list
- External links (GitHub, Patreon, CC license)

**Style:** Organized, scannable, benefit-focused intros

---

## 🎨 WRITING STYLE GUIDELINES

### Tone
- Professional but friendly
- Direct and concise
- Helpful, not condescending
- Technical accuracy without unnecessary complexity

### Formatting
- Sentence case for headings ("Getting started", not "Getting Started")
- **Bold** for emphasis, not *italics*
- Code blocks specify language: ` ```swift `, ` ```bash `
- Lists: `-` for unordered, `1.` for ordered

### File Naming
```
✅ getting-started.md
✅ memory-and-rag.md
✅ tools-reference.md

❌ GettingStarted.md
❌ Memory_And_RAG.md
❌ 01-tools-reference.md
```

### Forbidden Characters
- ❌ Em dashes (—)
- ❌ En dashes (–)
- ❌ Fancy quotes (" ")
- ✅ Regular hyphens (-)
- ✅ Straight quotes (")

### Forbidden Phrases
- ❌ "Let's dive in" / "Let's explore"
- ❌ "Without further ado"
- ❌ "At its core" / "At the heart of"
- ❌ "Seamlessly" / "Effortlessly"
- ❌ "Leverage" (use "use")
- ❌ "Utilize" (use "use")
- ❌ "A myriad of" / "Plethora"
- ❌ "Game-changer" / "Revolutionary"

---

## 📞 GETTING STARTED

**Your next steps:**

1. Start web server in background (see YOUR FIRST ACTION at top)
2. Use collaboration tool (see YOUR FIRST ACTION at top)
3. WAIT for user to describe tasks
4. Read relevant documentation for context
5. Verify facts against SAM source code
6. Discuss approach with user via collaboration tool
7. Begin work using the WORKFLOW PATTERN above

**Remember:**
- Investigation before changes
- Verification against source code
- Checkpoint before committing
- Test in browser
- Collaborate throughout

**The methodology works. Follow it exactly.**

Good luck! 🚀
