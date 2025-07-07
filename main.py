#!/usr/bin/env python3

import json
import uuid
import asyncio
import weakref
from typing import Dict, List, Optional, Any, Set, Protocol, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from mcp.server.fastmcp import FastMCP, Context

@dataclass
class PatternResult:
    pattern: str
    confidence: float
    fallback_used: bool = False
    strategy: str = "keyword"

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
    pattern_results: List[PatternResult] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.pattern_results is None:
            self.pattern_results = []

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
class SessionConfig:
    max_thoughts: int = 1000
    max_branches: int = 50
    memory_limit_mb: int = 100
    auto_cleanup: bool = True
    pattern_confidence_threshold: float = 0.6

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
    config: SessionConfig = None
    memory_usage: int = 0
    
    def __post_init__(self):
        if self.config is None:
            self.config = SessionConfig()

class PatternDetector(Protocol):
    def detect_patterns(self, content: str) -> List[PatternResult]:
        ...

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, Any] = {}
        self.pattern_detectors: List[PatternDetector] = []
    
    def register_plugin(self, name: str, plugin: Any):
        self.plugins[name] = plugin
    
    def register_pattern_detector(self, detector: PatternDetector):
        self.pattern_detectors.append(detector)
    
    def get_pattern_results(self, content: str) -> List[PatternResult]:
        results = []
        for detector in self.pattern_detectors:
            try:
                results.extend(detector.detect_patterns(content))
            except Exception:
                pass
        return results

class KeywordPatternDetector:
    def __init__(self):
        self.patterns = {
            "first principles": ["first principles", "breaking down", "fundamental"],
            "assumption": ["assumption", "assume", "given that"],
            "contradiction": ["contradiction", "however", "but", "alternatively"],
            "conclusion": ["therefore", "thus", "it follows", "consequently"]
        }
    
    def detect_patterns(self, content: str) -> List[PatternResult]:
        results = []
        content_lower = content.lower()
        
        for pattern_name, keywords in self.patterns.items():
            confidence = 0.0
            for keyword in keywords:
                if keyword in content_lower:
                    confidence = max(confidence, 0.8)
            
            if confidence > 0:
                results.append(PatternResult(
                    pattern=pattern_name,
                    confidence=confidence,
                    strategy="keyword"
                ))
        
        return results

class FallbackPatternDetector:
    def detect_patterns(self, content: str) -> List[PatternResult]:
        results = []
        if len(content) > 50:
            results.append(PatternResult(
                pattern="detailed_analysis",
                confidence=0.5,
                fallback_used=True,
                strategy="fallback"
            ))
        return results

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, ThinkingSession] = {}
        self.session_refs: Dict[str, weakref.ref] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def create_session(self, problem: str, criteria: str, constraints: List[str]) -> str:
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
        return session_id
    
    def get_session(self, session_id: str) -> Optional[ThinkingSession]:
        return self.sessions.get(session_id)
    
    def cleanup_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.session_refs:
            del self.session_refs[session_id]
    
    def check_memory_limits(self, session_id: str) -> bool:
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        thought_count = len(session.main_thread)
        for branch in session.branches.values():
            thought_count += len(branch.thoughts)
        
        if thought_count > session.config.max_thoughts:
            return False
        
        return True

class MCPCompatibilityLayer:
    def __init__(self):
        self.supported_versions = ["1.0", "1.1", "1.6"]
        self.client_version = "1.6"
        self.capabilities = {
            "tools": True,
            "resources": True,
            "prompts": True,
            "streaming": False
        }
    
    def detect_client_version(self, context: Optional[Context] = None) -> str:
        return self.client_version
    
    def negotiate_capabilities(self, client_caps: Dict[str, Any]) -> Dict[str, Any]:
        negotiated = {}
        for cap, supported in self.capabilities.items():
            negotiated[cap] = supported and client_caps.get(cap, False)
        return negotiated
    
    def adapt_response(self, response: Any, version: str) -> Any:
        if version in ["1.0", "1.1"]:
            if isinstance(response, dict) and "metadata" in response:
                response = {k: v for k, v in response.items() if k != "metadata"}
        return response

class SequentialThinkingEngine:
    def __init__(self):
        self.thoughts: Dict[str, Thought] = {}
        self.session_manager = SessionManager()
        self.plugin_manager = PluginManager()
        self.compatibility_layer = MCPCompatibilityLayer()
        self.current_session: Optional[str] = None
        self.patterns: Dict[str, int] = {}
        
        self.plugin_manager.register_pattern_detector(KeywordPatternDetector())
        self.plugin_manager.register_pattern_detector(FallbackPatternDetector())
        
    def start_session(self, problem: str, criteria: str, constraints: List[str]) -> str:
        session_id = self.session_manager.create_session(problem, criteria, constraints)
        self.current_session = session_id
        return session_id
    
    async def add_thought(self, content: str, dependencies: List[str] = None, 
                          confidence: float = 0.8, branch_id: Optional[str] = None) -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        session = self.session_manager.get_session(self.current_session)
        if not session:
            raise ValueError("Session not found")
        
        if not self.session_manager.check_memory_limits(self.current_session):
            raise ValueError("Session memory limit exceeded")
        
        if branch_id and branch_id not in session.branches:
            raise ValueError(f"Branch {branch_id} does not exist")
        
        thought_id = str(uuid.uuid4())[:8]
        thought_number = len(session.main_thread) + 1 if not branch_id else len(session.branches[branch_id].thoughts) + 1
        
        contradictions = await self._detect_contradictions_async(content, dependencies or [])
        pattern_results = self.plugin_manager.get_pattern_results(content)
        
        thought = Thought(
            id=thought_id,
            content=content,
            number=thought_number,
            total_estimated=max(5, thought_number + 2),
            timestamp=datetime.now().isoformat(),
            dependencies=dependencies or [],
            contradictions=contradictions,
            confidence=confidence,
            branch_id=branch_id,
            pattern_results=pattern_results
        )
        
        self.thoughts[thought_id] = thought
        
        if branch_id:
            session.branches[branch_id].thoughts.append(thought_id)
        else:
            session.main_thread.append(thought_id)
        
        session.last_updated = datetime.now().isoformat()
        
        await self._update_patterns_async(pattern_results)
        return thought_id
    
    async def revise_thought(self, original_id: str, new_content: str, confidence: float = 0.8) -> str:
        if original_id not in self.thoughts:
            raise ValueError("Original thought not found")
        
        original = self.thoughts[original_id]
        revised_id = str(uuid.uuid4())[:8]
        
        contradictions = await self._detect_contradictions_async(new_content, original.dependencies)
        pattern_results = self.plugin_manager.get_pattern_results(new_content)
        
        revised = Thought(
            id=revised_id,
            content=new_content,
            number=original.number,
            total_estimated=original.total_estimated,
            timestamp=datetime.now().isoformat(),
            dependencies=original.dependencies,
            contradictions=contradictions,
            confidence=confidence,
            branch_id=original.branch_id,
            revision_of=original_id,
            pattern_results=pattern_results
        )
        
        self.thoughts[revised_id] = revised
        
        session = self.session_manager.get_session(self.current_session)
        if original.branch_id:
            branch_thoughts = session.branches[original.branch_id].thoughts
            idx = branch_thoughts.index(original_id)
            branch_thoughts[idx] = revised_id
        else:
            idx = session.main_thread.index(original_id)
            session.main_thread[idx] = revised_id
        
        await self._update_patterns_async(pattern_results)
        return revised_id
    
    def create_branch(self, name: str, from_thought: str, purpose: str) -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        session = self.session_manager.get_session(self.current_session)
        if not session:
            raise ValueError("Session not found")
        
        if len(session.branches) >= session.config.max_branches:
            raise ValueError("Maximum branches exceeded")
        
        branch_id = str(uuid.uuid4())[:8]
        
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
        
        session = self.session_manager.get_session(self.current_session)
        if not session or branch_id not in session.branches:
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
    
    async def _detect_contradictions_async(self, content: str, dependencies: List[str]) -> List[str]:
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
    
    async def _update_patterns_async(self, pattern_results: List[PatternResult]):
        for result in pattern_results:
            if result.confidence >= 0.6:
                self.patterns[result.pattern] = self.patterns.get(result.pattern, 0) + 1
    
    def get_thought_tree(self) -> Dict[str, Any]:
        if not self.current_session:
            return {}
        
        session = self.session_manager.get_session(self.current_session)
        if not session:
            return {}
        
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
                    "dependencies": thought.dependencies,
                    "pattern_results": [asdict(pr) for pr in thought.pattern_results]
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
        
        session = self.session_manager.get_session(self.current_session)
        if not session:
            return {}
        
        all_thoughts = [self.thoughts[tid] for tid in session.main_thread]
        
        for branch in session.branches.values():
            all_thoughts.extend([self.thoughts[tid] for tid in branch.thoughts])
        
        contradictions = sum(1 for t in all_thoughts if t.contradictions)
        avg_confidence = sum(t.confidence for t in all_thoughts) / len(all_thoughts) if all_thoughts else 0
        revisions = sum(1 for t in all_thoughts if t.revision_of)
        
        pattern_quality = self._assess_pattern_quality(all_thoughts)
        
        return {
            "total_thoughts": len(all_thoughts),
            "contradictions_found": contradictions,
            "average_confidence": round(avg_confidence, 2),
            "revisions_made": revisions,
            "branches_created": len(session.branches),
            "patterns_detected": dict(self.patterns),
            "thinking_quality": self._assess_quality(),
            "pattern_quality": pattern_quality,
            "memory_usage": session.memory_usage
        }
    
    def _assess_quality(self) -> str:
        if not self.current_session:
            return "unknown"
        
        session = self.session_manager.get_session(self.current_session)
        if not session:
            return "unknown"
        
        total_thoughts = len(session.main_thread)
        
        if total_thoughts < 3:
            return "insufficient"
        elif total_thoughts < 7:
            return "basic"
        elif len(session.branches) > 0:
            return "advanced"
        else:
            return "good"
    
    def _assess_pattern_quality(self, thoughts: List[Thought]) -> Dict[str, Any]:
        if not thoughts:
            return {"quality": "unknown", "confidence_avg": 0.0}
        
        total_confidence = 0.0
        pattern_count = 0
        fallback_count = 0
        
        for thought in thoughts:
            for pattern in thought.pattern_results:
                total_confidence += pattern.confidence
                pattern_count += 1
                if pattern.fallback_used:
                    fallback_count += 1
        
        avg_confidence = total_confidence / pattern_count if pattern_count > 0 else 0.0
        fallback_ratio = fallback_count / pattern_count if pattern_count > 0 else 0.0
        
        quality = "high" if avg_confidence > 0.8 else "medium" if avg_confidence > 0.6 else "low"
        
        return {
            "quality": quality,
            "confidence_avg": round(avg_confidence, 2),
            "fallback_ratio": round(fallback_ratio, 2),
            "pattern_count": pattern_count
        }

mcp = FastMCP("Enhanced Sequential Thinking")
engine = SequentialThinkingEngine()

@mcp.tool()
def start_thinking_session(problem: str, success_criteria: str, constraints: str = "", ctx: Context = None) -> str:
    constraint_list = [c.strip() for c in constraints.split(",") if c.strip()] if constraints else []
    client_version = engine.compatibility_layer.detect_client_version(ctx)
    session_id = engine.start_session(problem, success_criteria, constraint_list)
    response = f"Started thinking session {session_id} for: {problem}"
    return engine.compatibility_layer.adapt_response(response, client_version)

@mcp.tool()
async def add_thought(content: str, dependencies: str = "", confidence: float = 0.8, 
                     branch_id: str = "", ctx: Context = None) -> str:
    dep_list = [d.strip() for d in dependencies.split(",") if d.strip()] if dependencies else []
    branch = branch_id if branch_id else None
    
    try:
        thought_id = await engine.add_thought(content, dep_list, confidence, branch)
        thought = engine.thoughts[thought_id]
        
        result = f"Added thought {thought_id}: {content[:50]}..."
        if thought.contradictions:
            result += f" WARNING: Contradicts: {', '.join(thought.contradictions)}"
        
        pattern_info = ""
        high_conf_patterns = [pr for pr in thought.pattern_results if pr.confidence > 0.8]
        if high_conf_patterns:
            pattern_info = f" Patterns: {', '.join(pr.pattern for pr in high_conf_patterns)}"
        
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        return engine.compatibility_layer.adapt_response(result + pattern_info, client_version)
    except Exception as e:
        return f"Error adding thought: {str(e)}"

@mcp.tool()
async def revise_thought(thought_id: str, new_content: str, confidence: float = 0.8, ctx: Context = None) -> str:
    try:
        revised_id = await engine.revise_thought(thought_id, new_content, confidence)
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        response = f"Revised {thought_id} -> {revised_id}: {new_content[:50]}..."
        return engine.compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error revising thought: {str(e)}"

@mcp.tool()
def create_branch(name: str, from_thought: str, purpose: str, ctx: Context = None) -> str:
    try:
        branch_id = engine.create_branch(name, from_thought, purpose)
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        response = f"Created branch {branch_id} '{name}' from {from_thought}: {purpose}"
        return engine.compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error creating branch: {str(e)}"

@mcp.tool()
def merge_branch(branch_id: str, target_thought: str = "", ctx: Context = None) -> str:
    try:
        target = target_thought if target_thought else None
        merged = engine.merge_branch(branch_id, target)
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        response = f"Merged branch {branch_id}: {len(merged)} thoughts integrated"
        return engine.compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error merging branch: {str(e)}"

@mcp.tool()
def analyze_thinking(ctx: Context = None) -> str:
    try:
        analysis = engine.get_analysis()
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        response = json.dumps(analysis, indent=2)
        return engine.compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error analyzing thinking: {str(e)}"

@mcp.resource("thinking://tree")
def get_thought_tree() -> str:
    try:
        tree = engine.get_thought_tree()
        return json.dumps(tree, indent=2)
    except Exception as e:
        return f"Error getting thought tree: {str(e)}"

@mcp.resource("thinking://analysis")
def get_analysis() -> str:
    try:
        analysis = engine.get_analysis()
        return json.dumps(analysis, indent=2)
    except Exception as e:
        return f"Error getting analysis: {str(e)}"

@mcp.resource("thinking://patterns")
def get_patterns() -> str:
    try:
        return json.dumps(engine.patterns, indent=2)
    except Exception as e:
        return f"Error getting patterns: {str(e)}"

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
    try:
        mcp.run()
    except Exception as e:
        print(f"Error running MCP server: {str(e)}")
        raise

if __name__ == "__main__":
    main()