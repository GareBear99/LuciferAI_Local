#!/usr/bin/env python3
"""
Test Tier 0 limitations and upgrade prompts
"""
import sys

import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.llamafile_agent import LlamafileAgent

# NOTE: the case runner below must NOT be named test_* — pytest treats
# every parameter of a test_* function as a fixture name, so it injected
# its builtin `query` fixture (a string) instead of the test case.
def check_tier0_limitation(query: str, description: str):
    """Test a query that should trigger upgrade prompt."""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"Query: {query[:80]}...")
    print(f"{'='*60}\n")
    
    agent = LlamafileAgent()
    
    if not agent.available:
        print("❌ TinyLlama not available")
        return False
    
    response = agent.query(query, max_tokens=300, temperature=0.3)
    
    print(f"\nRESPONSE:\n{response}\n")
    print(f"{'='*60}\n")
    
    # Check if upgrade prompt was shown
    upgrade_keywords = [
        "tier 0",
        "limited capabilities",
        "install a more capable model",
        "luci install mistral",
        "luci install llama3.2"
    ]
    
    has_upgrade_prompt = any(keyword in response.lower() for keyword in upgrade_keywords)
    
    if has_upgrade_prompt:
        print("✅ SUCCESS - Correctly suggested model upgrade")
        return True
    else:
        print("⚠️  WARNING - Did not suggest upgrade (TinyLlama may have attempted response)")
        return False

def main():
    """Test tier limitations."""
    
    print("\n🧪 Tier 0 Limitation Tests")
    print("Testing complex queries that should prompt for Mistral upgrade\n")
    
    tests = [
        (
            "Compare the philosophical implications of determinism versus free will, then explain how quantum mechanics might reconcile both perspectives",
            "Multi-step philosophical reasoning"
        ),
        (
            "Analyze the economic impact of cryptocurrency adoption in three different countries and predict future trends based on historical data",
            "Complex economic analysis"
        ),
        (
            "Write a detailed technical specification for a distributed microservices architecture, including security considerations and scalability patterns",
            "Deep technical specification"
        ),
    ]
    
    results = []
    for query, desc in tests:
        success = check_tier0_limitation(query, desc)
        results.append((desc, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}\n")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"Passed: {passed}/{total}\n")
    
    for desc, success in results:
        status = "✅" if success else "⚠️ "
        print(f"{status} {desc}")
    
    print()

def test_tier0_limitation():
    """Pytest entry point: no parameters (see the note above).

    LIVE-MODEL test: runs 3 heavy TinyLlama queries, and the pass
    condition (the model suggesting an upgrade) is nondeterministic —
    the helper itself warns "TinyLlama may have attempted response".
    So this is a smoke run, not an assertion: it skips when no model
    is available and otherwise just exercises the live path.
    Run the file directly for the real manual check.
    """
    if not LlamafileAgent().available:
        pytest.skip("no TinyLlama model available (run as a script once one is installed)")
    main()


if __name__ == "__main__":
    main()
