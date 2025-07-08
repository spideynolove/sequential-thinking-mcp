import json
import uuid
import subprocess
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from models import Thought, PackageInfo, ArchitectureDecision, PatternResult
from session_manager import SessionManager
from plugins import PluginManager

class PackageDiscoveryEngine:
    def __init__(self):
        self.package_cache: Dict[str, List[PackageInfo]] = {}
        self.discovery_sources = ["pip", "conda", "local"]
    
    def discover_packages(self, task_description: str, language: str = "python") -> List[PackageInfo]:
        cache_key = f"{task_description}:{language}"
        if cache_key in self.package_cache:
            return self.package_cache[cache_key]
        
        packages = []
        packages.extend(self._search_installed_packages(task_description))
        
        if language == "python":
            packages.extend(self._search_pypi(task_description))
        
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
        def sort_key(pkg: PackageInfo) -> tuple:
            return (-pkg.relevance_score, not pkg.installed)
        
        return sorted(packages, key=sort_key)

class ArchitectureDecisionTracker:
    def __init__(self):
        self.decisions: Dict[str, ArchitectureDecision] = {}
    
    def record_decision(self, title: str, context: str, options_considered: List[str],
                       chosen_option: str, rationale: str, consequences: str,
                       package_dependencies: List[str], thinking_session_id: str) -> str:
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
    
    def query_similar_decisions(self, technology: str = "", pattern: str = "",
                               package: str = "", similarity_threshold: float = 0.7) -> List[ArchitectureDecision]:
        similar_decisions = []
        search_terms = [technology, pattern, package]
        search_text = " ".join(term for term in search_terms if term).lower()
        
        for decision in self.decisions.values():
            decision_text = (decision.title + " " + decision.context + " " + 
                           decision.chosen_option + " " + decision.rationale).lower()
            
            if search_text and search_text in decision_text:
                similar_decisions.append(decision)
        
        return similar_decisions

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
    
    def detect_reinvention(self, proposed_code: str, existing_packages_checked: List[str],
                          confidence_threshold: float = 0.8) -> Dict[str, Any]:
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

class CodingWorkflowEngine:
    def __init__(self, thinking_engine: 'SequentialThinkingEngine'):
        self.thinking_engine = thinking_engine
        self.package_discovery = PackageDiscoveryEngine()
        self.architecture_tracker = ArchitectureDecisionTracker()
        self.reinvention_detector = CodeReinventionDetector()
    
    def start_coding_session(self, problem: str, success_criteria: str, constraints: List[str],
                            codebase_context: str = "", package_exploration_required: bool = True) -> str:
        session_id = self.thinking_engine.start_session(problem, success_criteria, constraints, coding_session=True)
        session = self.thinking_engine.session_manager.get_session(session_id)
        
        if session:
            session.codebase_context = codebase_context
            
            if package_exploration_required:
                asyncio.create_task(self._add_package_discovery_thought(session_id, problem))
        
        return session_id
    
    async def _add_package_discovery_thought(self, session_id: str, problem: str):
        original_session = self.thinking_engine.current_session
        self.thinking_engine.current_session = session_id
        
        try:
            await self.thinking_engine.add_thought(
                content=f"MANDATORY: Explore existing packages for: {problem}",
                confidence=0.9
            )
        finally:
            self.thinking_engine.current_session = original_session
    
    def explore_packages(self, task_description: str, language: str = "python",
                        thinking_session_id: str = "") -> List[PackageInfo]:
        packages = self.package_discovery.discover_packages(task_description, language)
        
        if thinking_session_id:
            session = self.thinking_engine.session_manager.get_session(thinking_session_id)
            if session:
                for package in packages:
                    session.package_registry[package.name] = package
        
        return packages
    
    def record_architecture_decision(self, title: str, context: str, options_considered: List[str],
                                   chosen_option: str, rationale: str, consequences: str,
                                   package_dependencies: List[str], thinking_session_id: str) -> str:
        decision_id = self.architecture_tracker.record_decision(
            title, context, options_considered, chosen_option,
            rationale, consequences, package_dependencies, thinking_session_id
        )
        
        session = self.thinking_engine.session_manager.get_session(thinking_session_id)
        if session:
            session.architecture_decisions[decision_id] = self.architecture_tracker.decisions[decision_id]
        
        return decision_id
    
    def detect_code_reinvention(self, proposed_code: str, existing_packages_checked: List[str],
                               confidence_threshold: float = 0.8) -> Dict[str, Any]:
        return self.reinvention_detector.detect_reinvention(
            proposed_code, existing_packages_checked, confidence_threshold
        )

class SequentialThinkingEngine:
    def __init__(self):
        self.thoughts: Dict[str, Thought] = {}
        self.session_manager = SessionManager()
        self.plugin_manager = PluginManager()
        self.current_session: Optional[str] = None
        self.patterns: Dict[str, int] = {}
        self.coding_workflow = CodingWorkflowEngine(self)
        
        from plugins import KeywordPatternDetector, FallbackPatternDetector, CodingPatternDetector
        self.plugin_manager.register_pattern_detector(KeywordPatternDetector())
        self.plugin_manager.register_pattern_detector(FallbackPatternDetector())
        self.plugin_manager.register_pattern_detector(CodingPatternDetector())
    
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
        
        from models import Branch
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
                    "pattern_results": [{"pattern": pr.pattern, "confidence": pr.confidence, 
                                       "fallback_used": pr.fallback_used, "strategy": pr.strategy} 
                                      for pr in thought.pattern_results]
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
        patterns = {}
        for thought in thoughts:
            for pattern_result in thought.pattern_results:
                if pattern_result.strategy == "coding_keyword":
                    patterns[pattern_result.pattern] = patterns.get(pattern_result.pattern, 0) + 1
        return patterns
    
    def _get_package_usage_stats(self, thoughts: List[Thought]) -> Dict[str, int]:
        package_mentions = {}
        for thought in thoughts:
            for package in thought.packages_explored:
                package_mentions[package.name] = package_mentions.get(package.name, 0) + 1
        return package_mentions