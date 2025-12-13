# Configuration Guide

**Fine-tune SAM to work exactly how you want.**

This comprehensive guide covers every setting, preference, and configuration option in SAM. Whether you're optimizing for speed, privacy, cost, or capability, these settings will help you get there.

**What you'll configure:**
- API providers and model selection
- Local model deployment (MLX and GGUF)
- Memory and context settings
- System prompts and behavior
- Advanced parameters for power users

**Who this is for:**
- Power users who want full control
- Teams deploying SAM across multiple users
- Anyone looking to optimize SAM's performance
- Users integrating SAM into existing workflows

---

## Table of Contents

1. [General Settings](#general-settings)
2. [Location Settings](#location-settings)
3. [API Configuration](#api-configuration)
4. [Local Models](#local-models)
5. [Personalities](#personalities)
6. [Shared Topics](#shared-topics)
7. [Conversation Settings](#conversation-settings)
8. [Advanced Parameters](#advanced-parameters)
9. [System Prompts](#system-prompts)

---

## General Settings

### Application Preferences

**Access**: SAM → Preferences (⌘ + ,) → General

**Default Model**:
- Model used for new conversations
- Can be changed per conversation

**Theme**:
- Light Mode
- Dark Mode (follows system)
- Auto (system preference)

**Launch Behavior**:
- Start with previous session
- Start with new conversation
- Restore window position

**Auto-Save**:
- Save conversations automatically
- Interval: 30 seconds (default)

---

## Location Settings

SAM can incorporate location context for more relevant responses.

**Access**: SAM → Preferences (⌘ + ,) → General → Location

### General Location (Manual)

**Purpose**: Provide location context without device permissions

**How to Set**:
1. Open Preferences → General
2. Find "General Location" field
3. Enter your location (e.g., "Austin, TX" or "London, UK")
4. Location used in conversations automatically

**Format Examples**:
- City, State: "Seattle, WA"
- City, Country: "Toronto, Canada"
- Region: "Pacific Northwest"

### Precise Location (Device-Based)

**Purpose**: Automatic location detection using Core Location

**How to Enable**:
1. Open Preferences → General
2. Toggle "Enable Precise Location"
3. Grant location permission when prompted
4. SAM automatically detects your city

**Privacy Features**:
- **City-Level Accuracy**: Uses `kCLLocationAccuracyKilometer`, not GPS
- **Local Storage Only**: Location stored in UserDefaults, never transmitted
- **Opt-In**: Must explicitly enable
- **Easy Disable**: Toggle off anytime

**Location Priority**:
1. Precise location (if enabled and available)
2. General location (if set)
3. No location (if neither configured)

---

## API Endpoints

### OpenAI

**Setup**:
1. Get API key from [platform.openai.com](https://platform.openai.com/api-keys)
2. In SAM: Preferences → **API Endpoints** → click **Add Provider**
3. Select **OpenAI** from the provider type dropdown
4. Paste your key (starts with `sk-`)
5. Click **Test** to verify the connection (optional)
6. Click **Save Provider**

**Available Models**:
- gpt-4-turbo
- gpt-4
- gpt-3.5-turbo
- gpt-4-1106-preview
- gpt-3.5-turbo-1106

**Settings**:
- Organization ID (optional)
- API Base URL (for proxies)
- Max Retries: 3 (default)
- Timeout: 60s (default)

### GitHub Copilot

**Setup (Device Flow Authentication)**:
1. Subscribe at [github.com/features/copilot](https://github.com/features/copilot)
2. In SAM: Preferences → **API Endpoints** → click **Add Provider**
3. Select **GitHub Copilot** from the provider type dropdown
4. Click **Authenticate with GitHub**
5. SAM displays a **user code** and opens GitHub in your browser
6. Enter the code on GitHub's device verification page
7. Authorize SAM to access Copilot
8. SAM automatically receives the access token
9. Click **Save Provider**

**Why Device Flow?**
- Industry-standard OAuth for desktop apps
- No need to copy/paste API keys
- Tokens refresh automatically
- More secure than manual key entry

**Available Models**:
- GPT-4, GPT-4 Turbo
- Claude 3.5 Sonnet (via Copilot)
- o1-preview, o1-mini

**Features**:
- Integrated authentication
- Automatic token refresh
- Free tier support

### Anthropic Claude

**Setup**:
1. Get API key from [console.anthropic.com](https://console.anthropic.com)
2. Preferences → **API Endpoints** → click **Add Provider**
3. Select **Anthropic** from dropdown
4. Paste key (starts with `sk-ant-`)
5. Click **Save Provider**

**Available Models**:
- Claude 3.5 Sonnet
- Claude 3 Opus
- Claude 3 Sonnet
- Claude 3 Haiku

### DeepSeek

**Setup**:
1. Get API key from [platform.deepseek.com](https://platform.deepseek.com)
2. Preferences → **API Endpoints** → click **Add Provider**
3. Select **DeepSeek** from dropdown
4. Paste key
5. Click **Save Provider**

### Google AI / Grok (via Custom Provider)

**Setup**:
1. Get API key from your provider
2. Preferences → **API Endpoints** → click **Add Provider**
3. Select **Custom** from dropdown
4. Configure the OpenAI-compatible endpoint URL
5. Paste API key
6. Click **Save Provider**

**Note**: Gemini and Grok work via the Custom provider option using OpenAI-compatible API endpoints.

---

## Local Models

### MLX Models (Apple Silicon)

**Requirements**:
- Apple Silicon Mac (M1/M2/M3/M4)
- macOS 14.0+
- Metal-capable GPU

**Setup via SAM** (Recommended):
1. Open SAM Preferences → **Local Models**
2. Use the **Download Models** search to find models on HuggingFace
3. Filter by **MLX** to show compatible models
4. Click **Download** to install
5. Model appears in **Installed Models** when complete

**Manual Setup**:
1. Download models from Hugging Face
2. Place in `~/Library/Caches/sam/models/`
3. SAM automatically detects and indexes models
4. Models appear in the model dropdown

**Recommended Models**:
- `mlx-community/Qwen2.5-7B-Instruct-8bit`
- `mlx-community/Mistral-7B-Instruct-v0.3-8bit`
- `mlx-community/Meta-Llama-3-8B-Instruct-8bit`

**Performance**:
- Near-native speed with Metal
- 8-bit: Best quality/size balance
- 4-bit: Faster, more memory efficient

### GGUF Models (All Macs)

**Requirements**:
- Any Mac (Intel or Apple Silicon)
- macOS 14.0+

**Setup via SAM** (Recommended):
1. Open SAM Preferences → **Local Models**
2. Search for models in **Download Models** section
3. Filter by **GGUF** to show compatible models
4. Click **Download** to install
5. Model appears in **Installed Models** when complete

**Manual Setup**:
1. Download .gguf files from Hugging Face
2. Place in `~/Library/Caches/sam/models/`
3. SAM automatically detects and indexes .gguf files
4. Models appear in the model dropdown

**Recommended Sources**:
- [TheBloke on Hugging Face](https://huggingface.co/TheBloke)

**Quantization Levels**:
- Q2: Smallest, lowest quality
- Q4_K_M: Good balance (recommended)
- Q5_K_M: Better quality, larger
- Q8: Best quality, largest

### Stable Diffusion Models

**Requirements**:
- CoreML-converted Stable Diffusion models
- Apple Silicon recommended

**Setup**:
1. Download CoreML-converted models (manual or via CivitAI)
2. Place in your local models directory
3. Filter by model type: "Stable Diffusion"
4. Select and load the model

**Supported**:
- Stable Diffusion 1.5
- Stable Diffusion 2.1
- SDXL (if converted to CoreML)
- Community models from CivitAI

**Generation Settings**:
- **Steps**: 1-150 (default: 25)
- **Guidance Scale**: 1.0-20.0 (default: 7.5)
- **Scheduler**: DPM++ SDE Karras (default), PNDM
- **Karras Timestep Spacing**: Enabled by default for DPM++ scheduler

**Direct SD Mode**:
Select an SD model without an LLM to bypass AI processing and generate images instantly from your exact prompts. Purple send button indicates Direct SD Mode is active.

### ALICE Remote Stable Diffusion

**Purpose**: Generate images on a remote GPU server running ALICE (AI Local Image Creation Engine). Useful for AMD GPU hardware like Steam Deck.

**Setup**:
1. Open SAM Preferences → **Stable Diffusion** → **Settings**
2. Enter ALICE server URL (e.g., `http://192.168.0.222:8090/v1`)
3. Enter API key (if required by your server)
4. Click **Test** to verify connection
5. Models from ALICE server appear in the model picker

**Using ALICE Models**:
1. Select an ALICE model from the model picker (shows "ALICE" location)
2. UI switches to Stable Diffusion generation mode
3. Enter your prompt and generate
4. Images are generated on the remote server and downloaded automatically

**Requirements**:
- Running ALICE server on your network
- Network access to the server
- Server must have at least one Stable Diffusion model loaded

**Model Picker Display**:
- Local models show "Local" location
- ALICE models show "ALICE" location
- Provider shows as "Stable Diffusion" for all SD models

### CivitAI Model Browser

**Access**: Preferences → Image Generation → Model Browser → CivitAI tab

Browse and download community-created Stable Diffusion models from CivitAI's massive library.

**API Key** (Optional):
1. Visit https://civitai.com
2. Sign in or create account
3. Go to Account Settings → API Keys
4. Create new API key and paste in SAM

**Note**: API key is optional. Works without authentication, but with lower rate limits.

**Download Settings**:
- **Download Path**: Where models are saved (default: local models directory)
- **Auto-Convert**: Automatically convert downloaded models to CoreML format
- **NSFW Filter**: Control visibility of adult content

**Features**:
- Search thousands of community models
- Filter by type, rating, and period
- View model details and example images
- One-click download and install
- Automatic CoreML conversion (if enabled)
- Models appear in model picker immediately

**Workflow**:
```
1. Open Preferences → Image Generation → Model Browser
2. Select CivitAI tab
3. Search for models (e.g., "anime style")
4. Browse results and preview images
5. Click download on desired model
6. Model auto-converts to CoreML (if enabled)
7. Select model from picker and start generating
```

### HuggingFace Model Browser

**Access**: Preferences → Image Generation → Model Browser → HuggingFace tab

Discover and download models directly from HuggingFace Hub.

**Features**:
- Browse HuggingFace model repository
- Search by keywords and tags
- View model details and descriptions
- One-click download and install
- Auto-load results when switching tabs

**Workflow**:
```
1. Open Preferences → Image Generation → Model Browser
2. Select HuggingFace tab
3. Search for models or browse popular options
4. Click download on desired model
5. Model appears in model picker
```

### LoRA Browser

**Access**: Preferences → Image Generation → LoRA Browser

Discover and manage LoRA (Low-Rank Adaptation) models for fine-tuning image generation.

**Three Tabs**:
- **Library**: View and manage your installed LoRAs
- **CivitAI**: Browse and download LoRAs from CivitAI
- **HuggingFace**: Discover LoRAs from HuggingFace Hub

**Supported Base Models**:
- SD 1.5
- SD 2.x
- SDXL
- Z-Image
- Flux

**Features**:
- Auto-load search results when switching tabs
- Pagination support for CivitAI (100 results per page)
- Base model filter for compatibility
- NSFW filter control
- View LoRA trigger words and compatibility info

**Using LoRAs**:
1. Browse and download LoRAs via the LoRA Browser
2. When generating images, reference LoRA by filename in your prompt
3. SAM automatically resolves paths and applies LoRAs during generation

**Tip**: Use the `list_loras` operation in the `image_generation` tool to see all available LoRAs with their compatibility info and trigger words.

---

## Personalities

SAM includes a comprehensive personality system with built-in personalities organized into categories.

**Access**: SAM → Preferences (⌘,) → Personalities

### Default Personalities

**General:**
- **Assistant** (default): Balanced, helpful, professional
- **Professional**: Business communication with response frameworks
- **Coach**: Supportive guidance and motivation

**Creative & Writing:**
- **Muse**: Brainstorming and ideation partner
- **Wordsmith**: Encouraging writing assistant
- **Document Assistant**: Document formatting and organization
- **Image Architect**: Transforms ideas into visual descriptions
- **Artist**: Creative soul with artistic appreciation

**Tech:**
- **Tech Buddy**: Friendly tech support for all levels
- **Tinkerer**: Hands-on problem solver with community-first mentorship
- **Crusty Coder**: Grumpy but brilliant senior developer
- **BOFH**: The legendary Bastard Operator From Hell

**Productivity:**
- **Motivator**: Productivity buddy for procrastination

**Domain Experts:**
- **Doctor**: Clinical diagnostic methodology
- **Counsel**: IRAC legal analysis framework
- **Finance Coach**: Financial literacy guide
- **Trader**: Options trading analyst
- **Scientist**: Research and scientific methodology
- **Philosopher**: Deep thinking and existential exploration

**Fun & Character:**
- **Comedian**: Comedy toolkit with techniques
- **Pirate**: Yarr! Nautical adventure personality
- **Time Traveler**: Temporal explorer from the future
- **Jester**: Playful court entertainer

### Creating Custom Personalities

1. Open Preferences → Personalities
2. Click **New Personality**
3. Fill in:
   - **Name**: Display name for the personality
   - **Description**: Short description (shown in tooltips)
   - **Traits**: Select personality traits from categories (tone, formality, verbosity, humor, teachingStyle)
   - **Custom Instructions**: Detailed behavior instructions
4. Click **Create Personality**

**Custom Instructions Example:**
```
You are a senior Swift developer specializing in iOS and macOS.
Always suggest modern Swift patterns (async/await, SwiftUI).
Avoid deprecated APIs and explain technical decisions briefly.
Prefer value types over reference types when appropriate.
```

### Setting Default Personality

1. Open Preferences → Personalities
2. Find the **"Default for New Conversations"** dropdown at the top
3. Select your preferred personality from the dropdown
4. New conversations will use this personality automatically

### Per-Conversation Selection

Each conversation can use a different personality:
1. Open conversation
2. Click personality selector in header
3. Choose from list (grouped by category)
4. Personality takes effect immediately

### Managing Personalities

**Edit**: Select personality → Modify fields → Save
**Delete**: Select custom personality → Click Delete (cannot delete defaults)
**Reset**: Delete all custom to restore defaults only

---

## Shared Topics

### Creating Topics

**Access**: Preferences → Shared Topics

**Create New Topic**:
1. In the **Create New Topic** section, enter a name in the **"Topic name"** field
2. Optionally add a description in the **"Description (optional)"** field
3. Click the **Create** button

**Result**: Creates directory at `~/SAM/{topic-name}/`

### Managing Topics

**Rename**:
1. Select topic
2. Click "Edit" or double-click name
3. Enter new name
4. Save

**Delete**:
1. Select topic
2. Click "Delete"
3. **WARNING**: Deletes all shared memories!
4. Confirm deletion

**Topic Settings**:
- Name (human-readable)
- Description (optional)
- Created date
- Last modified
- Memory count

---

## Conversation Settings

### Per-Conversation Configuration

**Access**: Click the **Parameters** button (slider icon) in the conversation toolbar to expand advanced parameters.

**Model Selection**:
- Use the model dropdown in the toolbar to select a different model
- Switch mid-conversation (applies to future messages only)

**Tools Toggle**:
- Toggle **Tools** on/off directly in the toolbar
- Or press ⌘T

**Shared Topics**:
- Toggle **Shared Topic** on/off in the toolbar
- Select topic from dropdown when enabled
- Changes working directory immediately

---

## Advanced Parameters

### Context & Generation

**Temperature** (0.0 - 2.0):
- **0.0**: Deterministic, focused, consistent
- **0.7**: Balanced (default)
- **1.0**: Creative, varied responses
- **1.5+**: Very creative, unpredictable

**Top-P** (0.0 - 1.0):
- Nucleus sampling - controls response diversity
- **1.0**: Full vocabulary (default)
- **0.9**: Top 90% of probability mass
- **Lower values**: More focused responses

**Max Tokens**:
- Maximum response length
- Configurable based on your needs
- Uses model defaults when not specified

**Context Size** (YaRN Profiles):
- **Default**: Low scaling for regular conversations
- **Extended**: Medium scaling for longer conversations
- **Universal**: High scaling for large documents (default)
- **Mega**: Enterprise scaling for massive documents

### Tool Configuration

**Advanced Tools**:
- Enable: Powerful operations allowed
- Disable: Only safe tools (default)

**Tool Categories**:
- Core: always enabled
- File Operations: configurable
- Terminal: requires approval
- Web: configurable
- Documents: configurable

### Iteration Management

**Max Iterations**:
- Configurable iteration limits
- Higher values allow more complex tasks
- Balance between autonomy and control

**Dynamic Iterations**:
- Enable: SAM can request more iterations when needed
- Disable: Hard limit enforced

---

## System Prompts

### Built-in Prompts

**General Assistant**:
- Default balanced assistant
- Good for all tasks

**Code Expert**:
- Specialized for programming
- Emphasizes best practices

**Research Assistant**:
- Optimized for research
- Comprehensive analysis

**Creative Writer**:
- Enhanced creativity
- Storytelling focus

### Custom Prompts

**Create**:
1. Preferences → System Prompts
2. Click "+"
3. Enter name and content
4. Save

**Variables**:
- `{{working_directory}}`: Current directory
- `{{conversation_title}}`: Conversation name
- `{{date}}`: Current date
- `{{user_name}}`: User name (if set)

**Example**:
```
You are a Python expert helping with {{conversation_title}}.
Working directory: {{working_directory}}
Focus on clean, maintainable code following PEP 8.
```

### Mini Prompts

**Purpose**: Quick prompt snippets for workflows

**Create**:
1. Preferences → Mini Prompts
2. Click "+"
3. Enter keyword and content
4. Save

**Use**: Type keyword in conversation

**Example**:
- Keyword: `review`
- Content: "Review this code for security issues, performance, and maintainability."

---

## Keyboard Shortcuts

**Global**:
- ⌘N: New conversation
- ⌘,: Preferences
- ⌘Q: Quit SAM
- ⌘W: Close window
- ⌘?: Open Help

**Conversation**:
- ⌘T: Toggle tools on/off
- ⌘K: Clear chat input
- ⌘Return: Send message
- ⌘L: Focus message input
- ⌘[: Previous conversation
- ⌘]: Next conversation

**File Operations**:
- ⌘O: Open file/conversation
- ⌘S: Save conversation
- ⌘E: Export conversation
- ⌘I: Import document

**Editor**:
- ⌘Z: Undo
- ⇧⌘Z: Redo
- ⌘A: Select all
- ⌘C: Copy
- ⌘V: Paste

---

## Security Settings

**API Keys**:
- Stored securely in macOS Keychain
- Never logged or transmitted (except to the provider's API)
- View or edit in Preferences

**Working Directory Authorization**:
- **Inside working directory**: Auto-approved operations
- **Outside working directory**: Requires your confirmation
- Can whitelist trusted directories

**HTTPS Enforcement**:
- All web operations require HTTPS
- HTTP requests automatically upgraded to HTTPS for security

---

## Performance Settings

**Memory Management**:
- Lazy loading: Databases loaded on-demand
- Auto-cleanup: Old memories pruned
- Cache size: Configurable

**Context Management**:
- Auto-pruning at 70% token limit
- YaRN compression configurable
- Cache conversation context

---

## Troubleshooting Configuration

**Reset to Defaults**:
1. Quit SAM
2. Delete: `~/Library/Application Support/SAM/config.json`
3. Restart SAM

**Backup Configuration**:
```bash
cp ~/Library/Application\ Support/SAM/config.json ~/SAM-config-backup.json
```

**Export/Import**:
- Use Preferences → Advanced → Export/Import
- Saves all settings to JSON file

---

## Next Steps

- **[Tools Reference](tools-reference.md)** - Complete MCP tools reference
- **[Advanced Workflows](advanced-workflows.md)** - Complex patterns
- **[Troubleshooting](troubleshooting.md)** - Common issues

---

**Master SAM's configuration for optimal performance!**
