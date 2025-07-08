from typing import Dict, List, Any, Protocol
from models import PatternResult

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