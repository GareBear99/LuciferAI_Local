# 🤖 LuciferAI AI Model Tier System

> **User Guide** - For technical details on tier selection and customization, see [TIER_SYSTEM.md](TIER_SYSTEM.md)

## Overview

LuciferAI uses a **5-tier AI model system (Tier 0-4)** that automatically categorizes and integrates common AI models based on their size, performance, and use cases. This system works seamlessly with your existing fallback infrastructure.

---

## 🎯 Tier Structure

### 🟢 Tier 0: Ultra-Lightweight (Bundled/Emergency)
**Size:** <2GB | **RAM:** <8GB | **OS:** All (including Catalina)

Perfect for:
- Legacy systems and older macOS versions
- Emergency fallback when resources are limited
- Quick responses and basic tasks
- Offline/portable installations

**Models:**
- **TinyLlama-1.1B** (600MB) — downloaded by `./setup_bundled_models.sh`, not shipped in the repo (the repo's `models/` is empty in a fresh clone)
  - Basic chat, simple questions
  - Works on macOS Catalina and older
  - Uses llamafile (no dependencies)
  
- **Phi-2** (1.7GB)
  - Microsoft's compact model
  - Good for code snippets and reasoning
  - Requires Ollama

---

### 🔵 Tier 1: Lightweight (Quick & Efficient)
**Size:** 1-2GB | **RAM:** 8-16GB | **OS:** Modern systems

Perfect for:
- General chat and conversation
- Basic coding assistance
- Fast responses
- Mobile/laptop development

**Models:**
- **Llama 3.2** (2GB)
  - Meta's latest lightweight model
  - Good for general chat and basic coding
  
- **Llama 3.2:1b** (1.3GB)
  - Ultra-fast variant
  - Mobile-friendly
  
- **Gemma:2b** (1.4GB)
  - Google's lightweight model
  - Strong at conversation

---

### 🟡 Tier 2: Mid-Size (Balanced Performance)
**Size:** 4-8GB | **RAM:** 16-32GB | **OS:** Modern systems

Perfect for:
- Advanced coding tasks
- Complex reasoning
- Multilingual support
- Production development

**Models:**
- **Mistral 7B** (4.1GB)
  - Excellent balanced performance
  - Strong coding abilities
  - Good reasoning
  
- **Llama 3.1 8B** (4.7GB)
  - Latest Meta model
  - Great instruction following
  - Strong reasoning
  
- **Gemma:7b** (4.8GB)
  - Google's mid-size model
  - Strong reasoning capabilities
  
- **Qwen 2.5 7B** (4.7GB)
  - Multilingual support
  - Strong coding abilities
  - Good for international projects

---

### 🔴 Tier 3: Advanced (Expert-Level)
**Size:** 4-26GB | **RAM:** 32GB+ | **OS:** High-performance systems

Perfect for:
- Expert-level coding
- Complex debugging and refactoring
- Architecture design
- Production code review

**Models:**
- **DeepSeek Coder 6.7B** (3.8GB)
  - Specialized coding model
  - Expert debugging
  - Code generation
  
- **DeepSeek Coder 33B** (19GB)
  - Advanced coding tasks
  - Complex refactoring
  - Enterprise-level code review
  
- **Code Llama 7B** (3.8GB)
  - Code completion
  - Programming assistance
  
- **Code Llama 13B** (7.4GB)
  - Advanced code generation
  - Architecture design
  
- **Mixtral 8x7B** (26GB)
  - Mixture of Experts model
  - High-performance reasoning
  - Complex multi-step tasks
  
- **WizardCoder 7B** (4.1GB)
  - Python specialist
  - Code optimization

---

### 🟣 Tier 4: Ultra-Expert / Frontier (70B+)
**Size:** 39GB | **RAM:** 32GB+ (64GB+ recommended) | **OS:** High-performance systems

Perfect for:
- Frontier research and architecture
- The hardest reasoning and coding tasks
- Enterprise-grade expert work

**Models:**
- **Llama3.1-70B** (39GB)
  - Meta's flagship open model
  - Ultra-expert reasoning and coding
  - The top of the shipped tier range — selected first when installed (`core/enhanced_agent.py`: tier priority "Tier 4 > Tier 3 > Tier 2 > Tier 1 > Tier 0")

> **Tier 5 (Cloud AI / GPT-4) is coming soon, not shipped.** The code reserves Tier 5 for cloud models, but no cloud tier is available in this repo — model tiers are Tier 0-4.

---

## 📥 Installation

### Install by Name

**Interactive Mode:**
```bash
python3 lucifer.py
> install tinyllama
> install llama3.2
> install mistral
> install deepseek-coder
```

**Command Line Mode** (one-shot — arguments are joined into the command; there is no `-c` flag):
```bash
python3 lucifer.py "install tinyllama"
python3 lucifer.py "install llama3.2"
python3 lucifer.py "install mistral"
python3 lucifer.py "install deepseek-coder"
```

### List All Models

**Interactive Mode:**
```bash
python3 lucifer.py
> llm list
```

**Command Line Mode:**
```bash
python3 lucifer.py "llm list"
```

This shows all models organized by tier with their sizes and use cases.

---

## 🗂️ Storage Location

All models install to the **project directory** for portability:

```
LuciferAI_Local/
├── bin/
│   └── llamafile          # Assembled from split parts on first run
└── models/
    ├── tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf  # After setup/manual download
    ├── llama3.2/
    │   └── .installed
    ├── mistral/
    │   └── .installed
    └── deepseek-coder/
        └── .installed
```

> **Note:** `models/` is empty in a fresh clone. The TinyLlama file arrives via `./setup_bundled_models.sh` (which installs it to `.luciferai/models/` — read by the llamafile agent) or a manual download into `models/`. `lucifer.py`'s startup check looks in `~/.luciferai/models/`, `models/`, and `bin/` — it does not look in `.luciferai/`, so the banner may report "Not installed" after the setup script ran even though the agent can use the model (a code inconsistency, flagged for a follow-up fix).

This means:
- ✅ Models stay with your project
- ✅ Easy version control
- ✅ Portable across machines
- ✅ No conflicts with global installations

---

## 🔄 Integration with Fallback System

The tier system integrates with LuciferAI's **5-tier fallback system** — a *separate* system from the model tiers: the fallback tiers describe the runtime environment (Native, Venv, Mirror, Stub, Emergency CLI), not the models.

| **Fallback Tier** | **Model Tier** | **Behavior** |
|-------------------|----------------|--------------|
| Tier 0 (Native) | Any | All models available |
| Tier 1 (Venv) | Any | Models work in virtual environment |
| Tier 2 (Mirror) | Any | Download models from mirrors |
| Tier 3 (Stub) | Tier 0-1 only | Use lightweight models |
| Tier 4 (Emergency) | Tier 0 only | TinyLlama fallback |

**Emergency Mode:** When system resources are critically low or on legacy systems, LuciferAI automatically uses Tier 0 models (TinyLlama).

---

## 🎯 Automatic Tier Selection

LuciferAI can recommend models based on your system:

```python
from luci.package_manager import PackageManager

pm = PackageManager()
recommended_tier = pm.get_recommended_tier()
models = pm.list_models_by_tier(recommended_tier)

print(f"Recommended for your system: Tier {recommended_tier}")
print(f"Models: {', '.join(models)}")
```

**Recommendation Algorithm:**
```
IF macOS Catalina or RAM < 8GB:
    → Tier 0 (TinyLlama, Phi)
ELIF RAM < 16GB:
    → Tier 1 (Llama 3.2, Gemma 2B)
ELIF RAM < 32GB:
    → Tier 2 (Mistral, Llama 3.1)
ELSE:
    → Tier 3 (DeepSeek, Mixtral)
    → Tier 4 (Llama3.1-70B) when a 70B-class model is installed and RAM allows
```

---

## 🔧 Platform Support

### llamafile (Tier 0)
- ✅ macOS Catalina (10.15)
- ✅ macOS Big Sur (11.0)
- ✅ macOS Monterey (12.0)
- ✅ macOS Ventura (13.0)
- ✅ macOS Sonoma (14.0+)
- ✅ Linux (all distributions)

### Ollama (Tiers 1-4)
- ⚠️ macOS Sonoma (14.0+) required
- ✅ Linux (all distributions)
- 🐳 Docker fallback for older macOS

### Docker Fallback
For macOS Catalina/Big Sur/Monterey/Ventura:
```bash
docker pull ollama/ollama
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

---

## 🚀 Quick Start Guide

### 1. Install Platform (First Time)

> **Note:** older guides use a global `LuciferAI` command. That alias only exists after running `./install_global.sh` (requires sudo — and that script hardcodes the original author's path, so it is broken for anyone else; a fix is owed). The commands below use the interactive prompt, which works without it.

```bash
# Automatic - installs llamafile with TinyLlama
python3 lucifer.py
> install llamafile

# Or install Ollama (Sonoma+ only)
> install ollama
```

### 2. Install Models by Use Case

**For Chat & Basic Tasks:**
```bash
python3 lucifer.py
> install llama3.2
```

**For Coding:**
```bash
python3 lucifer.py
> install mistral       # Balanced
> install deepseek-coder # Expert
```

**For Legacy Systems:**
```bash
# TinyLlama comes with llamafile via the setup script
python3 lucifer.py
> install llamafile
```

### 3. Use in Your Code
```python
from core.enhanced_agent import EnhancedLuciferAgent

agent = EnhancedLuciferAgent()
# Automatically uses best available model based on tier
response = agent.process_request("Explain Python decorators")
```

---

## 📊 Model Comparison

| Model | Tier | Size | Speed | Quality | Use Case |
|-------|------|------|-------|---------|----------|
| TinyLlama | 0 | 600MB | ⚡⚡⚡⚡⚡ | ⭐⭐ | Emergency/Basic |
| Phi-2 | 0 | 1.7GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | Code snippets |
| Llama 3.2 | 1 | 2GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | General chat |
| Gemma 2B | 1 | 1.4GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | Conversation |
| Mistral 7B | 2 | 4.1GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Coding/Balanced |
| Llama 3.1 | 2 | 4.7GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Reasoning |
| Qwen 2.5 | 2 | 4.7GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Multilingual |
| DeepSeek | 3 | 3.8GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | Expert coding |
| Code Llama | 3 | 3.8GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | Code completion |
| Mixtral | 3 | 26GB | ⚡ | ⭐⭐⭐⭐⭐ | Complex tasks |
| Llama3.1-70B | 4 | 39GB | ⚡ | ⭐⭐⭐⭐⭐ | Frontier/Ultra-Expert |

---

## 🔍 Troubleshooting

### "Model not found"
```bash
# List available models (inside python3 lucifer.py)
> llm list

# Install specific model
> install <model-name>
```

### "Out of memory"
Try a lower tier:
```bash
# Current tier too high? Use lighter model
> install llama3.2:1b  # Tier 1
> install tinyllama    # Tier 0
```

### "Ollama not available" (Catalina/Big Sur)
```bash
# Use llamafile instead
> install llamafile
```

---

## 📚 Related Documentation

- [Fallback System](FALLBACK_SYSTEM.md) - 5-tier OS fallback
- [Package Manager](../luci/README.md) - Installation system
- [Enhanced Agent](../core/enhanced_agent.py) - AI agent integration

---

**🩸 LuciferAI** - Built for reliability across all systems
