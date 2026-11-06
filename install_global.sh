#!/bin/bash
# 🩸 LuciferAI Global Command Installer
# Makes "LuciferAI" command available from any terminal

PURPLE='\033[35m'
GREEN='\033[32m'
YELLOW='\033[33m'
RESET='\033[0m'

echo ""
echo -e "${PURPLE}════════════════════════════════════════════════════════${RESET}"
echo -e "${PURPLE}        🩸 LuciferAI Global Command Installer${RESET}"
echo -e "${PURPLE}════════════════════════════════════════════════════════${RESET}"
echo ""

# Get the project directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create the global command script
COMMAND_SCRIPT="/usr/local/bin/LuciferAI"

echo -e "${YELLOW}Creating global LuciferAI command...${RESET}"

# Create the command: write the template to a temp file, substitute the
# real project directory (portable sed — no `sed -i ''`, which is macOS-only),
# then install it with sudo. No user or machine path is hardcoded anywhere.
TMP_SCRIPT="$(mktemp)"
cat > "$TMP_SCRIPT" << 'EOF'
#!/bin/bash
# LuciferAI Global Command

PROJECT_DIR="__LUCIFER_PROJECT_DIR__"

# Colors
PURPLE='\033[35m'
GREEN='\033[32m'
RED='\033[31m'
YELLOW='\033[33m'
BLUE='\033[34m'
RESET='\033[0m'

# If no arguments, show usage
if [ $# -eq 0 ]; then
    echo -e "${PURPLE}🩸 LuciferAI - Usage:${RESET}"
    echo ""
    echo -e "${YELLOW}Interactive Mode:${RESET}"
    echo "  LuciferAI                  - Start interactive mode"
    echo ""
    echo -e "${YELLOW}Install Command:${RESET}"
    echo "  LuciferAI install <pkg>    - Install package (brew/pip/npm)"
    echo "  LuciferAI install python   - Install Python"
    echo "  LuciferAI install node     - Install Node.js"
    echo "  LuciferAI install requests - Install Python package"
    echo ""
    echo -e "${YELLOW}Quick Commands:${RESET}"
    echo "  LuciferAI test             - Run test suite"
    echo "  LuciferAI test-all         - Full test suite (pytest)"
    echo "  LuciferAI version          - Show version"
    echo "  LuciferAI help             - Show help"
    echo ""
    exit 0
fi

# Handle commands
case "$1" in
    "install")
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Please specify what to install${RESET}"
            echo "Example: LuciferAI install requests"
            exit 1
        fi
        
        PACKAGE="$2"
        echo -e "${PURPLE}🩸 LuciferAI Install${RESET}"
        echo ""
        
        # Detect package type and install
        case "$PACKAGE" in
            python|python3)
                echo -e "${YELLOW}Installing Python via Homebrew...${RESET}"
                brew install python3
                ;;
            node|nodejs)
                echo -e "${YELLOW}Installing Node.js via Homebrew...${RESET}"
                brew install node
                ;;
            ollama)
                echo -e "${YELLOW}Installing Ollama via Homebrew...${RESET}"
                brew install ollama
                ;;
            *)
                # Try to detect package manager
                echo -e "${YELLOW}Detecting package type for: $PACKAGE${RESET}"
                
                # Try pip first (most common for Python projects)
                if command -v pip3 &> /dev/null; then
                    echo -e "${BLUE}Installing via pip3...${RESET}"
                    pip3 install "$PACKAGE"
                elif command -v pip &> /dev/null; then
                    echo -e "${BLUE}Installing via pip...${RESET}"
                    pip install "$PACKAGE"
                elif command -v npm &> /dev/null; then
                    echo -e "${BLUE}Installing via npm...${RESET}"
                    npm install -g "$PACKAGE"
                elif command -v brew &> /dev/null; then
                    echo -e "${BLUE}Installing via brew...${RESET}"
                    brew install "$PACKAGE"
                else
                    echo -e "${RED}No package manager found!${RESET}"
                    echo "Please install Homebrew, pip, or npm first"
                    exit 1
                fi
                ;;
        esac
        
        if [ $? -eq 0 ]; then
            echo ""
            echo -e "${GREEN}✅ Successfully installed: $PACKAGE${RESET}"
        else
            echo ""
            echo -e "${RED}❌ Installation failed${RESET}"
            exit 1
        fi
        ;;
    
    "test")
        echo -e "${PURPLE}🩸 Running LuciferAI Tests${RESET}"
        cd "$PROJECT_DIR" && python3 tests/test_master_controller.py
        ;;
    
    "test-all")
        echo -e "${PURPLE}🩸 Running Complete Test Suite${RESET}"
        cd "$PROJECT_DIR" && python3 -m pytest tests/
        ;;
    
    "version")
        if [ -f "$PROJECT_DIR/VERSION" ]; then
            VERSION=$(cat "$PROJECT_DIR/VERSION")
        else
            VERSION="1.0.0 (development)"
        fi
        echo -e "${PURPLE}🩸 LuciferAI Version: $VERSION${RESET}"
        ;;
    
    "help")
        echo -e "${PURPLE}🩸 LuciferAI - Autonomous AI Development Assistant${RESET}"
        echo ""
        echo "Run 'LuciferAI' without arguments to start interactive mode"
        echo "Run 'LuciferAI install <package>' to install packages"
        echo ""
        cd "$PROJECT_DIR" && ./lucifer.py
        ;;
    
    *)
        # Default: start interactive mode
        cd "$PROJECT_DIR" && ./lucifer.py
        ;;
esac
EOF

# Substitute this machine's project directory and install the command.
sed "s|__LUCIFER_PROJECT_DIR__|$PROJECT_DIR|g" "$TMP_SCRIPT" | sudo tee "$COMMAND_SCRIPT" > /dev/null
rm -f "$TMP_SCRIPT"

# Make it executable
sudo chmod +x "$COMMAND_SCRIPT"

echo -e "${GREEN}✅ Global command created: $COMMAND_SCRIPT${RESET}"
echo ""
echo -e "${YELLOW}Testing installation...${RESET}"

# Test the command
if command -v LuciferAI &> /dev/null; then
    echo -e "${GREEN}✅ LuciferAI command is now available globally!${RESET}"
    echo ""
    echo -e "${PURPLE}Usage:${RESET}"
    echo "  LuciferAI                  - Start interactive mode"
    echo "  LuciferAI install requests - Install Python package"
    echo "  LuciferAI install ollama   - Install Ollama"
    echo "  LuciferAI test             - Run tests"
    echo "  LuciferAI version          - Show version"
    echo ""
    echo -e "${GREEN}Try it: ${YELLOW}LuciferAI install requests${RESET}"
else
    echo -e "${RED}❌ Installation failed${RESET}"
    exit 1
fi

echo ""
echo -e "${PURPLE}════════════════════════════════════════════════════════${RESET}"
echo -e "${GREEN}  Installation complete! Use 'LuciferAI' from any terminal${RESET}"
echo -e "${PURPLE}════════════════════════════════════════════════════════${RESET}"
echo ""
