# 🩸 LuciferAI Installation Guide

> **Read this first:** LuciferAI is **not a pip package** — there is no `setup.py`, `pyproject.toml`, or `setup.cfg` in this repo, so `pip install .`, `pip install --user .`, `pip install -e .`, and `pip install git+https://...` all fail. There is no Homebrew formula and no conda package. `./install.sh` installs the Python dependencies from `requirements.txt` and optionally downloads the model — or just clone the repo and run `python3 lucifer.py` (the app runs without the model, rule-based only).

## 🚀 Quick Install (The Working Path)

```bash
git clone https://github.com/GareBear99/LuciferAI_Local.git
cd LuciferAI_Local
python3 lucifer.py
```

That's it — no build step, no package install. `python3 lucifer.py` auto-assembles the llamafile binary from the split parts in `bin/` into `.luciferai/bin/`, checks for the TinyLlama model, prints the setup command if the model is missing, and continues without it (rule-based command parsing only).

## 📦 Install the Model (Optional, Recommended)

The TinyLlama model is **not** shipped in the repo (`models/` is empty in a fresh clone). Download it with the setup script:

```bash
./setup_bundled_models.sh
```

This downloads llamafile 0.8.13 (~34MB) and TinyLlama 1.1B (~600MB, TheBloke GGUF) into `<project>/.luciferai/bin/` and `<project>/models/` — the canonical layout every component uses (`core/lucifer_paths.py`).

> **Note:** `lucifer.py`'s startup check, the setup script, and the llamafile agent all use the same canonical layout (`core/lucifer_paths.py`): binary at `<project>/.luciferai/bin/llamafile`, models at `<project>/models/*.gguf`. If the banner says "Not installed" after the setup script, re-run the script — it verifies the binary runs and the model is a real GGUF before claiming success.

## 📋 Requirements

- Python 3.9 or higher
- macOS or Linux (Windows via WSL)
- `curl` or `wget` (for the model download)

### Python Dependencies

```bash
pip3 install -r requirements.txt
```

> **Note:** `requirements.txt` lists everything the code imports (`requests`, `cryptography`, `tqdm`, `schedule`) plus `pytest`.

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

`./install_global.sh` creates `/usr/local/bin/LuciferAI` via sudo, with this clone's directory baked in (derived from the script's own location — no path is hardcoded).

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
