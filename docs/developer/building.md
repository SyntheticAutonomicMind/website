# Building SAM from Source

**Everything you need to build SAM from source.**

Want to contribute to SAM? Run the latest development version? Or customize SAM for your needs? This guide walks you through building SAM from source on macOS.

**What's covered:**
- System requirements and prerequisites
- Dependency installation (Xcode, Homebrew, build tools)
- Git submodule setup
- Building debug and release versions
- Common build problems and solutions
- Running and testing your build

**Why build from source:**
- Contribute features or bug fixes
- Test unreleased features
- Customize SAM for your specific needs
- Learn how SAM works internally
- Report issues with detailed diagnostics

**Time required:** 15-30 minutes (first time), 5 minutes (subsequent builds)

**Prerequisites:**
- macOS 14+ (macOS 15 Sequoia recommended)
- Apple Silicon Mac (M1/M2/M3/M4) or Intel Mac
- ~5GB disk space for dependencies and build artifacts
- Basic terminal/command line knowledge

Let's get SAM built and running.

---

## Quick Start (TL;DR)

Ensure Xcode (including Command Line Tools), Homebrew, and required build tools are installed, then run:

```bash
cd /path/to/SAM
git submodule update --init --recursive
make build-debug
```

**If you hit the CMake compiler error** ("No CMAKE_C_COMPILER could be found"), follow the Xcode CLI steps below.

## Platform Requirements

- **macOS 14+** (project `Package.swift` targets macOS 14.0)
- **Xcode** (full app installed, preferred) OR at minimum Xcode Command Line Tools
- **Apple Silicon** (arm64) recommended for best MLX performance; build scripts currently target `arm64`

## Prerequisites (tools)

Install these tools if you haven't already. You mentioned you already installed `cmake`, `ccache`, and Xcode. Good. The rest below are commonly required.

Using Homebrew (recommended):

```bash
# install Homebrew if missing (visit https://brew.sh for details)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# install common build tools
brew install git cmake ccache pkg-config wget
```

Notes:
- `libtool`, `dsymutil`, `clang`, `clang++`, and other Apple toolchain binaries are provided by Xcode / Command Line Tools. They are not installed via Homebrew.
- `ccache` is optional but recommended for faster incremental builds.

## Xcode / Command Line Tools

If CMake complains about missing C/C++ compilers (the error you encountered), it's usually because the Xcode Command Line Tools aren't fully installed or `xcode-select` is not pointing to the right developer directory.

Run these commands to install/verify and accept the license:

```bash
# Install Xcode command line tools (will prompt a GUI dialog)
xcode-select --install

# If you have the full Xcode app, make sure xcode-select points to it (adjust path if you installed Xcode somewhere else)
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer

# Accept the license (required for some CI/headless scenarios)
sudo xcodebuild -license accept

# Verify the developer directory
xcode-select -p

# Check compiler is available
clang --version
clang++ --version
```

If `clang` is missing after installing Xcode CLT, restart your terminal session and re-run `clang --version`.

## Git submodules

The project depends on `external/llama.cpp` (and possibly other externals). Initialize submodules before building:

```bash
git submodule update --init --recursive
```

If the submodule update fails behind a proxy, ensure your Git credentials and proxy settings are correct.

## Swift toolchain and SPM

SAM uses Swift Package Manager (SPM). Ensure your Xcode installation includes a Swift toolchain compatible with `swift-tools-version: 5.9`.

Check Swift version:

```bash
swift --version
```

Resolve Swift packages before building if you want to pre-fetch dependencies:

```bash
swift package resolve
```

You can also run `swift build` or `swift test` to exercise Swift targets directly.

## Building llama.cpp (required binary target)

The `Makefile` runs `scripts/build-llama-macos.sh` which requires:

- cmake
- xcodebuild
- libtool
- dsymutil
- clang (from Xcode)

When you run `make build-debug`, the first step is the `llamacpp` target which runs that script. If that script fails with the CMake compiler error, follow the Xcode / Command Line Tools steps above.

If you prefer to run the builder manually for debugging:

```bash
cd external/llama.cpp
./scripts/build-llama-macos.sh
# or: bash scripts/build-llama-macos.sh
```

Watch the output for missing tool names. The script explicitly checks for `cmake`, `xcodebuild`, `libtool`, and `dsymutil`.

## Build Flow (Recommended Steps)

1. Navigate to the repository root:

```bash
cd /Users/andrew/repositories/fewtarius/SAM
```

2. Initialize submodules and fetch Swift packages:

```bash
git submodule update --init --recursive
swift package resolve
```

3. Build the debug version (this builds llama.cpp first):

```bash
make build-debug
```

4. If successful, find your build at:

**Executable**:
```
.build/Build/Products/Debug/SAM
```

**App Bundle**:
```
.build/Build/Products/Debug/SAM.app
```

## Troubleshooting - Common Errors

### 1. CMake Compiler Not Found

**Error**: "No CMAKE_C_COMPILER could be found" or "No CMAKE_CXX_COMPILER could be found"

**Cause**: Xcode Command Line Tools not installed or `xcode-select` pointing to wrong location

**Fix**:

```bash
# Install CLI tools
xcode-select --install
# Or explicitly point to Xcode
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
# Accept license
sudo xcodebuild -license accept
# Verify
clang --version
cmake --version
```

If the problem persists, try setting environment variables (temporary):

```bash
export CC=clang
export CXX=clang++
make build-debug
```

### 2. Submodule Missing

**Error**: llama.cpp not found

**Fix**:

```bash
git submodule update --init --recursive
```

### 3. Swift Package Resolution Errors

**Error**: SPM network errors or package resolution failures

**Fix**:

```bash
swift package resolve --verbose
# Or inspect Package.resolved
cat Package.resolved
```

### 4. Xcodebuild Scheme Errors

**Error**: `xcodebuild` complains about missing scheme

**Fix**: The Makefile uses scheme `SAM-Package`. If needed, regenerate the Xcode project:

```bash
swift package generate-xcodeproj
# Or open Package.swift directly in Xcode
open Package.swift
```

## Signing / Notarization

The Makefile contains targets to sign and notarize (`sign`, `notarize`, `distribute`). For signing you need a valid Developer ID and the `APPLE_DEVELOPER_ID` environment variable set. Example:

```bash
export APPLE_DEVELOPER_ID='Developer ID Application: Your Name (TEAMID)'
make sign-release
```

## Developer checklist / quick commands

```bash
# 1. Verify developer tools
xcode-select -p
clang --version
cmake --version

# 2. Initialize repo
git submodule update --init --recursive
swift package resolve

# 3. Build debug
make build-debug

# 4. Run
.build/Build/Products/Debug/SAM
```

## Notes and caveats

- The llama.cpp build in `scripts/build-llama-macos.sh` intentionally builds arm64-only frameworks for Apple Silicon. If you need x86_64 support, you'll need to adapt the script and pass `-DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"` and build both architectures.
- MLX integration requires the `mlx-swift` SPM package; make sure your network allows fetching GitHub packages.
- If you require reproducible CI builds, pin package versions in `Package.resolved` and install Homebrew packages as part of the CI image.

---

## Next Steps

After building successfully:

- **[Developers Guide](developers-guide.md)** - Code architecture and contribution guidelines
- **[Contributing](contributing.md)** - How to submit your changes
- **[API Reference](api-reference.md)** - REST API documentation
