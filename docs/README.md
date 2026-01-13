# SAM - Synthetic Autonomic Mind

**The AI That Works *With* You, Not Just *For* You**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Platform](https://img.shields.io/badge/platform-macOS%2014.0%2B-lightgrey.svg)](https://www.apple.com/macos/)
[![Swift](https://img.shields.io/badge/swift-5.9%2B-orange.svg)](https://swift.org/)

---

## Stop Copy-Pasting. Start Shipping.

**What if your AI assistant could actually *finish* projects?**

Not just suggest code, but read your codebase, write the implementation, run the tests, and fix what breaks. SAM is a native macOS application that transforms AI from a chat interface into a **genuine collaborator**.

Run multiple specialized agents in parallel, work on long-running projects with persistent memory, generate images locally, and keep everything private on your Mac.

**Your data stays on your Mac. Always.**

### Why SAM Changes Everything

🧠 **Intelligent Memory System**
- Store and recall important information within conversations
- Use **Shared Topics** to link conversations for persistent, cross-session memory
- Semantic search understands *meaning*, not just keywords
- Import documents once, search them across sessions

📚 **Documents Become Searchable Knowledge**
- Import PDFs, Word docs, text files, and code
- Ask questions about any part of your documents
- Search semantically across all imported content
- Cross-reference multiple documents in one conversation

🤖 **Autonomous Agents That Actually Work**
- Subagents handle complex tasks with dedicated iteration budgets
- One agent on backend, one on frontend, one on testing
- High iteration limits per task with no babysitting required
- Transparent reasoning: watch SAM think through problems step by step

🔄 **Multi-Conversation Project Workflows**
- **Shared Topics**: Multiple AI conversations collaborate on one project
- Files, memory, and terminals shared across all conversations in a topic
- Perfect for complex projects that need different specialized expertise
- Human-readable workspace: `~/SAM/{your-project}/`

💪 **Context Windows That Scale**
- **YaRN Context Processing**: Multiple profiles from regular conversations to enterprise documents
- Intelligent compression preserves what matters
- Handle large documents without "context too long" errors
- Older context archived and searchable with `recall_history`

🛠️ **Built-In Tools**
- File operations, terminal execution, web research
- Professional SerpAPI integration: Google, Bing, Amazon, Scholar, and more
- Git operations, build tasks, document import
- Local image generation with Stable Diffusion

🎓 **Train Your Own Models**
- Fine-tune local models on your own data using LoRA
- Export conversations and documents as training data
- PII detection automatically protects sensitive information
- Create specialized assistants for any domain

🔐 **Privacy Is Not Optional**
- **Your data never leaves your Mac.** Ever.
- Run completely offline with local MLX/GGUF models
- 7 providers: OpenAI, Anthropic, GitHub Copilot, DeepSeek, Local MLX, Local GGUF, Custom
- API keys secured in macOS Keychain
- Zero telemetry, zero tracking, zero compromise

---

## Quick Navigation

### For End Users
New to SAM? Start here to get up and running quickly.

- **[Getting Started](end-user/getting-started.md)** - Installation and your first conversation
- **[Features Overview](end-user/features-overview.md)** - What SAM can do for you
- **[LoRA Training](end-user/lora-training.md)** - Fine-tune models on your own data
- **[Memory & RAG Guide](end-user/memory-and-rag.md)** - Understanding SAM's memory system
- **[Shared Topics Guide](end-user/shared-topics.md)** - Multi-conversation collaboration
- **[Use Cases](end-user/use-cases.md)** - Real-world scenarios showing SAM's value

### For Power Users
Ready to unlock SAM's full potential?

- **[Configuration Guide](power-user/configuration.md)** - Complete settings reference
- **[Tools Reference](power-user/tools-reference.md)** - Complete MCP tools reference
- **[Advanced Workflows](power-user/advanced-workflows.md)** - Subagents, complex projects, optimization
- **[Troubleshooting](power-user/troubleshooting.md)** - Common issues and solutions

### For Developers
Want to extend SAM or contribute to the project?

- **[Developers Guide](developer/developers-guide.md)** - Complete guide for developers
- **[The Unbroken Method](developer/the-unbroken-method.md)** - AI collaboration methodology
- **[Architecture](developer/architecture.md)** - System design and components
- **[API Reference](developer/api-reference.md)** - REST API documentation
- **[Contributing](developer/contributing.md)** - How to contribute code
- **[Building from Source](developer/building.md)** - Development setup
- **[Templates](developer/templates/)** - Ready-to-use prompts, handoffs, and tools

---

## At a Glance

### What You Get

**Multiple AI Providers**
- OpenAI (GPT-4, GPT-4-turbo, O1/O3 reasoning models)
- GitHub Copilot (Device Flow auth, GPT-4, Claude, O1)
- Anthropic Claude (3.5 Sonnet, Claude 4, Claude 4.5)
- DeepSeek models
- Local MLX models (Apple Silicon optimized, per-conversation KV cache)
- Local GGUF models (via llama.cpp, state serialization)
- Custom OpenAI-compatible endpoints (Gemini, Grok, and others)

**Personality System**
- Built-in personalities organized by category
- Custom personality creation with traits and instructions
- Per-conversation personality selection
- Categories: General, Creative, Tech, Productivity, Domain Experts, Fun

**Advanced Memory System**
- Vector RAG with Apple NaturalLanguage embeddings
- Conversation-scoped and topic-scoped memory
- Semantic search across all conversations
- Document import with intelligent chunking
- Cross-conversation memory retrieval
- Context archive with recall_history tool

**YaRN Context Management**
- Multiple context profiles: Default, Extended, Universal (default), Mega
- Intelligent message importance analysis
- Semantic clustering and compression
- Attention scaling for extended contexts
- Memory-integrated relevance scoring

**Shared Topics & Collaboration**
- Human-readable workspace directories (`~/SAM/{topic-name}/`)
- Multiple conversations share files, memory, terminals
- Perfect for complex projects requiring different expertise
- Persistent workspaces across conversation lifecycle

**Autonomous Capabilities**
- Sequential thinking architecture
- Multi-step workflow execution
- Subagent delegation with isolated contexts
- Recursive subagent nesting
- Dynamic iteration management

**Image Generation**
- Stable Diffusion integration with CoreML optimization
- Model Browser: Browse and download models from CivitAI and HuggingFace
- LoRA Browser: Discover and manage LoRAs from multiple sources
- Direct SD Mode: bypass LLM for instant generation
- Multiple schedulers (DPM++ with Karras, Euler, Euler A, PNDM)
- Full control over generation parameters
- Auto-conversion of downloaded models to CoreML

**Native macOS Experience**
- Beautiful SwiftUI interface
- Dark mode support
- Conversation management with persistent history
- Markdown rendering with syntax highlighting
- Keyboard shortcuts and menu integration

**RESTful API**
- OpenAI-compatible endpoints
- Server-Sent Events (SSE) streaming
- Enhanced response metadata (provider info, model capabilities, workflow details, cost estimates)
- Conversation management APIs
- Tool execution protocol
- Autonomous workflow endpoints

---

## Why Choose SAM?

### For Individual Users
- **Remember Everything**: Import documents, notes, and code. SAM makes them all searchable with semantic understanding.
- **Handle Complexity**: From simple questions to multi-day projects, SAM scales to your needs.
- **Privacy Guaranteed**: Your data never leaves your Mac. Use local models for complete offline operation.
- **One Conversation, Multiple Skills**: Discuss different topics in the same conversation - SAM maintains context.

### For Developers
- **True Coding Partner**: SAM reads your codebase, writes code, runs tests, and commits changes autonomously.
- **Multi-Aspect Projects**: Use shared topics for specialized conversations handling frontend, backend, testing, docs.
- **Semantic Code Search**: Find relevant code across your project using natural language.
- **Terminal Integration**: SAM executes commands, debugs issues, and iterates on solutions.

### For Researchers & Writers
- **Document Intelligence**: Import research papers, notes, drafts - SAM understands and synthesizes information.
- **Web Research**: Professional web search with SerpAPI, scraping, and automatic synthesis.
- **Massive Context**: Handle large documents with scalable context profiles.
- **Cross-Document Insights**: Search and connect information across all imported documents.

### For Teams & Complex Workflows
- **Shared Topic Collaboration**: Multiple specialized conversations work together on the same project.
- **Subagent Delegation**: Break complex tasks into specialized subtasks with dedicated agents.
- **Workflow Automation**: SAM can handle multi-step processes autonomously with proper planning.
- **Version Control Integration**: Built-in git operations for proper code management.

---

## Core Capabilities

### Memory & Intelligence
- **Vector RAG Service**: Semantic search and document chunking
- **YaRN Context Processor**: Multiple profiles from regular to enterprise scale
- **Memory Manager**: SQLite-based storage with conversation/topic scoping
- **Semantic Understanding**: Apple NaturalLanguage for true contextual comprehension

### File & Code Operations
- **File Operations**: Read, write, search, replace, rename, delete with authorization
- **Semantic Code Search**: Find functions, classes, patterns using natural language
- **Multi-File Editing**: Apply changes across multiple files atomically
- **Glob & Regex Search**: Powerful file and content search capabilities

### Terminal & Execution
- **11 Terminal Operations**: Execute commands, manage sessions, capture output
- **Pseudo-Terminal Support**: Full PTY with interactive command support
- **Multi-Session Management**: Create and switch between terminal sessions
- **Persistent History**: Terminal state persists across conversation lifecycle

### Web & Research
- **6 Web Operations**: Research, search, scrape, fetch with professional tools
- **SerpAPI Integration**: Google, Bing, Amazon, shopping, maps, and more
- **Web Scraping**: JavaScript-enabled scraping with WebKit
- **Research Synthesis**: Multi-source research with automatic memory storage

### Document Management
- **3 Document Operations**: Import, create, get info with full format support
- **Format Support**: PDF, Word, text files, code files
- **Page-Aware Processing**: Preserves document structure for accurate retrieval
- **Memory Integration**: Documents stored in searchable vector database

### Build & Version Control
- **5 Build/VCS Operations**: Task management, git operations
- **Task Automation**: Create and execute build tasks
- **Git Integration**: Diff, commit, status directly from conversation
- **Workflow Support**: Integrate with development workflows

---

## Getting Started

### Requirements
- macOS 14.0 (Sonoma) or later
- 4GB+ RAM (8GB+ recommended)
- 4GB+ free disk space
- Internet connection (for cloud providers and updates)

### Installation

**Option 1: Download Pre-built App** (Recommended)
1. Visit the [Releases page](https://github.com/SyntheticAutonomicMind/SAM/releases)
2. Download latest `SAM.app.zip`
3. Extract and move to Applications folder
4. Right-click → Open (first launch only)

**Option 2: Build from Source**
```bash
git clone https://github.com/SyntheticAutonomicMind/SAM.git
cd SAM
git submodule update --init --recursive
make build-release
open .build/Build/Products/Release/SAM.app
```

### First Steps
1. **Configure Provider**: Add your OpenAI/Copilot API key (or skip to use local models)
2. **Start Conversation**: Click "+" to create your first conversation
3. **Ask Anything**: SAM understands natural language - just chat naturally
4. **Import Documents** (optional): Drag PDFs, docs, or code files to make them searchable
5. **Create Shared Topic** (optional): For complex projects, create a shared workspace

### Learn More
- Read the **[Getting Started Guide](end-user/getting-started.md)** for detailed walkthrough
- Explore **[Features Overview](end-user/features-overview.md)** to see what SAM can do
- Check out **[Advanced Workflows](power-user/advanced-workflows.md)** for power user techniques

---

## Community & Support

### Get Help
- **Documentation**: Start with the guides above
- **Troubleshooting**: See [Troubleshooting Guide](power-user/troubleshooting.md)
- **GitHub Issues**: [Report bugs or request features](https://github.com/SyntheticAutonomicMind/SAM/issues)

### Contributing
SAM is open source and welcomes contributions! See [Contributing Guide](developer/contributing.md) for:
- Code contributions
- Documentation improvements
- Bug reports and feature requests
- Community support

### License
SAM is licensed under the GNU General Public License v3.0. See [LICENSE](https://github.com/SyntheticAutonomicMind/SAM/blob/main/LICENSE) for details.

---

## Technical Highlights

For those interested in the technical implementation:

- **Architecture**: Native SwiftUI with modular design
- **Memory System**: SQLite + Vector RAG with Apple NaturalLanguage
- **Context Management**: YaRN implementation with 5 scaling profiles
- **Tool System**: 15 consolidated MCP tools with operation routing
- **API Server**: OpenAI-compatible REST API with SSE streaming
- **Local Inference**: MLX (Metal acceleration) and llama.cpp integration
- **Security**: Working directory authorization, keychain integration, HTTPS enforcement

See [Architecture](developer/architecture.md) for detailed technical information.

---

**Ready to get started?** → [Installation Guide](end-user/getting-started.md)

**Want to see all features?** → [Features Overview](end-user/features-overview.md)

**Need help?** → [Troubleshooting Guide](power-user/troubleshooting.md)
