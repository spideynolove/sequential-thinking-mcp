#!/usr/bin/env python3

import json
import uuid
import subprocess
import os
import re
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
class PackageInfo:
    name: str
    version: str
    description: str
    installed: bool = False
    relevance_score: float = 0.0
    integration_examples: List[str] = None
    api_methods: List[str] = None
    
    def __post_init__(self):
        if self.integration_examples is None:
            self.integration_examples = []
        if self.api_methods is None:
            self.api_methods = []

@dataclass
class ArchitectureDecision:
    id: str
    title: str
    context: str
    options_considered: List[str]
    chosen_option: str
    rationale: str
    consequences: str
    package_dependencies: List[str]
    thinking_session_id: str
    timestamp: str
    status: str = "active"  # active, superseded, deprecated

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
    packages_explored: List[PackageInfo] = None
    architecture_decisions: List[str] = None
    coding_context: bool = False

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.pattern_results is None:
            self.pattern_results = []
        if self.packages_explored is None:
            self.packages_explored = []
        if self.architecture_decisions is None:
            self.architecture_decisions = []

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
    coding_session: bool = False
    package_registry: Dict[str, PackageInfo] = None
    architecture_decisions: Dict[str, ArchitectureDecision] = None
    codebase_context: Optional[str] = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = SessionConfig()
        if self.package_registry is None:
            self.package_registry = {}
        if self.architecture_decisions is None:
            self.architecture_decisions = {}

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

class CodingPatternDetector:
    def __init__(self):
        self.coding_patterns = {
            "package_needed": ["import", "install", "dependency", "library", "framework"],
            "api_exploration": ["api", "method", "function", "endpoint", "interface"],
            "code_reinvention": ["implement", "write", "create", "build", "develop"],
            "integration_planning": ["integrate", "connect", "combine", "merge", "link"],
            "architecture_decision": ["choose", "select", "decide", "architecture", "design"]
        }
    
    def detect_patterns(self, content: str) -> List[PatternResult]:
        results = []
        content_lower = content.lower()
        
        for pattern_name, keywords in self.coding_patterns.items():
            confidence = 0.0
            matched_keywords = []
            
            for keyword in keywords:
                if keyword in content_lower:
                    confidence = max(confidence, 0.7)
                    matched_keywords.append(keyword)
            
            if confidence > 0:
                results.append(PatternResult(
                    pattern=pattern_name,
                    confidence=confidence + (0.1 * len(matched_keywords)),
                    strategy="coding_keyword"
                ))
        
        return results

class PackageDiscoveryEngine:
    def __init__(self):
        self.package_cache: Dict[str, List[PackageInfo]] = {}
        self.discovery_sources = ["pip", "conda", "local"]
    
    def discover_packages(self, task_description: str, language: str = "python") -> List[PackageInfo]:
        cache_key = f"{task_description}:{language}"
        if cache_key in self.package_cache:
            return self.package_cache[cache_key]
        
        packages = []
        
        # Search installed packages
        packages.extend(self._search_installed_packages(task_description))
        
        # Search PyPI for Python packages
        if language == "python":
            packages.extend(self._search_pypi(task_description))
        
        # Rank packages by relevance
        ranked_packages = self._rank_packages(packages, task_description)
        
        self.package_cache[cache_key] = ranked_packages
        return ranked_packages
    
    def _search_installed_packages(self, task_description: str) -> List[PackageInfo]:
        packages = []
        keywords = task_description.lower().split()
        
        try:
            result = subprocess.run(["pip", "list", "--format=json"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                installed_packages = json.loads(result.stdout)
                for pkg in installed_packages:
                    relevance = self._calculate_relevance(pkg["name"], keywords)
                    if relevance > 0.3:
                        packages.append(PackageInfo(
                            name=pkg["name"],
                            version=pkg["version"],
                            description=f"Installed package: {pkg['name']}",
                            installed=True,
                            relevance_score=relevance
                        ))
        except (subprocess.TimeoutExpired, json.JSONDecodeError):
            pass
        
        return packages
    
    def _search_pypi(self, task_description: str) -> List[PackageInfo]:
        # Simplified PyPI search - in production, use PyPI API
        common_packages = {
            "requests": "HTTP library for Python",
            "pandas": "Data manipulation and analysis library",
            "numpy": "Numerical computing library",
            "matplotlib": "Plotting library",
            "flask": "Web framework",
            "django": "Web framework",
            "pytest": "Testing framework",
            "sqlalchemy": "Database toolkit",
            "scikit-learn": "Machine learning library",
            "tensorflow": "Machine learning framework"
        }
        
        packages = []
        keywords = task_description.lower().split()
        
        for name, desc in common_packages.items():
            relevance = self._calculate_relevance(name + " " + desc, keywords)
            if relevance > 0.2:
                packages.append(PackageInfo(
                    name=name,
                    version="latest",
                    description=desc,
                    installed=False,
                    relevance_score=relevance
                ))
        
        return packages
    
    def _calculate_relevance(self, text: str, keywords: List[str]) -> float:
        text_lower = text.lower()
        matches = sum(1 for keyword in keywords if keyword in text_lower)
        return matches / len(keywords) if keywords else 0.0
    
    def _rank_packages(self, packages: List[PackageInfo], task_description: str) -> List[PackageInfo]:
        # Sort by relevance score (descending) and prefer installed packages
        def sort_key(pkg: PackageInfo) -> tuple:
            return (-pkg.relevance_score, not pkg.installed)
        
        return sorted(packages, key=sort_key)

class ArchitectureDecisionTracker:
    def __init__(self):
        self.decisions: Dict[str, ArchitectureDecision] = {}
    
    def record_decision(
        self,
        title: str,
        context: str,
        options_considered: List[str],
        chosen_option: str,
        rationale: str,
        consequences: str,
        package_dependencies: List[str],
        thinking_session_id: str
    ) -> str:
        decision_id = str(uuid.uuid4())[:8]
        
        decision = ArchitectureDecision(
            id=decision_id,
            title=title,
            context=context,
            options_considered=options_considered,
            chosen_option=chosen_option,
            rationale=rationale,
            consequences=consequences,
            package_dependencies=package_dependencies,
            thinking_session_id=thinking_session_id,
            timestamp=datetime.now().isoformat()
        )
        
        self.decisions[decision_id] = decision
        return decision_id
    
    def query_similar_decisions(
        self,
        technology: str = "",
        pattern: str = "",
        package: str = "",
        similarity_threshold: float = 0.7
    ) -> List[ArchitectureDecision]:
        similar_decisions = []
        search_terms = [technology, pattern, package]
        search_text = " ".join(term for term in search_terms if term).lower()
        
        for decision in self.decisions.values():
            decision_text = (decision.title + " " + decision.context + " " + 
                           decision.chosen_option + " " + decision.rationale).lower()
            
            if search_text and search_text in decision_text:
                similar_decisions.append(decision)
        
        return similar_decisions

class CodingWorkflowEngine:
    def __init__(self, thinking_engine: 'SequentialThinkingEngine'):
        self.thinking_engine = thinking_engine
        self.package_discovery = PackageDiscoveryEngine()
        self.architecture_tracker = ArchitectureDecisionTracker()
        self.coding_patterns = CodingPatternDetector()
        self.reinvention_detector = CodeReinventionDetector()
        
        # Register coding pattern detector
        thinking_engine.plugin_manager.register_pattern_detector(self.coding_patterns)
    
    def start_coding_session(
        self,
        problem: str,
        success_criteria: str,
        constraints: List[str],
        codebase_context: str = "",
        package_exploration_required: bool = True
    ) -> str:
        # Create enhanced thinking session for coding
        session_id = self.thinking_engine.start_session(problem, success_criteria, constraints)
        session = self.thinking_engine.session_manager.get_session(session_id)
        
        if session:
            session.coding_session = True
            session.codebase_context = codebase_context
            
            # Force package discovery as first step if required
            if package_exploration_required:
                asyncio.create_task(self._add_package_discovery_thought(session_id, problem))
        
        return session_id
    
    async def _add_package_discovery_thought(self, session_id: str, problem: str):
        # Add mandatory package discovery thought
        original_session = self.thinking_engine.current_session
        self.thinking_engine.current_session = session_id
        
        try:
            await self.thinking_engine.add_thought(
                content=f"MANDATORY: Explore existing packages for: {problem}",
                confidence=0.9
            )
        finally:
            self.thinking_engine.current_session = original_session
    
    def explore_packages(
        self,
        task_description: str,
        language: str = "python",
        thinking_session_id: str = ""
    ) -> List[PackageInfo]:
        packages = self.package_discovery.discover_packages(task_description, language)
        
        # Store results in thinking session if provided
        if thinking_session_id:
            session = self.thinking_engine.session_manager.get_session(thinking_session_id)
            if session:
                for package in packages:
                    session.package_registry[package.name] = package
        
        return packages
    
    def record_architecture_decision(
        self,
        title: str,
        context: str,
        options_considered: List[str],
        chosen_option: str,
        rationale: str,
        consequences: str,
        package_dependencies: List[str],
        thinking_session_id: str
    ) -> str:
        decision_id = self.architecture_tracker.record_decision(
            title, context, options_considered, chosen_option,
            rationale, consequences, package_dependencies, thinking_session_id
        )
        
        # Store in thinking session
        session = self.thinking_engine.session_manager.get_session(thinking_session_id)
        if session:
            session.architecture_decisions[decision_id] = self.architecture_tracker.decisions[decision_id]
        
        return decision_id
    
    def detect_code_reinvention(
        self,
        proposed_code: str,
        existing_packages_checked: List[str],
        confidence_threshold: float = 0.8
    ) -> Dict[str, Any]:
        return self.reinvention_detector.detect_reinvention(
            proposed_code, existing_packages_checked, confidence_threshold
        )

class CodeReinventionDetector:
    def __init__(self):
        self.common_functionality_patterns = {
            "http_requests": ["http", "request", "get", "post", "api", "curl"],
            "data_processing": ["csv", "json", "xml", "parse", "dataframe"],
            "database": ["sql", "database", "query", "orm", "connection"],
            "testing": ["test", "assert", "mock", "unittest", "pytest"],
            "web_framework": ["server", "route", "middleware", "template", "framework"],
            "authentication": ["auth", "login", "token", "jwt", "session", "password"],
            "logging": ["log", "debug", "info", "error", "warning"],
            "datetime": ["date", "time", "datetime", "timestamp", "timezone"]
        }
    
    def detect_reinvention(
        self,
        proposed_code: str,
        existing_packages_checked: List[str],
        confidence_threshold: float = 0.8
    ) -> Dict[str, Any]:
        proposed_lower = proposed_code.lower()
        potential_reinvention = []
        
        for functionality, keywords in self.common_functionality_patterns.items():
            matches = sum(1 for keyword in keywords if keyword in proposed_lower)
            confidence = matches / len(keywords) if keywords else 0.0
            
            if confidence >= confidence_threshold:
                potential_reinvention.append({
                    "functionality": functionality,
                    "confidence": confidence,
                    "keywords_matched": [kw for kw in keywords if kw in proposed_lower]
                })
        
        return {
            "is_potential_reinvention": len(potential_reinvention) > 0,
            "confidence_score": max([pr["confidence"] for pr in potential_reinvention], default=0.0),
            "detected_patterns": potential_reinvention,
            "packages_checked": existing_packages_checked,
            "recommendation": "Explore existing packages before implementing" if potential_reinvention else "Implementation appears novel"
        }

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, ThinkingSession] = {}
        self.session_refs: Dict[str, weakref.ref] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def create_session(self, problem: str, criteria: str, constraints: List[str], coding_session: bool = False) -> str:
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
            last_updated=now,
            coding_session=coding_session
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
        
        # Initialize CodingWorkflowEngine
        self.coding_workflow = CodingWorkflowEngine(self)
        
    def start_session(self, problem: str, criteria: str, constraints: List[str], coding_session: bool = False) -> str:
        session_id = self.session_manager.create_session(problem, criteria, constraints, coding_session)
        self.current_session = session_id
        return session_id
    
    async def add_thought(self, content: str, dependencies: List[str] = None, 
                          confidence: float = 0.8, branch_id: Optional[str] = None, 
                          coding_context: bool = False, packages_explored: List[PackageInfo] = None) -> str:
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
        
        # Enhanced thought with coding context
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
            pattern_results=pattern_results,
            coding_context=coding_context,
            packages_explored=packages_explored or []
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
    
    def _get_coding_patterns(self, thoughts: List[Thought]) -> Dict[str, int]:
        """Helper to extract coding patterns from thoughts."""
        patterns = {}
        for thought in thoughts:
            for pattern_result in thought.pattern_results:
                if pattern_result.strategy == "coding_keyword":
                    patterns[pattern_result.pattern] = patterns.get(pattern_result.pattern, 0) + 1
        return patterns
    
    def _get_package_usage_stats(self, thoughts: List[Thought]) -> Dict[str, int]:
        """Helper to get package usage statistics."""
        package_mentions = {}
        for thought in thoughts:
            for package in thought.packages_explored:
                package_mentions[package.name] = package_mentions.get(package.name, 0) + 1
        return package_mentions

# Cross-system integration interface
class CrossSystemIntegration:
    """Interface for integrating with memory-bank-mcp and other systems."""
    
    def __init__(self, thinking_engine: SequentialThinkingEngine):
        self.thinking_engine = thinking_engine
        self.shared_context = {}
    
    def get_package_context(self, session_id: str) -> Dict[str, Any]:
        """Get package context for sharing with other systems."""
        session = self.thinking_engine.session_manager.get_session(session_id)
        if not session:
            return {}
        
        return {
            "packages": {name: asdict(pkg) for name, pkg in session.package_registry.items()},
            "architecture_decisions": {id: asdict(dec) for id, dec in session.architecture_decisions.items()},
            "coding_session": session.coding_session,
            "last_updated": session.last_updated
        }
    
    def set_external_package_context(self, session_id: str, external_context: Dict[str, Any]):
        """Receive package context from external systems."""
        session = self.thinking_engine.session_manager.get_session(session_id)
        if not session:
            return
        
        # Merge external package information
        if "packages" in external_context:
            for name, pkg_data in external_context["packages"].items():
                if name not in session.package_registry:
                    session.package_registry[name] = PackageInfo(**pkg_data)
        
        # Merge architecture decisions
        if "architecture_decisions" in external_context:
            for dec_id, dec_data in external_context["architecture_decisions"].items():
                if dec_id not in session.architecture_decisions:
                    session.architecture_decisions[dec_id] = ArchitectureDecision(**dec_data)

mcp = FastMCP("Enhanced Sequential Thinking with Coding Integration")
engine = SequentialThinkingEngine()
cross_system = CrossSystemIntegration(engine)

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

# New Coding Workflow MCP Tools

@mcp.tool()
def start_coding_session(
    problem: str,
    success_criteria: str,
    constraints: str = "",
    codebase_context: str = "",
    package_exploration_required: bool = True,
    ctx: Context = None
) -> str:
    """Start a specialized coding session with package discovery and architecture decision tracking."""
    try:
        constraint_list = [c.strip() for c in constraints.split(",") if c.strip()] if constraints else []
        
        session_id = engine.coding_workflow.start_coding_session(
            problem=problem,
            success_criteria=success_criteria,
            constraints=constraint_list,
            codebase_context=codebase_context,
            package_exploration_required=package_exploration_required
        )
        
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        response = f"Started coding session {session_id} for: {problem}"
        
        if package_exploration_required:
            response += "\nPackage exploration enabled - will explore existing solutions first."
        
        return engine.compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error starting coding session: {str(e)}"

@mcp.tool()
def explore_packages(
    task_description: str,
    language: str = "python",
    thinking_session_id: str = "",
    ctx: Context = None
) -> str:
    """Discover and explore existing packages for a given task before writing new code."""
    try:
        session_id = thinking_session_id or engine.current_session
        if not session_id:
            return "Error: No active session. Start a thinking session first."
        
        packages = engine.coding_workflow.explore_packages(
            task_description=task_description,
            language=language,
            thinking_session_id=session_id
        )
        
        if not packages:
            return f"No relevant packages found for: {task_description}"
        
        result = f"Found {len(packages)} relevant packages for: {task_description}\n\n"
        
        for i, pkg in enumerate(packages[:5], 1):  # Show top 5
            status = "✓ Installed" if pkg.installed else "◯ Available"
            result += f"{i}. {pkg.name} ({pkg.version}) - {status}\n"
            result += f"   Description: {pkg.description}\n"
            result += f"   Relevance: {pkg.relevance_score:.2f}\n\n"
        
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        return engine.compatibility_layer.adapt_response(result, client_version)
    except Exception as e:
        return f"Error exploring packages: {str(e)}"

@mcp.tool()
def record_architecture_decision(
    decision_title: str,
    context: str,
    options_considered: str,
    chosen_option: str,
    rationale: str,
    consequences: str,
    package_dependencies: str = "",
    thinking_session_id: str = "",
    ctx: Context = None
) -> str:
    """Record an architecture decision with rationale and consequences."""
    try:
        session_id = thinking_session_id or engine.current_session
        if not session_id:
            return "Error: No active session. Start a thinking session first."
        
        options_list = [opt.strip() for opt in options_considered.split(",") if opt.strip()]
        deps_list = [dep.strip() for dep in package_dependencies.split(",") if dep.strip()] if package_dependencies else []
        
        decision_id = engine.coding_workflow.record_architecture_decision(
            title=decision_title,
            context=context,
            options_considered=options_list,
            chosen_option=chosen_option,
            rationale=rationale,
            consequences=consequences,
            package_dependencies=deps_list,
            thinking_session_id=session_id
        )
        
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        response = f"Recorded architecture decision ADR-{decision_id}: {decision_title}"
        return engine.compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error recording architecture decision: {str(e)}"

@mcp.tool()
def detect_code_reinvention(
    proposed_code: str,
    existing_packages_checked: str = "",
    confidence_threshold: float = 0.8,
    ctx: Context = None
) -> str:
    """Detect if proposed code might be reinventing existing package functionality."""
    try:
        packages_checked = [pkg.strip() for pkg in existing_packages_checked.split(",") if pkg.strip()] if existing_packages_checked else []
        
        result = engine.coding_workflow.detect_code_reinvention(
            proposed_code=proposed_code,
            existing_packages_checked=packages_checked,
            confidence_threshold=confidence_threshold
        )
        
        response = f"Code Reinvention Analysis:\n"
        response += f"Potential Reinvention: {'Yes' if result['is_potential_reinvention'] else 'No'}\n"
        response += f"Confidence Score: {result['confidence_score']:.2f}\n"
        response += f"Recommendation: {result['recommendation']}\n\n"
        
        if result['detected_patterns']:
            response += "Detected Patterns:\n"
            for pattern in result['detected_patterns']:
                response += f"- {pattern['functionality']} (confidence: {pattern['confidence']:.2f})\n"
                response += f"  Keywords: {', '.join(pattern['keywords_matched'])}\n"
        
        if result['packages_checked']:
            response += f"\nPackages Checked: {', '.join(result['packages_checked'])}\n"
        
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        return engine.compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error detecting code reinvention: {str(e)}"

@mcp.tool()
def query_architecture_decisions(
    technology: str = "",
    pattern: str = "",
    package: str = "",
    similarity_threshold: float = 0.7,
    ctx: Context = None
) -> str:
    """Query previous architecture decisions for similar contexts."""
    try:
        decisions = engine.coding_workflow.architecture_tracker.query_similar_decisions(
            technology=technology,
            pattern=pattern,
            package=package,
            similarity_threshold=similarity_threshold
        )
        
        if not decisions:
            return "No similar architecture decisions found."
        
        response = f"Found {len(decisions)} similar architecture decisions:\n\n"
        
        for i, decision in enumerate(decisions, 1):
            response += f"{i}. ADR-{decision.id}: {decision.title}\n"
            response += f"   Context: {decision.context[:100]}...\n"
            response += f"   Chosen: {decision.chosen_option}\n"
            response += f"   Packages: {', '.join(decision.package_dependencies)}\n"
            response += f"   Date: {decision.timestamp}\n\n"
        
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        return engine.compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error querying architecture decisions: {str(e)}"

@mcp.tool()
async def add_coding_thought(
    content: str,
    dependencies: str = "",
    confidence: float = 0.8,
    branch_id: str = "",
    explore_packages: bool = True,
    ctx: Context = None
) -> str:
    """Add a thought with coding context and optional package exploration."""
    try:
        dep_list = [d.strip() for d in dependencies.split(",") if d.strip()] if dependencies else []
        branch = branch_id if branch_id else None
        
        packages_explored = []
        if explore_packages and engine.current_session:
            # Quick package exploration based on thought content
            packages_explored = engine.coding_workflow.explore_packages(
                task_description=content,
                thinking_session_id=engine.current_session
            )
        
        thought_id = await engine.add_thought(
            content=content,
            dependencies=dep_list,
            confidence=confidence,
            branch_id=branch,
            coding_context=True,
            packages_explored=packages_explored
        )
        
        thought = engine.thoughts[thought_id]
        
        result = f"Added coding thought {thought_id}: {content[:50]}..."
        if thought.contradictions:
            result += f" WARNING: Contradicts: {', '.join(thought.contradictions)}"
        
        # Show package suggestions if found
        if packages_explored:
            top_packages = packages_explored[:3]
            result += f"\nPackage suggestions: {', '.join(pkg.name for pkg in top_packages)}"
        
        pattern_info = ""
        high_conf_patterns = [pr for pr in thought.pattern_results if pr.confidence > 0.8]
        if high_conf_patterns:
            pattern_info = f" Patterns: {', '.join(pr.pattern for pr in high_conf_patterns)}"
        
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        return engine.compatibility_layer.adapt_response(result + pattern_info, client_version)
    except Exception as e:
        return f"Error adding coding thought: {str(e)}"

# Additional MCP tools for cross-system integration
@mcp.tool()
def get_cross_system_context(session_id: str = "", ctx: Context = None) -> str:
    """Get package and architecture context for sharing with other systems."""
    try:
        target_session = session_id or engine.current_session
        if not target_session:
            return "Error: No session specified and no active session"
        
        context = cross_system.get_package_context(target_session)
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        response = json.dumps(context, indent=2)
        return engine.compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error getting cross-system context: {str(e)}"

@mcp.tool()
def set_external_context(external_context: str, session_id: str = "", ctx: Context = None) -> str:
    """Set external package and architecture context from other systems."""
    try:
        target_session = session_id or engine.current_session
        if not target_session:
            return "Error: No session specified and no active session"
        
        context_data = json.loads(external_context)
        cross_system.set_external_package_context(target_session, context_data)
        
        client_version = engine.compatibility_layer.detect_client_version(ctx)
        response = f"Successfully integrated external context for session {target_session}"
        return engine.compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error setting external context: {str(e)}"

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

@mcp.resource("thinking://packages")
def get_package_registry() -> str:
    """Get the package registry for the current session."""
    try:
        if not engine.current_session:
            return json.dumps({"error": "No active session"}, indent=2)
        
        session = engine.session_manager.get_session(engine.current_session)
        if not session:
            return json.dumps({"error": "Session not found"}, indent=2)
        
        package_data = {
            "session_id": session.id,
            "packages": {name: asdict(pkg) for name, pkg in session.package_registry.items()}
        }
        return json.dumps(package_data, indent=2)
    except Exception as e:
        return f"Error getting package registry: {str(e)}"

@mcp.resource("thinking://architecture-decisions")
def get_architecture_decisions() -> str:
    """Get architecture decisions for the current session."""
    try:
        if not engine.current_session:
            return json.dumps({"error": "No active session"}, indent=2)
        
        session = engine.session_manager.get_session(engine.current_session)
        if not session:
            return json.dumps({"error": "Session not found"}, indent=2)
        
        decisions_data = {
            "session_id": session.id,
            "decisions": {dec_id: asdict(dec) for dec_id, dec in session.architecture_decisions.items()}
        }
        return json.dumps(decisions_data, indent=2)
    except Exception as e:
        return f"Error getting architecture decisions: {str(e)}"

@mcp.resource("thinking://coding-analysis")
def get_coding_analysis() -> str:
    """Get coding-specific analysis for the current session."""
    try:
        if not engine.current_session:
            return json.dumps({"error": "No active session"}, indent=2)
        
        session = engine.session_manager.get_session(engine.current_session)
        if not session:
            return json.dumps({"error": "Session not found"}, indent=2)
        
        # Get all thoughts for analysis
        all_thoughts = [engine.thoughts[tid] for tid in session.main_thread]
        for branch in session.branches.values():
            all_thoughts.extend([engine.thoughts[tid] for tid in branch.thoughts])
        
        coding_thoughts = [t for t in all_thoughts if t.coding_context]
        
        analysis = {
            "session_id": session.id,
            "is_coding_session": session.coding_session,
            "total_thoughts": len(all_thoughts),
            "coding_thoughts": len(coding_thoughts),
            "packages_discovered": len(session.package_registry),
            "architecture_decisions": len(session.architecture_decisions),
            "coding_patterns": engine._get_coding_patterns(coding_thoughts),
            "package_usage_stats": engine._get_package_usage_stats(coding_thoughts)
        }
        
        return json.dumps(analysis, indent=2)
    except Exception as e:
        return f"Error getting coding analysis: {str(e)}"

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