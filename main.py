#!/usr/bin/env python3

import json
import uuid
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from mcp.server.fastmcp import FastMCP, Context

@dataclass
class Thought:
    id: str
    content: str
    number: int
    total_estimated: int
    timestamp: str
    dependencies: List[str]
    contradictions: List[str]
    confidence: float
    branch_id: Optional[str] = None
    revision_of: Optional[str] = None
    is_checkpoint: bool = False
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class Branch:
    id: str
    name: str
    created_from: str
    purpose: str
    thoughts: List[str]
    merged: bool = False
    merge_target: Optional[str] = None

@dataclass
class ThinkingSession:
    id: str
    problem_statement: str
    success_criteria: str
    constraints: List[str]
    main_thread: List[str]
    branches: Dict[str, Branch]
    patterns: List[str]
    started: str
    last_updated: str

class SequentialThinkingEngine:
    def __init__(self):
        self.thoughts: Dict[str, Thought] = {}
        self.sessions: Dict[str, ThinkingSession] = {}
        self.current_session: Optional[str] = None
        self.patterns: Dict[str, int] = {}
        
    def start_session(self, problem: str, criteria: str, constraints: List[str]) -> str:
        session_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        
        session = ThinkingSession(
            id=session_id,
            problem_statement=problem,
            success_criteria=criteria,
            constraints=constraints,
            main_thread=[],
            branches={},
            patterns=[],
            started=now,
            last_updated=now
        )
        
        self.sessions[session_id] = session
        self.current_session = session_id
        return session_id
    
    def add_thought(self, content: str, dependencies: List[str] = None, 
                   confidence: float = 0.8, branch_id: Optional[str] = None) -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        thought_id = str(uuid.uuid4())[:8]
        session = self.sessions[self.current_session]
        
        if branch_id and branch_id not in session.branches:
            raise ValueError(f"Branch {branch_id} does not exist")
        
        thought_number = len(session.main_thread) + 1 if not branch_id else len(session.branches[branch_id].thoughts) + 1
        
        contradictions = self._detect_contradictions(content, dependencies or [])
        
        thought = Thought(
            id=thought_id,
            content=content,
            number=thought_number,
            total_estimated=max(5, thought_number + 2),
            timestamp=datetime.now().isoformat(),
            dependencies=dependencies or [],
            contradictions=contradictions,
            confidence=confidence,
            branch_id=branch_id
        )
        
        self.thoughts[thought_id] = thought
        
        if branch_id:
            session.branches[branch_id].thoughts.append(thought_id)
        else:
            session.main_thread.append(thought_id)
        
        session.last_updated = datetime.now().isoformat()
        
        self._update_patterns(content)
        return thought_id
    
    def revise_thought(self, original_id: str, new_content: str, confidence: float = 0.8) -> str:
        if original_id not in self.thoughts:
            raise ValueError("Original thought not found")
        
        original = self.thoughts[original_id]
        revised_id = str(uuid.uuid4())[:8]
        
        revised = Thought(
            id=revised_id,
            content=new_content,
            number=original.number,
            total_estimated=original.total_estimated,
            timestamp=datetime.now().isoformat(),
            dependencies=original.dependencies,
            contradictions=self._detect_contradictions(new_content, original.dependencies),
            confidence=confidence,
            branch_id=original.branch_id,
            revision_of=original_id
        )
        
        self.thoughts[revised_id] = revised
        
        session = self.sessions[self.current_session]
        if original.branch_id:
            branch_thoughts = session.branches[original.branch_id].thoughts
            idx = branch_thoughts.index(original_id)
            branch_thoughts[idx] = revised_id
        else:
            idx = session.main_thread.index(original_id)
            session.main_thread[idx] = revised_id
        
        return revised_id
    
    def create_branch(self, name: str, from_thought: str, purpose: str) -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        branch_id = str(uuid.uuid4())[:8]
        session = self.sessions[self.current_session]
        
        branch = Branch(
            id=branch_id,
            name=name,
            created_from=from_thought,
            purpose=purpose,
            thoughts=[]
        )
        
        session.branches[branch_id] = branch
        return branch_id
    
    def merge_branch(self, branch_id: str, target_thought: Optional[str] = None) -> List[str]:
        if not self.current_session:
            raise ValueError("No active session")
        
        session = self.sessions[self.current_session]
        if branch_id not in session.branches:
            raise ValueError("Branch not found")
        
        branch = session.branches[branch_id]
        merged_thoughts = []
        
        for thought_id in branch.thoughts:
            thought = self.thoughts[thought_id]
            thought.branch_id = None
            session.main_thread.append(thought_id)
            merged_thoughts.append(thought_id)
        
        branch.merged = True
        branch.merge_target = target_thought
        
        return merged_thoughts
    
    def _detect_contradictions(self, content: str, dependencies: List[str]) -> List[str]:
        contradictions = []
        content_lower = content.lower()
        
        negative_indicators = ["not", "false", "incorrect", "wrong", "impossible"]
        positive_indicators = ["true", "correct", "right", "possible", "valid"]
        
        for dep_id in dependencies:
            if dep_id in self.thoughts:
                dep_content = self.thoughts[dep_id].content.lower()
                
                content_negative = any(word in content_lower for word in negative_indicators)
                dep_positive = any(word in dep_content for word in positive_indicators)
                
                if content_negative and dep_positive:
                    contradictions.append(dep_id)
        
        return contradictions
    
    def _update_patterns(self, content: str):
        words = content.lower().split()
        key_phrases = [
            "first principles", "breaking down", "assumption", "because", "therefore",
            "however", "alternatively", "given that", "it follows", "contradiction"
        ]
        
        for phrase in key_phrases:
            if phrase in content.lower():
                self.patterns[phrase] = self.patterns.get(phrase, 0) + 1
    
    def get_thought_tree(self) -> Dict[str, Any]:
        if not self.current_session:
            return {}
        
        session = self.sessions[self.current_session]
        
        def build_tree(thought_ids: List[str]) -> List[Dict]:
            tree = []
            for tid in thought_ids:
                thought = self.thoughts[tid]
                node = {
                    "id": tid,
                    "content": thought.content,
                    "number": thought.number,
                    "confidence": thought.confidence,
                    "contradictions": len(thought.contradictions) > 0,
                    "revision_of": thought.revision_of,
                    "dependencies": thought.dependencies
                }
                tree.append(node)
            return tree
        
        result = {
            "problem": session.problem_statement,
            "main_thread": build_tree(session.main_thread),
            "branches": {}
        }
        
        for branch_id, branch in session.branches.items():
            result["branches"][branch_id] = {
                "name": branch.name,
                "purpose": branch.purpose,
                "thoughts": build_tree(branch.thoughts),
                "merged": branch.merged
            }
        
        return result
    
    def get_analysis(self) -> Dict[str, Any]:
        if not self.current_session:
            return {}
        
        session = self.sessions[self.current_session]
        all_thoughts = [self.thoughts[tid] for tid in session.main_thread]
        
        for branch in session.branches.values():
            all_thoughts.extend([self.thoughts[tid] for tid in branch.thoughts])
        
        contradictions = sum(1 for t in all_thoughts if t.contradictions)
        avg_confidence = sum(t.confidence for t in all_thoughts) / len(all_thoughts) if all_thoughts else 0
        revisions = sum(1 for t in all_thoughts if t.revision_of)
        
        return {
            "total_thoughts": len(all_thoughts),
            "contradictions_found": contradictions,
            "average_confidence": round(avg_confidence, 2),
            "revisions_made": revisions,
            "branches_created": len(session.branches),
            "patterns_detected": dict(self.patterns),
            "thinking_quality": self._assess_quality()
        }
    
    def _assess_quality(self) -> str:
        if not self.current_session:
            return "unknown"
        
        session = self.sessions[self.current_session]
        total_thoughts = len(session.main_thread)
        
        if total_thoughts < 3:
            return "insufficient"
        elif total_thoughts < 7:
            return "basic"
        elif len(session.branches) > 0:
            return "advanced"
        else:
            return "good"

mcp = FastMCP("Enhanced Sequential Thinking")
engine = SequentialThinkingEngine()

@mcp.tool()
def start_thinking_session(problem: str, success_criteria: str, constraints: str = "", ctx: Context = None) -> str:
    constraint_list = [c.strip() for c in constraints.split(",") if c.strip()] if constraints else []
    session_id = engine.start_session(problem, success_criteria, constraint_list)
    return f"Started thinking session {session_id} for: {problem}"

@mcp.tool()
def add_thought(content: str, dependencies: str = "", confidence: float = 0.8, 
               branch_id: str = "", ctx: Context = None) -> str:
    dep_list = [d.strip() for d in dependencies.split(",") if d.strip()] if dependencies else []
    branch = branch_id if branch_id else None
    
    thought_id = engine.add_thought(content, dep_list, confidence, branch)
    thought = engine.thoughts[thought_id]
    
    result = f"Added thought {thought_id}: {content[:50]}..."
    if thought.contradictions:
        result += f" WARNING: Contradicts: {', '.join(thought.contradictions)}"
    
    return result

@mcp.tool()
def revise_thought(thought_id: str, new_content: str, confidence: float = 0.8, ctx: Context = None) -> str:
    revised_id = engine.revise_thought(thought_id, new_content, confidence)
    return f"Revised {thought_id} -> {revised_id}: {new_content[:50]}..."

@mcp.tool()
def create_branch(name: str, from_thought: str, purpose: str, ctx: Context = None) -> str:
    branch_id = engine.create_branch(name, from_thought, purpose)
    return f"Created branch {branch_id} '{name}' from {from_thought}: {purpose}"

@mcp.tool()
def merge_branch(branch_id: str, target_thought: str = "", ctx: Context = None) -> str:
    target = target_thought if target_thought else None
    merged = engine.merge_branch(branch_id, target)
    return f"Merged branch {branch_id}: {len(merged)} thoughts integrated"

@mcp.tool()
def analyze_thinking(ctx: Context = None) -> str:
    analysis = engine.get_analysis()
    return json.dumps(analysis, indent=2)

@mcp.resource("thinking://tree")
def get_thought_tree() -> str:
    tree = engine.get_thought_tree()
    return json.dumps(tree, indent=2)

@mcp.resource("thinking://analysis")
def get_analysis() -> str:
    analysis = engine.get_analysis()
    return json.dumps(analysis, indent=2)

@mcp.resource("thinking://patterns")
def get_patterns() -> str:
    return json.dumps(engine.patterns, indent=2)

@mcp.prompt()
def thinking_guide() -> str:
    return """Sequential Thinking Process:

1. start_thinking_session(problem, success_criteria, constraints)
2. add_thought(content, dependencies, confidence, branch_id)
3. revise_thought(thought_id, new_content, confidence) 
4. create_branch(name, from_thought, purpose)
5. merge_branch(branch_id, target_thought)
6. analyze_thinking()

Resources:
- thinking://tree - Complete thought structure
- thinking://analysis - Quality metrics  
- thinking://patterns - Learning insights

Best Practices:
- Start with problem decomposition
- Build logical dependencies
- Create branches for alternatives
- Revise when new insights emerge
- Analyze before concluding"""

def main():
    mcp.run()

if __name__ == "__main__":
    main()