# Handoff Templates

**Templates for the four-document handoff protocol used in The Unbroken Method.**

These documents ensure perfect context transfer between sessions, whether you're handing off to yourself tomorrow or to a teammate.

---

## Overview

When a session must end, create these four documents:

| Document | Purpose | Audience |
|----------|---------|----------|
| CONTINUATION_PROMPT | Complete standalone context for next session (consolidates session history) | Next AI session |
| AGENT_PLAN | Remaining work breakdown with investigation steps | Next AI session |
| FEATURES | New features implemented this session | External consumers (website, marketing) |
| CHANGELOG | Detailed changes in standard format | External consumers (release notes) |

**CRITICAL PREREQUISITE:** Before creating handoff documents, ensure ALL technical documentation is up-to-date:
- Subsystem docs if you modified a component
- Flow diagrams if you changed data flows
- Specifications if you completed a feature

**Rule:** Documentation is NOT optional. Code without docs is incomplete work.

---

## 1. CONTINUATION_PROMPT Template

**Purpose:** Everything the next session needs to continue immediately, including session history.

**Critical Rule:** This document must be STANDALONE. No external references. The next session should be able to start productive work with ONLY this document.

```markdown
# Continuation Prompt - [Date] [Time]

## Context Summary
[2-3 sentences: What is this project? What were we working on?]

---

## Completed This Session

### [Task/Feature 1]
- What was done: [Specific description]
- Files modified: [List files]
- Testing performed: [What was tested, results]
- Commits: [Commit hashes/messages]

### [Task/Feature 2]
- What was done: [Specific description]
- Files modified: [List files]
- Testing performed: [What was tested, results]
- Commits: [Commit hashes/messages]

---

## Documentation Updated
- [List any subsystem docs, flow diagrams, or specs that were updated]
- [Or "None" if no documentation changes were needed]

---

## Current State

### Build Status
- Last build: [Success/Failure]
- Build command: `[command]`
- Known warnings: [List or "None"]

### Test Status
- Tests passing: [Yes/No/Partial]
- Test command: `[command]`
- Failing tests: [List or "None"]

### Runtime Status
- Application runs: [Yes/No]
- Known issues: [List or "None"]

---

## Pending Work

### Priority 1: [Task Name]
**Why:** [Why this is important]
**Approach:** [How to tackle it]
**Files involved:** [Key files]
**Success criteria:** [How to know it's done]

### Priority 2: [Task Name]
**Why:** [Why this is important]
**Approach:** [How to tackle it]
**Files involved:** [Key files]
**Success criteria:** [How to know it's done]

---

## Session History (Decisions & Lessons)

### Decisions Made
- **[Decision 1]:** [What was decided and why]
- **[Decision 2]:** [What was decided and why]

### What Worked
- [Successful approach or decision]
- [Successful approach or decision]

### What Didn't Work
- [Failed approach and why]
- [Failed approach and why]

### Anti-Patterns Discovered
- [New anti-pattern to avoid]

---

## Key Files Reference

```
project/
├── [key-file-1]    # [What it does]
├── [key-file-2]    # [What it does]
└── [key-dir/]      # [What it contains]
```

---

## Starting Instructions

**First thing to do:**
1. [Specific first action]
2. [Specific second action]

**Build and verify:**
```bash
[build command]
[test command]
```

**Then continue with:** [Next task from Priority 1]

---

## Critical Reminders

- [Important constraint or rule]
- [Important constraint or rule]
- [Don't forget about X]
```

---

## 2. AGENT_PLAN Template

**Purpose:** Detailed breakdown of remaining work with investigation steps.

```markdown
# Agent Plan - [Date] [Time]

## Remaining Tasks (Priority Order)

---

### Task 1: [Name]

**Priority:** High/Medium/Low
**Estimated Time:** [X hours]
**Dependencies:** [None / Task X must complete first]

**Description:**
[What needs to be done and why]

**Investigation Steps:**
1. [ ] Read [specific file/section]
2. [ ] Search for [pattern/usage]
3. [ ] Test [specific behavior]
4. [ ] [Other investigation]

**Implementation Steps:**
1. [ ] [Specific implementation step]
2. [ ] [Specific implementation step]
3. [ ] [Specific implementation step]

**Testing:**
- [ ] [Test case 1]
- [ ] [Test case 2]
- [ ] Build passes
- [ ] Integration test

**Success Criteria:**
- [Measurable outcome 1]
- [Measurable outcome 2]

---

### Task 2: [Name]

[Same structure as Task 1]

---

## Known Blockers

### Blocker: [Name]
**Impact:** [What it blocks]
**Proposed Solution:** [How to resolve]
**Owner:** [Who can resolve this / needs user input]

---

## Questions for User

- [Question needing clarification]
- [Decision needing user input]

---

## Time Estimates

| Task | Estimate | Notes |
|------|----------|-------|
| Task 1 | X hours | [Any caveats] |
| Task 2 | X hours | [Any caveats] |
| **Total** | **X hours** | |
```

---

## 3. FEATURES Template

**Purpose:** New features implemented this session, for external consumers like website or marketing.

```markdown
# Features - [Date]

## New Features

### [Feature Name]

**What it does:**
[User-facing description of the feature]

**How to use it:**
[Instructions or examples for end users]

**Technical details:**
[Brief technical notes if relevant]

---

### [Feature Name 2]

**What it does:**
[User-facing description]

**How to use it:**
[Instructions or examples]

---

## Improvements

- [Improvement 1]: [Brief description of what got better]
- [Improvement 2]: [Brief description of what got better]

---

## Bug Fixes (User-Facing)

- [Bug fix 1]: [What was broken and is now fixed]
- [Bug fix 2]: [What was broken and is now fixed]

---

## Documentation Updates

- [New doc 1]: [Brief description]
- [Updated doc 1]: [What changed]
```

---

## 4. CHANGELOG Template

**Purpose:** User-facing summary of changes (for release notes, website, etc.).

```markdown
# Changelog - [Date]

## [Version or Date Range]

### Added
- [New feature description]
- [New feature description]

### Changed
- [Change description]
- [Change description]

### Fixed
- [Bug fix description]
- [Bug fix description]

### Removed
- [Removed feature/code description]

### Security
- [Security-related change]

### Breaking Changes
- [Breaking change with migration notes]

---

## Detailed Changes

### [Feature Name]

[Longer description for documentation/marketing purposes]

**What it does:**
[User-facing description]

**How to use it:**
[Instructions or examples]

---

## Migration Notes

[If there are breaking changes, explain how users should update]

---

## Contributors

- [Name/handle] - [Contribution]
```

---

## Usage Tips

### When to Create Handoffs

- **Token limits approaching** - Create full handoff before context is lost
- **Work phase complete** - Document what was accomplished
- **Switching focus** - Preserve context for current work
- **End of day** - Ensure tomorrow picks up seamlessly
- **Team handoff** - Transferring work to another person

### Quality Checklist

Before finalizing handoff documents:

- [ ] CONTINUATION_PROMPT is completely standalone
- [ ] Build/test commands are exact and verified
- [ ] File paths are correct
- [ ] Priority order reflects actual importance
- [ ] Success criteria are measurable
- [ ] Starting instructions are specific
- [ ] No references to "see other document" in CONTINUATION_PROMPT

### Organizing Handoffs

Recommended directory structure:

```
project-docs/
├── YYYY-MM-DD/
│   └── HHMM/
│       ├── CONTINUATION_PROMPT.md
│       ├── AGENT_PLAN.md
│       ├── FEATURES.md
│       └── CHANGELOG.md
```

---

## Related Templates

- [Quick Start Prompt](quick-start-prompt.md) - Minimal collaboration prompt
- [Full Collaboration Prompt](full-collaboration-prompt.md) - Complete prompt
- [Anti-Pattern Template](anti-pattern-template.md) - Document failures
- [Collaboration Tool Scripts](collaboration-tool.md) - Checkpoint automation
