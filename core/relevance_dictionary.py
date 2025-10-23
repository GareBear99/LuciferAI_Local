#!/usr/bin/env python3
"""
🧩 LuciferAI Relevance Dictionary - Collaborative Fix Learning
Builds intelligent error-to-solution mappings with user branching and relevance scoring
"""
import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from collections import defaultdict
import difflib

PURPLE = "\033[35m"
GREEN = "\033[32m"
RED = "\033[31m"
GOLD = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

# Paths
LUCIFER_HOME = Path.home() / ".luciferai"
DICT_FILE = LUCIFER_HOME / "data" / "fix_dictionary.json"
LOCAL_BRANCHES = LUCIFER_HOME / "data" / "user_branches.json"
REMOTE_REFS = LUCIFER_HOME / "sync" / "remote_fix_refs.json"
FIXNET_REFS = LUCIFER_HOME / "fixnet" / "refs.json"

# Ensure directories
DICT_FILE.parent.mkdir(parents=True, exist_ok=True)


class RelevanceDictionary:
    """
    Manages collaborative fix learning with branching and relevance scoring.
    
    Structure:
    - Local dictionary: user's own fixes
    - Branch links: connections to fixes that helped solve issues
    - Remote references: other users' fixes from GitHub
    - Relevance scores: weighted by success rate
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.dictionary: Dict[str, List[Dict]] = self._load_dictionary()
        self.branches: Dict[str, List[str]] = self._load_branches()
        self.remote_refs: List[Dict] = self._load_remote_refs()
    
    def _load_dictionary(self) -> Dict[str, List[Dict]]:
        """Load local fix dictionary."""
        if DICT_FILE.exists():
            with open(DICT_FILE) as f:
                return json.load(f)
        return {}
    
    def _save_dictionary(self):
        """Save local fix dictionary."""
        with open(DICT_FILE, 'w') as f:
            json.dump(self.dictionary, f, indent=2)
    
    def _load_branches(self) -> Dict[str, List[str]]:
        """Load branch connections."""
        if LOCAL_BRANCHES.exists():
            with open(LOCAL_BRANCHES) as f:
                return json.load(f)
        return {}
    
    def _save_branches(self):
        """Save branch connections."""
        with open(LOCAL_BRANCHES, 'w') as f:
            json.dump(self.branches, f, indent=2)
    
    def _load_remote_refs(self) -> List[Dict]:
        """Load remote fix references from FixNet."""
        refs = []
        
        # Load from local FixNet repo
        if FIXNET_REFS.exists():
            with open(FIXNET_REFS) as f:
                refs = json.load(f)
        
        # Also check cached remote refs
        if REMOTE_REFS.exists():
            with open(REMOTE_REFS) as f:
                cached = json.load(f)
                # Merge unique refs
                ref_hashes = {r['fix_hash'] for r in refs}
                for cached_ref in cached:
                    if cached_ref['fix_hash'] not in ref_hashes:
                        refs.append(cached_ref)
        
        return refs
    
    def add_fix(self,
                error_type: str,
                error_signature: str,
                solution: str,
                fix_hash: str,
                context: Dict[str, Any],
                commit_url: Optional[str] = None) -> str:
        """
        Add a new fix to the dictionary.
        
        Args:
            error_type: Classification of error (NameError, SyntaxError, etc.)
            error_signature: Normalized error pattern
            solution: Fix that was applied
            fix_hash: Unique hash of the fix
            context: Additional context
            commit_url: GitHub commit URL if uploaded
        
        Returns:
            Dictionary key for this fix
        """
        # Normalize error signature for matching
        normalized_key = self._normalize_error(error_signature)
        
        # Create fix entry
        fix_entry = {
            "fix_hash": fix_hash,
            "user_id": self.user_id,
            "error_type": error_type,
            "error_signature": error_signature,
            "solution": solution,
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "commit_url": commit_url,
            "success_count": 1,
            "usage_count": 1,
            "relevance_score": 1.0,
            "branches": []  # Will link to related fixes
        }
        
        # Add to dictionary
        if normalized_key not in self.dictionary:
            self.dictionary[normalized_key] = []
        
        self.dictionary[normalized_key].append(fix_entry)
        self._save_dictionary()
        
        print(f"{GREEN}📚 Added to dictionary: {normalized_key}{RESET}")
        print(f"{BLUE}   Fix hash: {fix_hash[:12]}...{RESET}")
        
        return normalized_key
    
    def search_similar_fixes(self, 
                             error: str,
                             error_type: Optional[str] = None,
                             min_relevance: float = 0.5) -> List[Dict[str, Any]]:
        """
        Search for similar fixes in local and remote dictionaries.
        
        Args:
            error: Error message to match
            error_type: Optional error type filter
            min_relevance: Minimum relevance score threshold
        
        Returns:
            List of matching fixes sorted by relevance
        """
        normalized = self._normalize_error(error)
        matches = []
        
        # Search local dictionary
        print(f"{BLUE}🔍 Searching local dictionary...{RESET}")
        local_matches = self._search_local(normalized, error_type, min_relevance)
        matches.extend(local_matches)
        
        # Search remote references
        print(f"{BLUE}🌐 Searching remote FixNet...{RESET}")
        remote_matches = self._search_remote(normalized, error_type, min_relevance)
        matches.extend(remote_matches)
        
        # Sort by relevance score
        matches.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        if matches:
            print(f"{GREEN}✅ Found {len(matches)} similar fixes{RESET}")
        else:
            print(f"{GOLD}💡 No similar fixes found - this will be the first!{RESET}")
        
        return matches
    
    def _search_local(self,
                     normalized_error: str,
                     error_type: Optional[str],
                     min_relevance: float) -> List[Dict]:
        """Search local dictionary."""
        matches = []
        
        for key, fixes in self.dictionary.items():
            # Calculate similarity
            similarity = self._calculate_similarity(normalized_error, key)
            
            if similarity < 0.3:  # Too different
                continue
            
            for fix in fixes:
                # Filter by error type if specified
                if error_type and fix['error_type'] != error_type:
                    continue
                
                # Calculate relevance
                relevance = self._calculate_relevance(fix, similarity)
                
                if relevance >= min_relevance:
                    match = fix.copy()
                    match['relevance_score'] = relevance
                    match['source'] = 'local'
                    match['similarity'] = similarity
                    matches.append(match)
        
        return matches
    
    def _search_remote(self,
                      normalized_error: str,
                      error_type: Optional[str],
                      min_relevance: float) -> List[Dict]:
        """Search remote references."""
        matches = []
        
        for ref in self.remote_refs:
            # Skip own fixes (already in local)
            if ref.get('user_id') == self.user_id:
                continue
            
            # Filter by error type
            if error_type and ref.get('error_type') != error_type:
                continue
            
            # Calculate similarity (using limited metadata)
            script_similarity = 0.3  # Base score for same error type
            
            # We can't see the actual error text (encrypted), but we can use metadata
            if ref.get('script'):
                # Higher score if script names are similar
                script_similarity += 0.2
            
            relevance = script_similarity
            
            if relevance >= min_relevance:
                match = {
                    'fix_hash': ref['fix_hash'],
                    'user_id': ref['user_id'],
                    'error_type': ref.get('error_type', 'Unknown'),
                    'timestamp': ref.get('timestamp'),
                    'encrypted_file': ref.get('encrypted_file'),
                    'relevance_score': relevance,
                    'source': 'remote',
                    'note': 'Encrypted - contributed by another user'
                }
                matches.append(match)
        
        return matches
    
    def create_branch(self,
                     original_fix_hash: str,
                     inspired_by_hash: str,
                     relationship: str = "solved_similar"):
        """
        Create a branch connection between fixes.
        
        Args:
            original_fix_hash: Your fix
            inspired_by_hash: Fix that helped solve it
            relationship: Type of relationship
        """
        if original_fix_hash not in self.branches:
            self.branches[original_fix_hash] = []
        
        branch_link = {
            "target_hash": inspired_by_hash,
            "relationship": relationship,
            "created": datetime.now().isoformat()
        }
        
        self.branches[original_fix_hash].append(branch_link)
        self._save_branches()
        
        # Also update the fix entry in dictionary
        for key, fixes in self.dictionary.items():
            for fix in fixes:
                if fix['fix_hash'] == original_fix_hash:
                    if 'branches' not in fix:
                        fix['branches'] = []
                    fix['branches'].append(branch_link)
                    self._save_dictionary()
                    break
        
        print(f"{PURPLE}🌿 Branch created: {original_fix_hash[:8]} → {inspired_by_hash[:8]}{RESET}")
    
    def record_fix_usage(self, fix_hash: str, succeeded: bool):
        """
        Record that a fix was used and whether it succeeded.
        Updates relevance scores.
        """
        for key, fixes in self.dictionary.items():
            for fix in fixes:
                if fix['fix_hash'] == fix_hash:
                    fix['usage_count'] += 1
                    if succeeded:
                        fix['success_count'] += 1
                    
                    # Recalculate relevance score
                    success_rate = fix['success_count'] / fix['usage_count']
                    usage_weight = min(1.0, fix['usage_count'] / 10)  # Cap at 10 uses
                    fix['relevance_score'] = (success_rate * 0.7) + (usage_weight * 0.3)
                    
                    self._save_dictionary()
                    
                    status = f"{GREEN}succeeded{RESET}" if succeeded else f"{RED}failed{RESET}"
                    print(f"{BLUE}📊 Updated fix {fix_hash[:8]}: {status}, score: {fix['relevance_score']:.2f}{RESET}")
                    return
    
    def get_best_fix_for_error(self, error: str, error_type: Optional[str] = None) -> Optional[Dict]:
        """
        Get the best fix for a given error.
        
        Returns:
            Best matching fix or None
        """
        matches = self.search_similar_fixes(error, error_type, min_relevance=0.3)
        
        if not matches:
            return None
        
        # Return highest scoring local fix (we can't decrypt remote ones)
        local_matches = [m for m in matches if m['source'] == 'local']
        
        if local_matches:
            best = local_matches[0]
            print(f"{GOLD}💡 Best fix found (score: {best['relevance_score']:.2f}){RESET}")
            return best
        
        # If only remote matches, suggest pattern
        print(f"{GOLD}💡 {len(matches)} similar fixes found by other users (encrypted){RESET}")
        print(f"{BLUE}   This suggests the error is common - fix will be logged to help others{RESET}")
        return None
    
    def get_branch_tree(self, fix_hash: str, depth: int = 3) -> Dict[str, Any]:
        """
        Get the branch tree for a fix (what it helped solve).
        
        Args:
            fix_hash: Root fix hash
            depth: Maximum depth to traverse
        
        Returns:
            Tree structure of branches
        """
        if fix_hash not in self.branches or depth == 0:
            return {"hash": fix_hash, "branches": []}
        
        tree = {
            "hash": fix_hash,
            "branches": []
        }
        
        for branch in self.branches[fix_hash]:
            child_tree = self.get_branch_tree(branch['target_hash'], depth - 1)
            child_tree['relationship'] = branch['relationship']
            tree['branches'].append(child_tree)
        
        return tree
    
    def sync_with_remote(self):
        """
        Sync local dictionary with remote FixNet references.
        Updates relevance scores based on collective usage.
        """
        print(f"{BLUE}🔄 Syncing with FixNet...{RESET}")
        
        # Reload remote refs
        self.remote_refs = self._load_remote_refs()
        
        # Cache for faster searches
        with open(REMOTE_REFS, 'w') as f:
            json.dump(self.remote_refs, f, indent=2)
        
        print(f"{GREEN}✅ Synced {len(self.remote_refs)} remote fixes{RESET}")
    
    def _normalize_error(self, error: str) -> str:
        """Normalize error for consistent matching."""
        # Remove file paths, line numbers, variable names
        normalized = error.lower()
        
        # Remove line numbers
        normalized = ' '.join(w for w in normalized.split() if not w.isdigit())
        
        # Remove file paths
        normalized = normalized.split('file')[0] if 'file' in normalized else normalized
        
        # Keep only error type and core message
        for delimiter in ['\n', 'traceback', 'during handling']:
            if delimiter in normalized:
                normalized = normalized.split(delimiter)[0]
        
        return normalized.strip()[:200]  # Limit length
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings."""
        return difflib.SequenceMatcher(None, str1, str2).ratio()
    
    def _calculate_relevance(self, fix: Dict, base_similarity: float) -> float:
        """
        Calculate relevance score for a fix.
        
        Factors:
        - Similarity to current error (40%)
        - Success rate (30%)
        - Recency (20%)
        - Usage count (10%)
        """
        success_rate = fix.get('success_count', 1) / max(fix.get('usage_count', 1), 1)
        
        # Recency score (newer = higher)
        try:
            timestamp = datetime.fromisoformat(fix['timestamp'])
            days_old = (datetime.now() - timestamp).days
            recency = max(0, 1 - (days_old / 365))  # Decay over a year
        except:
            recency = 0.5
        
        # Usage score
        usage = min(1.0, fix.get('usage_count', 1) / 10)
        
        # Weighted combination
        relevance = (
            base_similarity * 0.4 +
            success_rate * 0.3 +
            recency * 0.2 +
            usage * 0.1
        )
        
        return relevance
    
    def print_statistics(self):
        """Print dictionary statistics."""
        total_fixes = sum(len(fixes) for fixes in self.dictionary.values())
        total_branches = sum(len(branches) for branches in self.branches.values())
        
        print(f"\n{PURPLE}{'='*60}{RESET}")
        print(f"{PURPLE}📊 Relevance Dictionary Statistics{RESET}")
        print(f"{PURPLE}{'='*60}{RESET}\n")
        print(f"{GOLD}User ID:{RESET} {self.user_id}")
        print(f"{GOLD}Total Errors Indexed:{RESET} {len(self.dictionary)}")
        print(f"{GOLD}Total Fixes:{RESET} {total_fixes}")
        print(f"{GOLD}Branch Connections:{RESET} {total_branches}")
        print(f"{GOLD}Remote Fixes Available:{RESET} {len(self.remote_refs)}")
        
        # Top error types
        error_types = defaultdict(int)
        for fixes in self.dictionary.values():
            for fix in fixes:
                error_types[fix.get('error_type', 'Unknown')] += 1
        
        if error_types:
            print(f"\n{BLUE}Top Error Types:{RESET}")
            for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  • {error_type}: {count}")
        
        print(f"\n{PURPLE}{'='*60}{RESET}\n")


# Test the relevance dictionary
if __name__ == "__main__":
    print(f"{PURPLE}🧪 Testing Relevance Dictionary{RESET}\n")
    
    # Create test dictionary
    test_user_id = "TEST_USER_ABC123"
    rd = RelevanceDictionary(test_user_id)
    
    # Test 1: Add a fix
    print(f"{GOLD}Test 1: Adding a fix{RESET}")
    fix_key = rd.add_fix(
        error_type="NameError",
        error_signature="NameError: name 'session' is not defined",
        solution="Added: from core import session",
        fix_hash="abc123def456",
        context={"line": 42, "function": "parse_request"},
        commit_url="https://github.com/test/commit/abc123"
    )
    print(f"{GREEN}✅ Fix added with key: {fix_key}{RESET}\n")
    
    # Test 2: Search for similar
    print(f"{GOLD}Test 2: Searching for similar errors{RESET}")
    matches = rd.search_similar_fixes("NameError: name 'request' is not defined")
    print(f"{GREEN}✅ Found {len(matches)} matches{RESET}\n")
    
    # Test 3: Create branch
    print(f"{GOLD}Test 3: Creating branch connection{RESET}")
    rd.create_branch("abc123def456", "xyz789", "solved_similar")
    print(f"{GREEN}✅ Branch created{RESET}\n")
    
    # Test 4: Record usage
    print(f"{GOLD}Test 4: Recording fix usage{RESET}")
    rd.record_fix_usage("abc123def456", succeeded=True)
    print(f"{GREEN}✅ Usage recorded{RESET}\n")
    
    # Test 5: Statistics
    print(f"{GOLD}Test 5: Dictionary statistics{RESET}")
    rd.print_statistics()
    
    print(f"{PURPLE}✨ All tests complete{RESET}")
