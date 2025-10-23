#!/usr/bin/env python3
"""
🧠 LuciferAI Enhanced Agent - Self-Healing with FixNet Integration
Automatically detects errors, searches for fixes, applies them, and uploads to FixNet
"""
import sys
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add parent paths
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
sys.path.insert(0, str(Path(__file__).parent))

from file_tools import read_file, write_file, edit_file, find_files, grep_search, list_directory
from command_tools import run_command, run_python_code, get_env_info, check_command_exists, is_risky_command
from lucifer_auth import LuciferAuth
from fixnet_uploader import FixNetUploader
from relevance_dictionary import RelevanceDictionary

PURPLE = "\033[35m"
GREEN = "\033[32m"
RED = "\033[31m"
GOLD = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"


class EnhancedLuciferAgent:
    """
    Enhanced agent with:
    - Authentication
    - Self-healing (FixNet integration)
    - Collaborative learning
    - Error detection & auto-fix
    """
    
    def __init__(self):
        print(f"{PURPLE}🩸 Initializing Enhanced LuciferAI...{RESET}")
        
        # Initialize components
        self.auth = LuciferAuth()
        self.auth.auth_init()
        
        # Get user ID for FixNet
        self.user_id = self._get_user_id()
        
        self.uploader = FixNetUploader(self.user_id)
        self.dictionary = RelevanceDictionary(self.user_id)
        
        self.conversation_history: List[Dict[str, str]] = []
        self.tools_executed: List[str] = []
        self.env = get_env_info()
        self.fixes_applied = 0
        
        print(f"{GREEN}✅ Enhanced LuciferAI ready{RESET}")
        print(f"{BLUE}👤 User ID: {self.user_id}{RESET}")
        print(f"{GOLD}📁 Working directory: {self.env['cwd']}{RESET}\n")
    
    def _get_user_id(self) -> str:
        """Get user ID from auth system or generate."""
        import hashlib
        import uuid
        device_id = str(uuid.UUID(int=uuid.getnode()))
        username = os.getenv("USER", "unknown")
        combined = f"{device_id}-{username}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16].upper()
    
    def process_request(self, user_input: str) -> str:
        """
        Main entry point - process user request with auto-fix.
        """
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Route request
        response = self._route_request(user_input)
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
    
    def _route_request(self, user_input: str) -> str:
        """Route request to appropriate handler."""
        user_lower = user_input.lower().strip()
        
        # FixNet commands
        if 'fixnet' in user_lower or 'dictionary' in user_lower:
            if 'sync' in user_lower:
                return self._handle_fixnet_sync()
            elif 'stats' in user_lower or 'statistics' in user_lower:
                return self._handle_dictionary_stats()
            elif 'search' in user_lower:
                # Extract error pattern
                match = re.search(r'search\s+(?:for\s+)?["\']?(.+?)["\']?$', user_lower)
                if match:
                    error = match.group(1)
                    return self._handle_search_fixes(error)
        
        # Fix/run script commands
        if 'fix' in user_lower:
            if match := re.search(r'fix\s+(.+)', user_lower):
                filepath = match.group(1).strip()
                return self._handle_fix_script(filepath)
        
        if 'run' in user_lower:
            if match := re.search(r'run\s+(.+)', user_lower):
                target = match.group(1).strip()
                # Check if it's a file or command
                if Path(target).exists() and target.endswith('.py'):
                    return self._handle_run_script(target)
                else:
                    return self._handle_run_command(target)
        
        # File operations (from original agent)
        if any(keyword in user_lower for keyword in ['read', 'show', 'cat', 'view', 'open']):
            if match := re.search(r'(?:read|show|cat|view|open)\s+(.+)', user_lower):
                filepath = match.group(1).strip()
                return self._handle_read_file(filepath)
        
        if any(keyword in user_lower for keyword in ['find', 'search for file', 'locate']):
            if match := re.search(r'(?:find|locate)\s+(?:files?\s+)?(.+)', user_lower):
                pattern = match.group(1).strip()
                return self._handle_find_files(pattern)
        
        if any(keyword in user_lower for keyword in ['list', 'ls']):
            if match := re.search(r'(?:list|ls)\s+(?:in\s+)?(.+)', user_lower):
                path = match.group(1).strip() or "."
            else:
                path = "."
            return self._handle_list_directory(path)
        
        if any(keyword in user_lower for keyword in ['where am i', 'current directory', 'pwd']):
            return self._handle_env_info()
        
        if user_lower in ['help', '?']:
            return self._handle_help()
        
        return self._handle_unknown(user_input)
    
    def _handle_run_script(self, filepath: str) -> str:
        """Run a Python script with auto-fix on error."""
        print(f"{BLUE}⚡ Running script: {filepath}{RESET}")
        self.tools_executed.append(f"run_script({filepath})")
        
        filepath = os.path.expanduser(filepath)
        
        if not os.path.exists(filepath):
            return f"{RED}❌ File not found: {filepath}{RESET}"
        
        # Run script
        result = run_python_code(open(filepath).read(), timeout=15)
        
        if result["success"]:
            return f"{GREEN}✅ Script executed successfully{RESET}\n\n{result['stdout']}"
        else:
            # Error detected - trigger auto-fix
            error = result["stderr"]
            print(f"\n{GOLD}⚠️  Error detected - initiating auto-fix...{RESET}\n")
            
            return self._auto_fix_script(filepath, error)
    
    def _handle_fix_script(self, filepath: str) -> str:
        """Manually trigger fix for a script."""
        print(f"{BLUE}🔧 Analyzing script: {filepath}{RESET}")
        
        filepath = os.path.expanduser(filepath)
        
        if not os.path.exists(filepath):
            return f"{RED}❌ File not found: {filepath}{RESET}"
        
        # Run to detect error
        result = run_python_code(open(filepath).read(), timeout=15)
        
        if result["success"]:
            return f"{GREEN}✅ Script runs successfully - no fixes needed{RESET}"
        
        error = result["stderr"]
        return self._auto_fix_script(filepath, error)
    
    def _auto_fix_script(self, filepath: str, error: str) -> str:
        """
        Automatic fix workflow:
        1. Search dictionary for similar fixes
        2. Apply known fix if found
        3. If not found or fails, generate new fix
        4. Upload to FixNet
        5. Update dictionary
        """
        print(f"\n{PURPLE}{'='*60}{RESET}")
        print(f"{PURPLE}🔧 LuciferAI Auto-Fix System{RESET}")
        print(f"{PURPLE}{'='*60}{RESET}\n")
        
        print(f"{RED}Error:{RESET}\n{error[:300]}...\n")
        
        # Step 1: Search dictionary
        print(f"{GOLD}[1/5] Searching for similar fixes...{RESET}")
        error_type = self._classify_error(error)
        best_fix = self.dictionary.get_best_fix_for_error(error, error_type)
        
        if best_fix and best_fix.get('source') == 'local':
            # Step 2: Try applying known fix
            print(f"\n{GOLD}[2/5] Applying known fix (score: {best_fix['relevance_score']:.2f})...{RESET}")
            print(f"{BLUE}   Solution: {best_fix['solution']}{RESET}")
            
            success = self._apply_fix_to_script(filepath, best_fix['solution'], error)
            
            # Record usage
            self.dictionary.record_fix_usage(best_fix['fix_hash'], success)
            
            if success:
                self.fixes_applied += 1
                print(f"\n{GREEN}✅ Known fix applied successfully!{RESET}")
                return f"{GREEN}✅ Script fixed using known solution (score: {best_fix['relevance_score']:.2f}){RESET}\n\n{best_fix['solution']}"
            else:
                print(f"\n{GOLD}⚠️  Known fix didn't work, generating new fix...{RESET}")
        
        # Step 3: Generate new fix (placeholder - would use AI here)
        print(f"\n{GOLD}[3/5] Generating new fix...{RESET}")
        new_solution = self._generate_fix(filepath, error, error_type)
        
        if not new_solution:
            return f"{RED}❌ Could not generate fix automatically{RESET}\n\n{GOLD}💡 Suggestion: {self._get_fix_hint(error)}{RESET}"
        
        # Step 4: Apply new fix
        print(f"{GOLD}[4/5] Applying new fix...{RESET}")
        success = self._apply_fix_to_script(filepath, new_solution, error)
        
        if not success:
            return f"{RED}❌ Auto-fix failed{RESET}\n\n{GOLD}Generated fix: {new_solution}{RESET}"
        
        self.fixes_applied += 1
        
        # Step 5: Upload to FixNet
        print(f"\n{GOLD}[5/5] Uploading fix to FixNet...{RESET}")
        
        commit_url = self.uploader.full_fix_upload_flow(
            script_path=filepath,
            error=error,
            solution=new_solution,
            context={
                "error_type": error_type,
                "script": os.path.basename(filepath),
                "fixes_applied_this_session": self.fixes_applied
            }
        )
        
        # Add to dictionary
        import hashlib
        fix_hash = hashlib.sha256(new_solution.encode()).hexdigest()
        
        dict_key = self.dictionary.add_fix(
            error_type=error_type,
            error_signature=error,
            solution=new_solution,
            fix_hash=fix_hash,
            context={"filepath": filepath},
            commit_url=commit_url
        )
        
        # Check if inspired by a similar fix
        if best_fix:
            print(f"\n{PURPLE}🌿 Creating branch link...{RESET}")
            self.dictionary.create_branch(
                fix_hash,
                best_fix['fix_hash'],
                "solved_similar"
            )
        
        return f"""{GREEN}✅ Script fixed and uploaded to FixNet!{RESET}

{BLUE}Fix Applied:{RESET}
{new_solution}

{GOLD}FixNet Commit:{RESET}
{commit_url or 'Local only (configure GitHub remote to push)'}

{PURPLE}Dictionary:{RESET}
Added to dictionary key: {dict_key[:50]}...
"""
    
    def _apply_fix_to_script(self, filepath: str, solution: str, original_error: str) -> bool:
        """
        Apply a fix to the script and verify it works.
        
        Returns:
            True if fix succeeded
        """
        try:
            # Read current script
            with open(filepath) as f:
                original_content = f.read()
            
            # For simple fixes (imports), add at top
            if solution.startswith("Added:") or solution.startswith("from ") or solution.startswith("import "):
                import_line = solution.replace("Added: ", "").strip()
                
                # Add import at top (after shebang/docstring if present)
                lines = original_content.split('\n')
                insert_pos = 0
                
                # Skip shebang and docstrings
                for i, line in enumerate(lines):
                    if line.startswith('#!') or line.startswith('"""') or line.startswith("'''"):
                        insert_pos = i + 1
                    elif line.strip() and not line.startswith('#'):
                        break
                
                lines.insert(insert_pos, import_line)
                new_content = '\n'.join(lines)
                
                # Write back
                with open(filepath, 'w') as f:
                    f.write(new_content)
                
                # Test if it works now
                result = run_python_code(new_content, timeout=10)
                
                if result["success"]:
                    return True
                else:
                    # Revert if still fails
                    with open(filepath, 'w') as f:
                        f.write(original_content)
                    return False
            
            # For other fixes, would need more sophisticated patching
            return False
        
        except Exception as e:
            print(f"{RED}❌ Error applying fix: {e}{RESET}")
            return False
    
    def _generate_fix(self, filepath: str, error: str, error_type: str) -> Optional[str]:
        """
        Generate a fix for the error.
        In production, this would use AI (Ollama/Mistral).
        For now, uses pattern matching.
        """
        # Extract key info from error
        if "ModuleNotFoundError" in error or "No module named" in error:
            # Extract module name
            match = re.search(r"No module named ['\"]([^'\"]+)['\"]", error)
            if match:
                module = match.group(1)
                return f"from {module} import *"
        
        elif "NameError" in error and "is not defined" in error:
            # Extract variable name
            match = re.search(r"name ['\"]([^'\"]+)['\"] is not defined", error)
            if match:
                var_name = match.group(1)
                # Try to guess module
                common_imports = {
                    'os': 'import os',
                    'sys': 'import sys',
                    'json': 'import json',
                    'Path': 'from pathlib import Path',
                    'datetime': 'from datetime import datetime',
                    'time': 'import time'
                }
                if var_name in common_imports:
                    return common_imports[var_name]
                else:
                    return f"# TODO: Import or define '{var_name}'"
        
        return None
    
    def _classify_error(self, error: str) -> str:
        """Classify error type."""
        error_lower = error.lower()
        
        if "nameerror" in error_lower:
            return "NameError"
        elif "syntaxerror" in error_lower:
            return "SyntaxError"
        elif "importerror" in error_lower or "modulenotfound" in error_lower:
            return "ImportError"
        elif "typeerror" in error_lower:
            return "TypeError"
        elif "attributeerror" in error_lower:
            return "AttributeError"
        else:
            return "Unknown"
    
    def _get_fix_hint(self, error: str) -> str:
        """Get a hint for fixing the error."""
        if "import" in error.lower() or "module" in error.lower():
            return "Try installing the missing module or checking import paths"
        elif "name" in error.lower():
            return "Check variable/function names and imports"
        elif "syntax" in error.lower():
            return "Review syntax - check for missing colons, parentheses, or indentation"
        else:
            return "Review the error message and check the documentation"
    
    def _handle_search_fixes(self, error: str) -> str:
        """Search dictionary for fixes matching an error."""
        print(f"{BLUE}🔍 Searching FixNet for: {error}{RESET}")
        
        matches = self.dictionary.search_similar_fixes(error, min_relevance=0.3)
        
        if not matches:
            return f"{GOLD}💡 No fixes found for '{error}'{RESET}"
        
        response = f"{GREEN}✅ Found {len(matches)} similar fixes:{RESET}\n\n"
        
        for i, match in enumerate(matches[:5], 1):
            source_icon = "📁" if match['source'] == 'local' else "🌐"
            response += f"{source_icon} {i}. {match.get('error_type', 'Unknown')} "
            response += f"(score: {match['relevance_score']:.2f})\n"
            
            if match['source'] == 'local':
                response += f"   Solution: {match.get('solution', 'N/A')[:80]}...\n"
                response += f"   Success: {match.get('success_count', 0)}/{match.get('usage_count', 0)}\n"
            else:
                response += f"   User: {match.get('user_id', 'Unknown')}\n"
                response += f"   Note: {match.get('note', 'Encrypted')}\n"
            
            response += "\n"
        
        if len(matches) > 5:
            response += f"{GOLD}... and {len(matches) - 5} more matches{RESET}"
        
        return response
    
    def _handle_fixnet_sync(self) -> str:
        """Sync with FixNet."""
        print(f"{BLUE}🔄 Syncing with FixNet...{RESET}")
        self.dictionary.sync_with_remote()
        return f"{GREEN}✅ Synced with FixNet - {len(self.dictionary.remote_refs)} remote fixes available{RESET}"
    
    def _handle_dictionary_stats(self) -> str:
        """Show dictionary statistics."""
        self.dictionary.print_statistics()
        return ""  # Stats are printed directly
    
    # Original agent methods (unchanged)
    def _handle_read_file(self, filepath: str) -> str:
        print(f"{BLUE}🔍 Reading file: {filepath}{RESET}")
        self.tools_executed.append(f"read_file({filepath})")
        result = read_file(filepath)
        if result["success"]:
            return f"{GREEN}✅ Read {filepath}{RESET}\n\n{result['content']}"
        return f"{RED}❌ Error: {result['error']}{RESET}"
    
    def _handle_find_files(self, pattern: str) -> str:
        print(f"{BLUE}🔍 Finding files: {pattern}{RESET}")
        pattern = pattern.strip('"\'')
        result = find_files(pattern, self.env['cwd'])
        if result["success"]:
            if result["count"] == 0:
                return f"{GOLD}No files found matching '{pattern}'{RESET}"
            response = f"{GREEN}✅ Found {result['count']} files:{RESET}\n\n"
            for match in result["matches"][:20]:
                response += f"  📄 {match['relative']}\n"
            if result["count"] > 20:
                response += f"\n{GOLD}... and {result['count'] - 20} more{RESET}"
            return response
        return f"{RED}❌ Error: {result['error']}{RESET}"
    
    def _handle_list_directory(self, path: str) -> str:
        print(f"{BLUE}📂 Listing directory: {path}{RESET}")
        result = list_directory(path)
        if result["success"]:
            response = f"{GREEN}✅ Contents of {result['path']}:{RESET}\n\n"
            for item in result["items"]:
                icon = "📁" if item["type"] == "dir" else "📄"
                size = f"({item['size']} bytes)" if item["size"] else ""
                response += f"  {icon} {item['name']} {size}\n"
            return response
        return f"{RED}❌ Error: {result['error']}{RESET}"
    
    def _handle_run_command(self, command: str) -> str:
        print(f"{BLUE}⚡ Running command: {command}{RESET}")
        if is_risky_command(command):
            return f"{RED}⚠️  Risky command detected. Please run manually.{RESET}"
        result = run_command(command, cwd=self.env['cwd'])
        if result["success"]:
            return f"{GREEN}✅ Command executed{RESET}\n\n{result['stdout']}"
        return f"{RED}❌ Command failed{RESET}\n\n{result.get('stderr', result.get('error'))}"
    
    def _handle_env_info(self) -> str:
        return f"""{GREEN}📍 Environment:{RESET}
  Directory: {self.env['cwd']}
  User: {self.env['user']}
  Shell: {self.env['shell']}
  Platform: {self.env['platform']}
"""
    
    def _handle_help(self) -> str:
        return f"""{PURPLE}👾 Enhanced LuciferAI Capabilities:{RESET}

{GREEN}🔧 Self-Healing:{RESET}
  • "run <script.py>" - Execute with auto-fix on error
  • "fix <script.py>" - Manually trigger fix analysis
  • "search fixes for '<error>'" - Search FixNet for solutions

{GREEN}🌐 FixNet:{RESET}
  • "fixnet sync" - Sync with remote fixes
  • "fixnet stats" - View dictionary statistics
  • Automatic upload of new fixes to GitHub

{GREEN}📂 File Operations:{RESET}
  • "read <file>" - Read file
  • "find <pattern>" - Find files
  • "list <dir>" - List directory

{GREEN}⚡ Commands:{RESET}
  • "run <command>" - Execute command
  • "where am i" - Environment info

{GOLD}✨ New: All scripts automatically fixed and uploaded to FixNet!{RESET}
"""
    
    def _handle_unknown(self, user_input: str) -> str:
        return f"""{GOLD}🤔 Not sure how to handle that.

Try:{RESET}
  • "help" - See capabilities
  • "run script.py" - Execute with auto-fix
  • "fixnet stats" - View fix dictionary
"""


# Test enhanced agent
if __name__ == "__main__":
    print(f"{PURPLE}╔════════════════════════════════════════╗{RESET}")
    print(f"{PURPLE}║   👾 Enhanced LuciferAI Test Suite    ║{RESET}")
    print(f"{PURPLE}╚════════════════════════════════════════╝{RESET}\n")
    
    agent = EnhancedLuciferAgent()
    
    # Test commands
    test_commands = [
        "help",
        "where am i",
        "fixnet stats",
        "list .",
    ]
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"\n{PURPLE}{'='*60}{RESET}")
        print(f"{GOLD}Test {i}: {cmd}{RESET}")
        print(f"{PURPLE}{'='*60}{RESET}\n")
        
        response = agent.process_request(cmd)
        print(response)
    
    print(f"\n\n{GREEN}✅ Enhanced agent tests complete!{RESET}")
