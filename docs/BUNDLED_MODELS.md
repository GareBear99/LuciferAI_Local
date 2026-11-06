# 🎁 LuciferAI Bundled Models

LuciferAI's bundled setup downloads **llamafile** (0.8.6) and **TinyLlama** (~600MB) via `./setup_bundled_models.sh`, providing instant AI capabilities that work on all systems, including legacy macOS versions. The llamafile runner also ships in the repo as split parts (`bin/llamafile.part.*`) that `lucifer.py` assembles on first run; the TinyLlama model itself is **not** in the repo and must be downloaded.

---

## 🚀 Quick Setup

Run the bundled setup script to download and configure models:

```bash
./setup_bundled_models.sh
```

This will:
1. Create `.luciferai/bin/` and `.luciferai/models/` inside the project directory
2. Download llamafile 0.8.6 (~34MB) into `.luciferai/bin/`
3. Download TinyLlama 1.1B model (~600MB, TheBloke GGUF) into `.luciferai/models/`

**Total download:** ~634MB

> **Where the files go — read this before trusting the paths below.** The setup script installs to `<project>/.luciferai/`, which is where the llamafile agent looks (`core/llamafile_agent.py`). But `lucifer.py`'s startup check looks in `~/.luciferai/`, `bin/`, and `models/` — it does **not** look in `.luciferai/` — so after the setup script the banner may still report "Not installed" even though the agent can use the model (a code inconsistency, flagged for a follow-up fix). If the banner says "Not installed", copy the files to `~/.luciferai/bin/` + `~/.luciferai/models/` (or to the repo's `bin/` + `models/`, which the "Manual Installation" section below does and which the startup check does read).

---

## 📦 What's Included

### llamafile (Tier 0 Platform)
- **Location (setup script):** `.luciferai/bin/llamafile`
- **Location (manual install / assembled from repo parts):** `bin/llamafile`
- **Size:** 34MB
- **Compatibility:** All macOS versions (Catalina+), Linux
- **Purpose:** Standalone AI model runner (no dependencies)

### TinyLlama 1.1B (Tier 0 Model)
- **Location (setup script):** `.luciferai/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf`
- **Location (manual install):** `models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf`
- **Size:** 600MB
- **Tier:** 0 (Ultra-Lightweight)
- **Use Cases:**
  - Basic chat and Q&A
  - Quick responses
  - Emergency fallback
  - Legacy system support

---

## 🎯 Usage

### Direct Usage
```bash
# Interactive chat — after the setup script (paths in .luciferai/)
./.luciferai/bin/llamafile -m ./.luciferai/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --interactive

# Single prompt
./.luciferai/bin/llamafile -m ./.luciferai/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -p "Explain Python decorators"

# After a manual install (paths in bin/ + models/)
./bin/llamafile -m ./models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --interactive
```

### In LuciferAI
```bash
python3 lucifer.py
```

The main banner will automatically detect bundled models:
```
🤖 AI Models:
   ✅ llamafile (bundled)
   ✅ TinyLlama 1.1B (bundled, Tier 0)
```

---

## 🔄 Tier System Integration

LuciferAI uses a **5-tier model system (Tier 0-4)**:

| Tier | Models | Use Case | RAM |
|------|--------|----------|-----|
| **🟢 Tier 0** | TinyLlama, Phi | Basic tasks, legacy systems | <8GB |
| **🔵 Tier 1** | Llama 3.2, Gemma 2B | Quick responses, chat | 8-16GB |
| **🟡 Tier 2** | Mistral, Llama 3.1 | Balanced coding | 16-32GB |
| **🔴 Tier 3** | DeepSeek, Mixtral | Expert coding | 32GB+ |
| **🟣 Tier 4** | Llama3.1-70B | Frontier / Ultra-Expert | 32GB+ (64GB+ recommended) |

> **Tier 5 (Cloud AI / GPT-4) is coming soon, not shipped.** Model tiers are Tier 0-4.

**Bundled models (Tier 0)** work as:
- ✅ Emergency fallback when system resources are low
- ✅ Primary AI on macOS Catalina and older
- ✅ Portable AI that doesn't require Ollama
- ✅ Quick setup for testing

---

## 📁 Directory Structure

After the setup script:
```
LuciferAI_Local/
├── .luciferai/
│   ├── bin/
│   │   └── llamafile                              # 34MB, executable
│   └── models/
│       └── tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf  # 600MB, model file
├── setup_bundled_models.sh                    # Setup script
└── lucifer.py                                 # Main CLI
```

After a manual install (or after `lucifer.py` assembles llamafile from the repo's split parts):
```
LuciferAI_Local/
├── bin/
│   └── llamafile                              # 34MB, executable
├── models/
│   └── tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf  # 600MB, model file
```

The setup-script location (`.luciferai/`) is where the llamafile agent looks; the manual/assembly location (`bin/` + `models/`) is what `lucifer.py`'s startup check reads, along with `~/.luciferai/`. See the note in Quick Setup — the two locations do not fully overlap, which is a known code inconsistency.

---

## 🔧 Manual Installation

If the setup script doesn't work or you want to install manually — this installs into the repo's `bin/` + `models/`, which `lucifer.py`'s startup check reads (along with `~/.luciferai/`):

### 1. Create Directories
```bash
mkdir -p bin models
```

### 2. Download llamafile
```bash
# macOS / Linux
curl -L -o bin/llamafile https://github.com/Mozilla-Ocho/llamafile/releases/download/0.8.6/llamafile-0.8.6
chmod +x bin/llamafile
```

### 3. Download TinyLlama
```bash
curl -L -o models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
  https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

---

## 🆚 Bundled vs Ollama Models

### Bundled (llamafile + TinyLlama)
**Pros:**
- ✅ Works on macOS Catalina (10.15)
- ✅ No dependencies
- ✅ Portable (stays in project)
- ✅ Quick setup

**Cons:**
- ⚠️ Tier 0 only (basic capabilities)
- ⚠️ Slower than Ollama
- ⚠️ Limited model selection

### Ollama Models
**Pros:**
- ✅ Full tier support (Tier 0-4)
- ✅ Faster inference
- ✅ Large model library
- ✅ Easy model management

**Cons:**
- ⚠️ Requires macOS Sonoma (14.0+)
- ⚠️ Separate installation
- ⚠️ Global system dependency

---

## 🎓 Upgrade Path

**Start:** Bundled models (Tier 0)
```bash
./setup_bundled_models.sh
```

**Upgrade:** Install Ollama for more models
```bash
./setup_luci.sh              # First: defines the luci shell function (reload your shell)
luci install ollama          # macOS Sonoma+ only
luci install llama3.2        # Tier 1
luci install mistral         # Tier 2
luci install deepseek-coder  # Tier 3
```

**Result:** Both systems work together
- Bundled models: Emergency fallback
- Ollama models: Primary AI

---

## 🧪 Testing

Verify bundled models are working:

```bash
# Test llamafile (setup-script location)
./.luciferai/bin/llamafile --version

# Test TinyLlama
./.luciferai/bin/llamafile -m ./.luciferai/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -p "Hello"

# After a manual install, the same commands with ./bin/llamafile and ./models/...

# Test in LuciferAI
python3 lucifer.py
# Banner should show: ✅ llamafile (bundled)
#                     ✅ TinyLlama 1.1B (bundled, Tier 0)
# (See the Quick Setup note: the banner checks ~/.luciferai/, bin/, and models/ —
#  it may report "Not installed" after the setup script even though the agent can use the model.)
```

---

## 🔍 Troubleshooting

### "Permission denied" when running llamafile
```bash
chmod +x bin/llamafile
```

### "No such file or directory"
```bash
# Ensure paths are correct
ls -l bin/llamafile
ls -l models/tinyllama-*.gguf
```

### Model not detected in banner
```bash
# Check exact filename
ls models/
# Should show: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

### Download interrupted
```bash
# Remove partial file and retry (setup script downloads to .luciferai/models/)
rm .luciferai/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
./setup_bundled_models.sh
```

---

## 📚 Related Documentation

- [MODEL_TIERS.md](MODEL_TIERS.md) - Complete tier system guide
- [FALLBACK_SYSTEM.md](FALLBACK_SYSTEM.md) - 5-tier OS fallback
- [Package Manager](../luci/README.md) - Installing additional models

---

**🩸 LuciferAI** - AI that works everywhere, from Catalina to Sonoma
