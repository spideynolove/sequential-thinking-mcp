## Sequential Thinking MCP - Coding Integration TODOs

### Coding-Specific Thought Patterns
- **Add coding reasoning templates**: `package_evaluation`, `api_selection`, `integration_planning`
- **Create dependency reasoning chains**: Track why certain packages were chosen over alternatives
- **Implement `code_contradiction_detection()`**: Detect when AI suggests rewriting existing functionality
- **Add coding confidence scoring**: Higher confidence for using existing APIs vs writing new code

### Integration Workflow Tools
- **Add `start_coding_session()` specialized method**: Include package discovery as first step
- **Create `evaluate_existing_solution()` thought type**: Force evaluation of existing packages before new code
- **Implement `integration_branch()` for package exploration**: Compare multiple package options
- **Add `validate_coding_decision()` tool**: Check if coding decisions align with existing codebase patterns

### Package Discovery Integration
```python
@mcp.tool()
def explore_package_apis(package_name: str, use_case: str) -> str:
    """Force exploration of existing package APIs before writing new code"""
    # Check installed packages first
    # Document available APIs
    # Create usage examples
    # Store in thinking session
```

### Coding Pattern Detection
- **Add `PackageUsageDetector` class**: Detect when existing packages should be used
- **Create `CodeReinventionDetector`**: Flag attempts to rewrite existing functionality  
- **Implement `IntegrationPatternDetector`**: Recognize good integration patterns to follow
- **Add `APIDiscoveryDetector`**: Automatically suggest relevant APIs for tasks

### Architecture Decision Tracking
- **Create `architecture_decision_records` collection type**: Store why certain packages/approaches were chosen
- **Add `integration_constraints` thought type**: Document technical constraints that influence package choice
- **Implement `package_evaluation_matrix`**: Compare packages systematically with confidence scores

---

## Cross-System Integration TODOs

### Shared Package Context System
- **Create unified package registry**: Both systems access same package/API database
- **Implement cross-system memory sharing**: Coding decisions in one system influence the other
- **Add package usage validation layer**: Both systems check package usage before code generation

### File Reading Integration for AI Agents
```python
# Both systems need this capability
@mcp.tool()
def read_codebase_files(file_patterns: List[str]) -> str:
    """Read existing codebase files to understand current patterns"""
    # Use window.fs.readFile equivalent for MCP
    # Parse and index existing code
    # Store in memory/thinking systems
```

### PRP-Style Integration Validation
- **Add coding PRP templates**: Force package exploration in every coding task
- **Create integration validation checklists**: Verify existing APIs are checked before new code
- **Implement "package-first" thinking workflows**: Default to existing solutions unless proven inadequate

### Combined Workflow Architecture
```python
class CodingWorkflowEngine:
    def __init__(self):
        self.memory_bank = MemoryBankEngine()
        self.thinking_engine = SequentialThinkingEngine()
        self.package_registry = PackageRegistry()
    
    def start_coding_task(self, task: str):
        # 1. Start both memory and thinking sessions
        # 2. Load package context first
        # 3. Force exploration of existing solutions
        # 4. Validate decisions against existing patterns
```