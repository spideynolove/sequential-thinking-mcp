# Sequential Thinking MCP

An advanced Model Context Protocol (MCP) server that enables structured sequential thinking with first principles reasoning, branch management, cognitive analysis, and enterprise-grade scalability.

## Features

### Core Capabilities
- **Sequential Thought Tracking**: Build logical chains of reasoning with dependencies
- **Branch Management**: Explore alternative reasoning paths and merge insights
- **Contradiction Detection**: Automatically identify conflicting thoughts with confidence scoring
- **Pattern Recognition**: Learn from thinking patterns with multiple detection strategies
- **Quality Analysis**: Assess thinking depth, structure, and effectiveness
- **Resource Access**: Visual thought trees and analytics

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

### 1. Start a Thinking Session

```python
start_thinking_session(
    problem="How to build a recommendation system?",
    success_criteria="Scalable system with <100ms response time",
    constraints="Limited to open source tools, $1000 budget"
)
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

| Tool | Description | New Features |
|------|-------------|--------------|
| `start_thinking_session` | Initialize a new thinking session with problem definition | Session isolation, memory management |
| `add_thought` | Add a sequential thought with dependencies and confidence | Async processing, pattern confidence |
| `revise_thought` | Update existing thoughts with new insights | Revision tracking, quality metrics |
| `create_branch` | Start alternative reasoning paths | Branch isolation, concurrent processing |
| `merge_branch` | Integrate branch insights into main thread | Conflict resolution, quality preservation |
| `analyze_thinking` | Get quality metrics and patterns | Enhanced analytics, performance monitoring |

## Resources

Access structured data through MCP resources:

- `thinking://tree` - Complete visual thought structure with confidence metrics
- `thinking://analysis` - Quality metrics, performance data, and insights  
- `thinking://patterns` - Learning from thinking patterns with strategy tracking

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

1. **Start with Problem Decomposition**: Break complex problems into smaller, manageable components
2. **Build Logical Dependencies**: Connect thoughts to show how insights build upon each other  
3. **Use High Confidence for Facts**: Reserve confidence scores above 0.8 for well-established facts
4. **Create Branches for Alternatives**: Explore different approaches using separate reasoning branches
5. **Monitor Resource Usage**: Use session limits to prevent memory issues with large thinking sessions
6. **Revise When New Insights Emerge**: Update thoughts as understanding deepens
7. **Analyze Before Concluding**: Use quality analysis to ensure thorough exploration

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

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review architecture guidelines for contributions
- Test with provided examples