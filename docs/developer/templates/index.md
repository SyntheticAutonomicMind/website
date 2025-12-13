# Unbroken Method Templates

Ready-to-use templates for implementing The Unbroken Method in your AI-assisted development workflow.

---

## Choose Your Starting Point

### [Quick Start Prompt](quick-start-prompt.md)
**Best for:** Getting started immediately, trying out the methodology, simple projects

A minimal, one-page prompt covering the essential principles. Copy, paste, and start working.

### [Full Collaboration Prompt](full-collaboration-prompt.md)
**Best for:** Serious projects, teams adopting the methodology, complex multi-session work

Complete prompt with all seven pillars, anti-patterns, session protocols, and customization guidance.

### [Handoff Templates](handoff-templates.md)
**Best for:** Multi-session projects, team handoffs, context preservation

Templates for the four-document handoff protocol: CONTINUATION_PROMPT, AGENT_PLAN, FEATURES, and CHANGELOG.

### [Anti-Pattern Template](anti-pattern-template.md)
**Best for:** Building your failure catalog, team learning, preventing repeated mistakes

Structure and examples for documenting anti-patterns as you discover them.

### [Collaboration Tool Scripts](collaboration-tool.md)
**Best for:** Programmatic checkpoints, terminal-based workflows, automation

Bash and Python scripts for implementing collaboration checkpoints in your workflow.

---

## Quick Reference: The Seven Pillars

| Pillar | Principle | Key Practice |
|--------|-----------|--------------|
| 1. Continuous Context | Never break the conversation | Checkpoints + structured handoffs |
| 2. Complete Ownership | If you find it, you fix it | No "out of scope" or "separate issue" |
| 3. Investigation First | Understand before acting | Read, search, test, then implement |
| 4. Root Cause Focus | Solve problems, not symptoms | Ask "why?" until you find the cause |
| 5. Complete Deliverables | Finish what you start | No partial solutions or TODOs |
| 6. Structured Handoffs | Perfect context transfer | Four-document protocol |
| 7. Learning from Failure | Codify mistakes | Anti-pattern catalog |

---

## Editor-Specific Setup

### VS Code with GitHub Copilot
Save your prompt as `.github/copilot-instructions.md` in your repository root.

### Cursor
Add to your `.cursorrules` file or project-level settings.

### Claude Projects
Add as project instructions in the Claude web interface.

### ChatGPT
Use as custom instructions or system prompt.

### Other AI Assistants
Most AI assistants support custom instructions or system prompts. Adapt the templates to your tool's format.

---

## Getting Started

1. **Start minimal** - Use the [Quick Start Prompt](quick-start-prompt.md) for your first session
2. **Add as needed** - Incorporate elements from the [Full Prompt](full-collaboration-prompt.md) as you discover needs
3. **Document failures** - When something goes wrong, add it to your [Anti-Pattern Catalog](anti-pattern-template.md)
4. **Plan for handoffs** - When sessions end, use the [Handoff Templates](handoff-templates.md)

---

## Related Documentation

- [The Unbroken Method](../the-unbroken-method.md) - Full methodology explanation
- [Developers Guide](../developers-guide.md) - SAM-specific development practices
- [Contributing Guide](../contributing.md) - How to contribute to SAM
