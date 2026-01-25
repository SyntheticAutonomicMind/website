# CLIO Project Instructions - SAM Website

**Project:** SAM (Synthetic Autonomic Mind) Official Documentation Website  
**Language:** Markdown, HTML, CSS, JavaScript  
**Architecture:** Static documentation site with markdown viewer  
**Purpose:** Provide comprehensive, accurate documentation for SAM users (end-users, power-users, developers)

---

## CRITICAL: READ FIRST BEFORE ANY WORK

### The Unbroken Method (Core Principles)

This project follows **The Unbroken Method** for human-AI collaboration. This isn't just project style—it's the core operational framework.

**The Seven Pillars:**

1. **Continuous Context** - Never break the conversation. Maintain momentum through collaboration checkpoints.
2. **Complete Ownership** - If you find a bug, fix it. No "out of scope."
3. **Investigation First** - Read documentation and verify against source code before changing it. Never assume.
4. **Root Cause Focus** - Fix documentation problems, not symptoms.
5. **Complete Deliverables** - No "TODO" placeholders or draft sections. Finish what you start.
6. **Structured Handoffs** - Document everything for the next session.
7. **Learning from Failure** - Document mistakes to prevent repeats.

**If you skip this, you will violate the project's core methodology.**

### Collaboration Checkpoint Discipline

**Use collaboration tool at EVERY key decision point:**

| Checkpoint | When | Purpose |
|-----------|------|---------|
| After Investigation | Before any changes | Share findings, get approval for changes |
| After Implementation | Before commit | Show results, verify accuracy |

**[FAIL]** Make documentation changes without investigation  
**[OK]** Investigate freely, but checkpoint before committing changes

---

## Quick Start for Documentation Work

### Before Editing Any Documentation

1. **Understand the project:**
   ```bash
   cat README.md                    # Project overview
   cat .github/copilot-instructions.md  # Documentation standards
   ```

2. **Know the standards:**
   - All files: `lowercase-with-hyphens.md`
   - Markdown rendering via `viewer.html`
   - Internal links must work
   - Technical facts verified against SAM source code (`../SAM-dist/Sources/`)
   - No broken links

3. **Use the workflow:**
   ```bash
   python3 -m http.server 8000     # Start local web server
   # Open http://localhost:8000 in browser
   ```

### Core Workflow

```
1. Investigate: Read existing content and source code
2. Checkpoint: Use collaboration tool to propose changes
3. Implement: Make the changes
4. Verify: Test locally, check links, verify accuracy
5. Commit: Make clear commit with message
```

---

## Key Directories & Files

### Core Files
| File | Purpose |
|------|---------|
| `index.html` | Landing page and feature showcase |
| `viewer.html` | Markdown documentation viewer with rendering engine |
| `README.md` | Repository documentation and project overview |
| `.github/copilot-instructions.md` | AI assistant guidelines and documentation standards |
| `css/styles.css` | Global styling |
| `css/markdown.css` | Markdown-specific rendering styles |

### Key Directories
| Path | Purpose | Status |
|------|---------|--------|
| `docs/` | All documentation content | [OK] Primary work area |
| `docs/README.md` | Documentation index | [OK] Main reference |
| `docs/end-user/` | End-user guides | [OK] Content here |
| `docs/power-user/` | Advanced configuration guides | [OK] Content here |
| `docs/developer/` | Developer guides | [OK] Content here |
| `docs/architecture/` | Deep technical documentation | [OK] Content here |
| `scripts/` | Utility scripts | [OK] Scripts directory |
| `project-docs/` | Session handoffs and context | [OK] For between-session continuity |
| `.clio/` | CLIO session files | [OK] Session management |

---

## Source Code Verification (MANDATORY)

**CRITICAL**: Before documenting ANY feature, verify against SAM's source code at `../SAM-dist/Sources/`.

This is NOT optional. All documentation must be technically accurate and verified.

### Verification Process

1. **Read relevant source files** before writing or updating documentation
2. **Confirm feature behavior** matches actual SAM implementation
3. **Use correct terminology** from the codebase
4. **Never assume** - always verify against source

### Key Source Directories

| Directory | Contains |
|-----------|----------|
| `../SAM-dist/Sources/UserInterface/` | UI components, settings views, workflows |
| `../SAM-dist/Sources/UserInterface/Help/HelpView.swift` | **SOURCE OF TRUTH** for user workflows, keyboard shortcuts, menu paths |
| `../SAM-dist/Sources/APIFramework/` | Provider integration, conversation management |
| `../SAM-dist/Sources/ToolService/` | MCP tools and operations |
| `../SAM-dist/Sources/ConfigurationSystem/` | Settings, prompts, personalities |
| `../SAM-dist/Sources/DatabaseService/` | Memory, embeddings, storage |
| `../SAM-dist/Sources/ConversationEngine/` | Conversation settings, YaRN profiles |
| `../SAM-dist/Sources/StableDiffusionIntegration/` | Image generation features |

### Content Validation Checklist

Before committing ANY documentation change:

- [ ] **Terminology** - Matches source code exactly
- [ ] **Feature descriptions** - Confirm features exist as described
- [ ] **Workflows/procedures** - Steps are technically correct
- [ ] **Code examples** - Syntax and parameters verified
- [ ] **Model/provider lists** - Current in source code
- [ ] **File paths** - Verified against actual installation
- [ ] **Default values** - Match source code defaults
- [ ] **API parameters** - All documented parameters exist
- [ ] **External links** - URLs are valid and relevant
- [ ] **Cross-references** - Links exist and work locally

### How to Validate During Investigation

```
1. Read the documentation being modified
2. For each technical claim/fact/number:
   a. Identify the source file that would contain this
   b. Read the source file: cat ../SAM-dist/Sources/Path/File.swift
   c. Verify claim matches source code
   d. Document your findings
3. For each workflow/procedure:
   a. Trace through UI code in UserInterface/
   b. Verify buttons/menus/paths exist and work as described
   c. Check HelpView.swift for canonical keyboard shortcuts
4. After investigation: Use collaboration checkpoint tool
```

---

## Documentation Standards

### File Naming Convention
- All files: `lowercase-with-hyphens.md`
- Examples: `getting-started.md`, `memory-and-rag.md`, `tools-reference.md`

### Content Principles
1. **Clarity First** - Every sentence must be natural, readable, and helpful
2. **User-Focused** - Organized by what users want to accomplish
3. **Technically Accurate** - All facts verified against SAM source code
4. **Consistent** - Uniform tone, style, and formatting

### Writing Style
- **Tone**: Professional but friendly, direct and concise
- **Voice**: Active voice preferred
- **Technical Terms**: Introduce simply, then use proper terminology
- **Examples**: Concrete and actionable
- **Headings**: Clear hierarchy, descriptive
- **Lists**: Use bullets/numbers logically

### Markdown Formatting
```markdown
# Main Title (H1 - only one per file)

## Section (H2)

### Subsection (H3)

**Bold** for emphasis, `code` for inline code

[Link text](path/to/file.md) for internal links
[External](https://example.com) for external links

- Bullet list
- With items

1. Numbered list
2. With sequence

> Block quote for important notes

\`\`\`language
code block
\`\`\`
```

### Link Conventions
- **Internal links**: Use relative paths, e.g., `[Getting Started](getting-started.md)`
- **Cross-section links**: E.g., `[See memory guide](../guides/memory.md)`
- **External links**: Full URLs, e.g., `[Documentation](https://example.com)`
- **Viewer.html links**: Use `?file=` parameter for navigation

---

## Testing & Verification

### Before Committing Changes

1. **Start local web server**:
   ```bash
   python3 -m http.server 8000
   # Open http://localhost:8000 in browser
   ```

2. **Verify all changes**:
   - [ ] Modified markdown files render correctly
   - [ ] All internal links work (click through pages)
   - [ ] No broken links in modified files
   - [ ] Formatting looks correct
   - [ ] Code examples are readable

3. **Check technical accuracy**:
   - [ ] Verified against SAM source code
   - [ ] Terminology matches source code
   - [ ] Features described actually exist
   - [ ] Keyboard shortcuts are correct (per HelpView.swift)

4. **Manual testing**:
   - Render page in `viewer.html`
   - Click all internal links
   - Check mobile responsiveness (if applicable)
   - Verify dark theme displays correctly

---

## Commit Workflow

### Commit Message Format
```bash
docs: <action> <file/component> for <reason>

# Examples:
docs: Polish getting-started.md for readability
docs: Fix broken links in memory guide
docs: Add missing Stable Diffusion configuration examples
docs: Update keyboard shortcuts per HelpView.swift
```

### Before Committing: Checklist
- [ ] Tested locally (`python3 -m http.server 8000`)
- [ ] Clicked through pages and verified links work
- [ ] No broken links in modified files
- [ ] Consistent formatting with existing content
- [ ] Technical facts verified against SAM source
- [ ] No placeholder/TODO/draft sections
- [ ] Commit message explains WHAT and WHY

---

## Anti-Patterns: NEVER DO THESE

| Anti-Pattern | Why | What To Do Instead |
|--------------|-----|-------------------|
| Skip source code verification | Creates incorrect documentation | Always verify against SAM source |
| Leave TODO/draft sections | Technical debt | Complete the documentation |
| Assume feature behavior | Documentation becomes inaccurate | Read source code, verify |
| Commit without local testing | Breaks website rendering | Test locally before commit |
| Broken internal links | Poor user experience | Test all links locally |
| Inconsistent terminology | Confuses users | Use terms from source code |
| Make assumptions about workflows | Users get incorrect instructions | Verify against HelpView.swift |

---

## Development Tools & Commands

### Local Development
```bash
# Start local web server
python3 -m http.server 8000

# Open in browser
open http://localhost:8000

# Check for broken links (after editing)
# Click through modified pages manually

# Check git status
git status
git log --oneline -10
```

### Common Tasks
```bash
# See what changed
git diff docs/getting-started.md

# Review before committing
git status
cat docs/your-file.md

# Check file exists
ls -la docs/category/filename.md

# Search documentation
grep -r "search term" docs/
```

### Verification Commands
```bash
# Check file encoding and format
file docs/your-file.md

# Verify markdown syntax
cat docs/your-file.md | head -20

# Find all links in a file
grep -o '\[.*\](.*\.md)' docs/your-file.md
```

---

## Documentation Categories

### End-User Documentation (`docs/end-user/`)
**Target Audience**: Users learning SAM basics, getting started

**Topics**:
- Getting started guides
- Feature overview
- Basic usage patterns
- FAQ

**Standards**:
- Simple, friendly tone
- No advanced technical jargon
- Step-by-step instructions
- Real-world examples

### Power-User Documentation (`docs/power-user/`)
**Target Audience**: Advanced users configuring SAM

**Topics**:
- Advanced configuration
- Tool integration
- Optimization techniques
- Complex workflows

**Standards**:
- Technical but accessible
- Assume familiarity with basics
- Detail parameter options
- Include examples and use cases

### Developer Documentation (`docs/developer/`)
**Target Audience**: Developers extending SAM

**Topics**:
- API reference
- Tool development
- Integration guides
- Custom providers

**Standards**:
- Technical and precise
- Code examples required
- API parameters documented
- Error handling explained

### Architecture Documentation (`docs/architecture/`)
**Target Audience**: Technical architects and developers

**Topics**:
- System design
- Component relationships
- Data flow
- Internal protocols

**Standards**:
- Deep technical detail
- Diagrams recommended (Mermaid)
- Design decisions explained
- Performance implications discussed

---

## Collaboration Checkpoints

### After Investigation (BEFORE Implementation)
Use this checkpoint when you've researched a documentation change:

**What to include:**
- What you found during investigation
- Documentation inconsistencies discovered
- Specific files/sections to modify
- Proposed changes (be explicit)
- How you verified accuracy
- Link testing plan

**Example format**:
```
Investigation complete. Here's what I found:

[SEARCH] Source code verification:
- Verified keyboard shortcuts in HelpView.swift
- Confirmed feature exists in ConversationEngine
- Updated terminology to match source code

[TARGET] Proposed changes:
- Update docs/power-user/advanced-config.md
- Fix 2 broken links to memory guide
- Add missing YaRN profile examples

[VERIFY] Testing plan:
- Render page locally in viewer.html
- Click all internal links
- Compare against HelpView.swift

Approve? [User confirms to proceed]
```

### After Implementation (BEFORE Commit)
Use this checkpoint when changes are complete:

**What to include:**
- Files modified
- Testing results
- Link verification
- Accuracy verification status

**Example format**:
```
Implementation complete. Results:

[FILES] Modified:
- docs/power-user/advanced-config.md (added YaRN examples)
- docs/README.md (fixed 2 broken links)

[VERIFY] Testing:
- [OK] Renders in viewer.html
- [OK] All internal links work (tested manually)
- [OK] Keyboard shortcuts match HelpView.swift
- [OK] Code examples verified

[STATUS] Complete and ready to commit

Ready to commit?
```

---

## Quick Reference

### Documentation File Structure
```
docs/
├── README.md                    # Documentation index
├── end-user/
│   ├── getting-started.md
│   ├── features-overview.md
│   └── ...
├── power-user/
│   ├── advanced-configuration.md
│   ├── tools-reference.md
│   └── ...
├── developer/
│   ├── api-reference.md
│   ├── custom-tools.md
│   └── ...
└── architecture/
    ├── system-design.md
    ├── data-flow.md
    └── ...
```

### Key Files to Reference
- **Source of Truth for Workflows**: `../SAM-dist/Sources/UserInterface/Help/HelpView.swift`
- **Documentation Standards**: `.github/copilot-instructions.md`
- **Project README**: `README.md`
- **Documentation Index**: `docs/README.md`

### Important Reminders
- **Verify everything** against SAM source code (`../SAM-dist/Sources/`)
- **Test locally** before committing (`python3 -m http.server 8000`)
- **Check all links** work in local browser
- **Use collaboration tool** at checkpoints
- **Complete deliverables** - no TODOs or placeholders
- **Match terminology** from source code exactly

---

## Session Handoff Procedures (MANDATORY)

### CRITICAL: Session Handoff Directory Structure

When ending a session, **ALWAYS** create a properly structured handoff directory:

```
ai-assisted/YYYYMMDD/HHMM/
├── CONTINUATION_PROMPT.md  [MANDATORY] - Next session's complete context
├── AGENT_PLAN.md           [MANDATORY] - Remaining priorities & blockers
├── CHANGELOG.md            [OPTIONAL]  - User-facing changes (if applicable)
└── NOTES.md                [OPTIONAL]  - Additional technical notes
```

**NEVER COMMIT** `ai-assisted/` or `project-docs/` directories to git. Always verify before committing:

```bash
git status  # Ensure no handoff files staged
git add -A
git status  # Double-check
git commit -m "message"
```

**Handoff should include:**
- Current state of documentation
- In-progress work and status
- Next steps for next session
- Key decisions made
- Lessons learned
- Links to relevant source files

---

## Contact & Resources

**SAM Project**: https://github.com/SyntheticAutonomicMind/SAM  
**Website Repository**: https://github.com/SyntheticAutonomicMind/website  
**Live Documentation**: https://www.syntheticautonomicmind.org

**For Questions**:
- Check existing documentation in `docs/`
- Review source code in `../SAM-dist/Sources/`
- Refer to `.github/copilot-instructions.md` for detailed guidelines
