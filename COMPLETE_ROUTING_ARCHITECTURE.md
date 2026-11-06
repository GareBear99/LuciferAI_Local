# 🗺️ LuciferAI Complete Routing Architecture

**Date:** January 23, 2026  
**Scope:** ALL possible routes including FixNet, non-FixNet, fallback routes, and script workflows

---

## 📐 Architecture Overview

```
User Input
    ↓
process_request() [Main Entry Point]
    ↓
[Command Detection & Routing]
    ↓
├─→ Direct Commands (help, exit, clear)
├─→ LLM Management (llm list, llm enable)
├─→ Model Installation (install mistral)
├─→ File Operations (create, move, delete)
├─→ Script Operations (run, fix, watch)
├─→ FixNet Operations (sync, upload)
├─→ GitHub Operations (link, upload)
├─→ Universal Task System (complex tasks)
├─→ LLM Query Routes (questions, generation)
└─→ Fallback/Unknown Handler
```

---

## 🎯 Main Entry Point

### `process_request(user_input: str) → str`
**Location:** `core/enhanced_agent.py:776`

**Flow:**
```python
def process_request(user_input: str):
    # 1. Session logging
    session_logger.log_request(user_input)
    
    # 2. Command detection
    user_lower = user_input.lower().strip()
    
    # 3. Route to appropriate handler
    if [condition]:
        return _handle_XXXX(...)
    
    # 4. Fallback to unknown handler
    return _handle_unknown(user_input)
```

---

## 🔀 Route Categories

### **Category 1: Direct System Commands** (No LLM)
These execute immediately without LLM involvement

| Command | Handler | Location | Description |
|---------|---------|----------|-------------|
| `help` | `_handle_help()` | Line 2156 | Show help menu |
| `exit` / `quit` | Return "EXIT" | Line 977 | Exit program |
| `clear` / `cls` | `_handle_clear()` | Line 2198 | Clear screen |
| `mainmenu` | `_handle_main_menu()` | Line 2242 | Show main menu |
| `memory` | `_handle_memory()` | Line 3050 | Show conversation history |
| `clear history` | `clear_history()` | Line 3058 | Clear conversation |

---

### **Category 2: LLM Management Commands** (No LLM)
Manage LLM models and settings

| Command | Handler | Location | Description |
|---------|---------|----------|-------------|
| `llm list` | `_handle_llm_list()` | Line 5154 | List all models |
| `llm list all` | `_handle_llm_list_all()` | Line 5366 | List all 74 models |
| `llm enable <model>` | `_handle_llm_enable()` | Line 5474 | Enable a model |
| `llm disable <model>` | `_handle_llm_disable()` | Line 5548 | Disable a model |
| `llm enable all` | `_handle_llm_enable_all()` | Line 5740 | Enable all installed |
| `llm disable all` | `_handle_llm_disable_all()` | Line 5794 | Disable all |
| `llm enable tier0-3` | `_handle_llm_enable_tier()` | Line 5799 | Enable tier range |
| `backup models` | `_handle_backup_models()` | Line 6008 | Set backup location |
| `models info` | `_handle_models_info()` | Line 6060 | Show model info |

---

### **Category 3: Model Installation** (Package Manager)
Install/uninstall AI models

| Command Pattern | Handler | Location | Description |
|----------------|---------|----------|-------------|
| `install mistral` | `_handle_ollama_install_request()` | Line 1721 | Install LLM model |
| `install core models` | `_handle_install_core_models()` | Line 7038 | Install 4 core models |
| `install all models` | `_handle_install_all_models()` | Line 7053 | Install all 74 models |
| `install tier X` | `_handle_install_tier()` | Line 7106 | Install models in tier |
| `install <package>` | `_handle_luci_install_package()` | Line 1730 | Install non-LLM packages |

---

### **Category 4: File Operations** (Universal Task System)
Create, move, delete files/folders

| Command Pattern | Handler | Route Through | Location |
|----------------|---------|---------------|----------|
| `create file X` | `_handle_creation_task()` | UniversalTaskSystem | Line 8779 |
| `create folder X` | `_handle_creation_task()` | UniversalTaskSystem | Line 8779 |
| `move X to Y` | `_handle_creation_task()` | UniversalTaskSystem | Line 8779 |
| `delete X` | `_handle_delete()` | Direct | Line 6099 |
| `open X` | `_handle_open()` | Direct | Line 6138 |
| `read X` | `_handle_read_file()` | Direct | Line 6194 |
| `list [path]` | `_handle_list()` | Direct | Line 6240 |
| `find X` | `_handle_find()` | Direct | Line 6299 |
| `copy X Y` | `_handle_copy()` | Direct | Line 6332 |

**Universal Task System Flow:**
```
create file test.py
    ↓
_handle_creation_task()
    ↓
UniversalTaskSystem.parse_command()
    ↓
Detect: SIMPLE complexity
    ↓
_handle_single_task_with_llm()
    ↓
Step 1/2: Create file
Step 2/2: Verify file
```

---

### **Category 5: Script Execution Routes** (With FixNet Integration)
Run and fix Python scripts

#### **5A: Run Script**
**Command:** `run script.py`  
**Handler:** `_handle_run_script()` | Line 1853

**Flow:**
```
run script.py
    ↓
Execute script
    ↓
Success? → Show output, EXIT
    ↓
Error detected? 
    ↓
Prompt: "Fix script? (y/n)"
    ↓
YES → _auto_fix_script() [FixNet Route]
NO  → Exit
```

#### **5B: Fix Script (Manual)**
**Command:** `fix script.py`  
**Handler:** `_handle_fix_script()` | Line 1911

**Flow:**
```
fix script.py
    ↓
Run script to detect error
    ↓
Error found? → _auto_fix_script() [FixNet Route]
No error? → "Script runs successfully"
```

#### **5C: Watch Script (Daemon)**
**Command:** `watch script.py` or `daemon watch script.py`  
**Handler:** `_handle_daemon()` | Line 7220

**Flow:**
```
daemon watch script.py
    ↓
Add to watcher queue
    ↓
Start daemon (background monitoring)
    ↓
On file change:
    ├─→ Re-run script
    ├─→ Detect errors
    └─→ Auto-fix via FixNet if error
```

---

### **Category 6: FixNet Routes** (Auto-Fix Workflow)

#### **6A: Auto-Fix Script** (5-Step Workflow)
**Entry Points:**
1. From `run script.py` → error → user confirms fix
2. From `fix script.py` → error detected
3. From `daemon watch` → error detected
4. From `_handle_multi_step_script_creation()` → script fails after generation

**Handler:** `_auto_fix_script(filepath, error)` | Line 1929

**Complete 5-Step Flow:**
```
─────────────────────────────────────────────────
Step 1/5: Searching for similar fixes...
─────────────────────────────────────────────────
    ↓
dictionary.get_best_fix_for_error(error, error_type)
    ↓
    ├─→ Found local fix? 
    │   ├─→ Apply fix → Success? → Upload & Exit
    │   └─→ Failed? → Continue to Step 3
    │
    └─→ No local fix? → Continue to Step 3

─────────────────────────────────────────────────
Step 2/5: Applying known fix (if found)
─────────────────────────────────────────────────
    ↓
_apply_fix_to_script(filepath, solution, error)
    ↓
Record usage: dictionary.record_fix_usage(fix_hash, success)

─────────────────────────────────────────────────
Step 3/5: Generating new fix...
─────────────────────────────────────────────────
    ↓
_generate_fix(filepath, error, error_type)
    ↓
Uses LLM to generate fix code
    ↓
Options:
    ├─→ Search consensus fixes first
    │   ├─→ USE_CONSENSUS: Use existing fix
    │   ├─→ ADAPT_CONSENSUS: Modify existing fix
    │   └─→ GENERATE_NEW: Create new fix
    │
    └─→ No consensus? → Generate from scratch

─────────────────────────────────────────────────
Step 4/5: Applying new fix...
─────────────────────────────────────────────────
    ↓
_apply_fix_to_script(filepath, new_solution, error)

─────────────────────────────────────────────────
Step 5/5: Uploading fix to FixNet...
─────────────────────────────────────────────────
    ↓
uploader.full_fix_upload_flow(...)
    ↓
SmartUploadFilter decides:
    ├─→ Novel fix? → Upload to GitHub
    ├─→ Duplicate? → Save locally only
    └─→ Branching fix? → Upload + create branch link
    ↓
dictionary.add_fix(...) → Update local dictionary
    ↓
dictionary.create_branch(...) → Link to inspired fix
```

#### **6B: FixNet Integration Module**
**Location:** `core/fixnet_integration.py`

**Components:**
```
IntegratedFixNet
    ├─→ FixNetUploader (encrypt + GitHub push)
    ├─→ RelevanceDictionary (track fixes)
    └─→ SmartUploadFilter (decide what to upload)
```

**Method:** `apply_fix()`  
**Flow:**
```
1. Search for similar fixes in dictionary
2. Smart filter decides if should upload
3. Upload if novel/branching (or keep local)
4. Update dictionary with relevance tracking
5. Create branch if inspired by another fix
```

#### **6C: FixNet Sync**
**Command:** `fixnet sync`  
**Handler:** `_handle_fixnet_sync()` | Line 7324

**Flow:**
```
fixnet sync
    ↓
dictionary.sync_with_remote()
    ↓
Download remote fixes from GitHub
    ↓
Merge with local dictionary
    ↓
Show sync statistics
```

#### **6D: FixNet Stats**
**Command:** `fixnet stats`  
**Handler:** `_handle_fixnet_stats()` | Line 7338

**Flow:**
```
fixnet stats
    ↓
Show statistics:
    ├─→ Total fixes (local + remote)
    ├─→ Upload acceptance rate
    ├─→ Duplicate rejection rate
    └─→ Branch connections
```

---

### **Category 7: GitHub Integration** (Non-FixNet)
Upload projects to GitHub

| Command | Handler | Location | Description |
|---------|---------|----------|-------------|
| `github link` | `_handle_github_link()` | Line 7491 | Link GitHub account |
| `github upload [project]` | `_handle_github_upload()` | Line 7590 | Upload project |
| `github update [project]` | `_handle_github_update()` | Line 7793 | Update existing repo |
| `github status` | `_handle_github_status()` | Line 7960 | Show GitHub status |
| `github projects` | `_handle_github_projects()` | Line 8012 | List repositories |

---

### **Category 8: Environment Management**
Manage Python environments

| Command | Handler | Location | Description |
|---------|---------|----------|-------------|
| `environments` / `envs` | `_handle_environments()` | Line 8148 | List all virtual envs |
| `env search <query>` | `_handle_env_search()` | Line 8198 | Search for env |
| `activate <env>` | `_handle_activate_env()` | Line 8241 | Activate environment |

---

### **Category 9: Badge & Stats System**
Track user progress and achievements

| Command | Handler | Location | Description |
|---------|---------|----------|-------------|
| `badges` | `_handle_badges()` | Line 4050 | Show badge progress |
| `stats` | `_handle_stats()` | Line 4071 | Show user statistics |

---

### **Category 10: Soul Combat System** (Game)
RPG-style combat mechanics

| Command | Handler | Location | Description |
|---------|---------|----------|-------------|
| `soul` | `_handle_soul()` | Line 8272 | Manage Soul Modulator |
| `demo test tournament` | `_handle_combat_demo()` | Line 8305 | Run physics demo |

---

### **Category 11: Multi-Step Script Creation** (WITH Steps)
Create scripts with LLM code generation

**Entry Point:** `_handle_multi_step_script_creation()` | Line 9527

**Detection Logic:**
```python
has_creation = 'make' or 'create' or 'write' or 'build'
has_target = 'script' or 'program' or 'code' or 'file'
has_action_connector = 'that' or 'which' or 'to' (word boundary)
has_action_verbs = [80+ verbs like 'open', 'tell', 'give', etc.]

is_script_request = has_creation AND has_target AND 
                    ((has_action_connector AND has_action_verbs) OR has_action_verbs)
```

**Command Examples:**
- ✅ `"make a script that opens the browser"`
- ❌ `"make a script that tells me my gps"` (BUG: "tells" missing from verb list)

**Flow:**
```
make a script that opens browser
    ↓
[Script Request Detected]
    ↓
_handle_multi_step_script_creation()
    ↓

─────────────────────────────────────────────────
📋 Task Checklist (generated by LLM):
  [ ] 1. Create file
  [ ] 2. Write code
  [ ] 3. Run script (if tier 2+)
─────────────────────────────────────────────────

Step 1/2: Creating file...
    ↓
    ├─→ Check file exists?
    │   ├─→ YES: Prompt overwrite (y/n)
    │   └─→ NO: Create file
    ↓
    ✅ Created file: open_browser.py
    [✓] 1. Create file

─────────────────────────────────────────────────
Step 2/2: Writing code to file...
─────────────────────────────────────────────────
    ↓
Route to best model (bypass routing):
    ├─→ Tier 0-1: Search templates only
    │   ├─→ Template found? → Use it
    │   └─→ No template? → Try next tier
    │
    └─→ Tier 2+: Check templates, then generate
        ├─→ Good template found? 
        │   └─→ LLM validates: USE_AS_IS / NEEDS_MODIFICATION
        │
        └─→ No good template? → Generate new code
            ↓
            LLM generates code (tier-appropriate max_tokens)
            ↓
            Write to file
            ↓
            ✅ Code written
            [✓] 2. Write code

[Optional] Step 3/2: Running script... (if tier 2+ or user requested)
    ↓
    Run script
    ↓
    ├─→ Success? → ✅ Show output
    └─→ Error? → Auto-fix with FixNet (up to 3 retries)
        ↓
        FixNet auto-fix workflow:
        ├─→ Search consensus fixes
        ├─→ Apply/adapt/generate fix
        ├─→ Upload if novel
        └─→ Retry execution

─────────────────────────────────────────────────
📋 Final Checklist:
  [✓] 1. Create file
  [✓] 2. Write code
  [✓] 3. Run script
─────────────────────────────────────────────────
🎉 All steps completed successfully!
```

---

### **Category 12: Simple Task Workflow** (WITH Steps)
Simple file/folder creation with verification

**Entry Point:** `_handle_single_task_with_llm()` | Line 9409  
**Condition:** Task complexity == SIMPLE

**Command Examples:**
- `"create file test.py"`
- `"make folder myproject"`

**Flow:**
```
create file test.py
    ↓
[SIMPLE Task Detected]
    ↓

─────────────────────────────────────────────────
Step 1/2: Create file 'test.py'
─────────────────────────────────────────────────
    ↓
    Execute task
    ↓
    ✅ Created file: test.py
    ✅ Step 1/2 Complete

─────────────────────────────────────────────────
Step 2/2: Verifying file exists
─────────────────────────────────────────────────
    ↓
    Check file exists?
    ├─→ YES: ✅ File verified
    └─→ NO: ❌ File not found
    ✅ Step 2/2 Complete
```

---

### **Category 13: Find and Write Workflow** (3-4 Steps)
Find file and modify it

**Entry Point:** `_handle_find_and_write_workflow()` | Line 10876

**Detection:**
```python
has_find = 'find' in command
has_write_action = 'write' or 'add' or 'modify' or 'change' or 'update'
has_target = 'script' or 'file' or 'code'

is_find_and_write = has_find AND has_write_action AND has_target
```

**Flow:**
```
Step 1: Find target file
Step 2: Write changes
Step 3: Validate changes
[Optional] Step 4: Run script
```

---

### **Category 14: General LLM Query** (Questions & Answers)
Natural language queries and conversations

**Entry Points:**
1. Multi-word input not matching other patterns
2. Questions (starts with "how", "what", "why", etc.)
3. General conversation

**Handler:** `_handle_general_llm_query()` | Line 9568

**Flow:**
```
"what is python?"
    ↓
[Question Detected]
    ↓
_handle_general_llm_query()
    ↓
Check model availability:
    ├─→ llamafile models? → Use llamafile backend
    ├─→ Ollama models? → Use Ollama backend
    └─→ No models? → "LLM not available" message
    ↓
Route to best model:
    ├─→ Bypass lower tiers
    └─→ Select highest tier available
    ↓
LLM generates response
    ↓
Format code blocks (white background)
    ↓
Display response
```

---

### **Category 15: Fallback Routes** (Error Handling)

#### **15A: Unknown Command**
**Handler:** `_handle_unknown()` | Line 8891

**Flow:**
```
unknown command
    ↓
Check for typos:
    ├─→ Exact typo match? → Suggest correction
    └─→ Fuzzy match found? → "Did you mean X?"
    ↓
No match? → Show help + suggest similar commands
```

#### **15B: Ollama Required**
**Handler:** `_handle_ollama_required()` | Line 8968

**Flow:**
```
Command requires LLM but none available
    ↓
Check macOS version:
    ├─→ Catalina? → Suggest llamafile (Ollama incompatible)
    └─→ Other? → Show Ollama installation instructions
```

#### **15C: Model Fallback**
**Location:** Throughout LLM routing

**Flow:**
```
Try primary model
    ↓
Model fails/unavailable?
    ↓
Try next tier down
    ↓
Keep trying until:
    ├─→ Model succeeds → Use it
    └─→ All fail → Fallback to rule-based or error message
```

---

## 🔄 Tier-Based Model Routing

### **Bypass Routing System**
**Location:** `enhanced_agent.py:_get_best_available_model()`

**Algorithm:**
```
Get all enabled models
    ↓
Filter out corrupted models
    ↓
Remove duplicate model files
    ↓
Sort by tier (highest first)
    ↓
Return best model

Display:
💡 Bypassed: gemma2 (Tier 1), phi-2 (Tier 0), tinyllama (Tier 0)
🧠 Using mistral-7b (Tier 2)
```

---

## 📊 Route Priority Map

**Priority Order (Highest → Lowest):**

1. **Direct System Commands** (help, exit, clear)
2. **Test Commands** (tinyllama test, mistral test)
3. **LLM Management** (llm list, llm enable)
4. **Session Commands** (session list, session stats)
5. **Badge/Stats** (badges, stats, soul)
6. **Model Installation** (install mistral, install tier 2)
7. **FixNet Sync** (fixnet sync, fixnet stats)
8. **GitHub Commands** (github link, github upload)
9. **Environment Commands** (environments, activate)
10. **File Operations** (delete, open, read, list, find, copy)
11. **Script Execution** (run X, fix X, daemon watch X)
12. **Package Installation** (install numpy, install brew)
13. **Image Operations** (image search, image download)
14. **Zip Operations** (zip X, unzip X)
15. **Multi-Step Script Creation** (make script that...)
16. **Find and Write Workflow** (find X and write...)
17. **Universal Task System** (create file/folder with complex logic)
18. **General LLM Query** (questions, conversation)
19. **Unknown/Fallback** (typo suggestions, help)

---

## 🧩 Integration Points

### **FixNet ↔ Script Execution**
```
run script.py → Error → Auto-fix → FixNet upload
fix script.py → Error → Auto-fix → FixNet upload
daemon watch → Error → Auto-fix → FixNet upload
create script → Generated → Run → Error → Auto-fix → FixNet upload
```

### **Universal Task System ↔ LLM**
```
create file X → Parse command → Detect complexity → 
    SIMPLE: 2-step workflow
    MODERATE: Tree display + LLM commentary
    COMPLEX: Multi-step with planning
    ADVANCED: Full research + generation + testing
```

### **Model Routing ↔ All LLM Operations**
```
Any LLM request → Get best model → Bypass lower tiers → 
    Model succeeds? → Use it
    Model fails? → Try next tier
    All fail? → Error or fallback
```

---

## 🔍 Example: Complete Flow for "make me a script that tells me my gps point"

### **Current Behavior (BUG):**
```
Input: "make me a script that tells me my gps point"
    ↓
process_request()
    ↓
Check is_script_request:
    has_creation: ✅ YES ("make")
    has_target: ✅ YES ("script")
    has_action_connector: ✅ YES ("that")
    has_action_verbs: ❌ NO ("tells" not in list)
    ↓
is_script_request = FALSE ❌
    ↓
Route to: _handle_general_llm_query()
    ↓
💡 Bypassed: gemma2, phi-2, tinyllama
🧠 Using mistral-7b
    ↓
Generate code directly (NO STEPS SHOWN)
```

### **Expected Behavior (After Fix):**
```
Input: "make me a script that tells me my gps point"
    ↓
process_request()
    ↓
Check is_script_request:
    has_creation: ✅ YES ("make")
    has_target: ✅ YES ("script")
    has_action_connector: ✅ YES ("that")
    has_action_verbs: ✅ YES ("tells" NOW IN LIST)
    ↓
is_script_request = TRUE ✅
    ↓
Route to: _handle_multi_step_script_creation()
    ↓
───────────────────────────────────────────
📋 Task Checklist:
  [ ] 1. Create file
  [ ] 2. Write code
  [ ] 3. Run script
───────────────────────────────────────────

💡 Bypassed: gemma2, phi-2, tinyllama
🧠 Using mistral-7b (Tier 2)

───────────────────────────────────────────
📝 Step 1/2: Creating file...
───────────────────────────────────────────
✅ Created file: gps_location.py
[✓] 1. Create file

───────────────────────────────────────────
📝 Step 2/2: Writing code to file...
───────────────────────────────────────────
🤔 mistral-7b generating new code...
✅ Code written successfully
[✓] 2. Write code

───────────────────────────────────────────
📋 Final Checklist:
  [✓] 1. Create file
  [✓] 2. Write code
───────────────────────────────────────────
🎉 All steps completed successfully!
```

---

## 🎯 Quick Reference: Command → Route Mapping

| Command | Route Category | Handler | Uses FixNet? | Shows Steps? |
|---------|---------------|---------|--------------|--------------|
| `help` | System | Direct | No | No |
| `llm list` | LLM Mgmt | Direct | No | No |
| `install mistral` | Installation | Package Mgr | No | No |
| `create file X` | File Ops | Universal Task | No | Yes (2 steps) |
| `run script.py` | Script Exec | Direct → FixNet if error | Yes (if error) | No (unless error → 5 steps) |
| `fix script.py` | Script Exec | Direct → FixNet | Yes | Yes (5 steps) |
| `daemon watch X` | Script Exec | Daemon → FixNet if error | Yes (if error) | No |
| `make script that X` | Script Creation | Multi-step | No (unless error after) | Yes (2-3 steps) |
| `fixnet sync` | FixNet | Direct | Yes | No |
| `what is python?` | LLM Query | General LLM | No | No |

---

## 📚 Key Files Reference

| File | Purpose | Key Functions |
|------|---------|---------------|
| `enhanced_agent.py` | Main routing logic | `process_request()`, all `_handle_*()` |
| `fixnet_integration.py` | FixNet orchestration | `apply_fix()`, `search_fixes()` |
| `fixnet_uploader.py` | GitHub upload | `full_fix_upload_flow()` |
| `relevance_dictionary.py` | Fix tracking | `add_fix()`, `search_similar_fixes()` |
| `smart_upload_filter.py` | Upload decisions | `should_upload()` |
| `universal_task_system.py` | Task parsing & execution | `parse_command()`, `execute_task()` |
| `llm_backend.py` | LLM abstraction | `generate()`, `chat()` |
| `command_keywords.py` | Keyword definitions | Action verbs, synonyms, etc. |
| `fallback_system.py` | Tier fallback | System-wide fallback strategies |

---

## 🏁 Summary

**Total Routes:** 100+ possible execution paths  
**Main Categories:** 15 major route categories  
**FixNet Integration Points:** 4 (run, fix, daemon, multi-step creation errors)  
**Step Workflows:** 3 (multi-step creation, simple task, auto-fix)  
**Fallback Layers:** 3 (model tier, Ollama→llamafile, unknown command)

**Architecture Philosophy:**
1. **Route early** - Direct commands bypass LLM
2. **Fallback gracefully** - Multiple fallback layers
3. **Integrate FixNet** - Auto-fix on all script errors
4. **Show progress** - Step workflows for multi-step operations
5. **User control** - Confirmations for destructive actions

---

**Document Version:** 1.0  
**Last Updated:** January 23, 2026  
**Maintainer:** AI Agent (Warp)
