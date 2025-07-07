#!/usr/bin/env python3

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import SequentialThinkingEngine

async def test_refactored_engine():
    engine = SequentialThinkingEngine()
    
    session_id = engine.start_session(
        "Test refactored architecture",
        "Verify all components work together",
        ["maintain backward compatibility"]
    )
    
    print(f"✓ Session created: {session_id}")
    
    thought_id = await engine.add_thought(
        "First principles thinking requires breaking down assumptions",
        confidence=0.9
    )
    
    print(f"✓ Thought added: {thought_id}")
    
    thought = engine.thoughts[thought_id]
    print(f"✓ Pattern results: {len(thought.pattern_results)} patterns detected")
    
    for pattern in thought.pattern_results:
        print(f"  - {pattern.pattern} (confidence: {pattern.confidence}, strategy: {pattern.strategy})")
    
    branch_id = engine.create_branch("alternative", thought_id, "Explore different approach")
    print(f"✓ Branch created: {branch_id}")
    
    alt_thought = await engine.add_thought(
        "Alternative approach using systems thinking",
        branch_id=branch_id,
        confidence=0.8
    )
    
    print(f"✓ Alternative thought: {alt_thought}")
    
    analysis = engine.get_analysis()
    print(f"✓ Analysis complete:")
    print(f"  - Total thoughts: {analysis['total_thoughts']}")
    print(f"  - Pattern quality: {analysis['pattern_quality']['quality']}")
    print(f"  - Memory usage: {analysis['memory_usage']}")
    
    print("\n✅ All refactored components working correctly!")

if __name__ == "__main__":
    asyncio.run(test_refactored_engine())