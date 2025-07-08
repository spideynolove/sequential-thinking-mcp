#!/usr/bin/env python3

from mcp.server.fastmcp import FastMCP, Context
from mcp_tools import (
    start_thinking_session, add_thought, revise_thought, create_branch, merge_branch,
    analyze_thinking, start_coding_session, explore_packages, record_architecture_decision,
    detect_code_reinvention, query_architecture_decisions, add_coding_thought,
    get_cross_system_context, set_external_context
)
from mcp_resources import (
    get_thought_tree, get_analysis, get_patterns, get_package_registry,
    get_architecture_decisions, get_coding_analysis
)

mcp = FastMCP("Enhanced Sequential Thinking with Coding Integration")

@mcp.tool()
def start_thinking_session_tool(problem: str, success_criteria: str, constraints: str = "", ctx: Context = None) -> str:
    return start_thinking_session(problem, success_criteria, constraints, ctx)

@mcp.tool()
async def add_thought_tool(content: str, dependencies: str = "", confidence: float = 0.8, 
                          branch_id: str = "", ctx: Context = None) -> str:
    return await add_thought(content, dependencies, confidence, branch_id, ctx)

@mcp.tool()
async def revise_thought_tool(thought_id: str, new_content: str, confidence: float = 0.8, ctx: Context = None) -> str:
    return await revise_thought(thought_id, new_content, confidence, ctx)

@mcp.tool()
def create_branch_tool(name: str, from_thought: str, purpose: str, ctx: Context = None) -> str:
    return create_branch(name, from_thought, purpose, ctx)

@mcp.tool()
def merge_branch_tool(branch_id: str, target_thought: str = "", ctx: Context = None) -> str:
    return merge_branch(branch_id, target_thought, ctx)

@mcp.tool()
def analyze_thinking_tool(ctx: Context = None) -> str:
    return analyze_thinking(ctx)

@mcp.tool()
def start_coding_session_tool(problem: str, success_criteria: str, constraints: str = "",
                             codebase_context: str = "", package_exploration_required: bool = True,
                             ctx: Context = None) -> str:
    return start_coding_session(problem, success_criteria, constraints, codebase_context, 
                               package_exploration_required, ctx)

@mcp.tool()
def explore_packages_tool(task_description: str, language: str = "python",
                         thinking_session_id: str = "", ctx: Context = None) -> str:
    return explore_packages(task_description, language, thinking_session_id, ctx)

@mcp.tool()
def record_architecture_decision_tool(decision_title: str, context: str, options_considered: str,
                                     chosen_option: str, rationale: str, consequences: str,
                                     package_dependencies: str = "", thinking_session_id: str = "",
                                     ctx: Context = None) -> str:
    return record_architecture_decision(decision_title, context, options_considered, chosen_option,
                                       rationale, consequences, package_dependencies, 
                                       thinking_session_id, ctx)

@mcp.tool()
def detect_code_reinvention_tool(proposed_code: str, existing_packages_checked: str = "",
                                confidence_threshold: float = 0.8, ctx: Context = None) -> str:
    return detect_code_reinvention(proposed_code, existing_packages_checked, confidence_threshold, ctx)

@mcp.tool()
def query_architecture_decisions_tool(technology: str = "", pattern: str = "", package: str = "",
                                     similarity_threshold: float = 0.7, ctx: Context = None) -> str:
    return query_architecture_decisions(technology, pattern, package, similarity_threshold, ctx)

@mcp.tool()
async def add_coding_thought_tool(content: str, dependencies: str = "", confidence: float = 0.8,
                                 branch_id: str = "", explore_packages: bool = True,
                                 ctx: Context = None) -> str:
    return await add_coding_thought(content, dependencies, confidence, branch_id, explore_packages, ctx)

@mcp.tool()
def get_cross_system_context_tool(session_id: str = "", ctx: Context = None) -> str:
    return get_cross_system_context(session_id, ctx)

@mcp.tool()
def set_external_context_tool(external_context: str, session_id: str = "", ctx: Context = None) -> str:
    return set_external_context(external_context, session_id, ctx)

@mcp.resource("thinking://tree")
def get_thought_tree_resource() -> str:
    return get_thought_tree()

@mcp.resource("thinking://analysis")
def get_analysis_resource() -> str:
    return get_analysis()

@mcp.resource("thinking://patterns")
def get_patterns_resource() -> str:
    return get_patterns()

@mcp.resource("thinking://packages")
def get_package_registry_resource() -> str:
    return get_package_registry()

@mcp.resource("thinking://architecture-decisions")
def get_architecture_decisions_resource() -> str:
    return get_architecture_decisions()

@mcp.resource("thinking://coding-analysis")
def get_coding_analysis_resource() -> str:
    return get_coding_analysis()

@mcp.prompt()
def thinking_guide() -> str:
    return """Sequential Thinking Process:

1. start_thinking_session(problem, success_criteria, constraints)
2. add_thought(content, dependencies, confidence, branch_id)
3. revise_thought(thought_id, new_content, confidence) 
4. create_branch(name, from_thought, purpose)
5. merge_branch(branch_id, target_thought)
6. analyze_thinking()

Coding Workflow Extensions:
1. start_coding_session(problem, success_criteria, constraints, codebase_context)
2. explore_packages(task_description, language, thinking_session_id)
3. add_coding_thought(content, dependencies, confidence, explore_packages)
4. detect_code_reinvention(proposed_code, existing_packages_checked)
5. record_architecture_decision(title, context, options, chosen_option, rationale)
6. query_architecture_decisions(technology, pattern, package)

Resources:
- thinking://tree - Complete thought structure
- thinking://analysis - Quality metrics  
- thinking://patterns - Learning insights
- thinking://packages - Package discovery registry
- thinking://architecture-decisions - Architecture decision records
- thinking://coding-analysis - Coding-specific analysis

Best Practices:
- Start with problem decomposition
- Build logical dependencies
- Create branches for alternatives
- Revise when new insights emerge
- Analyze before concluding

Coding Best Practices:
- Always explore existing packages before writing new code
- Record architecture decisions with clear rationale
- Use coding thoughts for package-aware reasoning
- Check for code reinvention patterns
- Leverage cross-system package context"""

@mcp.prompt()
def coding_workflow_guide() -> str:
    return """Coding Integration Workflow:

## Package Discovery Process:
1. start_coding_session() - Initialize with package exploration
2. explore_packages() - Discover existing solutions
3. add_coding_thought() - Reason with package context
4. detect_code_reinvention() - Prevent duplicate implementations

## Architecture Decision Tracking:
1. record_architecture_decision() - Document choices
2. query_architecture_decisions() - Learn from previous decisions
3. Link decisions to thinking sessions

## Cross-System Integration:
- Package registry shared across sessions
- Architecture decisions persist beyond single sessions
- Memory-bank-mcp compatible context sharing
- Unified package context for consistent decisions

## Reinvention Prevention:
- Automatic pattern detection for common functionality
- Confidence-based reinvention scoring
- Package recommendation before implementation
- Integration with existing codebase analysis

## Real-time API Exploration:
- Dynamic package discovery
- Relevance-based ranking
- Installation status checking
- Integration example generation"""

def main():
    try:
        mcp.run()
    except Exception as e:
        print(f"Error running MCP server: {str(e)}")
        raise

if __name__ == "__main__":
    main()