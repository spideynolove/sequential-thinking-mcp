from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class PatternResult:
    pattern: str
    confidence: float
    fallback_used: bool = False
    strategy: str = "keyword"
    
    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")

@dataclass
class PackageInfo:
    name: str
    version: str
    description: str
    installed: bool = False
    relevance_score: float = 0.0
    integration_examples: List[str] = field(default_factory=list)
    api_methods: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Package name cannot be empty")
        self.relevance_score = max(0.0, min(1.0, self.relevance_score))

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
    status: str = "active"
    
    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Decision title cannot be empty")

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
    tags: List[str] = field(default_factory=list)
    pattern_results: List[PatternResult] = field(default_factory=list)
    packages_explored: List[PackageInfo] = field(default_factory=list)
    architecture_decisions: List[str] = field(default_factory=list)
    coding_context: bool = False

    def __post_init__(self):
        if not self.content.strip():
            raise ValueError("Thought content cannot be empty")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")

@dataclass
class Branch:
    id: str
    name: str
    created_from: str
    purpose: str
    thoughts: List[str]
    merged: bool = False
    merge_target: Optional[str] = None
    
    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Branch name cannot be empty")

@dataclass
class SessionConfig:
    max_thoughts: int = 1000
    max_branches: int = 50
    memory_limit_mb: int = 100
    auto_cleanup: bool = True
    pattern_confidence_threshold: float = 0.6
    
    def __post_init__(self):
        if self.max_thoughts < 1:
            raise ValueError("Max thoughts must be positive")
        if not (0.0 <= self.pattern_confidence_threshold <= 1.0):
            raise ValueError("Pattern confidence threshold must be between 0.0 and 1.0")

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
    config: SessionConfig = field(default_factory=SessionConfig)
    memory_usage: int = 0
    coding_session: bool = False
    package_registry: Dict[str, PackageInfo] = field(default_factory=dict)
    architecture_decisions: Dict[str, ArchitectureDecision] = field(default_factory=dict)
    codebase_context: Optional[str] = None
    
    def __post_init__(self):
        if not self.problem_statement.strip():
            raise ValueError("Problem statement cannot be empty")
        if not self.success_criteria.strip():
            raise ValueError("Success criteria cannot be empty")