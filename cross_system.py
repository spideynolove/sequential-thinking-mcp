from typing import Dict, Any
from models import PackageInfo, ArchitectureDecision
from engines import SequentialThinkingEngine

class CrossSystemIntegration:
    def __init__(self, thinking_engine: SequentialThinkingEngine):
        self.thinking_engine = thinking_engine
        self.shared_context = {}
    
    def get_package_context(self, session_id: str) -> Dict[str, Any]:
        session = self.thinking_engine.session_manager.get_session(session_id)
        if not session:
            return {}
        
        return {
            "packages": {name: {
                "name": pkg.name,
                "version": pkg.version,
                "description": pkg.description,
                "installed": pkg.installed,
                "relevance_score": pkg.relevance_score,
                "integration_examples": pkg.integration_examples,
                "api_methods": pkg.api_methods
            } for name, pkg in session.package_registry.items()},
            "architecture_decisions": {id: {
                "id": dec.id,
                "title": dec.title,
                "context": dec.context,
                "options_considered": dec.options_considered,
                "chosen_option": dec.chosen_option,
                "rationale": dec.rationale,
                "consequences": dec.consequences,
                "package_dependencies": dec.package_dependencies,
                "thinking_session_id": dec.thinking_session_id,
                "timestamp": dec.timestamp,
                "status": dec.status
            } for id, dec in session.architecture_decisions.items()},
            "coding_session": session.coding_session,
            "last_updated": session.last_updated
        }
    
    def set_external_package_context(self, session_id: str, external_context: Dict[str, Any]):
        session = self.thinking_engine.session_manager.get_session(session_id)
        if not session:
            return
        
        if "packages" in external_context:
            for name, pkg_data in external_context["packages"].items():
                if name not in session.package_registry:
                    session.package_registry[name] = PackageInfo(**pkg_data)
        
        if "architecture_decisions" in external_context:
            for dec_id, dec_data in external_context["architecture_decisions"].items():
                if dec_id not in session.architecture_decisions:
                    session.architecture_decisions[dec_id] = ArchitectureDecision(**dec_data)