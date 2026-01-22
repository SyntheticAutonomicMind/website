# Getting Started with CLIO

**Your Terminal AI Assistant for Quick Development Tasks**

---

## What is CLIO?

**CLIO (Command Line Intelligence Orchestrator)** is an AI assistant that runs entirely in your terminal. If you're comfortable with the command line and want AI help without leaving it, CLIO is for you.

CLIO is made by the same team that created SAM and shares the same privacy-first philosophy: your code and conversations stay on your machine.

### Why Use CLIO?

- **Terminal-native** - No browser tabs or GUI windows, just your terminal
- **Lightweight** - Requires only Perl (included on macOS and most Linux)
- **Privacy-focused** - Everything stored locally on your machine
- **Real operations** - CLIO actually reads files, runs commands, and uses git
- **Persistent sessions** - Pick up where you left off anytime
- **Works everywhere** - macOS, Linux, remote servers via SSH

### CLIO vs SAM: When to Use Which?

**Use CLIO for:**
- Quick code reviews
- File operations and searching
- Git workflow (commit, branch, diff)
- Running tests and build commands
- Terminal-focused development
- Working on remote servers

**Use SAM for:**
- Complex multi-day projects
- Document research and semantic search
- Training custom models
- Image generation
- Multi-conversation collaboration (Shared Topics)
- Visual project management

**Use both together** for the best development experience!

---

## Quick Start

### Installation

**1. Clone and install:**
```bash
git clone https://github.com/SyntheticAutonomicMind/CLIO.git
cd CLIO
sudo ./install.sh
```

**2. Verify it works:**
```bash
clio --help
```

### First-Time Setup

**GitHub Copilot** (Recommended)

Start CLIO and login:
```bash
clio --new
: /login
```

Follow the browser prompts to authorize. That's it!

**Other Providers**

If you prefer OpenAI or another provider:
```bash
clio --new
: /api provider openai
: /api key YOUR_API_KEY
: /config save
```

---

## Using CLIO

### Start a Conversation

```bash
# New conversation
clio --new

# Resume last session
clio --resume
```

### Ask Questions

Just type naturally:

```
: What files are in this directory?
: Read main.py and explain what it does
: Find all TODO comments in the project
: What git branches exist?
```

### Give Instructions

```
: Create a new Python script called process_data.py
: Fix the syntax error in src/utils.py
: Run the test suite and show results
: Commit these changes with a descriptive message
```

### Exit

```
: /exit
```

Or press `Ctrl+D`

---

## Essential Commands

### Session Management
- `/exit` - End session
- `/new` - Start fresh conversation
- `/clear` - Clear screen

### Configuration
- `/api provider [name]` - Change AI provider
- `/api key [key]` - Set API key
- `/config show` - Show current settings
- `/config save` - Save settings

### Help
- `/help` - Show all commands
- `/version` - Show CLIO version

---

## What CLIO Can Do

### Read & Analyze Code
```
: Read src/database.py and explain the main class
: What does the authenticate function do?
: Are there any security issues in auth.py?
```

### Edit Files
```
: Add error handling to the login function
: Refactor utils.py to use modern Python syntax
: Add type hints to all functions in main.py
```

### Search & Find
```
: Find all files that import 'requests'
: Search for database connection code
: List all Python files in this project
```

### Git Operations
```
: Show git status
: What changed in the last commit?
: Create a new branch called feature/api-v2
: Commit these changes
```

### Run Commands
```
: Run the test suite
: Build the project
: Check code style with flake8
: Run the app and show output
```

### Get Help
```
: How do I use asyncio in Python?
: What's the best way to handle CSV files?
: Explain decorators with an example
```

---

## Example Session

```bash
$ clio --new

: Read the README.md file

SYSTEM: [file_operations] - Reading README.md (156 lines)

CLIO: I've read your README. This is a Python project for data 
processing with CSV files. The main entry point is in main.py and 
it uses pandas for data manipulation.

Would you like me to explain any specific part?

: Are there any tests?

CLIO: I can see a tests/ directory. Let me check what's there.

SYSTEM: [file_operations] - Listing tests/ directory (4 files)

CLIO: Yes, you have test files:
- test_main.py
- test_utils.py  
- test_data_processor.py
- conftest.py

Would you like me to run the test suite?

: Yes, run the tests

SYSTEM: [terminal_operations] - Executing: python -m pytest tests/

CLIO: All tests passed! ✓

8 tests in total:
- test_main.py: 3 passed
- test_utils.py: 2 passed
- test_data_processor.py: 3 passed

The test coverage looks good for the core functionality.

: /exit

Session saved to ~/.clio/sessions/sess_20260118_143052
```

---

## Converting from Other AI Coding Assistants

**Switching from GitHub Copilot, Cursor, or another AI assistant?** CLIO can help you convert your existing project instructions!

### The Migration Process

Many AI coding tools use custom instruction files to guide their behavior:
- **GitHub Copilot**: `.github/copilot-instructions.md`
- **Cursor**: `.cursor/instructions.md` or `.cursorrules`
- **Aider**: `.aider.conf.yml`

CLIO uses `.clio/instructions.md` for project-specific guidance. The good news? CLIO can convert your existing instructions automatically!

### Step-by-Step Conversion

**1. Navigate to your project:**
```bash
cd ~/your-project
```

**2. Start CLIO and configure it:**
```bash
clio --new
: /login    # Or configure your preferred provider
```

**3. Ask CLIO to study and convert:**

Here's the prompt to use:

```
Please study this project, as well as CLIO's instructions 
(https://raw.githubusercontent.com/SyntheticAutonomicMind/CLIO/refs/heads/main/.clio/instructions.md) 
and the current .github/copilot-instructions.md file, then develop a set of 
instructions that CLIO can use. Save them to .clio/instructions.md
```

**4. Let CLIO do the work:**

CLIO will:
- Read your existing instruction files
- Study the project structure
- Understand CLIO's instruction format
- Create a converted `.clio/instructions.md` file
- Save it in the right location

**5. Review and refine:**

```
: Show me what you created
: Let's add a section about our testing workflow
: Update it to mention our deployment process
```

### What Gets Converted?

CLIO will translate:
- **Code style guidelines** → CLIO formatting rules
- **Project structure** → File navigation guidance
- **Workflows** → CLIO-compatible procedures
- **Terminology** → Project-specific vocabulary
- **Common tasks** → CLIO command examples

### Real Example: This Website

This SAM website project was converted from Copilot instructions:

**Before (Copilot):**
```markdown
# GitHub Copilot Instructions for SAM Website

When working on documentation:
- Verify all technical facts against SAM source code
- Use lowercase-with-hyphens.md for filenames
- Test locally with python3 -m http.server 8000
```

**After (CLIO):**
```markdown
# CLIO Project Instructions - SAM Website

**CRITICAL: READ FIRST BEFORE ANY WORK**

### Before Editing Any Documentation

1. **Understand the project:**
   cat README.md
   cat .github/copilot-instructions.md

2. **Know the standards:**
   - All files: lowercase-with-hyphens.md
   - Verify against SAM source code
   - Test locally: python3 -m http.server 8000
```

CLIO's format is more structured and action-oriented for terminal use.

### Benefits of Converting

✅ **Keep your project knowledge** - Don't lose institutional knowledge  
✅ **Immediate productivity** - CLIO knows your project from day one  
✅ **Consistency** - Same standards across AI tools  
✅ **Easy updates** - Edit one file for all CLIO sessions  

### Pro Tips

**Start with what you have:**
Even partial instructions help CLIO understand your project better than starting from scratch.

**Iterate:**
After conversion, use CLIO for a few tasks and refine the instructions based on what works.

**Keep both:**
You can maintain both Copilot and CLIO instructions if you use multiple tools.

**Update together:**
When project standards change, update both instruction files or ask CLIO to sync them.

---

## Tips for Best Results

### Be Specific
❌ "Fix the code"  
✓ "Fix the syntax error in line 42 of main.py"

### Use Context
CLIO remembers the conversation:
```
: Read the main.py file
: Now add better error handling to that file
```

### Verify Changes
```
: Show me what changed before committing
: Run tests before we commit
```

### Combine Actions
```
: Create a new branch, fix the typo in README, and commit
```

---

## Configuration

### Change Themes

```bash
: /style list        # See available styles
: /style photon      # Retro BBS style
: /theme compact     # Compact output
: /config save       # Save preferences
```

### Set Custom Session Directory

```bash
export CLIO_SESSION_DIR="$HOME/clio-sessions"
```

### Debug Mode

See what CLIO is doing:
```bash
clio --debug
```

---

## Troubleshooting

### "Can't find CLIO modules"

Run from the CLIO directory or reinstall:
```bash
cd /path/to/CLIO
./clio
# OR
sudo ./install.sh
```

### "API key not set"

Configure your provider:
```bash
: /api key YOUR_KEY
: /config save
```

### Colors not working

Set your terminal type:
```bash
export TERM=xterm-256color
```

### Need help?

- Check `/help` in CLIO
- Read the full [CLIO User Guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/main/docs/USER_GUIDE.md)
- Visit the [CLIO repository](https://github.com/SyntheticAutonomicMind/CLIO)

---

## Next Steps

**For Developers:** Read the complete [CLIO Developer Guide](clio.md) for:
- Advanced workflows
- Custom instructions for SAM projects
- Integration with SAM
- Session management strategies

**For SAM Users:** Learn how to use CLIO and SAM together:
- Use SAM for planning and research
- Use CLIO for implementation
- Connect CLIO to SAM's API
- Share context between tools

**Dive Deeper:**
- [Custom Instructions Guide](https://github.com/SyntheticAutonomicMind/CLIO/blob/main/docs/CUSTOM_INSTRUCTIONS.md)
- [Architecture Documentation](https://github.com/SyntheticAutonomicMind/CLIO/blob/main/docs/ARCHITECTURE.md)
- [The Unbroken Method](the-unbroken-method.md) - AI collaboration methodology

---

## Welcome to CLIO!

You now have a powerful AI assistant in your terminal. Whether you're fixing bugs, writing new features, or just exploring code, CLIO is ready to help.

Start your first session:
```bash
clio --new
```

Happy coding! 🚀
