import json
from engines import SequentialThinkingEngine

engine = SequentialThinkingEngine()

def get_thought_tree() -> str:
    try:
        tree = engine.get_thought_tree()
        return json.dumps(tree, indent=2)
    except Exception as e:
        return f"Error getting thought tree: {str(e)}"

def get_analysis() -> str:
    try:
        analysis = engine.get_analysis()
        return json.dumps(analysis, indent=2)
    except Exception as e:
        return f"Error getting analysis: {str(e)}"

def get_patterns() -> str:
    try:
        return json.dumps(engine.patterns, indent=2)
    except Exception as e:
        return f"Error getting patterns: {str(e)}"

def get_package_registry() -> str:
    try:
        if not engine.current_session:
            return json.dumps({"error": "No active session"}, indent=2)
        
        session = engine.session_manager.get_session(engine.current_session)
        if not session:
            return json.dumps({"error": "Session not found"}, indent=2)
        
        package_data = {
            "session_id": session.id,
            "packages": {name: {
                "name": pkg.name,
                "version": pkg.version,
                "description": pkg.description,
                "installed": pkg.installed,
                "relevance_score": pkg.relevance_score,
                "integration_examples": pkg.integration_examples,
                "api_methods": pkg.api_methods
            } for name, pkg in session.package_registry.items()}
        }
        return json.dumps(package_data, indent=2)
    except Exception as e:
        return f"Error getting package registry: {str(e)}"

def get_architecture_decisions() -> str:
    try:
        if not engine.current_session:
            return json.dumps({"error": "No active session"}, indent=2)
        
        session = engine.session_manager.get_session(engine.current_session)
        if not session:
            return json.dumps({"error": "Session not found"}, indent=2)
        
        decisions_data = {
            "session_id": session.id,
            "decisions": {dec_id: {
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
            } for dec_id, dec in session.architecture_decisions.items()}
        }
        return json.dumps(decisions_data, indent=2)
    except Exception as e:
        return f"Error getting architecture decisions: {str(e)}"

def get_coding_analysis() -> str:
    try:
        if not engine.current_session:
            return json.dumps({"error": "No active session"}, indent=2)
        
        session = engine.session_manager.get_session(engine.current_session)
        if not session:
            return json.dumps({"error": "Session not found"}, indent=2)
        
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