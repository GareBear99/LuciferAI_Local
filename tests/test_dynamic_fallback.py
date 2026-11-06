#!/usr/bin/env python3
"""
Test script to validate the dynamic fallback step parsing
Tests various multi-part requests to ensure proper parsing
"""
import sys
import re
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent / "core"))


def parse_dynamic_steps(request: str) -> list:
    """Parse user request into dynamic steps for Tier 0/1 fallback.
    
    Intelligently detects multiple actions in a single request:
    - Create directory/folder
    - Move/copy files
    - Create scripts/files
    - Run/test scripts
    """
    request_lower = request.lower()
    steps = []
    
    # Action keywords to detect
    directory_keywords = ['directory', 'folder', 'dir']
    move_keywords = ['move', 'mv', 'transfer', 'relocate']
    create_keywords = ['create', 'make', 'build', 'generate', 'write']
    script_keywords = ['script', 'file', '.py', '.sh', '.js', '.txt']
    run_keywords = ['run', 'execute', 'test', 'launch']
    
    # Detect directory/folder creation
    has_directory = any(kw in request_lower for kw in directory_keywords)
    has_create = any(kw in request_lower for kw in create_keywords)
    
    if has_directory and has_create:
        # Extract directory name if possible
        dir_match = re.search(r'(?:directory|folder|dir)\s+(?:called|named)?\s*["\']?([\w-]+)', request_lower)
        if not dir_match:
            # Name BEFORE the keyword: "create utils folder".
            dir_match = re.search(r'(?:create|make|build)\s+(?:a\s+)?([\w-]+)\s+(?:folder|directory|dir)\b', request_lower)
        dir_name = dir_match.group(1) if dir_match else "directory"
        steps.append(f"Create {dir_name} directory")
    
    # Detect move operations
    has_move = any(kw in request_lower for kw in move_keywords)
    if has_move:
        # Extract file being moved if possible
        file_match = re.search(r'move\s+([\w.-]+)', request_lower)
        file_name = file_match.group(1) if file_match else "file"
        
        # Extract destination if possible
        dest_match = re.search(r'(?:to|into)\s+(?:the\s+)?([\w-]+)', request_lower)
        dest_name = dest_match.group(1) if dest_match else "destination"
        
        steps.append(f"Move {file_name} to {dest_name}")
    
    # Detect script/file creation (separate from directory)
    has_script = any(kw in request_lower for kw in script_keywords)
    if has_script and has_create:
        # Extract EVERY script/file name: after "script"/"file", after an
        # action verb, or after "with" — "create processor.py",
        # "make app.js", "build a directory api_client with client.py".
        # The old regex only matched a name after "script"/"file", so a
        # bare filename was dropped and the plan never mentioned it.
        script_names = []
        for m in re.finditer(
            r'(?:script|file|create|make|build|generate|write|with)\s+'
            r'(?:a\s+)?(?:new\s+)?(?:called\s+|named\s+)?[\"\']?([\w.-]+\.[\w]+)',
            request_lower,
        ):
            if m.group(1) not in script_names:
                script_names.append(m.group(1))
        if script_names:
            for script_name in script_names:
                steps.append(f"Create {script_name}")
        else:
            # No filename: keep the descriptive subject ("data analysis
            # script") so the step still says WHAT the script is about.
            # Without this, "create a comprehensive data analysis script
            # that reads CSV files..." produced only "Create script file"
            # and the purpose step ("Write code to reads csv files...")
            # never mentioned data/analysis at all.
            subject_match = re.search(r'([a-z][a-z ]{0,30}?)\s+(?:script|file)\b', request_lower)
            subject = subject_match.group(1).strip() if subject_match else ""
            subject = re.sub(r'^(?:create|make|build|generate|write)\s+(?:a\s+|an\s+|the\s+)?', '', subject)
            # A bare article is all that is left when the request is just
            # "create a file" / "create a script" — strip it so the step
            # falls back to "Create script file" (which names the file).
            subject = re.sub(r'^(?:a|an|the)$', '', subject).strip()
            steps.append(f"Create {subject} script" if subject else "Create script file")
        
        # Extract what the script should do
        purpose_match = re.search(r'(?:that|which|to)\s+(.{1,40})', request_lower)
        if purpose_match:
            purpose = purpose_match.group(1).strip()
            # Clean up common trailing words
            purpose = re.sub(r'\s+(?:and|then|,).*$', '', purpose)
            steps.append(f"Write code to {purpose}")
        else:
            # Use a portion of the request
            steps.append(f"Write code for: {request[:45]}")
    
    # Detect run/test operations (but not for non-executable files or filenames)
    # Look for run/test/execute as actual actions, not just in filenames
    has_run_action = False
    for kw in run_keywords:
        # Check if keyword appears as an action (not in filename)
        # e.g. "and run it" or "then test" but not "run.py"
        pattern = rf'\b{kw}\b(?!\.(py|sh|js))'  # word boundary, not followed by file extension
        if re.search(pattern, request_lower):
            # Make sure it's not part of a filename like "run.py"
            # Check if preceded by action words or followed by pronouns
            context_pattern = rf'(?:and|then|also)\s+{kw}|{kw}\s+(?:it|the|this)'
            if re.search(context_pattern, request_lower):
                has_run_action = True
                break
    
    # Only add run step for executable file types with explicit run action
    executable_extensions = ['.py', '.sh', '.js', '.rb', '.pl']
    has_executable = any(ext in request_lower for ext in executable_extensions)
    if has_run_action and has_script and has_executable:
        steps.append("Run and test the script")
    
    # Fallback: if no steps detected, create generic 3-step plan
    if not steps:
        steps = [
            "Create the file",
            "Verify file exists",
            f"Write code for: {request[:45]}"
        ]
    
    # Limit to reasonable number of steps (3-5 for Tier 0/1)
    if len(steps) > 5:
        steps = steps[:5]
    elif len(steps) < 3:
        # Pad with verification step if needed
        steps.append("Verify creation")
    
    return steps


# NOTE: this helper must NOT be named test_* and must NOT take a parameter
# named `request` — pytest treats every parameter of a test_* function as a
# fixture name, so it injected its builtin `request` fixture (a
# FixtureRequest object) instead of the string, and parse_dynamic_steps
# crashed on `.lower()` ('TopRequest' has no 'lower').
def check_request(user_request: str, expected_keywords: list = None):
    """Parse a request, display the steps, assert the expected keywords."""
    print(f"\n{'='*70}")
    print(f"REQUEST: {user_request}")
    print(f"{'='*70}")

    steps = parse_dynamic_steps(user_request)

    print(f"\nPARSED STEPS ({len(steps)} steps):")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")

    if expected_keywords:
        print(f"\nVALIDATION:")
        all_steps_text = " ".join(steps).lower()
        for keyword in expected_keywords:
            found = keyword.lower() in all_steps_text
            status = "✓" if found else "✗"
            print(f"  {status} Should contain '{keyword}': {'PASS' if found else 'FAIL'}")
            assert found, f"parsed steps for {user_request!r} lack {keyword!r}: {steps}"

    return steps


# The cases main() runs, shared with the pytest test below.
CASES = [
    ("create a script called hello.py that prints hello world",
     ["hello.py", "print"]),
    ("create a directory called myproject and create a file run.py in it",
     ["myproject", "run.py"]),
    ("move test.txt to the documents folder",
     ["move", "test.txt", "documents"]),
    ("create a folder called tools, create a script calc.py that does math, and run it",
     ["tools", "calc.py", "math", "run"]),
    ("make a python script that opens the browser",
     ["script", "open", "browser"]),
    ("create a comprehensive data analysis script that reads CSV files, processes them with pandas, generates visualizations, and exports results",
     ["script", "data", "analysis"]),
    ("move old_script.py to archive and create a new script main.py",
     ["move", "old_script.py", "archive", "main.py"]),
    ("do something with the files",
     ["file"]),
]


def test_request():
    """Pytest entry point: no parameters (see the note on check_request)."""
    for user_request, expected_keywords in CASES:
        check_request(user_request, expected_keywords)


def main():
    """Run tests on various request types."""
    print("=" * 70)
    print("DYNAMIC FALLBACK STEP PARSING TEST")
    print("=" * 70)

    for user_request, expected_keywords in CASES:
        check_request(user_request, expected_keywords)

    print(f"\n{'='*70}")
    print("TEST COMPLETE")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
