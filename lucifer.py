#!/usr/bin/env python3
"""
👾 LuciferAI - Local Warp AI Clone
Interactive terminal assistant
"""
import sys
import os
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

# Use enhanced agent with FixNet integration
from enhanced_agent import EnhancedLuciferAgent as LuciferAgent

PURPLE = "\033[35m"
GREEN = "\033[32m"
RED = "\033[31m"
GOLD = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_banner():
    """Print startup banner."""
    print(f"\n{PURPLE}{'═'*70}{RESET}")
    print(f"{PURPLE}║{' '*68}║{RESET}")
    print(f"{PURPLE}║{BOLD}    👾 LuciferAI - Local Terminal Assistant (Warp AI Clone){RESET}{PURPLE}     ║{RESET}")
    print(f"{PURPLE}║{' '*68}║{RESET}")
    print(f"{PURPLE}{'═'*70}{RESET}\n")
    print(f"{GOLD}💡 Type 'help' to see what I can do, 'exit' to quit{RESET}\n")


def main():
    """Main interactive loop."""
    print_banner()
    
    # Initialize agent
    agent = LuciferAgent()
    
    # Interactive loop
    while True:
        try:
            # Prompt
            user_input = input(f"\n{PURPLE}You >{RESET} ").strip()
            
            if not user_input:
                continue
            
            # Handle exit
            if user_input.lower() in ['exit', 'quit', 'q']:
                print(f"\n{PURPLE}👋 Farewell, mortal. LuciferAI signing off.{RESET}\n")
                break
            
            # Handle clear
            if user_input.lower() in ['clear', 'cls']:
                os.system('clear' if os.name != 'nt' else 'cls')
                print_banner()
                continue
            
            # Handle history clear
            if user_input.lower() == 'clear history':
                agent.clear_history()
                continue
            
            # Process request
            print(f"\n{BLUE}LuciferAI >{RESET}", end=" ")
            response = agent.process_request(user_input)
            print(response)
        
        except KeyboardInterrupt:
            print(f"\n\n{GOLD}⚠️  Interrupted. Type 'exit' to quit.{RESET}")
            continue
        
        except EOFError:
            print(f"\n{PURPLE}👋 EOF detected. Exiting.{RESET}\n")
            break
        
        except Exception as e:
            print(f"\n{RED}❌ Error: {e}{RESET}")
            print(f"{GOLD}💡 Please try again or type 'help'{RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{PURPLE}👋 Exiting LuciferAI{RESET}\n")
        sys.exit(0)
