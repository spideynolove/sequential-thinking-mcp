# Sequential Thinking MCP

An advanced Model Context Protocol (MCP) server that enables structured sequential thinking with first principles reasoning, branch management, and cognitive analysis.

## Features

- **Sequential Thought Tracking**: Build logical chains of reasoning with dependencies
- **Branch Management**: Explore alternative reasoning paths and merge insights
- **Contradiction Detection**: Automatically identify conflicting thoughts
- **Confidence Scoring**: Track certainty levels for each thought
- **Pattern Recognition**: Learn from thinking patterns to improve reasoning
- **Quality Analysis**: Assess thinking depth and structure
- **Resource Access**: Visual thought trees and analytics

## Installation

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Quick Setup

```bash
git clone <your-repo-url>
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

| Tool | Description |
|------|-------------|
| `start_thinking_session` | Initialize a new thinking session with problem definition |
| `add_thought` | Add a sequential thought with dependencies and confidence |
| `revise_thought` | Update existing thoughts with new insights |
| `create_branch` | Start alternative reasoning paths |
| `merge_branch` | Integrate branch insights into main thread |
| `analyze_thinking` | Get quality metrics and patterns |

## Resources

Access structured data through MCP resources:

- `thinking://tree` - Complete visual thought structure
- `thinking://analysis` - Quality metrics and insights  
- `thinking://patterns` - Learning from thinking patterns

## Advanced Features

### Contradiction Detection
Automatically identifies conflicting thoughts and flags logical inconsistencies between dependent ideas.

### Confidence Tracking  
Each thought includes a confidence score (0.0-1.0) to track certainty levels and identify areas needing more exploration.

### Pattern Recognition
The system learns from your thinking patterns, tracking key phrases like "first principles", "assumption", "therefore" to suggest improvements.

### Branch Management
Create, explore, and merge alternative reasoning paths to thoroughly examine different approaches to problems.

### Dependency Mapping
Track which thoughts build on previous insights, creating a clear logical flow and identifying gaps in reasoning.

## Best Practices

1. **Start with Problem Decomposition**: Break complex problems into smaller, manageable components
2. **Build Logical Dependencies**: Connect thoughts to show how insights build upon each other  
3. **Use High Confidence for Facts**: Reserve confidence scores above 0.8 for well-established facts
4. **Create Branches for Alternatives**: Explore different approaches using separate reasoning branches
5. **Revise When New Insights Emerge**: Update thoughts as understanding deepens
6. **Analyze Before Concluding**: Use quality analysis to ensure thorough exploration

## Example Workflow

```python
# 1. Start session
start_thinking_session(
    problem="Design a scalable chat application",
    success_criteria="Handle 10k concurrent users with <100ms latency",
    constraints="Budget $5k, 3-month timeline"
)

# 2. Initial thoughts
thought1 = add_thought(
    content="Real-time communication requires WebSocket connections",
    confidence=0.9
)

thought2 = add_thought(
    content="Need to handle connection scaling - single server won't work",
    dependencies=thought1,
    confidence=0.8
)

# 3. Explore alternatives
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

# 4. Analyze and refine
analysis = analyze_thinking()
```

## Testing Installation

```bash
uv run -c "import main; print('Installation successful')"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review usage examples above