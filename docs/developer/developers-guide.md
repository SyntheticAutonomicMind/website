# Developers Guide

**Build an AI assistant that actually ships code.**

SAM was developed using a novel human-AI collaboration methodology called **The Unbroken Method**, and you can use the same approach. This guide covers everything you need to contribute to SAM, extend its capabilities, or learn from its architecture.

**What makes SAM's development unique:**
- Structured AI collaboration methodology
- Architecture designed for extensibility and testing
- Complete tool system you can extend
- Zero architectural debt carried forward

**This guide covers:**
- Setting up your development environment
- Building SAM from source
- Architecture and code organization
- Creating custom tools and extending SAM
- Testing, debugging, and release process

---

## Table of Contents

1. [Development Philosophy](#development-philosophy)
2. [Development Setup](#development-setup)
3. [Building SAM](#building-sam)
4. [Project Structure](#project-structure)
5. [Architecture Overview](#architecture-overview)
6. [Adding New Features](#adding-new-features)
7. [Creating Custom Tools](#creating-custom-tools)
8. [Testing](#testing)
9. [Debugging](#debugging)
10. [Performance Optimization](#performance-optimization)
11. [Release Process](#release-process)

---

## Development Philosophy

SAM was developed using **The Unbroken Method**, a systematic approach to human-AI collaboration that maximizes productivity and quality. This methodology is documented separately and applies to all SAM development work.

**Key Principles:**
- **Continuous Context**: Never break the conversation - maintain context across sessions
- **Complete Ownership**: Find it, fix it - no "out of scope" escapes
- **Investigation First**: Understand before acting - read code before modifying
- **Root Cause Focus**: Fix problems, not symptoms
- **Complete Deliverables**: Finish what you start - no partial implementations
- **Structured Handoffs**: Perfect context transfer between sessions
- **Learning from Failure**: Document anti-patterns to prevent recurrence

These principles enable consistent, high-quality development with features complete on first implementation.

**Read More:** [The Unbroken Method](the-unbroken-method.md) - Complete methodology documentation

---

## Development Setup

### Prerequisites

- **macOS 14.0+** (Sonoma or later)
- **Xcode 15.0+** with Command Line Tools
- **Swift 5.9+**
- **Git**
- **ccache** (optional, speeds up builds)

### Install Dependencies

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install ccache (optional but recommended)
brew install ccache

# Clone the repository
git clone https://github.com/SyntheticAutonomicMind/SAM.git
cd SAM

# Initialize submodules (llama.cpp, etc.)
git submodule update --init --recursive
```

### Configure Xcode

```bash
# Select Xcode command line tools
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer

# Accept license if needed
sudo xcodebuild -license accept
```

---

## Building SAM

### Quick Build

```bash
# Build debug version (faster, includes debug symbols)
make build-debug

# Run debug build
open .build/Build/Products/Debug/SAM.app
```

### Full Build Process

SAM uses a custom Makefile that handles:
1. Building llama.cpp framework (local GGUF models)
2. Compiling Metal shaders (MLX support)
3. Building Swift code
4. Creating app bundle with frameworks

```bash
# Clean previous builds
make clean

# Build llama.cpp framework
make llamacpp

# Build Metal library
make metallib

# Build full debug version
make build-debug

# Or build optimized release version
make build-release
```

### Build Output

After building:

```
.build/
└── Build/
    └── Products/
        ├── Debug/
        │   ├── SAM                    # Executable
        │   ├── SAM.app/               # App bundle
        │   └── PackageFrameworks/     # Dependencies
        └── Release/
            └── (same structure)
```

### Build Targets

The Makefile provides several targets:

| Target | Description |
|--------|-------------|
| `make build-debug` | Debug build with symbols |
| `make build-release` | Optimized release build |
| `make clean` | Remove build artifacts |
| `make llamacpp` | Build llama.cpp only |
| `make metallib` | Build Metal shaders only |
| `make test` | Run unit tests |

---

## Project Structure

```
SAM/
├── Sources/
│   ├── SAM/                          # App Entry Point
│   │   ├── main.swift                # @main entry
│   │   ├── AppDelegate.swift         # App lifecycle
│   │   ├── SAMCommands.swift         # App commands
│   │   └── Resources/                # App resources
│   │
│   ├── UserInterface/                # UI Layer
│   │   ├── Chat/                     # Chat components
│   │   │   ├── ChatWidget.swift      # Main chat interface
│   │   │   └── MessageView.swift     # Individual messages
│   │   ├── MainWindowView.swift      # Main window
│   │   ├── PreferencesView.swift     # Settings UI
│   │   ├── Help/                     # Help system
│   │   │   └── HelpView.swift        # Help documentation
│   │   └── ...
│   │
│   ├── APIFramework/                 # AI Provider Layer
│   │   ├── AIProvider.swift          # Provider protocol
│   │   ├── OpenAIProvider.swift      # OpenAI implementation
│   │   ├── GitHubCopilotProvider.swift
│   │   ├── MLXProvider.swift         # Local MLX models
│   │   ├── LlamaProvider.swift       # Local GGUF models
│   │   ├── AgentOrchestrator.swift   # LLM coordination
│   │   ├── EndpointManager.swift     # Provider management
│   │   ├── UniversalToolRegistry.swift # Tool registration
│   │   └── ...
│   │
│   ├── MCPFramework/                 # MCP Tool System
│   │   ├── MCPManager.swift          # MCP protocol manager
│   │   ├── MCPTypes.swift            # MCP data types
│   │   └── Tools/                    # MCP tool implementations
│   │       ├── ThinkTool.swift
│   │       ├── FileOperationsTool.swift
│   │       ├── TerminalOperationsTool.swift
│   │       ├── MemoryOperationsTool.swift
│   │       ├── RunSubagentTool.swift
│   │       └── ...
│   │
│   ├── ConversationEngine/           # Conversation Management
│   │   ├── ConversationManager.swift # Conversation state
│   │   ├── MemoryManager.swift       # Vector memory system
│   │   ├── YaRNContextProcessor.swift # Context compression
│   │   ├── AppleNLEmbeddingGenerator.swift # 512-dim embeddings
│   │   └── ...
│   │
│   ├── ConfigurationSystem/          # Settings & Configuration
│   │   ├── SystemPromptConfiguration.swift
│   │   ├── PersonalityManager.swift  # Personality system
│   │   ├── PersonalityTrait.swift    # Built-in personalities
│   │   ├── EndpointConfigurationModels.swift # ProviderType enum
│   │   └── ...
│   │
│   ├── MLXIntegration/               # MLX Support
│   │   ├── AppleMLXAdapter.swift
│   │   ├── MLXModelCache.swift
│   │   └── HuggingFaceAPIClient.swift
│   │
│   ├── StableDiffusionIntegration/   # Image Generation
│   │   └── ...
│   │
│   ├── SharedData/                   # Shared Topics
│   │   └── SharedStorage.swift
│   │
│   ├── VoiceFramework/               # Voice Features
│   │   └── SpeechRecognitionService.swift
│   │
│   └── Utilities/                    # Helper utilities
│       └── ...
│
├── external/
│   └── llama.cpp/                    # Submodule for GGUF support
│
├── Info.plist                        # App metadata
├── Package.swift                     # SPM dependencies
├── Makefile                          # Build system
└── README.md
```

---

## Architecture Overview

### Design Principles

SAM follows these core principles:

1. **Protocol-Oriented**: Use protocols for abstractions (AIProvider, ToolService)
2. **Async/Await**: Modern concurrency throughout
3. **SwiftUI**: Declarative, reactive UI
4. **Modular**: Clear separation of concerns
5. **Testable**: Dependency injection, mockable interfaces

### Component Layers

```
┌─────────────────────────────────────┐
│        UserInterface Layer          │
│  (SwiftUI Views, ChatWidget)        │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│      Business Logic Layer           │
│  (AgentOrchestrator, ToolService)   │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│       Provider Layer                │
│  (OpenAI, MLX, Copilot)             │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│      Infrastructure Layer           │
│  (Database, Network)                │
└─────────────────────────────────────┘
```

### Key Patterns

**1. Provider Pattern**

All AI providers implement `AIProvider` protocol:

```swift
protocol AIProvider {
    func sendMessage(
        _ message: String,
        context: [Message],
        tools: [Tool]?,
        stream: Bool
    ) async throws -> ChatResponse
}
```

**2. Tool System**

Tools are discovered, registered, and executed dynamically:

```swift
protocol ToolService {
    func register(_ tool: Tool)
    func execute(_ tool: ToolCall) async throws -> ToolResult
}
```

**3. Streaming**

Server-Sent Events (SSE) for real-time responses:

```swift
for try await chunk in provider.streamMessage(...) {
    await updateUI(with: chunk)
}
```

**4. State Management**

SwiftUI's `@State`, `@StateObject`, `@EnvironmentObject`:

```swift
@StateObject private var conversationManager = ConversationManager()
@State private var messages: [Message] = []
```

---

## Adding New Features

### Example: Add a New Tool

**Step 1: Define Tool**

Create `Sources/MCPFramework/Tools/MyNewTool.swift`:

```swift
import Foundation
import Logging

public final class MyNewTool: MCPTool {
    
    // MARK: - Protocol Conformance
    
    public let name = "my_new_tool"
    public let description = """
    Brief description of what the tool does.
    
    USE FOR:
    - List the use cases
    
    PARAMETERS:
    - param1: Description of first parameter
    """
    
    public var parameters: [String: MCPToolParameter] {
        return [
            "param1": MCPToolParameter(
                type: .string,
                description: "First parameter description",
                required: true
            ),
            "param2": MCPToolParameter(
                type: .number,
                description: "Optional second parameter",
                required: false
            )
        ]
    }
    
    // MARK: - Execution
    
    private let logger = Logger(label: "com.sam.mcp.MyNewTool")
    
    public func execute(
        arguments: [String: Any],
        conversationManager: ConversationManager?,
        conversationId: UUID?
    ) async throws -> MCPToolResponse {
        
        // 1. Validate required arguments
        guard let param1 = arguments["param1"] as? String else {
            return MCPToolResponse(
                success: false,
                output: MCPOutput(content: "Error: param1 is required", mimeType: "text/plain"),
                toolName: name
            )
        }
        
        // 2. Get optional arguments
        let param2 = arguments["param2"] as? Double ?? 0.0
        
        // 3. Perform tool operation
        let result = processParameters(param1, param2)
        
        // 4. Return success result
        return MCPToolResponse(
            success: true,
            output: MCPOutput(content: result, mimeType: "text/plain"),
            toolName: name
        )
    }
    
    private func processParameters(_ p1: String, _ p2: Double) -> String {
        // Your tool logic here
        return "Processed: \(p1) with value \(p2)"
    }
}
```

**Step 2: Register Tool**

In `Sources/SAM/main.swift`, add the tool registration:

```swift
// In the tool registration section
conversationManager.mcpManager.registerTool(MyNewTool(), name: "my_new_tool")
```

**Step 3: Build and Test**

```bash
make build-debug
# Test by asking SAM to use your new tool
```

### Example: Add a New Provider

**Step 1: Create Provider Class**

Create `Sources/APIFramework/MyProvider.swift`:

```swift
import Foundation

class MyProvider: AIProvider {
    let apiKey: String
    let baseURL: URL
    
    init(apiKey: String) {
        self.apiKey = apiKey
        self.baseURL = URL(string: "https://api.myprovider.com")!
    }
    
    func sendMessage(
        _ message: String,
        context: [Message],
        tools: [Tool]?,
        stream: Bool
    ) async throws -> ChatResponse {
        // Implement API call
        let request = createRequest(message: message, context: context)
        let (data, _) = try await URLSession.shared.data(for: request)
        
        return try JSONDecoder().decode(ChatResponse.self, from: data)
    }
}
```

**Step 2: Register Provider**

In `Sources/ConfigurationSystem/EndpointManager.swift`:

```swift
func registerProviders() {
    register("openai", OpenAIProvider.self)
    register("copilot", GitHubCopilotProvider.self)
    register("myprovider", MyProvider.self)  // Add your provider
}
```

**Step 3: Add UI Configuration**

In `Sources/UserInterface/PreferencesView.swift`, add settings UI for your provider.

---

## Creating Custom Tools

### Tool Lifecycle

1. **Discovery**: Tool registered via `MCPManager.registerTool()`
2. **Definition**: Tool schema (parameters) sent to LLM
3. **Execution**: LLM calls tool with arguments
4. **Result**: Tool returns `MCPToolResponse` to LLM

### Tool Template

```swift
import Foundation
import Logging

/// Custom MCP tool implementation
public final class MyCustomTool: MCPTool {
    
    // MARK: - Required Protocol Properties
    
    public let name = "my_custom_tool"
    public let description = """
    Brief description of what the tool does.
    
    USE FOR:
    - Use case 1
    - Use case 2
    """
    
    public var parameters: [String: MCPToolParameter] {
        return [
            "arg1": MCPToolParameter(
                type: .string,
                description: "Description of arg1",
                required: true
            ),
            "arg2": MCPToolParameter(
                type: .number,
                description: "Description of arg2",
                required: false
            )
        ]
    }
    
    // MARK: - Execution
    
    private let logger = Logger(label: "com.sam.mcp.MyCustomTool")
    
    public func execute(
        arguments: [String: Any],
        conversationManager: ConversationManager?,
        conversationId: UUID?
    ) async throws -> MCPToolResponse {
        
        // 1. Validate required arguments
        guard let arg1 = arguments["arg1"] as? String else {
            return MCPToolResponse(
                success: false,
                output: MCPOutput(content: "Error: arg1 is required", mimeType: "text/plain"),
                toolName: name
            )
        }
        
        let arg2 = arguments["arg2"] as? Double ?? 0.0
        
        // 2. Perform tool operation
        do {
            let result = try await performOperation(arg1, arg2)
            
            // 3. Return success result
            return MCPToolResponse(
                success: true,
                output: MCPOutput(content: result, mimeType: "text/plain"),
                toolName: name
            )
        } catch {
            // 4. Return error result
            return MCPToolResponse(
                success: false,
                output: MCPOutput(content: "Error: \\(error.localizedDescription)", mimeType: "text/plain"),
                toolName: name
            )
        }
    }
    
    // MARK: - Helper Methods
    
    private func performOperation(
        _ arg1: String,
        _ arg2: Double
    ) async throws -> String {
        // Your tool logic here
        return "Result"
    }
}
```

### Tool Best Practices

1. **Clear Descriptions**: Help LLM understand when to use tool
2. **Validate Inputs**: Check arguments before execution
3. **Error Handling**: Return meaningful error messages
4. **Async Operations**: Use `async/await` for network/file I/O
5. **Safety**: Validate dangerous operations (terminal, file writes)

---

## Testing

### Unit Tests

```bash
# Run all tests
make test

# Run specific test file
swift test --filter MyToolTests

# Run with coverage
swift test --enable-code-coverage
```

### Writing Tests

```swift
import XCTest
@testable import SAM

final class MyFeatureTests: XCTestCase {
    var sut: MyFeature!
    
    override func setUp() {
        super.setUp()
        sut = MyFeature()
    }
    
    override func tearDown() {
        sut = nil
        super.tearDown()
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

Test full workflows:

```swift
func testFullChatFlow() async throws {
    // Create conversation
    let conversation = Conversation()
    
    // Send message
    let response = try await provider.sendMessage(
        "Hello",
        context: [],
        tools: nil,
        stream: false
    )
    
    // Verify response
    XCTAssertFalse(response.content.isEmpty)
}
```

---

## Debugging

### Xcode Debugging

1. **Breakpoints**: Click line number in Xcode
2. **LLDB**: Use `po` command to inspect variables
3. **View Hierarchy**: Debug → View Debugging → Capture View Hierarchy

### Console Logging

SAM uses structured logging:

```swift
import os.log

let logger = Logger(subsystem: "com.sam", category: "MyFeature")

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error: \(error.localizedDescription)")
```

View logs:
```bash
# Console.app → Search "SAM"
# Or use log command:
log stream --predicate 'subsystem == "com.sam"' --level debug
```

### Network Debugging

Use Charles Proxy or Proxyman to inspect HTTP/HTTPS traffic:

1. Install proxy tool
2. Configure macOS to use proxy
3. Install SSL certificate
4. Monitor SAM's API calls

---

## Performance Optimization

### Profiling

Use Xcode Instruments:

```bash
# Build with profiling enabled
xcodebuild -scheme SAM -configuration Release

# Launch Instruments
open /Applications/Xcode.app/Contents/Applications/Instruments.app
```

Key instruments:
- **Time Profiler**: CPU usage
- **Allocations**: Memory usage
- **Leaks**: Memory leaks
- **Network**: Network activity

### Optimization Tips

**1. Async/Await**
```swift
// ❌ Bad: Synchronous
let result = expensiveOperation()

// ✅ Good: Asynchronous
let result = await Task.detached {
    expensiveOperation()
}.value
```

**2. Lazy Loading**
```swift
// ❌ Bad: Load all upfront
let models = loadAllModels()

// ✅ Good: Lazy load
lazy var models = { loadAllModels() }()
```

**3. Caching**
```swift
// Cache expensive computations
private var cache: [String: Result] = [:]

func compute(_ input: String) -> Result {
    if let cached = cache[input] {
        return cached
    }
    let result = expensiveComputation(input)
    cache[input] = result
    return result
}
```

---

## Release Process

### Version Numbering

SAM uses semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes

### Creating a Release

**1. Update Version**

Edit `Info.plist`:
```xml
<key>CFBundleShortVersionString</key>
<string>1.0.25</string>
```

**2. Build Release**

```bash
make build-release
```

**3. Create Archive**

```bash
cd .build/Build/Products/Release
zip -r SAM.app.zip SAM.app
```

**4. Sign Archive**

```bash
# Sign with Sparkle EdDSA key
./bin/sign_update SAM.app.zip

# Output:
# sparkle:edSignature="..." length="..."
```

**5. Update Appcast**

Edit `appcast.xml`:
```xml
<item>
    <title>SAM 1.0.25</title>
    <sparkle:version>1.0.25</sparkle:version>
    <sparkle:edSignature>PASTE_SIGNATURE_HERE</sparkle:edSignature>
    <enclosure url="https://github.com/SyntheticAutonomicMind/SAM/releases/download/v1.0.25/SAM.app.zip" />
</item>
```

**6. Create GitHub Release**

```bash
gh release create v1.0.25 SAM.app.zip \
  --title "SAM 1.0.25" \
  --notes "Release notes here"
```

**7. Commit Appcast**

```bash
git add appcast.xml
git commit -m "chore: Update appcast for v1.0.25"
git push origin main
```

---

## Advanced Topics

### Metal Shaders

SAM uses Metal for GPU acceleration (MLX):

```bash
# Compile Metal shaders
xcrun metal -c shader.metal -o shader.air
xcrun metallib shader.air -o default.metallib
```

### Code Signing

For distribution outside App Store:

```bash
# Sign app bundle
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: YOUR NAME" \
  SAM.app

# Verify signature
codesign --verify --deep --strict --verbose=2 SAM.app
```

### Notarization

Required for macOS 10.15+:

```bash
# Create archive
ditto -c -k --keepParent SAM.app SAM.zip

# Submit for notarization
xcrun notarytool submit SAM.zip \
  --apple-id your@email.com \
  --team-id TEAMID \
  --password "app-specific-password"

# Staple ticket
xcrun stapler staple SAM.app
```

---

## Resources

### Documentation

- [Swift.org](https://swift.org/documentation/)
- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui)
- [Async/Await Guide](https://docs.swift.org/swift-book/LanguageGuide/Concurrency.html)

### Tools

- **Xcode**: IDE for Swift development
- **Swift Package Manager**: Dependency management
- **Instruments**: Performance profiling
- **lldb**: Debugger

### Community

- [Swift Forums](https://forums.swift.org/)
- [GitHub Discussions](https://github.com/SyntheticAutonomicMind/SAM/discussions)
- [Contributing Guide](contributing.md)

---

**Happy Developing! 🚀**
