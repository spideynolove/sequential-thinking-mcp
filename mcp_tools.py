import json
from mcp.server.fastmcp import Context
from engines import SequentialThinkingEngine
from cross_system import CrossSystemIntegration
from compatibility import MCPCompatibilityLayer

engine = SequentialThinkingEngine()
cross_system = CrossSystemIntegration(engine)
compatibility_layer = MCPCompatibilityLayer()

def start_thinking_session(problem: str, success_criteria: str, constraints: str = "", ctx: Context = None) -> str:
    constraint_list = [c.strip() for c in constraints.split(",") if c.strip()] if constraints else []
    client_version = compatibility_layer.detect_client_version(ctx)
    session_id = engine.start_session(problem, success_criteria, constraint_list)
    response = f"Started thinking session {session_id} for: {problem}"
    return compatibility_layer.adapt_response(response, client_version)

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
        
        client_version = compatibility_layer.detect_client_version(ctx)
        return compatibility_layer.adapt_response(result + pattern_info, client_version)
    except Exception as e:
        return f"Error adding thought: {str(e)}"

async def revise_thought(thought_id: str, new_content: str, confidence: float = 0.8, ctx: Context = None) -> str:
    try:
        revised_id = await engine.revise_thought(thought_id, new_content, confidence)
        client_version = compatibility_layer.detect_client_version(ctx)
        response = f"Revised {thought_id} -> {revised_id}: {new_content[:50]}..."
        return compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error revising thought: {str(e)}"

def create_branch(name: str, from_thought: str, purpose: str, ctx: Context = None) -> str:
    try:
        branch_id = engine.create_branch(name, from_thought, purpose)
        client_version = compatibility_layer.detect_client_version(ctx)
        response = f"Created branch {branch_id} '{name}' from {from_thought}: {purpose}"
        return compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error creating branch: {str(e)}"

def merge_branch(branch_id: str, target_thought: str = "", ctx: Context = None) -> str:
    try:
        target = target_thought if target_thought else None
        merged = engine.merge_branch(branch_id, target)
        client_version = compatibility_layer.detect_client_version(ctx)
        response = f"Merged branch {branch_id}: {len(merged)} thoughts integrated"
        return compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error merging branch: {str(e)}"

def analyze_thinking(ctx: Context = None) -> str:
    try:
        analysis = engine.get_analysis()
        client_version = compatibility_layer.detect_client_version(ctx)
        response = json.dumps(analysis, indent=2)
        return compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error analyzing thinking: {str(e)}"

def start_coding_session(problem: str, success_criteria: str, constraints: str = "",
                        codebase_context: str = "", package_exploration_required: bool = True,
                        ctx: Context = None) -> str:
    try:
        constraint_list = [c.strip() for c in constraints.split(",") if c.strip()] if constraints else []
        
        session_id = engine.coding_workflow.start_coding_session(
            problem=problem,
            success_criteria=success_criteria,
            constraints=constraint_list,
            codebase_context=codebase_context,
            package_exploration_required=package_exploration_required
        )
        
        client_version = compatibility_layer.detect_client_version(ctx)
        response = f"Started coding session {session_id} for: {problem}"
        
        if package_exploration_required:
            response += "\nPackage exploration enabled - will explore existing solutions first."
        
        return compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error starting coding session: {str(e)}"

def explore_packages(task_description: str, language: str = "python",
                    thinking_session_id: str = "", ctx: Context = None) -> str:
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
        
        for i, pkg in enumerate(packages[:5], 1):
            status = "✓ Installed" if pkg.installed else "○ Available"
            result += f"{i}. {pkg.name} ({pkg.version}) - {status}\n"
            result += f"   Description: {pkg.description}\n"
            result += f"   Relevance: {pkg.relevance_score:.2f}\n\n"
        
        client_version = compatibility_layer.detect_client_version(ctx)
        return compatibility_layer.adapt_response(result, client_version)
    except Exception as e:
        return f"Error exploring packages: {str(e)}"

def record_architecture_decision(decision_title: str, context: str, options_considered: str,
                                chosen_option: str, rationale: str, consequences: str,
                                package_dependencies: str = "", thinking_session_id: str = "",
                                ctx: Context = None) -> str:
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
        
        client_version = compatibility_layer.detect_client_version(ctx)
        response = f"Recorded architecture decision ADR-{decision_id}: {decision_title}"
        return compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error recording architecture decision: {str(e)}"

def detect_code_reinvention(proposed_code: str, existing_packages_checked: str = "",
                           confidence_threshold: float = 0.8, ctx: Context = None) -> str:
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
        
        client_version = compatibility_layer.detect_client_version(ctx)
        return compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error detecting code reinvention: {str(e)}"

def query_architecture_decisions(technology: str = "", pattern: str = "", package: str = "",
                                similarity_threshold: float = 0.7, ctx: Context = None) -> str:
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
        
        client_version = compatibility_layer.detect_client_version(ctx)
        return compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error querying architecture decisions: {str(e)}"

async def add_coding_thought(content: str, dependencies: str = "", confidence: float = 0.8,
                            branch_id: str = "", explore_packages: bool = True,
                            ctx: Context = None) -> str:
    try:
        dep_list = [d.strip() for d in dependencies.split(",") if d.strip()] if dependencies else []
        branch = branch_id if branch_id else None
        
        packages_explored = []
        if explore_packages and engine.current_session:
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
        
        if packages_explored:
            top_packages = packages_explored[:3]
            result += f"\nPackage suggestions: {', '.join(pkg.name for pkg in top_packages)}"
        
        pattern_info = ""
        high_conf_patterns = [pr for pr in thought.pattern_results if pr.confidence > 0.8]
        if high_conf_patterns:
            pattern_info = f" Patterns: {', '.join(pr.pattern for pr in high_conf_patterns)}"
        
        client_version = compatibility_layer.detect_client_version(ctx)
        return compatibility_layer.adapt_response(result + pattern_info, client_version)
    except Exception as e:
        return f"Error adding coding thought: {str(e)}"

def get_cross_system_context(session_id: str = "", ctx: Context = None) -> str:
    try:
        target_session = session_id or engine.current_session
        if not target_session:
            return "Error: No session specified and no active session"
        
        context = cross_system.get_package_context(target_session)
        client_version = compatibility_layer.detect_client_version(ctx)
        response = json.dumps(context, indent=2)
        return compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error getting cross-system context: {str(e)}"

def set_external_context(external_context: str, session_id: str = "", ctx: Context = None) -> str:
    try:
        target_session = session_id or engine.current_session
        if not target_session:
            return "Error: No session specified and no active session"
        
        context_data = json.loads(external_context)
        cross_system.set_external_package_context(target_session, context_data)
        
        client_version = compatibility_layer.detect_client_version(ctx)
        response = f"Successfully integrated external context for session {target_session}"
        return compatibility_layer.adapt_response(response, client_version)
    except Exception as e:
        return f"Error setting external context: {str(e)}"