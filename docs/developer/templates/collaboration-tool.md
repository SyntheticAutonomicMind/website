# Collaboration Tool Scripts

**Programmatic tools for creating checkpoints in your AI collaboration workflow.**

These scripts pause execution for human input, display context clearly, and maintain collaboration flow without breaking the conversation.

---

## Why Use a Collaboration Tool?

The collaboration tool is the heart of The Unbroken Method. It:

- **Pauses for human input** - Creates natural checkpoints
- **Preserves context** - AI stays in the same session
- **Enables validation** - Catch issues before they compound
- **Creates rhythm** - Investigation → Checkpoint → Implementation

Without a tool, you're limited to chat responses, which break flow and can lose context.

---

## Bash Implementation

### Basic Version

```bash
#!/bin/bash
# collaboration.sh - Simple checkpoint tool
# Usage: ./collaboration.sh "Your message here"

MESSAGE="${1:-Press Enter to continue}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CHECKPOINT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "$MESSAGE"
echo ""
read -p "Response: " response

if [ -n "$response" ]; then
    echo ""
    echo "User response: $response"
fi

echo ""
echo "Continuing..."
```

### Enhanced Version (with colors)

```bash
#!/bin/bash
# collaboration.sh - Enhanced checkpoint tool with colors
# Usage: ./collaboration.sh "Your message here"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

MESSAGE="${1:-Press Enter to continue}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🤝 COLLABORATION CHECKPOINT${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "$MESSAGE"
echo ""
echo -en "${GREEN}Enter your response: ${NC}"
read -r response

if [ -n "$response" ]; then
    echo ""
    echo -e "${YELLOW}User response:${NC} $response"
fi

echo ""
echo "Continuing..."
exit 0
```

### Installation

```bash
# Create scripts directory
mkdir -p scripts

# Create the script
cat > scripts/collaboration.sh << 'EOF'
#!/bin/bash
# [Paste script content here]
EOF

# Make executable
chmod +x scripts/collaboration.sh

# Test it
./scripts/collaboration.sh "Test checkpoint. Press Enter: "
```

---

## Python Implementation

### Basic Version

```python
#!/usr/bin/env python3
"""
collaboration.py - Checkpoint tool for AI collaboration
Usage: python collaboration.py "Your message here"
"""

import sys

def checkpoint(message="Press Enter to continue"):
    """Create a collaboration checkpoint and wait for user input."""
    print()
    print("━" * 50)
    print("CHECKPOINT")
    print("━" * 50)
    print()
    print(message)
    print()
    
    response = input("Response: ")
    
    if response:
        print()
        print(f"User response: {response}")
    
    print()
    print("Continuing...")
    return response

if __name__ == "__main__":
    message = sys.argv[1] if len(sys.argv) > 1 else "Press Enter to continue"
    checkpoint(message)
```

### Enhanced Version (with logging)

```python
#!/usr/bin/env python3
"""
collaboration.py - Enhanced checkpoint tool with logging
Usage: python collaboration.py "Your message here"
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Colors for terminal output
class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

def checkpoint(message="Press Enter to continue", log_file=None):
    """
    Create a collaboration checkpoint and wait for user input.
    
    Args:
        message: The message to display
        log_file: Optional path to log checkpoints
    
    Returns:
        The user's response string
    """
    timestamp = datetime.now().isoformat()
    
    # Display checkpoint
    print()
    print("━" * 60)
    print(f"{Colors.BLUE}🤝 COLLABORATION CHECKPOINT{Colors.NC}")
    print("━" * 60)
    print()
    print(message)
    print()
    
    # Get response
    response = input(f"{Colors.GREEN}Enter your response: {Colors.NC}")
    
    if response:
        print()
        print(f"{Colors.YELLOW}User response:{Colors.NC} {response}")
    
    # Log if requested
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, 'a') as f:
            f.write(f"\n--- Checkpoint: {timestamp} ---\n")
            f.write(f"Message: {message}\n")
            f.write(f"Response: {response}\n")
    
    print()
    print("Continuing...")
    return response

if __name__ == "__main__":
    message = sys.argv[1] if len(sys.argv) > 1 else "Press Enter to continue"
    log_file = os.environ.get('CHECKPOINT_LOG')  # Optional: set CHECKPOINT_LOG env var
    checkpoint(message, log_file)
```

### Installation

```bash
# Create scripts directory
mkdir -p scripts

# Create the script
cat > scripts/collaboration.py << 'EOF'
# [Paste script content here]
EOF

# Make executable
chmod +x scripts/collaboration.py

# Test it
python3 scripts/collaboration.py "Test checkpoint. Press Enter: "
```

---

## Usage Patterns

### Before Major Implementation

```bash
scripts/collaboration.sh "I've investigated the issue and found:

- Root cause is in FileManager.swift line 234
- The path validation is missing a null check
- This affects all file operations

Proposed fix:
- Add null check before path resolution
- Add unit test for edge case

Press Enter to proceed with implementation: "
```

### After Investigation

```bash
scripts/collaboration.sh "Investigation complete.

Findings:
1. The bug is in MessageBus, not ChatWidget
2. Messages are being duplicated during streaming
3. Root cause: Both components create messages

Options:
A) Make MessageBus the single source of truth
B) Add deduplication logic

I recommend Option A - cleaner architecture.

Which approach? (Enter for A, or type B): "
```

### Before Ending Session

```bash
scripts/collaboration.sh "Work complete. Summary:

Completed:
✓ Fixed file validation bug
✓ Added unit tests
✓ Updated documentation

Commits:
- abc123: fix(files): Add null check to path validation
- def456: test(files): Add edge case coverage

All tests passing. Build successful.

Press Enter to confirm and end session: "
```

### When Uncertain

```bash
scripts/collaboration.sh "I'm uncertain about the best approach here.

The feature could be implemented as:
1. A new class (more isolated, more code)
2. An extension to existing class (less code, tighter coupling)

Both work. What's your preference?

Type 1 or 2, or Enter for my recommendation (Option 1): "
```

---

## Integration Tips

### In Your Instructions File

Add this to your AI collaboration prompt:

```markdown
## Collaboration Tool

Use the collaboration tool for checkpoints:

```bash
scripts/collaboration.sh "Your message. Press Enter: "
```

**When to use:**
- After investigation, before implementation
- After completing significant work
- When uncertain about approach
- Before ending the session

**Format your message with:**
- What you found/did
- What you propose next
- Any questions
- Clear call to action
```

### Handling Tool Failures

If the script fails (permissions, missing file), use fallbacks:

```bash
# Fallback 1: Direct read
read -p "CHECKPOINT: Your message. Press Enter: " response

# Fallback 2: Printf + read
printf "CHECKPOINT: Your message.\nPress Enter: "
read response

# Fallback 3: Echo + cat (last resort)
echo "CHECKPOINT: Type 'continue' and press Enter:"
cat
```

### Logging Checkpoints

Track checkpoints for later review:

```bash
# Set environment variable
export CHECKPOINT_LOG="./checkpoint_history.log"

# Or modify script to always log
LOGFILE="./scratch/checkpoints.log"
echo "[$(date)] $MESSAGE" >> "$LOGFILE"
echo "[$(date)] Response: $response" >> "$LOGFILE"
```

---

## Troubleshooting

### Script Not Found

```bash
# Check path
which scripts/collaboration.sh
ls -la scripts/collaboration.sh

# Use absolute path
/path/to/project/scripts/collaboration.sh "Message"
```

### Permission Denied

```bash
# Make executable
chmod +x scripts/collaboration.sh

# Or run with interpreter
bash scripts/collaboration.sh "Message"
python3 scripts/collaboration.py "Message"
```

### Input Not Captured

```bash
# Check terminal mode
# Some AI tools run in non-interactive mode

# Try with explicit stdin
echo "" | scripts/collaboration.sh "Message"
```

### Colors Not Showing

```bash
# Check terminal support
echo -e "\033[0;32mGreen\033[0m"

# Use plain version without colors
# Or check TERM environment variable
```

---

## Related Templates

- [Quick Start Prompt](quick-start-prompt.md) - Minimal collaboration prompt
- [Full Collaboration Prompt](full-collaboration-prompt.md) - Complete prompt
- [Handoff Templates](handoff-templates.md) - Session transition documents
- [Anti-Pattern Template](anti-pattern-template.md) - Document failures
