# CLIO - Command Line Intelligence Orchestrator

**Your AI Pair Programming Partner for the Terminal**

---

## What is CLIO?

**CLIO (Command Line Intelligence Orchestrator)** is a terminal-based AI code assistant designed for developers who live in the command line. Built by the Synthetic Autonomic Mind organization, CLIO brings powerful AI capabilities directly into your terminal workflow without the overhead of browser tabs or GUI applications.

CLIO is the perfect companion to SAM—where SAM excels at complex, multi-conversation projects with its visual interface, CLIO provides instant AI assistance for terminal-focused development work.

### Why CLIO?

**Terminal-Native Experience**
- Runs entirely in your terminal with professional markdown rendering
- No browser tabs, no GUI overhead, just clean terminal interaction
- Streaming responses with syntax highlighting and proper formatting
- Color themes and customizable styles

**Portable & Minimal**
- Requires only Perl 5.20+ with core modules (no CPAN/npm/pip dependencies)
- Works on any modern macOS or Linux system
- Single executable that runs anywhere
- Zero external dependencies for core functionality

**Tool-Powered, Not Simulated**
- Real file operations using actual system tools
- Genuine git integration (status, diff, commit, branch, merge)
- Actual terminal command execution
- Action transparency—see exactly what CLIO is doing in real-time

**Privacy & Control**
- All conversations and data stored locally on your machine
- Only minimal context sent to AI providers
- Full control over what code and files are shared
- Same privacy-first philosophy as SAM

**Persistent Sessions**
- Automatically saves all conversations with full history
- Resume any session exactly where you left off
- Complete tool operation history preserved
- Perfect for long-running development tasks

**Custom Instructions**
- Per-project AI behavior via `.clio/instructions.md`
- Enforce coding standards automatically
- Share methodology and best practices
- Same CLIO installation adapts to each project's needs

---

## When to Use CLIO vs SAM

### Use CLIO When:
- Working primarily in the terminal
- Quick code reviews or file operations
- Writing scripts or automation
- Git workflow operations
- Single-threaded development tasks
- Remote development over SSH
- You prefer keyboard-driven workflows
- Working on systems without a GUI

### Use SAM When:
- Managing complex, multi-conversation projects
- Coordinating multiple specialized agents (subagents)
- Working with documents and semantic search
- Training custom models with LoRA
- Image generation with Stable Diffusion
- Building applications requiring visual feedback
- Multi-day projects with extensive context
- Using Shared Topics for team collaboration

### Use Both When:
- Developing SAM projects (recommended workflow)
- Complex codebases requiring different perspectives
- Combining visual design (SAM) with implementation (CLIO)
- Research in SAM, implementation in CLIO

**The Bottom Line:** SAM is your project orchestrator; CLIO is your terminal companion. They complement each other perfectly.

---

## Installation

### Prerequisites

**System Requirements:**
- macOS 10.14+ or Linux (any modern distribution)
- Perl 5.20 or higher (included on macOS, usually on Linux)
- Git (for version control operations)
- ANSI-compatible terminal emulator

**AI Provider Requirements:**
- GitHub Copilot subscription + device flow authentication, OR
- OpenAI API key, OR
- DeepSeek API key, OR
- Other compatible provider API key

### Installation Steps

**1. Clone the Repository**

```bash
git clone https://github.com/SyntheticAutonomicMind/CLIO.git
cd CLIO
```

**2. Run the Installer**

```bash
sudo ./install.sh
```

The installer will:
- Install CLIO executable to `/usr/local/bin/clio`
- Set up library files in `/usr/local/lib/clio/`
- Create configuration directory at `~/.clio/`
- Set proper permissions

**3. Verify Installation**

```bash
clio --help
```

You should see the CLIO help screen with available options.

### Configuration

**GitHub Copilot Setup** (Recommended)

GitHub Copilot is the default and recommended provider. No environment variables needed—just start CLIO and login:

```bash
clio --new
: /login
# Follow browser prompts to authorize with GitHub
# Tokens are saved automatically to ~/.clio/github_tokens.json
```

**Alternative Provider Setup**

For other providers, use interactive `/api` commands:

```bash
clio --new
: /api provider openai
: /api key YOUR_OPENAI_API_KEY
: /api model gpt-4o
: /config save
```

**Supported Providers:**
- `github_copilot` - GitHub Copilot (default, recommended)
- `openai` - OpenAI GPT models
- `deepseek` - DeepSeek models
- `openrouter` - OpenRouter gateway
- `llamacpp` - Local llama.cpp server
- `sam` - Connect to SAM's REST API
- Custom OpenAI-compatible endpoints

---

## Core Features

### File Operations
- **Read files:** `read this file and explain the main function`
- **Write files:** `create a new Python script that processes CSV files`
- **Search:** `find all files containing 'database connection'`
- **Edit:** `refactor the error handling in src/main.py`
- **Manage:** Create, delete, rename files and directories

### Version Control (Git)
- **Status:** `what files have changed?`
- **Diff:** `show me the diff for the last commit`
- **Commit:** `commit these changes with an appropriate message`
- **Branch:** `create a new branch for the authentication feature`
- **Full workflow:** CLIO handles staging, committing, and pushing

### Terminal Operations
- **Execute commands:** `run the test suite`
- **Build tasks:** `compile the project and show any errors`
- **Script execution:** `run the deployment script`
- **Output analysis:** CLIO interprets command output and suggests fixes

### Memory System
- **Store information:** `remember that our API endpoint is https://api.example.com`
- **Recall context:** `what was that configuration we discussed earlier?`
- **Cross-session memory:** Information persists across sessions

### Todo Lists
- **Task management:** `create a todo list for implementing user authentication`
- **Progress tracking:** CLIO automatically updates task status
- **Workflow organization:** Break complex tasks into manageable steps

### Web Operations
- **Fetch content:** `get the documentation from https://example.com/docs`
- **Research:** `what are the best practices for async/await in Python?`
- **Analyze:** CLIO fetches and processes web content for you

### Action Transparency
Every operation CLIO performs is shown in real-time:
```
SYSTEM: [file_operations] - Reading src/main.py (342 lines)
SYSTEM: [terminal_operations] - Executing: python -m pytest tests/
SYSTEM: [version_control] - Git status: 3 files modified, 1 untracked
```

You always know exactly what CLIO is doing.

---

## Custom Instructions for SAM Projects

One of CLIO's most powerful features is **custom instructions** via `.clio/instructions.md`. This lets you enforce project-specific standards, pass methodology, and ensure consistency.

### For SAM Development

When working on SAM projects, create `.clio/instructions.md` in your project root:

```markdown
# CLIO Custom Instructions - SAM Development

**Project:** SAM (Synthetic Autonomic Mind)  
**Language:** Swift 5.9+  
**Platform:** macOS 14.0+

## Core Principles

This project follows **The Unbroken Method** for human-AI collaboration.
See docs/developer/the-unbroken-method.md for complete details.

### The Seven Pillars

1. **Continuous Context** - Never break the conversation
2. **Complete Ownership** - If you find a bug, fix it
3. **Investigation First** - Verify before changing
4. **Root Cause Focus** - Fix problems, not symptoms
5. **Complete Deliverables** - No TODO placeholders
6. **Structured Handoffs** - Document everything
7. **Learning from Failure** - Document mistakes

## Coding Standards

- Swift 5.9+ with modern concurrency (async/await)
- SwiftUI for all UI components
- MVVM architecture pattern
- Comprehensive error handling with Result types
- Unit tests for all business logic
- Integration tests for API interactions

## Before Making Changes

1. Read existing code to understand architecture
2. Check related files and dependencies
3. Verify changes don't break existing functionality
4. Run tests before committing

## Commit Guidelines

- Clear, descriptive commit messages
- Reference issue numbers where applicable
- Group related changes in single commits
- Run `swift test` before committing

## File Organization

- Sources/ - All Swift source code
- Tests/ - Unit and integration tests
- Resources/ - Assets, configs, data files
- Documentation/ - Technical and user docs
```

### How Custom Instructions Work

1. **Automatic Loading:** When you start CLIO in a project directory, it automatically looks for `.clio/instructions.md`
2. **System Prompt Injection:** Your instructions are injected into the AI system prompt
3. **Consistent Behavior:** CLIO follows your guidelines for all operations in that project
4. **Project Portability:** Share `.clio/instructions.md` with your team for consistent AI behavior

### Example Use Cases

**Enforce Code Style:**
```markdown
## Code Style
- 4-space indentation (never tabs)
- Maximum line length: 100 characters
- Use trailing commas in multi-line arrays
- Always use explicit return types
```

**Pass Project Context:**
```markdown
## Architecture
- UserInterface/ - SwiftUI views and view models
- APIFramework/ - Provider integrations
- DatabaseService/ - SQLite and embeddings
- ConfigurationSystem/ - Settings and preferences
```

**Define Workflows:**
```markdown
## Testing Workflow
1. Write failing test first (TDD)
2. Implement minimal code to pass
3. Refactor for clarity and performance
4. Run full test suite before committing
```

For complete documentation on custom instructions, see the [CLIO Custom Instructions Guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/main/docs/CUSTOM_INSTRUCTIONS.md).

---

## Session Management

CLIO automatically saves all conversations for easy resumption.

### Starting Sessions

```bash
# Start a new conversation
clio --new

# Resume your last session
clio --resume

# Resume a specific session
clio --resume sess_20260118_143052

# Enable debug mode
clio --debug
```

### Session Storage

Sessions are stored in `~/.clio/sessions/` (or `$CLIO_SESSION_DIR` if set):

```
~/.clio/sessions/
├── sess_20260118_143052/
│   ├── conversation.json    # Full conversation history
│   ├── metadata.json        # Session info and timestamps
│   └── memory.json          # Memory context
└── sess_20260118_160334/
    └── ...
```

### Session Organization

- **One session per task:** Start fresh sessions for different tasks
- **Resume for continuity:** Pick up long-running work exactly where you left off
- **Archive completed work:** Sessions provide a complete record of what was done

---

## Example Workflows

### Code Review

```bash
clio --new
: Review the pull request in feature/authentication branch
: Check for security issues, code style, and test coverage
: Suggest improvements where needed
```

CLIO will:
1. Check out the branch
2. Review all changed files
3. Identify security concerns
4. Check test coverage
5. Provide detailed feedback

### Bug Fix

```bash
clio --resume  # Continue from debugging session
: The login form validation isn't working correctly
: Find the issue in src/auth/login.py and fix it
: Add tests to prevent regression
: Commit with an appropriate message
```

CLIO will:
1. Read the relevant files
2. Trace the logic
3. Identify the bug
4. Implement the fix
5. Write tests
6. Commit the changes

### Refactoring

```bash
clio --new
: Refactor the database module to use async/await
: Update all calling code
: Ensure tests still pass
```

CLIO will:
1. Analyze current implementation
2. Plan the refactoring
3. Update code systematically
4. Fix broken tests
5. Verify everything works

### New Feature

```bash
clio --new
: Implement CSV export for user reports
: Add menu item in the UI
: Include proper error handling
: Write integration test
```

CLIO will:
1. Create the export logic
2. Integrate with UI
3. Handle edge cases
4. Write comprehensive tests
5. Commit the complete feature

---

## Slash Commands

CLIO includes built-in slash commands for configuration and control:

### Session Management
- `/exit` - End current session (also: Ctrl+D)
- `/new` - Start fresh conversation (clears history)
- `/clear` - Clear screen

### API Configuration
- `/api provider [name]` - Set AI provider
- `/api key [key]` - Set API key
- `/api model [name]` - Set model
- `/login` - GitHub Copilot device flow authentication

### Settings
- `/config show` - Display current configuration
- `/config save` - Save configuration to `~/.clio/config.json`
- `/style [name]` - Change output style
- `/theme [name]` - Change color theme

### Help
- `/help` - Show all available commands
- `/version` - Display CLIO version

---

## Tips & Best Practices

### Start Specific
Instead of "fix the bug," try:
> "The user authentication fails when the password contains special characters. Find and fix the issue in src/auth/password_validator.py"

### Use Context
CLIO maintains conversation context:
> YOU: Read the main.py file  
> CLIO: [reads file]  
> YOU: Now refactor the error handling in that file

### Verify Before Committing
Always review changes before committing:
> "Show me the diff before committing"  
> "Run tests before we commit"

### Combine Operations
CLIO can handle multi-step workflows:
> "Create a new feature branch, implement the CSV export, write tests, and commit"

### Use Memory
Store important context:
> "Remember that our production API is at https://api.prod.example.com"  
> "Remember we use pytest for all tests"

### Leverage Custom Instructions
Create `.clio/instructions.md` for project-specific behavior:
- Coding standards enforcement
- Architecture guidelines
- Testing requirements
- Deployment workflows

---

## Integration with SAM

CLIO and SAM work together seamlessly in your development workflow.

### Recommended Workflow

**1. Research & Planning (SAM)**
- Use SAM's Shared Topics for project coordination
- Import documentation and research materials
- Plan architecture with SAM's visual interface
- Use subagents for complex design decisions

**2. Implementation (CLIO)**
- Switch to terminal for actual coding
- Use CLIO for file operations and git workflow
- Leverage custom instructions for consistency
- Quick iterations with CLIO's terminal speed

**3. Review & Testing (Both)**
- CLIO for running tests and fixing bugs
- SAM for complex debugging with multiple contexts
- CLIO for final git operations
- SAM for documentation updates

**4. Documentation (SAM)**
- Use SAM's visual interface for writing docs
- Leverage SAM's memory for project context
- Generate comprehensive guides
- SAM Web for remote documentation updates

### Connecting CLIO to SAM

You can configure CLIO to use SAM as its AI provider:

```bash
clio --new
: /api provider sam
: /api endpoint http://localhost:9090
: /config save
```

This routes all CLIO requests through SAM's REST API, letting you:
- Use SAM's local models through CLIO
- Leverage SAM's memory and context
- Maintain unified conversation history
- Benefit from SAM's advanced features in the terminal

### Example Combined Workflow

**Day 1 - Planning (SAM):**
- Create Shared Topic: "authentication-system"
- Research OAuth 2.0 standards
- Design database schema
- Plan implementation phases
- Export plan to project directory

**Day 2-4 - Implementation (CLIO):**
```bash
cd ~/SAM/authentication-system
clio --new
: Implement the OAuth client as planned
: Follow the design in ARCHITECTURE.md
: Use the database schema from schema.sql
```

**Day 5 - Integration (Both):**
- CLIO: Implement endpoints
- SAM: Test with Postman collection
- CLIO: Fix bugs from testing
- SAM: Update documentation

**Day 6 - Deployment (CLIO):**
```bash
clio --resume
: Run the full test suite
: Build the production binary
: Deploy to staging environment
: Verify deployment health
```

---

## Troubleshooting

### CLIO Won't Start

**Error: "Can't locate CLIO/UI/Chat.pm"**

**Cause:** Perl can't find library modules.

**Solutions:**
1. Run from CLIO directory: `cd /path/to/CLIO && ./clio`
2. Set PERL5LIB: `export PERL5LIB=/path/to/CLIO/lib:$PERL5LIB`
3. Reinstall: `sudo ./install.sh`

### Authentication Issues

**Error: "API key not set"**

**Cause:** No API credentials configured.

**Solution:**
```bash
clio --new
: /api key YOUR_API_KEY
: /config save
```

**GitHub Copilot Login Fails**

**Solutions:**
1. Check you have an active Copilot subscription
2. Try `/login` again
3. Check `~/.clio/github_tokens.json` exists
4. Ensure browser opens for device flow
5. Try alternative provider as fallback

### Terminal Display Issues

**Colors Not Working**

**Cause:** Terminal doesn't support ANSI colors or TERM not set.

**Solutions:**
```bash
# Check TERM variable
echo $TERM

# Should be xterm-256color or similar
export TERM=xterm-256color

# Add to shell profile to make permanent
echo 'export TERM=xterm-256color' >> ~/.bashrc
```

**UTF-8 Encoding Problems**

**Solution:**
```bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Add to shell profile
echo 'export LC_ALL=en_US.UTF-8' >> ~/.bashrc
echo 'export LANG=en_US.UTF-8' >> ~/.bashrc
```

### Performance Issues

**Slow Responses**

**Likely Causes:**
- Network latency (not CLIO)
- AI provider API performance
- Large file operations

**Solutions:**
1. Check internet connection
2. Try different model (may be faster)
3. Use local provider if available
4. Enable `--debug` to see what's slow

**Slow Markdown Rendering**

**Note:** This has been optimized in recent versions and should be <100ms for typical responses.

If still slow:
1. Update to latest CLIO version
2. Check terminal emulator performance
3. Try simpler theme: `: /theme compact`

---

## Additional Resources

### CLIO Documentation
- **[User Guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/main/docs/USER_GUIDE.md)** - Complete usage guide
- **[Architecture](https://github.com/SyntheticAutonomicMind/CLIO/blob/main/docs/ARCHITECTURE.md)** - System design
- **[Custom Instructions](https://github.com/SyntheticAutonomicMind/CLIO/blob/main/docs/CUSTOM_INSTRUCTIONS.md)** - Per-project configuration
- **[Installation](https://github.com/SyntheticAutonomicMind/CLIO/blob/main/INSTALL.md)** - Detailed setup guide

### SAM Resources
- **[The Unbroken Method](the-unbroken-method.md)** - AI collaboration methodology
- **[Developer Guide](developers-guide.md)** - Complete developer documentation
- **[Architecture](architecture.md)** - SAM system design
- **[Contributing](contributing.md)** - How to contribute to SAM

### Community
- **[GitHub Organization](https://github.com/SyntheticAutonomicMind)** - All SAM projects
- **[CLIO Repository](https://github.com/SyntheticAutonomicMind/CLIO)** - Source code and issues
- **[SAM Repository](https://github.com/SyntheticAutonomicMind/SAM)** - SAM source and issues

---

## Why Terminal-Based AI Matters

CLIO represents a philosophy: **AI assistance should adapt to your workflow, not force you to adapt to it.**

For developers who:
- Live in tmux/screen sessions
- Prefer Vim to VSCode
- Script everything
- Work on remote servers
- Value keyboard efficiency
- Want lightweight tools

CLIO brings AI assistance to where you actually work.

Combined with SAM's visual power, you have a complete AI development environment that respects your preferences and enhances your productivity.

**Start your CLIO journey today:**

```bash
git clone https://github.com/SyntheticAutonomicMind/CLIO.git
cd CLIO
sudo ./install.sh
clio --new
```

Welcome to the future of terminal-based development.
