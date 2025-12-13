# Contributors Guide

**Join the SAM community - all contributions welcome!**

Thinking about contributing to SAM? Whether you're fixing a bug, adding a feature, improving documentation, or sharing ideas, we'd love to have your help. This guide covers everything you need to know to contribute effectively.

**Ways to contribute:**
- **Bug fixes**: Find and fix issues
- **Features**: Build new capabilities
- **Documentation**: Improve guides and examples
- **Testing**: Add tests and improve coverage
- **Ideas**: Share feature requests and suggestions
- **UI/UX**: Improve the interface
- **Tools**: Create new MCP tools

**What's covered:**
- Getting started with the codebase
- Development workflow and best practices
- Code style and conventions
- Pull request process
- Testing requirements
- How to get help

**No contribution is too small!** Fixing typos, improving comments, or asking questions all help make SAM better.

**Time investment:**
- First contribution: 1-2 hours (setup + small fix)
- Ongoing contributions: Minutes to hours depending on scope

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Code Style Guidelines](#code-style-guidelines)
5. [Pull Request Process](#pull-request-process)
6. [Issue Guidelines](#issue-guidelines)
7. [Testing Requirements](#testing-requirements)
8. [Documentation](#documentation)

---

## Code of Conduct

### Our Pledge

We pledge to make participation in SAM a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes**:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes**:
- Trolling, insulting comments, and personal attacks
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, issues, and other contributions that do not align with this Code of Conduct.

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:
- macOS 14.0+ with Xcode 15.0+
- Git configured with your GitHub account
- Familiarity with Swift and SwiftUI
- Read the [Developer's Guide](developers-guide.md)

### Fork and Clone

```bash
# Fork the repository on GitHub (click "Fork" button)

# Clone your fork
git clone https://github.com/YOUR_USERNAME/SAM.git
cd SAM

# Add upstream remote
git remote add upstream https://github.com/SyntheticAutonomicMind/SAM.git

# Initialize submodules
git submodule update --init --recursive
```

### Build and Test

```bash
# Build SAM
make build-debug

# Run tests
make test

# Launch SAM
open .build/Build/Products/Debug/SAM.app
```

If everything builds and tests pass, you're ready to contribute!

---

## Development Workflow

### 1. Create a Branch

Always create a feature branch for your work:

```bash
# Update main
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/my-new-feature

# Or for bug fixes:
git checkout -b fix/issue-123
```

**Branch naming**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions

### 2. Make Changes

- Write clean, readable code
- Follow Swift style guidelines (below)
- Add tests for new functionality
- Update documentation if needed

### 3. Commit Changes

Use conventional commit format:

```bash
git add .
git commit -m "type(scope): description

- Detail 1
- Detail 2

Fixes #123"
```

**Commit types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `chore`: Maintenance

**Examples**:
```bash
git commit -m "feat(tools): Add new web scraping tool"
git commit -m "fix(ui): Fix conversation list crash on delete"
git commit -m "docs: Update API reference for streaming"
```

### 4. Push and Create PR

```bash
# Push to your fork
git push origin feature/my-new-feature

# Create pull request on GitHub
# Visit: https://github.com/SyntheticAutonomicMind/SAM/compare
```

---

## Code Style Guidelines

### Swift Style

SAM follows Swift standard conventions with some additions:

**1. Naming**

```swift
// ✅ Good: Clear, descriptive names
class ConversationManager { }
func sendMessage(to provider: AIProvider) { }
let maxTokenCount = 4096

// ❌ Bad: Ambiguous, abbreviated
class ConvMgr { }
func sndMsg(p: AIProv) { }
let mtc = 4096
```

**2. Formatting**

```swift
// ✅ Good: Consistent spacing, clear structure
func processMessage(
    _ message: String,
    with context: [Message],
    tools: [Tool]?
) async throws -> Response {
    guard !message.isEmpty else {
        throw MessageError.empty
    }
    
    return try await provider.send(
        message,
        context: context,
        tools: tools
    )
}

// ❌ Bad: Inconsistent formatting
func processMessage(_  message:String,with context:[Message],tools:[Tool]?)async throws->Response{
    guard !message.isEmpty else{throw MessageError.empty}
    return try await provider.send(message,context:context,tools:tools)
}
```

**3. Comments**

```swift
// ✅ Good: Explain why, not what
// Cache results to avoid re-fetching from API
private var cache: [String: Result] = [:]

/// Sends a message to the AI provider with optional tool calling.
/// - Parameters:
///   - message: The user's message
///   - tools: Available tools for the model to use
/// - Returns: The AI's response
func sendMessage(_ message: String, tools: [Tool]?) async throws -> Response

// ❌ Bad: State the obvious
// This variable stores cache
private var cache: [String: Result] = [:]

// This function sends a message
func sendMessage(_ message: String, tools: [Tool]?) async throws -> Response
```

**4. Error Handling**

```swift
// ✅ Good: Specific, actionable errors
enum ToolError: LocalizedError {
    case invalidArguments(String)
    case executionFailed(String)
    case permissionDenied
    
    var errorDescription: String? {
        switch self {
        case .invalidArguments(let detail):
            return "Invalid tool arguments: \(detail)"
        case .executionFailed(let reason):
            return "Tool execution failed: \(reason)"
        case .permissionDenied:
            return "Permission denied to execute tool"
        }
    }
}

// ❌ Bad: Generic errors
enum ToolError: Error {
    case error
}
```

**5. Async/Await**

```swift
// ✅ Good: Modern concurrency
func fetchData() async throws -> Data {
    try await URLSession.shared.data(from: url).0
}

// ❌ Bad: Completion handlers (avoid when possible)
func fetchData(completion: @escaping (Result<Data, Error>) -> Void) {
    URLSession.shared.dataTask(with: url) { data, _, error in
        // ...
    }.resume()
}
```

### SwiftUI Style

**1. View Structure**

```swift
// ✅ Good: Clear hierarchy, extracted subviews
struct ChatView: View {
    @StateObject private var viewModel: ChatViewModel
    
    var body: some View {
        VStack {
            MessageList(messages: viewModel.messages)
            InputField(text: $viewModel.input, onSend: viewModel.send)
        }
    }
}

// Extract complex views
struct MessageList: View {
    let messages: [Message]
    
    var body: some View {
        ScrollView {
            LazyVStack {
                ForEach(messages) { message in
                    MessageRow(message: message)
                }
            }
        }
    }
}
```

**2. State Management**

```swift
// ✅ Good: Clear state ownership
@StateObject private var manager = ConversationManager()  // Owner
@ObservedObject var manager: ConversationManager         // Observer
@State private var isExpanded = false                    // Local state
@Environment(\.colorScheme) var colorScheme              // Environment

// ❌ Bad: Unclear ownership
@State var manager = ConversationManager()  // Creates new instance on every view update!
```

---

## Pull Request Process

### Before Submitting

**Checklist**:
- [ ] Code builds without warnings
- [ ] All tests pass (`make test`)
- [ ] New tests added for new functionality
- [ ] Documentation updated if needed
- [ ] Commits follow conventional format
- [ ] Branch is up to date with main
- [ ] Code follows style guidelines

```bash
# Update your branch
git fetch upstream
git rebase upstream/main

# Run tests
make test

# Check for warnings
make build-debug
```

### PR Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested the changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Follows code style
- [ ] Commits follow conventions

Fixes #123
```

### Review Process

1. **Automated Checks**: CI/CD runs tests automatically
2. **Code Review**: Maintainer reviews code
3. **Feedback**: Address reviewer comments
4. **Approval**: Once approved, maintainer merges

**Review timeline**: Most PRs reviewed within 1-3 days.

---

## Issue Guidelines

### Reporting Bugs

Use the bug report template:

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- SAM version: 1.0.24
- macOS version: 14.2
- Hardware: M2 MacBook Pro

## Logs
```
Paste relevant logs here
```

## Screenshots
(if applicable)
```

### Requesting Features

Use the feature request template:

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why is this feature needed?

## Proposed Solution
How would you implement it?

## Alternatives Considered
What other approaches did you consider?

## Additional Context
Any other relevant information
```

### Asking Questions

Use GitHub Discussions for questions:
- Go to [Discussions](https://github.com/SyntheticAutonomicMind/SAM/discussions)
- Choose appropriate category
- Search existing discussions first

---

## Testing Requirements

### Unit Tests

All new features must include unit tests:

```swift
import XCTest
@testable import SAM

final class MyFeatureTests: XCTestCase {
    var sut: MyFeature!
    
    override func setUp() {
        super.setUp()
        sut = MyFeature()
    }
    
    func testFeatureBehavior() async throws {
        // Given
        let input = "test"
        
        // When
        let result = try await sut.process(input)
        
        // Then
        XCTAssertEqual(result, "expected")
    }
}
```

### Integration Tests

For complex features, add integration tests:

```swift
func testFullWorkflow() async throws {
    // Test complete feature workflow
    let provider = OpenAIProvider(apiKey: "test-key")
    let response = try await provider.sendMessage(
        "Hello",
        context: [],
        tools: nil,
        stream: false
    )
    
    XCTAssertFalse(response.content.isEmpty)
}
```

### Test Coverage

- Aim for **80%+ code coverage** on new code
- Use `swift test --enable-code-coverage` to check
- Focus on critical paths and edge cases

---

## Documentation

### Code Documentation

Use Swift's documentation markup:

```swift
/// Sends a message to the AI provider.
///
/// This method handles:
/// - Message formatting
/// - Context management
/// - Tool calling
/// - Error handling
///
/// - Parameters:
///   - message: The user's input message
///   - context: Previous messages for context
///   - tools: Available tools the model can use
/// - Returns: The AI provider's response
/// - Throws: `ProviderError` if the request fails
func sendMessage(
    _ message: String,
    context: [Message],
    tools: [Tool]?
) async throws -> Response {
    // Implementation
}
```

### User Documentation

When adding features that affect users:

1. Update relevant `.md` files in `user-docs/`
2. Add examples and screenshots
3. Update CHANGELOG (in repository root)

---

## Release Cycle

### Versioning

SAM uses [Semantic Versioning](https://semver.org/):
- **Major** (1.x.x): Breaking changes
- **Minor** (x.1.x): New features, backwards compatible
- **Patch** (x.x.1): Bug fixes

### Release Schedule

- **Major releases**: As needed (breaking changes)
- **Minor releases**: Monthly (new features)
- **Patch releases**: As needed (bug fixes)

---

## Recognition

### Contributors

All contributors are recognized in:
- GitHub contributors list
- CHANGELOG.md (for significant contributions)
- Release notes

### Maintainers

Current maintainers:
- [@fewtarius](https://github.com/fewtarius) - Project Lead

Interested in becoming a maintainer? Consistent, high-quality contributions over time may lead to maintainer status.

---

## Questions?

- **General Questions**: [GitHub Discussions](https://github.com/SyntheticAutonomicMind/SAM/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/SyntheticAutonomicMind/SAM/issues)
- **Security**: See SECURITY.md (if we add one)

---

**Thank you for contributing to SAM!**

Every contribution, no matter how small, makes SAM better for everyone.
