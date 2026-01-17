# SAM Web: Remote Access

**Access SAM from your iPad, iPhone, or any device with a browser.**

SAM Web is a web interface that lets you chat with SAM when you're away from your Mac. Perfect for quick questions from your tablet or accessing SAM from other devices on your network.

---

## What is SAM Web?

SAM Web is a browser-based interface that lets you chat with SAM from any device. All of SAM's backend features work through the chat interface - you're just controlling SAM remotely.

**How it works:**

SAM Web connects to SAM running on your Mac. When you chat with SAM through your iPad's browser, SAM executes everything on your Mac and streams the responses back to you. This means:

- ✅ **All SAM features work**: Image generation, file operations, terminal commands, web research, memory/RAG, and more
- ✅ **Full conversation management**: System prompts, personalities, mini-prompts, shared topics, folders
- ✅ **All your AI models**: Use any provider or model you've configured in SAM
- ✅ **Everything happens on your Mac**: Files are read/written on your Mac, images are saved on your Mac, terminal runs on your Mac

**What's different:**
- You can't drag-and-drop documents into the browser to upload them (may be available in a future release)
- You need SAM running on your Mac with the API server enabled
- You need network access to your Mac (same Wi-Fi or VPN)

Think of SAM Web as a remote control for SAM. Everything SAM can do, you can do through SAM Web - you're just doing it from a different device.

---

## Requirements

Before using SAM Web, you need:

1. **SAM installed and running** on your Mac
   - Download from [GitHub Releases](https://github.com/SyntheticAutonomicMind/SAM/releases)
   - SAM must stay running while you use SAM Web

2. **API server enabled** in SAM
   - Go to **SAM → Preferences → API Server**
   - Toggle **Enable API Server**
   - Copy your **API token** (you'll need this for SAM Web)

3. **Network access** to your Mac
   - Same network: Works automatically if both devices are on same Wi-Fi
   - Remote access: Requires VPN or port forwarding (advanced)

4. **Web browser** on your device
   - Safari, Chrome, Firefox, or any modern browser
   - Tested on macOS, iOS, iPadOS

---

## Getting Started

### Option 1: Quick Start (Recommended)

The easiest way to use SAM Web is to serve it directly from the repository:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SyntheticAutonomicMind/SAM-web.git
   cd SAM-web
   ```

2. **Start a local web server:**
   ```bash
   # Using Python (built into macOS)
   python3 -m http.server 8000
   
   # Or using Node.js
   npx http-server -p 8000 --cors
   
   # Or using Caddy
   caddy file-server --listen :8000
   ```

3. **Open in your browser:**
   - On same device: `http://localhost:8000`
   - On other devices: `http://YOUR_MAC_IP:8000`
     - Find your Mac's IP in **System Settings → Network**

4. **Connect to SAM:**
   - Enter your API token from SAM Preferences → API Server
   - Click **Connect to SAM**
   - Start chatting

### Option 2: Direct API Connection

You can also connect directly to SAM's API without downloading SAM Web:

1. Visit the hosted version (if available) or any SAM Web instance
2. Configure the connection to point to your Mac's IP address
3. Enter your API token
4. Start chatting

---

## Using SAM Web

### First-Time Setup

1. **Get your API token:**
   - Open SAM on your Mac
   - Go to **SAM → Preferences → API Server**
   - Copy the **API Token**

2. **Find your Mac's IP address:**
   - Go to **System Settings → Network**
   - Note your IP address (e.g., `192.168.1.100`)
   - Only needed for access from other devices

3. **Open SAM Web:**
   - In your browser, go to `http://localhost:8000` (same device)
   - Or `http://192.168.1.100:8000` (from iPad/other device)

4. **Enter credentials:**
   - Paste your API token
   - Click **Connect to SAM**

### Basic Features

**Chat Interface:**
- Type your message and press Enter or click Send
- See responses stream in real-time
- Code blocks have syntax highlighting
- Click copy button on code blocks to copy

**Conversations:**
- Create new conversations with the **New** button
- Load previous conversations from the sidebar
- Delete conversations with the trash icon
- Rename conversations by clicking the conversation title

**Mini-Prompts:**
- Quick context injection for specialized tasks
- Click the prompts icon to view available mini-prompts
- Click a mini-prompt to add it to your message
- Create, edit, or delete mini-prompts

**Model Selection:**
- Choose from available AI models
- Switch models mid-conversation
- Models must be configured in SAM first

**Parameters:**
- Adjust temperature for more creative or focused responses
- Configure top_p for sampling control
- Set max tokens for response length

### Tips for Best Experience

**On iPad:**
- Add to Home Screen for app-like experience
- Use landscape mode for more screen space
- Keyboard shortcuts work: Enter to send, Escape to cancel

**Performance:**
- Keep SAM and your device on the same network for best speed
- Close unused conversations to keep interface responsive
- Large conversations may load slower over network

**Privacy:**
- All data stays on your Mac (SAM Web is just an interface)
- API token is stored in your browser's LocalStorage
- No data sent to external servers

---

## Troubleshooting

### "Failed to connect to SAM"

**Possible causes:**
1. SAM is not running on your Mac
2. API server is disabled in SAM Preferences
3. Wrong API token
4. Network connectivity issues

**Solutions:**
1. Verify SAM is running with API server enabled
2. Check that your API token is correct (copy fresh from SAM)
3. Make sure both devices are on same network
4. Try pinging your Mac's IP address: `ping 192.168.1.100`

### "CORS errors in browser console"

**This shouldn't happen with normal setup**, but if it does:
1. Make sure you're serving SAM Web from a web server (not opening `index.html` directly)
2. Check that SAM's API server allows your origin
3. Try accessing from `http://localhost:8000` instead of file://

### "Models not loading"

1. Verify models are configured in SAM (open SAM → Preferences → Providers)
2. Check that at least one provider is configured with valid credentials
3. Refresh the SAM Web page to reload model list

### Connection works on Mac but not iPad

1. **Check network:** Make sure iPad is on same Wi-Fi network
2. **Find correct IP:** Use your Mac's local IP (192.168.x.x), not 127.0.0.1
3. **Check firewall:** macOS Firewall might be blocking connections
   - Go to **System Settings → Network → Firewall**
   - Add SAM to allowed apps or temporarily disable firewall to test
4. **Test port:** Try `http://YOUR_MAC_IP:8080` (SAM API) in iPad browser
   - You should see a JSON response if API is accessible

---

## Security Considerations

### Network Security

**Local network use (recommended):**
- Keep SAM Web on your trusted home/office network
- Use strong Wi-Fi password
- Don't expose port 8080 directly to internet

**Remote access (advanced users):**
- Use VPN to connect to your home network
- Or set up secure port forwarding through your router
- Consider using HTTPS with proper certificate

### Token Management

- API token grants full access to SAM's features
- Don't share your API token
- Rotate token periodically (regenerate in SAM Preferences)
- Revoke token if you suspect it's compromised

### Data Privacy

- SAM Web stores API token in browser LocalStorage
- All conversations stay on your Mac
- No data sent to external servers
- Use HTTPS if accessing over untrusted networks

---

## What You Can and Can't Do

SAM Web is a remote interface to SAM. All AI work happens on your Mac where SAM is installed. You're just controlling it from a different device.

**Everything works through chat:**
- Chat with full streaming responses
- Use all conversation features (system prompts, personalities, mini-prompts, shared topics, folders)
- Access all AI models and providers you've configured
- Generate images (saved on your Mac)
- Read, write, and edit files (on your Mac)
- Run terminal commands (on your Mac)
- Search your documents and memory
- Use all of SAM's tools and capabilities

**What's missing:**
- **Document upload**: Can't drag-and-drop documents into the browser yet (may be available in a future release)
- **LoRA training UI**: No web interface for training models (use the native app)
- **Conversation export**: Can't export conversations as files (use the native app)
- **Memory/RAG management UI**: Can't manage documents through a UI (but SAM can still access them via tools)

The key thing to understand: When you ask SAM to do something through SAM Web, it happens on your Mac. If you ask SAM to generate an image, edit a file, or run a command, it does that on your Mac and shows you the results.

---

## Technical Details

### Architecture

**Frontend:**
- Pure HTML5, CSS3, JavaScript (ES6+)
- No build step or dependencies
- Zero npm packages
- All assets self-hosted

**Communication:**
- REST API via SAM's Vapor server
- Server-Sent Events (SSE) for streaming
- Bearer token authentication

**Storage:**
- LocalStorage for API token and settings
- SessionStorage for temporary state
- No backend database (all data in SAM)

### API Endpoints Used

- `POST /api/chat/completions` - Send messages
- `GET /api/conversations` - List conversations
- `POST /api/conversations` - Create conversation
- `DELETE /api/conversations/:id` - Delete conversation
- `GET /api/models` - List available models
- `GET /api/prompts/mini` - List mini-prompts
- `POST /api/prompts/mini` - Create mini-prompt

### Browser Compatibility

- ✅ Safari 14+ (macOS, iOS, iPadOS)
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+

**Minimum requirements:**
- JavaScript enabled
- LocalStorage support
- Server-Sent Events (SSE) support
- Modern CSS (Grid, Flexbox)

---

## Repository

**Source code:** [github.com/SyntheticAutonomicMind/SAM-web](https://github.com/SyntheticAutonomicMind/SAM-web)

**License:** GNU General Public License v3.0 (same as SAM)

**Contributions:** Welcome! See repository for contribution guidelines.

---

## Related Documentation

- [Features Overview](features-overview.md) - All SAM capabilities
- [Getting Started](getting-started.md) - Install and configure SAM
- [Configuration](../power-user/configuration.md) - Set up API server and providers
- [Troubleshooting](../power-user/troubleshooting.md) - Fix common issues

---

**SAM Web brings SAM to your iPad and other devices. For full features, use the native macOS app.**
