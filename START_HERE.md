# 🚀 START HERE - LuciferAI Quick Start

**Want to run LuciferAI right now? Follow these 3 steps:**

---

## Step 1: Run It (NO Installation Needed!)

```bash
# Navigate to LuciferAI directory
cd LuciferAI_Local  # Or wherever you put it

# Run LuciferAI (that's it!)
python3 lucifer.py
```

**That's literally it!** No installation, no setup, no build steps.

### What Happens on First Run:
1. ✅ **Auto-assembles** llamafile binary from parts (if present in `bin/`)
2. ✅ **Shows what's missing** and prints the setup command (`./setup_bundled_models.sh`) — it does **not** download anything itself and does **not** prompt; it continues without the model (rule-based command parsing only)
3. ✅ **Creates** `~/.luciferai/` directory structure as needed
4. ✅ **Starts** immediately

### What Happens on Subsequent Runs:
1. ✅ **Starts quickly** (startup time was not benchmarked)
2. ✅ Everything cached in `~/.luciferai/`
3. ✅ **Works offline** once the model is present (startup syncs FixNet state from GitHub and runs a WiFi check, so the app is not fully offline on boot)

---

## Step 2: Try Commands

Once you see the `>` prompt, try these:

```bash
# Basic commands
> help                                    # See all commands
> llm list                                # See what models you have

# Make stuff
> make me a script that tells me my gps   # Natural language!
> create file test.py                     # File operations
> fix broken_script.py                    # Auto-fix errors

# Ask questions
> what is python                          # It will explain
> how do i use lists in python            # Ask anything

# Install better models (optional)
> install mistral                         # Better 7B model
> install core models                     # Get Llama3.2, Mistral, DeepSeek
```

---

## Common Issues

### "Python not found"
```bash
# Install Python 3.9+ first
# macOS: brew install python3
# Linux: sudo apt install python3
# Windows: Download from python.org
```

### "Module not found"
```bash
# Install dependencies
pip3 install colorama requests psutil
```

### Still stuck?
```bash
# Check Python version (need 3.9+)
python3 --version

# Run with debug info (there is no --verbose flag; verbose output is the LUCIFER_VERBOSE env var)
LUCIFER_VERBOSE=1 python3 lucifer.py
```

---

## What You Get Immediately

✅ **Works offline** once the model is present - No API keys needed  
✅ **TinyLlama available** - 1.1B model, downloaded by `./setup_bundled_models.sh` (not shipped in the repo)  
✅ **File operations** - Create, delete, move, copy files  
✅ **Script generation** - Natural language → code  
✅ **Auto-fix** - Fix broken scripts automatically  
✅ **Multi-tier** - Install bigger models as needed  

---

## Want to Test the New Features?

We implemented a routing system — 76 routing cases, reported as print-based checks in `tests/test_master_controller.py`:

```bash
# Run the tests
python3 tests/test_master_controller.py

# You should see:
# ✅ 76/76 routing cases reported passing
```

**What's New:**
- ✅ 100% of the 25 previously-failing commands now route (was 40-50%)
- ✅ Commands like "make me a script that **tells** me..." now work!
- ✅ 5-layer fallback system
- ✅ Emergency recovery mode

---

## Next Steps

1. **Run it:** `python3 lucifer.py`
2. **Try commands:** Start with `help`
3. **Install models:** Try `install core models` for better AI
4. **Read docs:** Check `README.md` for full feature list
5. **Test new features:** Run `python3 tests/test_master_controller.py`

---

## Full Documentation

- `README.md` - Complete feature list and documentation
- `MASTER_CONTROLLER_STATUS.md` - New routing system details
- `MASTER_CONTROLLER_SUMMARY.md` - Technical implementation details
- `docs/` - Additional guides and references

---

## Status

**Current Version:** Master Controller v1.0  
**Routing cases:** 76/76 reported passing (print-based checks)  
**Last Updated:** January 23, 2026

---

**Questions?** Check the README or open an issue on GitHub.

**Enjoy LuciferAI! 🎉**
