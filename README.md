# 👾 LuciferAI Local - Warp AI Clone

A **local, open-source terminal AI assistant** modeled after Warp AI. Execute commands, read/write files, search codebases, and more—all from an interactive terminal interface.

## 🌟 Features

### ✅ Phase 1 Complete
- **File Operations**: Read, write, edit, find files ✅
- **Code Search**: Grep-style search across directories ✅
- **Command Execution**: Run shell commands safely with risk detection ✅
- **Directory Listing**: Browse filesystem with metadata ✅
- **Environment Info**: Get current directory, user, shell info ✅
- **Interactive CLI**: Clean, colorful terminal interface ✅

### ✅ Phase 2 Complete - FixNet & Self-Healing
- **Authentication**: AES-256 encryption with device binding ✅
- **Auto-Fix**: Automatic error detection and repair ✅
- **FixNet Upload**: Encrypted fixes to public GitHub repo ✅
- **Relevance Dictionary**: Collaborative learning from all users ✅
- **Branch Tracking**: Links between related fixes ✅
- **Remote Search**: Find fixes from other users ✅

### 🔮 Phase 3 - Coming Soon
- **AI Model Integration**: Mistral, OpenAI, Claude, Ollama support
- **Conversation Memory**: Multi-turn conversations with context
- **Code Analysis**: AST-based code understanding

## 🚀 Quick Start

### Installation

```bash
cd ~/Desktop/Projects/LuciferAI_Local

# Install dependencies (no AI models yet for testing)
pip3 install rich colorama prompt_toolkit watchdog pathspec

# Make executable
chmod +x lucifer.py

# Run
./lucifer.py
```

### Usage Examples

```
You > help
👾 LuciferAI Capabilities...

You > read config.yaml
🔍 Reading file: config.yaml
✅ Read config.yaml (50 lines, 1234 bytes)
[file contents...]

You > find *.py
🔍 Finding files: *.py
✅ Found 5 Python files matching '*.py':
  📄 lucifer.py
  📄 core/agent.py
  📄 tools/file_tools.py
  ...

You > run git status
⚡ Running command: git status
✅ Command executed successfully:
On branch main
nothing to commit, working tree clean

You > list .
📂 Listing directory: .
✅ Contents of /Users/.../LuciferAI_Local:
  📁 core
  📁 tools
  📄 lucifer.py (2453 bytes)
  ...

You > exit
👋 Farewell, mortal. LuciferAI signing off.
```

## 📁 Project Structure

```
LuciferAI_Local/
├── lucifer.py              # Main CLI entry point
├── core/
│   └── agent.py            # Agent orchestrator & request router
├── tools/
│   ├── file_tools.py       # File operations (read/write/search)
│   └── command_tools.py    # Command execution & environment
├── logs/                   # Conversation logs (future)
├── tests/                  # Test suite
└── requirements.txt        # Python dependencies
```

## 🔧 Tool Functions

### File Tools (`tools/file_tools.py`)
- `read_file(path, line_range)` - Read files with optional line range
- `write_file(path, content)` - Write/create files
- `edit_file(path, search, replace)` - Search and replace in files
- `find_files(pattern, search_dir)` - Find files by pattern
- `grep_search(query, path)` - Search text in files
- `list_directory(path)` - List directory contents

### Command Tools (`tools/command_tools.py`)
- `run_command(command, cwd, timeout)` - Execute shell commands
- `run_python_code(code)` - Run Python code safely
- `get_env_info()` - Get environment information
- `check_command_exists(command)` - Check if command is available
- `is_risky_command(command)` - Detect dangerous commands

## 🧪 Testing

Each module has built-in tests:

```bash
# Test file tools
cd tools && python3 file_tools.py

# Test command tools
cd tools && python3 command_tools.py

# Test agent
cd core && python3 agent.py
```

## 🔒 Safety Features

- **Risky Command Detection**: Blocks dangerous commands (rm -rf, dd, etc.)
- **Timeout Protection**: Commands auto-timeout after 30s
- **Sandboxed Python**: Python code runs in subprocess
- **Path Validation**: All file paths are validated
- **Error Handling**: Comprehensive try/catch blocks

## 🎨 Current Workflow

```
User Input → Agent.process_request()
            ↓
    Parse Intent (regex-based)
            ↓
    Route to Handler (_handle_read_file, etc.)
            ↓
    Call Tool Function (read_file, run_command, etc.)
            ↓
    Format Response
            ↓
    Return to User
```

## 🚧 Roadmap

### Phase 1: Core Tools ✅ (Complete)
- [x] File operations
- [x] Command execution
- [x] Search functionality
- [x] Interactive CLI
- [x] Safety checks

### Phase 2: AI Integration (Next)
- [ ] Add Mistral AI client
- [ ] Implement conversation memory
- [ ] Add streaming responses
- [ ] Create AI model abstraction layer
- [ ] Support OpenAI, Claude, Ollama

### Phase 3: Advanced Features
- [ ] RAG with ChromaDB/FAISS
- [ ] Code analysis (AST parsing)
- [ ] Auto-fix suggestions
- [ ] File watcher daemon
- [ ] Git integration
- [ ] Multi-step planning

### Phase 4: GUI & Distribution
- [ ] PyQt5 GUI (optional)
- [ ] Build macOS .app
- [ ] Cross-platform packaging
- [ ] Plugin system

## 🤝 How to Add AI Models

### Option 1: Mistral AI (Recommended)

```bash
# Install
pip install mistralai

# Set API key
export MISTRAL_API_KEY="your-key-here"

# Usage in agent.py (coming soon)
from mistralai.client import MistralClient

client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
response = client.chat(
    model="mistral-large-latest",
    messages=[{"role": "user", "content": user_input}]
)
```

### Option 2: Ollama (Local, Free)

```bash
# Install Ollama
brew install ollama

# Download model
ollama pull codellama

# Usage (coming soon)
import ollama
response = ollama.chat(
    model="codellama",
    messages=[{"role": "user", "content": user_input}]
)
```

### Option 3: OpenAI

```bash
pip install openai
export OPENAI_API_KEY="your-key-here"
```

## 📝 Contributing

This is a personal project, but feel free to fork and customize!

## ⚖️ License

MIT License - Do whatever you want with it!

## 🎯 Design Philosophy

**Why not just use Warp AI?**
- Learn how agentic systems work
- Full control over data and privacy
- Customize for specific workflows
- Integrate with local tools
- No API costs with local models

**Inspired by:**
- Warp AI
- GitHub Copilot
- Cursor
- Aider

## 🩸 The LuciferAI Way

> "Born in Neon. Forged in Silence."

Purple theme, skull emojis, and a rebellious attitude. Because AI assistants don't have to be boring.

---

**Status**: Phase 1 Complete ✅ | Phase 2 In Progress 🚧

Made with 🩸 by TheRustySpoon
