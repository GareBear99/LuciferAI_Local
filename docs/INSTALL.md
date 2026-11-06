# 🩸 LuciferAI Installation Guide

> **Read this first:** LuciferAI is **not a pip package** — there is no `setup.py`, `pyproject.toml`, or `setup.cfg` in this repo, so `pip install .`, `pip install --user .`, `pip install -e .`, and `pip install git+https://...` all fail. There is no Homebrew formula and no conda package. Do not use `./install.sh` — every option in it runs `pip install`, which fails for the same reason. The working install is: clone the repo and run `python3 lucifer.py`. (The packaging gap is a known code fix owed to a follow-up pass.)

## 🚀 Quick Install (The Working Path)

```bash
git clone https://github.com/GareBear99/LuciferAI_Local.git
cd LuciferAI_Local
python3 lucifer.py
```

That's it — no build step, no package install. `python3 lucifer.py` auto-assembles the llamafile binary from the split parts in `bin/`, checks for the TinyLlama model, prints the setup command if the model is missing, and continues without it (rule-based command parsing only).

## 📦 Install the Model (Optional, Recommended)

The TinyLlama model is **not** shipped in the repo (`models/` is empty in a fresh clone). Download it with the setup script:

```bash
./setup_bundled_models.sh
```

This downloads llamafile 0.8.6 (~34MB) and TinyLlama 1.1B (~600MB, TheBloke GGUF) into `<project>/.luciferai/bin/` and `<project>/.luciferai/models/` — the location the llamafile agent reads (`core/llamafile_agent.py`).

> **Note:** `lucifer.py`'s startup check looks in `~/.luciferai/`, `bin/`, and `models/` — it does **not** look in `.luciferai/` — so after the setup script the banner may still report "Not installed" even though the agent can use the model (a code inconsistency, flagged for a follow-up fix). If the banner says "Not installed", copy the files to `~/.luciferai/bin/` + `~/.luciferai/models/` (or to the repo's `bin/` + `models/`, which the "Manual Installation" section in `docs/BUNDLED_MODELS.md` does and which the startup check does read).

## 📋 Requirements

- Python 3.9 or higher
- macOS or Linux (Windows via WSL)
- `curl` or `wget` (for the model download)

### Python Dependencies

```bash
pip3 install colorama requests psutil
```

> **Note:** `requirements.txt` does not list `requests` even though the code imports it, and it does not list `pytest` even though the README tells contributors to run `python -m pytest tests/`. Install both explicitly (`pip3 install requests pytest`) until that is fixed. The fallback Tier 1 auto-creates a venv and installs `requirements.txt`, so the same gap applies there.

## 🧰 The `luci` Command

`luci` is a shell function defined by `./setup_luci.sh` — it does not exist until you run that script:

```bash
./setup_luci.sh
# Reload your shell (or source the profile it updated), then:
luci install <package>    # Install a package/model
luci list                 # List installed packages
luci uninstall <package>  # Remove a package
luci update <package>     # Update a package
```

There is no `luci create` or `luci activate` — the package manager supports install/list/uninstall/update only.

## 🌐 Global `LuciferAI` Command

`./install_global.sh` creates `/usr/local/bin/LuciferAI` via sudo — but it hardcodes the original author's path (`/Users/TheRustySpoon/...`), so it is broken for anyone else. Until that is fixed, run the app as `python3 lucifer.py` from the repo directory instead of using a global command.

## ✅ Verify Installation

```bash
python3 lucifer.py
```

At the `>` prompt:

```bash
> help        # See all commands
> llm list    # See what models you have
```

There is no `--version` flag (`python3 lucifer.py --verbose` is not a flag either — verbose output is `LUCIFER_VERBOSE=1 python3 lucifer.py`).

To run the routing checks:

```bash
python3 tests/test_master_controller.py
# 76 routing cases, reported as print-based checks
```

## 🔄 Uninstall

Nothing was pip-installed, so there is nothing to `pip uninstall`. Delete the clone and the data directory:

```bash
rm -rf LuciferAI_Local ~/.luciferai
```

---

**Made with 🩸 by LuciferAI**
