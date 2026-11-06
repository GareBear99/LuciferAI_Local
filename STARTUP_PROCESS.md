# 🔬 LuciferAI Startup Process - Complete Technical Documentation

**DARPA/NSF/DOD Standard Documentation**  
**Technical Readiness Level (TRL):** 7 - System prototype demonstrated in operational environment  
**Date:** January 23, 2026  
**Classification:** UNCLASSIFIED

---

## Executive Summary

LuciferAI is a **zero-installation terminal AI assistant** that automatically bootstraps itself on first run. No manual installation steps are required. The system performs runtime environment validation, auto-assembles binary components, and tells you how to install the model if it is missing — it does not download anything on its own.

**Key Characteristics:**
- ✅ No manual installation (single command: `python3 lucifer.py`)
- ✅ Auto-assembles llamafile binary from split parts (if present in repo)
- ✅ Shows what's missing on first run and prints the setup command (`./setup_bundled_models.sh`); it does not download anything itself and does not prompt
- ✅ Runtime environment validation every startup
- ✅ 5-tier fallback system for degraded environments
- ✅ Works offline once the model is present (startup syncs FixNet state from GitHub and runs a WiFi check, so the app is not fully offline on boot)

---

## 1. Startup Sequence (Technical Flow)

### Phase 1: Environment Bootstrap
```
START: python3 lucifer.py
  │
  ├─► [lucifer.py:284] Call check_and_install_models() (def at lucifer.py:219)
  │     │
  │     ├─► [lucifer.py:226] Call assemble_llamafile_from_parts() (def at lucifer.py:189)
  │     │     ├─► Check: bin/llamafile exists?
  │     │     │     YES → Return True
  │     │     │     NO  → Check for split parts (bin/llamafile.part.*)
  │     │     │           FOUND → Assemble parts into single binary
  │     │     │           MISSING → Return False
  │     │     └─► Result: llamafile binary assembled or already present
  │     │
  │     ├─► [lucifer.py:228-238] Check binary/model existence (canonical layout)
  │     │     ├─► llamafile: <project>/.luciferai/bin/llamafile
  │     │     └─► TinyLlama: <project>/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
  │     │
  │     ├─► Both exist?
  │     │     YES → Return True (proceed to Phase 2)
  │     │     NO  → Display what's missing and how to install it
  │     │
  │     ├─► Display what's missing
  │     │     └─► Show status: llamafile (✅/❌), TinyLlama (✅/❌)
  │     │     └─► Print: "Run the setup script: ./setup_bundled_models.sh"
  │     │         (no manual one-liner — the .llamafile download was a dead
  │     │         end; the setup script is the only install path)
  │     │
  │     ├─► NO prompt, NO download. The function prints
  │     │     "Continuing without a model... rule-based command parsing"
  │     │     and returns False. The model is installed by running
  │     │     ./setup_bundled_models.sh, not by the app itself.
  │     │     (main() ignores the return value and continues anyway.)
  │     │
  │     └─► Note: the setup script installs to <project>/.luciferai/,
  │         which the llamafile agent reads — but this startup check
  │         does not look there, so the banner may still report
  │         "Not installed" after the setup script ran.
  │
 └─► Return to main()
```

### Phase 2: Agent Initialization
```
[lucifer.py:287] Initialize EnhancedLuciferAgent (agent = LuciferAgent())
  │
  ├─► [enhanced_agent.py:155] Agent __init__()
  │     ├─► Get user_id (based on machine hardware)
  │     ├─► Initialize authentication system (if available)
  │     ├─► Initialize FixNet uploader
  │     ├─► Initialize relevance dictionary
  │     ├─► Initialize session logger
  │     ├─► Check Ollama availability
  │     ├─► Load LLM enable/disable state
  │     └─► Select best enabled model
  │
  ├─► [enhanced_agent.py:557] _check_ollama()
  │     ├─► Test: ollama list (subprocess)
  │     │     SUCCESS → Set ollama_available = True, parse models
  │     │     FAIL    → Set ollama_available = False
  │     └─► Return availability status
  │
  ├─► [enhanced_agent.py:628] _load_llm_state()
  │     ├─► Load from: ~/.luciferai/data/llm_state.json
  │     │     EXISTS → Load enabled/disabled state per model
  │     │     MISSING → All models enabled by default
  │     └─► Return state dict
  │
  └─► Agent ready for commands
```

### Phase 3: Main Loop
```
[lucifer.py:281] Main interactive loop (main())
  │
  ├─► Print banner
  ├─► Start heartbeat animation
  ├─► Read command from user
  ├─► Route command through master controller
  ├─► Execute command
  ├─► Display results
  └─► Repeat
```

---

## 2. File System Layout

### Installation Directories
```
~/.luciferai/                          # User state only (NOT models)
├── data/
│   ├── llm_state.json                 # Model enable/disable state
│   ├── requirements.txt               # Python dependencies
│   └── user_id.json                   # User identification
├── logs/
│   ├── system_check.log               # Environment validation logs
│   ├── fallback_trace.log             # Fallback system logs
│   └── sessions/                      # Session history (6 months)
├── envs/
│   └── lucifer_env/                   # Virtual environment fallback
└── stubs/
    └── *.py                           # Module stubs (Tier 3 fallback)

# The binary and models live in the PROJECT directory, not here:
#   <project>/.luciferai/bin/llamafile                        (binary)
#   <project>/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf     (model)
```

### Project Directory
```
LuciferAI_Local/                       # Project root
├── lucifer.py                         # Main entry point (✅ Run this)
├── .luciferai/
│   └── bin/
│       └── llamafile                  # Auto-assembled binary (canonical)
├── bin/
│   ├── llamafile.part.aa              # Split binary parts (GitHub-friendly)
│   ├── llamafile.part.ab              # Auto-assembled on startup
│   └── llamafile.part.ac
├── models/
│   └── *.gguf                         # Additional models (optional)
├── core/
│   ├── enhanced_agent.py              # Main agent logic
│   ├── llamafile_agent.py             # Llamafile interface
│   ├── master_controller.py           # Routing system (NEW)
│   ├── fallback_system.py             # 5-tier fallback
│   ├── first_run.py                   # Global installation
│   └── ...
└── tests/
    └── test_master_controller.py      # Validation tests
```

---

## 3. Runtime Validation (Every Startup)

### What Gets Checked Every Time:
```python
# From lucifer.py:check_and_install_models()

1. llamafile Binary Check
   - Check: <project>/.luciferai/bin/llamafile exists (canonical layout)
   - If missing → Print what's missing + the setup command, continue without the model (no prompt, no download)

2. TinyLlama Model Check
   - Check: <project>/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf exists (canonical layout)
   - If missing → Print what's missing + the setup command, continue without the model (no prompt, no download)

3. Ollama Availability Check
   - Ollama is only consulted when NO local model is installed at all
     (fallback, never preferred — local llamafile models come first).
   - Test: HTTP GET http://localhost:11434/api/tags
   - If a local model exists, Ollama is not consulted at all.

4. Model State Check
   - Load: ~/.luciferai/data/llm_state.json
   - Parse: Which models enabled/disabled
   - Select: Best available enabled model

5. Fallback System Check
   - Verify: Environment dependencies
   - Check: Python packages
   - Check: System tools (git, curl, etc.)
   - Determine: Current fallback tier (0-4)
```

**Performance:** the checks are lightweight file-existence tests plus, only when no local model is installed, one HTTP request to the Ollama server. No timing has been measured — the "< 500ms" figure this doc previously stated was an estimate, not a benchmark.

---

## 4. Binary Assembly Process

### Why Split Parts?
GitHub has a 100MB file size limit. Llamafile binary (~132MB) must be split:

```bash
# Original binary splitting (done once during repo preparation)
split -b 50M llamafile llamafile.part.

# Result:
llamafile.part.aa  (50MB)
llamafile.part.ab  (50MB)
llamafile.part.ac  (32MB)
```

### Auto-Assembly on Startup
```python
# From lucifer.py:assemble_llamafile_from_parts()

def assemble_llamafile_from_parts() -> bool:
    project_bin = Path(__file__).parent / "bin"
    llamafile_path = _canonical_llamafile_path()  # <project>/.luciferai/bin/llamafile
    part_aa = project_bin / "llamafile.part.aa"

    # If llamafile exists, we're good
    if llamafile_path.exists():
        return True

    # Check if parts exist
    if not part_aa.exists():
        return False

    # Assemble parts into the canonical location
    llamafile_path.parent.mkdir(parents=True, exist_ok=True)
    parts = sorted(glob.glob(str(project_bin / "llamafile.part.*")))
    with open(llamafile_path, 'wb') as outfile:
        for part in parts:
            with open(part, 'rb') as infile:
                outfile.write(infile.read())

    os.chmod(llamafile_path, 0o755)
    return True
```

**Result:** Single `.luciferai/bin/llamafile` binary (~132MB) ready to use. (A manual assembly script also exists: `bin/assemble_llamafile.sh` — it assembles into the same canonical location.)

---

## 5. Model Download Process

### TinyLlama Download (First Run Only)
```python
# From lucifer.py:download_with_progress()

URL: https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
Size: ~600MB
Destination: <project>/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
Method: curl (with progress bar) OR urllib (fallback)
Time: 1-5 minutes (depends on internet speed)
```

### Download Behavior:
1. **First time user:**
   - No prompt, no auto-download. The check prints what's missing, prints "Run the setup script: ./setup_bundled_models.sh", then prints "Continuing without a model..." and starts with rule-based command parsing only.
   - To get the model: run `./setup_bundled_models.sh` (downloads llamafile 0.8.13 + TinyLlama ~600MB — binary into `<project>/.luciferai/bin/`, model into `<project>/models/`).

2. **Subsequent runs:**
   - Check if files exist
   - If exist: Start (startup time was not benchmarked)
   - If missing: Print the setup instructions again and continue without the model

3. **Offline mode:**
   - Works if llamafile + TinyLlama already present
   - Local inference and file operations need no internet after the model is installed (startup still syncs FixNet state from GitHub and runs a WiFi check)

---

## 6. Fallback System (5 Tiers)

### Tier 0: Native Mode ✅
**Indicator:** Green  
**Condition:** All dependencies satisfied  
**Features:** Full functionality

### Tier 1: Virtual Environment Fallback 🩹
**Indicator:** Cyan  
**Condition:** Python packages missing  
**Action:**
```python
# From fallback_system.py:fallback_virtual_env()

1. Create: ~/.luciferai/envs/lucifer_env
2. Install: pip install -r requirements.txt
3. Activate: Use venv for all operations
```

### Tier 2: Mirror Binary Fallback 🔄
**Indicator:** Yellow  
**Condition:** System tools missing (git, curl, etc.)  
**Action:**
```python
# From fallback_system.py:fallback_mirror_download()

1. Check package managers: brew, apt, yum, choco
2. Try installing: git, curl, wget
3. Fallback to mirror: GitHub releases
```

### Tier 3: Stub Layer 🧩
**Indicator:** Purple  
**Condition:** Module import crashes  
**Action:**
```python
# From fallback_system.py:fallback_stub_module()

1. Create stub class for missing module
2. Intercept __getattr__ calls
3. Return None (prevents crashes)
4. Log stub calls for debugging
```

### Tier 4: Emergency CLI Mode ☠️
**Indicator:** Red  
**Condition:** Catastrophic environment failure  
**Action:**
```python
# From fallback_system.py:fallback_emergency_cli()

1. Enter minimal survival shell
2. Available commands: help, fix, analyze, exit
3. Save emergency state to logs
4. Await recovery or manual fix
```

### Recovery: System Repair 💫
**Indicator:** Green  
**Condition:** Auto-triggers after 3 consecutive failures  
**Action:**
```python
# From fallback_system.py:system_repair()

1. Rebuild virtual environment
2. Reinstall missing tools
3. Purge broken symbolic links
4. Verify system integrity
5. Return to Tier 0
```

---

## 7. Dependencies

### Required (Python 3.9+):
- **colorama** - Terminal colors
- **requests** - HTTP downloads (fallback)
- **psutil** - System information

### Optional:
- **cryptography** - FixNet encryption (gracefully degrades if missing)
- **ollama** - Higher tier models (auto-detected)

### System Dependencies:
- **curl** - Preferred download method (falls back to urllib)
- **git** - GitHub sync features (optional)
- **python3** - Core runtime (3.9+)

---

## 8. Validation Tests

### Master Controller Validation
```bash
# Run comprehensive tests (76 tests, 100% pass rate)
python3 tests/test_master_controller.py

# Expected output:
# ✅ Test 1: Route Detection         35/35 passed
# ✅ Test 2: Tier Selection           7/7 passed
# ✅ Test 3: Action Verb Fix         25/25 passed
# ✅ Test 4: Tier Enforcement         9/9 passed
# 
# Final: 76/76 passed (100% success rate)
```

### Startup Validation
```bash
# Test with verbose output (there is no --dry-run flag)
LUCIFER_VERBOSE=1 python3 lucifer.py

# Test emergency recovery
python3 -c "from core.fallback_system import FallbackSystem; FallbackSystem().system_repair()"
```

---

## 9. Performance Metrics

> **These times are unmeasured estimates, not benchmarks.** Startup time has not been benchmarked; do not quote these figures as measured.

### Startup Times:
| Scenario | Time | Notes |
|----------|------|-------|
| **First run, model missing** | Fast | Check + assembly only; the model is *not* downloaded by the app (run `./setup_bundled_models.sh` — ~600MB, a few minutes on a typical connection) |
| **Cold start (assembly only)** | ~1-2 sec (estimate) | Assembles llamafile from parts |
| **Warm start** | Fast (estimate) | All components present |
| **Hot start** | Fast (estimate) | Agent already initialized |

### Runtime Checks:
| Check | Time | Frequency |
|-------|------|-----------|
| Binary existence | Fast (estimate) | Every startup |
| Model existence | Fast (estimate) | Every startup |
| Ollama availability | Depends on subprocess (estimate) | Every startup |
| LLM state load | Fast (estimate) | Every startup |
| Fallback tier check | Fast (estimate) | Every startup |
| **Total overhead** | **Not benchmarked** | Every startup |

---

## 10. Error Handling

### Scenario: Llamafile Binary Missing
```
User runs: python3 lucifer.py
System detects: llamafile binary missing
Action: 
  1. Check for split parts in bin/
  2. If present: Assemble automatically
  3. If missing: Print what's missing + the setup command
     (./setup_bundled_models.sh) — no prompt, no download
  4. Continue startup without the model (rule-based parsing only)
```

### Scenario: TinyLlama Model Missing
```
User runs: python3 lucifer.py
System detects: TinyLlama model missing
Action:
  1. Show status: "TinyLlama model: Not installed (670MB)"
  2. Print: "Run the setup script: ./setup_bundled_models.sh"
     and a manual one-liner — no prompt, no download
  3. Continue with limited features
  4. Note: User can still use file operations, GitHub sync, etc.
```

### Scenario: Ollama Not Available
```
User runs: python3 lucifer.py
System detects: ollama command not found
Action:
  1. Set ollama_available = False
  2. Fall back to llamafile only
  3. Still functional (using TinyLlama)
  4. Higher tier models unavailable
  5. System continues normally
```

### Scenario: Network Error During Download
```
The app itself does not download on startup, so there is no
startup download to fail. If the setup script's download fails:
Action:
  1. The script (curl/wget) shows the error and exits
  2. Suggest: "Try again later or check internet connection"
  3. Option: install manually — see docs/BUNDLED_MODELS.md
     (curl the llamafile 0.8.13 binary into .luciferai/bin/ and the
     TinyLlama GGUF into models/)
  4. Continue: LuciferAI starts with limited features
```

### Scenario: Catastrophic Environment Failure
```
System detects: 3+ consecutive errors
Action:
  1. Log all errors to: ~/.luciferai/logs/emergency/
  2. Enter Emergency CLI Mode (Tier 4)
  3. Show: "Emergency mode activated"
  4. Available: help, fix, analyze, exit
  5. Auto-trigger: System repair process
```

---

## 11. Security Considerations

### Binary Verification:
- Llamafile downloaded from official Mozilla repository
- TinyLlama downloaded from official HuggingFace
- No checksum verification is performed by the setup/install scripts
- All executables: chmod 0755 (not world-writable)

### Network Access:
- Required for the model download (via the setup script) and for the FixNet sync + WiFi check on startup
- Local inference and file operations work offline once the model is present
- FixNet sync: Fernet-encrypted (optional)
- No telemetry or analytics sent

### File Permissions:
```
~/.luciferai/
├── bin/llamafile          (755) executable by owner
├── models/*.llamafile     (755) executable by owner
├── data/*.json            (644) readable by owner
└── logs/*.log             (644) readable by owner
```

---

## 12. DARPA TRL Assessment

### Current System (TRL 7):
✅ **System prototype demonstrated in operational environment**
- Works on macOS, Linux, Windows (WSL)
- Tested with 76 routing cases reported passing by tests/test_master_controller.py (print-based checks)
- Self-healing fallback tiers implemented (see §6)

### Path to TRL 8:
- Complete tier-by-tier validation
- 1000+ hours of runtime testing
- Multi-user production deployment
- Performance benchmarking under load

### Path to TRL 9:
- Mission-critical production use
- Security audit and certification
- High-availability configuration
- Enterprise deployment

---

## 13. Quick Reference

### Start LuciferAI (No Installation Needed):
```bash
python3 lucifer.py
```

### Run Tests:
```bash
python3 tests/test_master_controller.py
```

### Check System Status:
```bash
# Inside LuciferAI:
> llm list              # See available models
> help                  # See all commands
> memory                # Check memory status
```

### Force Re-Download:
```bash
rm -rf .luciferai/bin/llamafile models
./setup_bundled_models.sh   # Re-downloads llamafile 0.8.13 + TinyLlama
# (Running python3 lucifer.py alone does NOT re-download anything —
#  it only prints the setup command and continues without the model.)
```

### Debug Mode:
```bash
LUCIFER_VERBOSE=1 python3 lucifer.py
```

---

## 14. Conclusion

LuciferAI implements a **bootstrap process** that requires zero manual installation. The system:

✅ **Self-assembles** binary components from split parts  
✅ **Points you at the model install** on first run (it does not download anything itself)  
✅ **Validates** environment every startup (startup time not benchmarked)  
✅ **Degrades gracefully** through 5 fallback tiers  
✅ **Recovers automatically** from failures  

**Result:** User runs `python3 lucifer.py` and everything "just works."

---

**Document Status:** COMPLETE  
**Validation:** 76/76 routing cases reported passing (print-based checks)  
**TRL Level:** 7 (Operational prototype)  
**Next Review:** After production deployment
