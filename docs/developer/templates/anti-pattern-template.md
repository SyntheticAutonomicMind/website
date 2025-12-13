# Anti-Pattern Template

**How to document failures systematically so you never make the same mistake twice.**

The anti-pattern catalog is a living document that grows with your project. Every time something goes wrong, document it here so future sessions can avoid the same pitfall.

---

## The Anti-Pattern Structure

```markdown
### Anti-Pattern: [Descriptive Name]

**Category:** [Architecture / Process / Communication / Code Quality]

**What It Looks Like:**
[Concrete example of the bad pattern - be specific]

**Why It's Wrong:**
[Explanation of the problems this causes]

**What To Do Instead:**
[The correct approach with example]

**Real Example:**
[Actual instance from your project history]

**Date Discovered:** [When this was learned]
```

---

## Example Anti-Patterns

### Anti-Pattern: Assumption Implementation

**Category:** Process

**What It Looks Like:**
Starting to write code based on what you think the system does without reading the actual implementation.

```swift
// Assuming there's a shared topics API based on a comment
let topics = try await SharedTopicsAPI.getAll()  // API doesn't exist!
```

**Why It's Wrong:**
- Assumptions are frequently wrong
- Time wasted debugging non-existent features
- May introduce bugs that don't surface immediately
- Contradicts existing patterns without knowing it

**What To Do Instead:**
1. Read the relevant existing code first
2. Search for similar patterns in the codebase
3. Test current behavior to confirm understanding
4. THEN propose and implement changes

```bash
# Before implementing, search for the API
grep -r "SharedTopics" Sources/
# Finding: No results. API was planned but never implemented.
```

**Real Example:**
Agent assumed SharedTopics API existed based on a TODO comment. Spent 2 hours implementing feature against non-existent API. Discovery: The API was a future plan, never built.

**Date Discovered:** November 12, 2025

---

### Anti-Pattern: Symptom Patching

**Category:** Code Quality

**What It Looks Like:**
Adding workarounds to hide errors instead of fixing the root cause.

```swift
// BAD: Suppress the error
do {
    try riskyOperation()
} catch {
    // Ignore it, usually works
}

// BAD: Add delay to "fix" race condition
DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
    updateUI()  // Hope the data is ready now
}
```

**Why It's Wrong:**
- Original bug remains, will resurface
- Code becomes fragile and unpredictable
- Debugging becomes harder
- Technical debt compounds

**What To Do Instead:**
Trace the error to its source and fix the actual cause.

```swift
// GOOD: Fix the validation
guard isValid(input) else {
    throw ValidationError.invalidInput(input)
}
try operation(validated: input)

// GOOD: Fix the race condition with proper synchronization
await dataLoader.waitForCompletion()
updateUI()  // Data is guaranteed ready
```

**Real Example:**
UI flickered during updates. Initial "fix" added 100ms delay. Root cause investigation revealed duplicate refresh calls. Proper fix: remove the duplicate call.

**Date Discovered:** November 15, 2025

---

### Anti-Pattern: Scope Escape

**Category:** Process

**What It Looks Like:**
Discovering an issue during work and labeling it "out of scope" or "separate issue."

```
Agent: "I noticed the model picker also shows the Downloads folder,
but that's a separate issue from what we're working on."
```

**Why It's Wrong:**
- Issues are discovered when context is fresh
- Deferred issues rarely get fixed
- Technical debt accumulates
- Quality standards erode

**What To Do Instead:**
Own everything you discover. Fix it now while you have context.

```
Agent: "While implementing X, I discovered the model picker shows 
the Downloads folder. Root cause: downloads directory is inside 
the models directory. I'll move the staging location to fix this 
before completing the original task."
```

**Real Example:**
Five "separate issues" were discovered and deferred during a feature implementation. None were ever addressed. All five caused user-reported bugs within two weeks.

**Date Discovered:** November 8, 2025

---

### Anti-Pattern: Partial Implementation

**Category:** Code Quality

**What It Looks Like:**
Delivering "basic" or "MVP" implementations that handle only the happy path.

```swift
func getImageSize(model: String) -> (Int, Int) {
    if model.contains("xl") {
        return (1024, 1024)
    }
    return (512, 512)  // TODO: Handle other sizes
}
```

**Why It's Wrong:**
- TODOs rarely get addressed
- Edge cases cause production bugs
- "Basic" versions become permanent
- Technical debt from day one

**What To Do Instead:**
Implement completely within scope. Query actual data when possible.

```swift
func getSupportedSizes(modelPath: URL) throws -> [(Int, Int)] {
    let model = try MLModel(contentsOf: modelPath)
    guard let inputDesc = model.modelDescription.inputDescriptionsByName["sample"],
          let shape = inputDesc.multiArrayConstraint?.shape else {
        throw ModelError.invalidStructure
    }
    return calculateSupportedSizes(from: shape)
}
```

**Real Example:**
"Basic" image size function was shipped. Three months later, new model released with different dimensions. Function returned wrong sizes. Users generated corrupted images before bug was caught.

**Date Discovered:** November 20, 2025

---

## Anti-Pattern Categories

### Architecture
Patterns that create structural problems:
- Wrong abstraction level
- Circular dependencies
- Multiple sources of truth
- Hardcoding vs configuration

### Process
Patterns that break workflow:
- Scope escape
- Assumption implementation
- Skipping investigation
- Ending without validation

### Communication
Patterns that break collaboration:
- Unclear checkpoints
- Missing context
- Ambiguous status reports
- Undocumented decisions

### Code Quality
Patterns that create technical debt:
- Symptom patching
- Partial implementation
- Magic numbers/strings
- Dead code accumulation

---

## Building Your Catalog

### When to Add Entries

Add a new anti-pattern when:
- A bug is traced to a repeated mistake
- Time is wasted on a preventable issue
- A pattern causes problems across multiple sessions
- You catch yourself about to repeat a mistake

### Review Process

Periodically review your catalog:
- Are patterns still relevant?
- Are descriptions clear enough?
- Are examples specific enough?
- Should any be promoted to your main instructions?

### Sharing

Include relevant anti-patterns in your collaboration prompt:

```markdown
## Project-Specific Anti-Patterns

See `docs/anti-patterns.md` for the full catalog. Key ones:

❌ Don't assume APIs exist - search first
❌ Don't add delays to fix race conditions - fix the race
❌ Don't defer "separate issues" - own everything
```

---

## Catalog Template

Start your anti-pattern catalog with this structure:

```markdown
# Anti-Pattern Catalog

**Project:** [Your Project Name]
**Last Updated:** [Date]

## Table of Contents
1. [Anti-Pattern Name](#anti-pattern-name)
2. [Anti-Pattern Name](#anti-pattern-name)

---

## Architecture Anti-Patterns

### [Pattern Name]
[Use the template structure above]

---

## Process Anti-Patterns

### [Pattern Name]
[Use the template structure above]

---

## Code Quality Anti-Patterns

### [Pattern Name]
[Use the template structure above]

---

## Changelog

| Date | Change |
|------|--------|
| YYYY-MM-DD | Added [pattern name] |
| YYYY-MM-DD | Updated [pattern name] |
```

---

## Related Templates

- [Quick Start Prompt](quick-start-prompt.md) - Minimal collaboration prompt
- [Full Collaboration Prompt](full-collaboration-prompt.md) - Complete prompt
- [Handoff Templates](handoff-templates.md) - Session transition documents
- [Collaboration Tool Scripts](collaboration-tool.md) - Checkpoint automation
