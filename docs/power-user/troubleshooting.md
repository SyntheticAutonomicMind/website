# Troubleshooting Guide

**Solutions to common issues with SAM.**

Running into problems? This guide covers the most common issues and how to fix them quickly.

---

## Installation Issues

### "SAM.app is damaged and can't be opened"

**Cause**: macOS Gatekeeper blocking unsigned app

**Solution**:
```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine /Applications/SAM.app

# Or allow in System Settings
# System Settings → Privacy & Security → Allow anyway
```

### "SAM.app can't be opened because Apple cannot check it"

**Cause**: First launch security check

**Solution**:
- Right-click SAM.app → Select "Open"
- Click "Open" in security dialog
- Only needed once

---

## API Key Issues

### "Invalid API key"

**Common Causes**:
- Key copied incorrectly (check for extra spaces)
- Key expired or revoked by the provider
- Using the wrong provider's key

**Solutions**:
1. Copy the key again from your provider's website
2. Remove any leading or trailing spaces
3. Verify the key works on the provider's website first
4. Confirm you're using the correct provider (OpenAI vs GitHub Copilot)

### "Insufficient quota" (OpenAI)

**Cause**: Your OpenAI account has no remaining API credits

**Solution**:
- Add a payment method at https://platform.openai.com/account/billing
- Check your usage at https://platform.openai.com/account/usage

### "Rate limit exceeded"

**Cause**: Too many API requests sent in a short time period

**Solutions**:
- Wait 60 seconds and try your request again
- For OpenAI: Upgrade your tier for higher rate limits
- Use local models instead (no rate limits)

---

## Model Issues

### Local model won't load

**Symptoms**: "Failed to load model" error

**Solutions**:

**For MLX models**:
1. Verify you have Apple Silicon (M1/M2/M3/M4)
2. Check model is in `~/Library/Caches/sam/models/`
3. Ensure model is compatible MLX format
4. Close other memory-intensive apps
5. Try smaller model if out of memory

**For GGUF models**:
1. Check model is in `~/Library/Caches/sam/models/`
2. Verify file is valid `.gguf` format
3. Try smaller quantization (Q4 instead of Q8)
4. Reduce context size in Advanced Parameters if out of memory

### Model is very slow

**Solutions**:
- Close other apps to free up RAM
- Use a smaller quantized model (Q4 instead of Q8)
- For MLX: Verify Metal acceleration is enabled
- For GGUF: Reduce the context size in Advanced Parameters
- Check Activity Monitor for high CPU or memory usage

### "Model not found"

**Solution**:
1. Refresh model list (reload button in dropdown)
2. Check model directory permissions
3. Restart SAM
4. Re-download model if corrupted

---

## Tool Issues

### Tools not working

**Symptoms**: Tools aren't being called by the AI, or fail when called

**Solutions**:
1. Enable the **Tools** toggle in the conversation toolbar (or press ⌘T)
2. Click the **Parameters** button to expand Advanced Parameters and check specific tool settings
3. Verify you've granted required system permissions
4. Note: Some models don't support tools (check model capabilities)
5. For local models: Tools are disabled by default (enable manually)

### Terminal tool permission denied

**Solution**:
- Grant Full Disk Access: System Settings → Privacy & Security → Full Disk Access → Add SAM
- Grant Automation: System Settings → Privacy & Security → Automation

### File tool can't read files

**Solution**:
- Grant Files and Folders access when prompted
- System Settings → Privacy & Security → Files and Folders → SAM

### Web fetch fails

**Symptoms**: "Failed to fetch URL" error

**Solutions**:
1. Check your internet connection
2. Verify the URL is accessible in your web browser
3. Some websites block automated requests (try browser_fetch instead)
4. Check your firewall settings aren't blocking SAM

---

## Performance Issues

### SAM is slow to launch

**Common Causes**:
- Loading large conversation history
- Checking for software updates
- Loading model catalogs

**Solutions**:
- Delete old, unused conversations
- Disable automatic update checks in Preferences
- Clear the cache: `~/Library/Caches/sam`

### UI feels laggy

**Solutions**:
- Close unnecessary conversations
- Reduce Advanced Parameters → Context Size
- Disable animations in System Settings
- Restart SAM

### High memory usage

**Solutions**:
- Unload models when not in use (Eject button)
- Use smaller quantized models
- Limit context size
- Close unused conversations

---

## Conversation Issues

### Conversations won't load

**Solutions**:
1. Restart SAM to reinitialize database connections
2. Check disk space - SAM needs free space to operate
3. Check Console.app for specific error messages
4. If a specific conversation fails, try deleting it and creating a new one
5. As a last resort, reset SAM completely (see Database Issues section)

### Can't delete conversation

**Solution**:
- Force quit SAM (⌘+Option+Esc)
- Restart SAM
- Try deleting again

### Conversation history missing

**Possible Causes**:
- Database corruption
- Disk full (no space to save)
- File permissions issue

**Solutions**:
1. Check available disk space
2. Verify database exists: `ls ~/Library/Application\ Support/SAM/`
3. Check database file permissions
4. Restore from Time Machine backup if available

---

## Update Issues

### "Update check failed"

**Common Causes**:
- No internet connection
- GitHub API rate limit reached
- Firewall or network blocking GitHub

**Solutions**:
- Check your internet connection
- Wait and try again later (rate limits reset hourly)
- Manually check the releases page on GitHub

### Update download fails

**Solutions**:
- Download manually from releases page
- Check disk space
- Verify internet connection stable

### Update installation fails

**Solutions**:
- Quit SAM completely
- Manually install: Replace SAM.app in Applications
- Check permissions on /Applications folder

---

## Logging and Debugging

### View SAM logs

**Console.app**:
1. Open Console.app
2. Search for "SAM" in search box
3. Filter by subsystem: `com.sam`

**Terminal**:
```bash
# View real-time logs
log stream --predicate 'subsystem == "com.sam"' --level debug

# View recent logs
log show --predicate 'subsystem == "com.sam"' --last 1h
```

### Export diagnostic information

```bash
# System info
system_profiler SPSoftwareDataType SPHardwareDataType

# SAM version
defaults read /Applications/SAM.app/Contents/Info CFBundleShortVersionString

# Check running processes
ps aux | grep SAM

# Check network connections
lsof -i -P | grep SAM
```

---

## Database Issues

### Reset SAM completely

**⚠️ Warning: This deletes all conversations, settings, and downloaded models**

```bash
# Backup first!
cp -r ~/Library/Application\ Support/SAM ~/Desktop/SAM-Backup
cp -r ~/Library/Caches/sam ~/Desktop/SAM-Cache-Backup

# Remove all data
rm -rf ~/Library/Application\ Support/SAM
rm -rf ~/Library/Caches/sam
defaults delete com.sam.SAM

# Restart SAM (creates fresh data)
```

### Export conversations before reset

Use SAM's built-in export feature:
1. Right-click on a conversation in the sidebar
2. Select **Export**
3. Choose format (JSON, Markdown, PDF, or DOCX)
4. Save to your preferred location

Repeat for each important conversation before resetting.
