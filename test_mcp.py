#!/usr/bin/env python3
"""
Test script to demonstrate Sequential Thinking MCP usage
"""
import json
from main import engine

def test_sequential_thinking():
    print("=== Sequential Thinking MCP Test ===\n")
    
    # 1. Start a thinking session
    print("1. Starting thinking session...")
    session_id = engine.start_session(
        problem="How to build a recommendation system?",
        criteria="Scalable system with <100ms response time",
        constraints=["Limited to open source tools", "$1000 budget"]
    )
    print(f"Started session: {session_id}\n")
    
    # 2. Add initial thoughts
    print("2. Adding initial thoughts...")
    thought1_id = engine.add_thought(
        content="First principle: recommendations match user preferences based on behavior patterns",
        confidence=0.9
    )
    print(f"Added thought: {thought1_id}")
    
    thought2_id = engine.add_thought(
        content="Need to collect user interaction data: clicks, purchases, time spent",
        dependencies=[thought1_id],
        confidence=0.8
    )
    print(f"Added thought: {thought2_id}")
    
    thought3_id = engine.add_thought(
        content="This approach is wrong - users don't always follow patterns",
        dependencies=[thought1_id],
        confidence=0.7
    )
    print(f"Added thought with contradiction: {thought3_id}\n")
    
    # 3. Create a branch for alternative approach
    print("3. Creating branch for alternative approach...")
    branch_id = engine.create_branch(
        name="collaborative_filtering",
        from_thought=thought2_id,
        purpose="Explore user-user similarity approach"
    )
    print(f"Created branch: {branch_id}")
    
    branch_thought_id = engine.add_thought(
        content="Calculate user similarity using cosine similarity on interaction vectors",
        branch_id=branch_id,
        confidence=0.7
    )
    print(f"Added branch thought: {branch_thought_id}\n")
    
    # 4. Get thought tree
    print("4. Getting thought tree...")
    tree = engine.get_thought_tree()
    print(json.dumps(tree, indent=2))
    print()
    
    # 5. Analyze thinking quality
    print("5. Analyzing thinking quality...")
    analysis = engine.get_analysis()
    print(json.dumps(analysis, indent=2))
    print()
    
    # 6. Show patterns detected
    print("6. Patterns detected:")
    print(json.dumps(engine.patterns, indent=2))

if __name__ == "__main__":
    test_sequential_thinking()