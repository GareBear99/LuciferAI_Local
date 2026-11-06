#!/bin/bash
# 🩸 LuciferAI Installer
#
# Installs LuciferAI's Python dependencies and (optionally) the TinyLlama
# model. LuciferAI is NOT a pip package — there is no setup.py,
# pyproject.toml, or setup.cfg in this repo, so `pip install .` cannot work.
# The install is:
#   1. pip install -r requirements.txt   (this script)
#   2. ./setup_bundled_models.sh        (optional — downloads the model)
#   3. python3 lucifer.py               (run it)
#
# Usage: ./install.sh
#   Use ./install_global.sh afterwards for a global `LuciferAI` command.

set -e

PURPLE='\033[35m'
GREEN='\033[32m'
RED='\033[31m'
YELLOW='\033[33m'
BLUE='\033[34m'
RESET='\033[0m'

echo ""
echo -e "${PURPLE}╔════════════════════════════════════════════════════════╗${RESET}"
echo -e "${PURPLE}║         🩸 LuciferAI Installer                        ║${RESET}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════╝${RESET}"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 1. Python 3.9+
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ python3 not found. Install Python 3.9+ first.${RESET}"
    exit 1
fi
if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo -e "${RED}❌ Python 3.9+ is required (found: $(python3 --version)).${RESET}"
    exit 1
fi
echo -e "${GREEN}✅ $(python3 --version)${RESET}"

# 2. Python dependencies (requirements.txt — no package install, there is
#    nothing to pip-install for LuciferAI itself).
echo ""
echo -e "${YELLOW}📦 Installing Python dependencies (requirements.txt)...${RESET}"
if python3 -m pip --version &> /dev/null; then
    python3 -m pip install -r requirements.txt
elif command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    echo -e "${RED}❌ pip not found. Install pip (python3 -m ensurepip) and re-run.${RESET}"
    exit 1
fi
echo -e "${GREEN}✅ Dependencies installed${RESET}"

# 3. Model (optional, ~600MB download). The app runs without it
#    (rule-based command parsing only); the setup script is idempotent and
#    skips files that already exist.
echo ""
if [ -f "$SCRIPT_DIR/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" ]; then
    echo -e "${GREEN}✅ TinyLlama model already installed (models/)${RESET}"
else
    read -r -p "Download the TinyLlama model now (~600MB)? [y/N] " answer || answer=""
    case "$answer" in
        y|Y|yes|YES)
            ./setup_bundled_models.sh
            ;;
        *)
            echo -e "${YELLOW}Skipping model download. Run ./setup_bundled_models.sh later to add it.${RESET}"
            ;;
    esac
fi

echo ""
echo -e "${PURPLE}════════════════════════════════════════════════════════${RESET}"
echo -e "${GREEN}Installation complete!${RESET}"
echo ""
echo -e "${PURPLE}Run it:${RESET}"
echo -e "  ${BLUE}python3 lucifer.py${RESET}"
echo ""
echo -e "${PURPLE}Global command (optional):${RESET}"
echo -e "  ${BLUE}./install_global.sh${RESET}   # adds the LuciferAI command to /usr/local/bin"
echo -e "${PURPLE}════════════════════════════════════════════════════════${RESET}"
echo ""
