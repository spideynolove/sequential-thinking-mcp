# Sequential Thinking MCP with Coding Integration

An advanced Model Context Protocol (MCP) server that enables structured sequential thinking with first principles reasoning, branch management, cognitive analysis, and enterprise-grade scalability. Now enhanced with comprehensive coding workflow integration to prevent code reinvention and accelerate development decisions.

## Features

### Core Capabilities
- **Sequential Thought Tracking**: Build logical chains of reasoning with dependencies
- **Branch Management**: Explore alternative reasoning paths and merge insights
- **Contradiction Detection**: Automatically identify conflicting thoughts with confidence scoring
- **Pattern Recognition**: Learn from thinking patterns with multiple detection strategies
- **Quality Analysis**: Assess thinking depth, structure, and effectiveness
- **Resource Access**: Visual thought trees and analytics

### 🆕 Coding Integration Features
- **Package Discovery**: Automatic exploration of existing libraries before coding
- **Architecture Decision Tracking**: Document and query technical decisions with full context
- **Code Reinvention Prevention**: Detect when you're rebuilding existing functionality
- **Cross-System Integration**: Share package context with memory-bank-mcp and other systems
- **Real-time API Exploration**: Discover and evaluate packages with relevance scoring
- **Coding Pattern Detection**: Identify coding-specific thought patterns and workflows

### Enterprise Architecture
- **Plugin System**: Modular pattern detectors with protocol-based architecture
- **Session Isolation**: Concurrent session handling with memory management
- **Async Processing**: Non-blocking operations for scalable performance
- **MCP Protocol Compatibility**: Version detection and capability negotiation
- **Robust Error Handling**: Comprehensive exception management and graceful degradation

## Installation

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Quick Setup

```bash
git clone https://github.com/spideynolove/sequential-thinking-mcp.git
cd sequential-thinking-mcp
uv sync
```

### Installation Options

#### Option 1: Direct UV Run
```bash
uv run main.py
```

#### Option 2: Global Installation
```bash
uv tool install .
sequential-thinking-mcp
```

#### Option 3: Development Mode
```bash
uv pip install -e .
```

## Claude Desktop Integration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "enhanced-sequential-thinking": {
      "command": "uv",
      "args": [
        "run",
        "/path/to/sequential-thinking-mcp/main.py"
      ]
    }
  }
}
```

## Usage

### Basic Thinking (Unchanged)

#### 1. Start a Thinking Session

```python
start_thinking_session(
    problem="How to build a recommendation system?",
    success_criteria="Scalable system with <100ms response time",
    constraints="Limited to open source tools, $1000 budget"
)
```

### 🆕 Coding Integration Usage

#### 1. Start a Coding Session (Enhanced)

```python
start_coding_session(
    problem="Build REST API for user management",
    success_criteria="Secure, scalable endpoints with automatic documentation",
    constraints="Must integrate with existing Django app",
    codebase_context="Django 4.2 project with PostgreSQL",
    package_exploration_required=True  # Automatic package discovery
)
```

#### 2. Explore Packages Before Coding

```python
# Discover relevant packages automatically
packages = explore_packages("web framework async", "python")
# Returns: FastAPI, Django, Flask with relevance scores and installation status

# Get package suggestions in thoughts
add_coding_thought(
    "Need async web framework for high performance API",
    explore_packages=True  # Automatically suggests relevant packages
)
```

#### 3. Prevent Code Reinvention

```python
# Check if you're reinventing existing functionality
result = detect_code_reinvention(
    proposed_code="def custom_http_client(): # custom HTTP implementation",
    existing_packages_checked="requests, httpx"
)
# Returns confidence score and alternative suggestions
```

#### 4. Track Architecture Decisions

```python
record_architecture_decision(
    decision_title="Web Framework Selection", 
    context="Need high-performance API with automatic documentation",
    options_considered="FastAPI, Django REST, Flask-RESTful",
    chosen_option="FastAPI",
    rationale="Built-in OpenAPI docs, type hints, async support",
    consequences="Newer ecosystem, learning curve for team"
)

# Query previous decisions for consistency
similar_decisions = query_architecture_decisions(technology="web framework")
```

### 2. Add Sequential Thoughts

```python
add_thought(
    content="First principle: recommendations match user preferences based on behavior patterns",
    confidence=0.9
)

add_thought(
    content="Need to collect user interaction data: clicks, purchases, time spent",
    dependencies="thought_id_1",
    confidence=0.8
)
```

### 3. Create Alternative Approaches

```python
create_branch(
    name="collaborative_filtering",
    from_thought="thought_id_2", 
    purpose="Explore user-user similarity approach"
)

add_thought(
    content="Calculate user similarity using cosine similarity on interaction vectors",
    branch_id="branch_id_1",
    confidence=0.7
)
```

### 4. Analyze Thinking Quality

```python
analyze_thinking()
```

## Available Tools

### Core Thinking Tools (Enhanced)

| Tool | Description | Enhanced Features |
|------|-------------|------------------|
| `start_thinking_session` | Initialize a new thinking session | Session isolation, memory management |
| `add_thought` | Add a sequential thought with dependencies | Async processing, pattern confidence |
| `revise_thought` | Update existing thoughts with new insights | Revision tracking, quality metrics |
| `create_branch` | Start alternative reasoning paths | Branch isolation, concurrent processing |
| `merge_branch` | Integrate branch insights into main thread | Conflict resolution, quality preservation |
| `analyze_thinking` | Get quality metrics and patterns | Enhanced analytics, performance monitoring |

### 🆕 Coding Integration Tools

| Tool | Description | Key Benefits |
|------|-------------|--------------|
| `start_coding_session` | Initialize coding session with package discovery | Automatic package exploration, coding context |
| `explore_packages` | Discover relevant packages for specific tasks | Real-time discovery, relevance scoring, installation status |
| `add_coding_thought` | Add thoughts with package awareness | Automatic package suggestions, coding pattern detection |
| `record_architecture_decision` | Document technical decisions with full context | Searchable decision history, rationale tracking |
| `query_architecture_decisions` | Search previous decisions for consistency | Technology/pattern filtering, similarity matching |
| `detect_code_reinvention` | Identify potential reinvention of existing code | Confidence scoring, alternative suggestions |
| `get_cross_system_context` | Export package context for other systems | Memory-bank-mcp integration, context sharing |
| `set_external_context` | Import package context from other systems | Cross-session learning, unified package knowledge |

## Resources

Access structured data through MCP resources:

### Core Resources
- `thinking://tree` - Complete visual thought structure with confidence metrics
- `thinking://analysis` - Quality metrics, performance data, and insights  
- `thinking://patterns` - Learning from thinking patterns with strategy tracking

### 🆕 Coding Integration Resources
- `thinking://packages` - Package discovery registry with relevance scores
- `thinking://architecture-decisions` - Architecture decision records (ADRs)
- `thinking://coding-analysis` - Coding-specific metrics and insights

## Advanced Features

### Plugin Architecture
Modular pattern detection system with protocol-based interfaces. Custom pattern detectors can be easily added without modifying core functionality.

### Session Management
- **Concurrent Sessions**: Multiple isolated thinking sessions
- **Memory Management**: Per-session resource limits and cleanup
- **Performance Monitoring**: Real-time memory usage and pattern quality tracking

### MCP Protocol Compatibility
- **Version Detection**: Automatic client version detection and adaptation
- **Capability Negotiation**: Protocol feature compatibility checking
- **Backward Compatibility**: Support for multiple MCP protocol versions

### Pattern Recognition Robustness
- **Multiple Strategies**: Keyword-based, semantic, and contextual pattern detection
- **Confidence Scoring**: 0.0-1.0 confidence ratings for all detected patterns
- **Fallback Mechanisms**: Graceful degradation when primary detection fails
- **Quality Metrics**: Pattern effectiveness and accuracy tracking

### Contradiction Detection
Enhanced contradiction analysis with confidence scoring, semantic understanding, and conflict resolution suggestions.

### Error Handling
Comprehensive exception management throughout the system with detailed error reporting and recovery mechanisms.

## Best Practices

### Core Thinking Practices
1. **Start with Problem Decomposition**: Break complex problems into smaller, manageable components
2. **Build Logical Dependencies**: Connect thoughts to show how insights build upon each other  
3. **Use High Confidence for Facts**: Reserve confidence scores above 0.8 for well-established facts
4. **Create Branches for Alternatives**: Explore different approaches using separate reasoning branches
5. **Monitor Resource Usage**: Use session limits to prevent memory issues with large thinking sessions
6. **Revise When New Insights Emerge**: Update thoughts as understanding deepens
7. **Analyze Before Concluding**: Use quality analysis to ensure thorough exploration

### 🆕 Coding Integration Best Practices
8. **Always Explore Packages First**: Use `explore_packages()` before implementing new functionality
9. **Document Architecture Decisions**: Record technical choices with full context and rationale
10. **Check for Code Reinvention**: Use `detect_code_reinvention()` regularly throughout development
11. **Leverage Cross-Session Learning**: Query previous decisions for consistent technology choices
12. **Use Specific Task Descriptions**: Better package discovery with detailed, specific descriptions
13. **Maintain Decision History**: Keep architecture decisions up-to-date as context changes
14. **Share Context Across Systems**: Integrate with memory-bank-mcp for unified package knowledge

## Example Workflow

```python
# 1. Start session with resource limits
start_thinking_session(
    problem="Design a scalable chat application",
    success_criteria="Handle 10k concurrent users with <100ms latency",
    constraints="Budget $5k, 3-month timeline"
)

# 2. Initial thoughts with confidence tracking
thought1 = add_thought(
    content="Real-time communication requires WebSocket connections",
    confidence=0.9
)

thought2 = add_thought(
    content="Need to handle connection scaling - single server won't work",
    dependencies=thought1,
    confidence=0.8
)

# 3. Explore alternatives with async processing
branch1 = create_branch(
    name="microservices_approach",
    from_thought=thought2,
    purpose="Evaluate microservices architecture for scaling"
)

add_thought(
    content="Separate services for auth, messaging, presence, and notifications",
    branch_id=branch1,
    confidence=0.7
)

# 4. Analyze with enhanced metrics
analysis = analyze_thinking()
```

## Performance & Scalability

### Memory Management
- Session-level memory monitoring and limits
- Automatic cleanup of inactive sessions
- Resource usage tracking and optimization

### Async Processing
- Non-blocking thought processing
- Concurrent pattern detection
- Parallel branch analysis

### Performance Monitoring
- Real-time memory usage tracking
- Pattern detection quality metrics
- Session performance analytics

## Testing Installation

```bash
# Test basic functionality
uv run -c "import main; print('Installation successful')"

# Test with sample session
uv run test_mcp.py
```

## Architecture

### Core Components
- **SequentialThinkingEngine**: Main reasoning engine with session management
- **SessionManager**: Handles concurrent sessions and resource limits
- **PatternDetector**: Plugin-based pattern recognition system
- **FastMCP Integration**: MCP protocol handling with version compatibility

### Plugin System
```python
# Custom pattern detector example
class CustomPatternDetector:
    def detect_patterns(self, content: str) -> List[PatternMatch]:
        # Implementation here
        pass
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the plugin architecture
4. Add tests for new functionality
5. Ensure backward compatibility
6. Submit a pull request

## Changelog

### v3.0.0 - Coding Integration Enhancement
- ✅ Complete coding workflow integration
- ✅ Package discovery and exploration engine
- ✅ Architecture decision tracking (ADR) system
- ✅ Code reinvention prevention detection
- ✅ Cross-system integration with memory-bank-mcp
- ✅ Real-time API exploration workflow
- ✅ Coding pattern detection and analysis
- ✅ Comprehensive documentation and testing
- ✅ Migration guide for existing users
- ✅ Full backward compatibility maintained

### v2.0.0 - Architecture Refactoring
- ✅ Plugin system for modular pattern detection
- ✅ Session isolation and concurrent processing
- ✅ MCP protocol compatibility layer
- ✅ Enhanced error handling and monitoring
- ✅ Async processing and performance optimization
- ✅ Backward compatibility maintained

### v1.0.0 - Initial Release
- Basic sequential thinking functionality
- Branch management and merging
- Pattern recognition and analysis
- MCP server implementation

## License

MIT License - see LICENSE file for details

## Documentation & Migration

### 📚 Comprehensive Documentation
- **[CODING_INTEGRATION.md](CODING_INTEGRATION.md)** - Complete coding workflow guide with examples
- **[MIGRATION.md](MIGRATION.md)** - Step-by-step migration guide for existing users
- **[tests/](tests/)** - Comprehensive test suite with integration examples

### 🔄 For Existing Users
**Zero Breaking Changes**: All existing tools work unchanged. New coding features are completely optional and additive.

**Migration Path**: 
1. Continue using existing thinking tools (no changes needed)
2. Try `start_coding_session()` for coding problems  
3. Gradually adopt package discovery and decision tracking
4. Leverage cross-system integration as needed

See [MIGRATION.md](MIGRATION.md) for detailed adoption strategies.

## Support

For issues and questions:
- Create an issue on GitHub
- Check [CODING_INTEGRATION.md](CODING_INTEGRATION.md) for comprehensive usage guide
- Review [MIGRATION.md](MIGRATION.md) for adoption strategies
- Review architecture guidelines for contributions
- Test with provided examples