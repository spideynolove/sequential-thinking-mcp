# Sequential Thinking MCP - Installation Guide

## Quick Setup

1. **Clone/Download the project:**
   ```bash
   git clone <your-repo> sequential-thinking-mcp
   cd sequential-thinking-mcp
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Add to Claude Code:**
   ```bash
   claude mcp add sequential-thinking uv run /full/path/to/sequential-thinking-mcp/main.py
   ```

4. **Verify installation:**
   ```bash
   claude mcp list
   ```

## Usage in Claude Code

### Start a Thinking Session
```
start_thinking_session(
    problem="How to build a scalable web application?",
    success_criteria="Handle 10k users with <100ms response",
    constraints="Budget $5k, 3-month timeline"
)
```

### Add Sequential Thoughts
```
add_thought(
    content="Need to choose appropriate architecture pattern",
    confidence=0.8
)

add_thought(
    content="Microservices vs monolith - consider team size and complexity",
    dependencies="<previous-thought-id>",
    confidence=0.7
)
```

### Create Alternative Approaches
```
create_branch(
    name="microservices_approach",
    from_thought="<thought-id>",
    purpose="Explore distributed architecture benefits"
)
```

### Analyze Your Thinking
```
analyze_thinking()
```

## Available Tools

| Tool | Purpose |
|------|---------|
| `start_thinking_session` | Begin structured problem solving |
| `add_thought` | Build logical reasoning chains |
| `revise_thought` | Update insights as understanding evolves |
| `create_branch` | Explore alternative approaches |
| `merge_branch` | Integrate insights from different paths |
| `analyze_thinking` | Get quality metrics and learning patterns |

## MCP Resources

Access structured data with @ mentions:
- `@sequential-thinking:thinking://tree` - Complete thought structure
- `@sequential-thinking:thinking://analysis` - Quality metrics
- `@sequential-thinking:thinking://patterns` - Learning insights

## Installation Scopes

### Local (Default)
```bash
claude mcp add sequential-thinking -s local uv run /path/to/main.py
```
- Private to you in current project only

### Project (Team Sharing)
```bash
claude mcp add sequential-thinking -s project uv run /path/to/main.py
```
- Shared with team via `.mcp.json` file
- Include in version control

### User (Global)
```bash
claude mcp add sequential-thinking -s user uv run /path/to/main.py
```
- Available across all your projects

## Troubleshooting

### Server Won't Start
```bash
# Test directly
uv run main.py

# Check dependencies
uv sync

# Verify path is absolute
claude mcp add sequential-thinking uv run $(pwd)/main.py
```

### Can't See Tools
- Restart Claude Code session
- Check server status: `claude mcp get sequential-thinking`
- Use `/mcp` command in Claude Code to check connection

### Permission Issues
```bash
# Make script executable
chmod +x main.py

# Or use uv explicitly
claude mcp add sequential-thinking uv run /absolute/path/to/main.py
```

## Example Workflow

1. **Start session** with clear problem definition
2. **Add initial thoughts** with confidence scores
3. **Build dependencies** between related ideas
4. **Create branches** for alternative approaches
5. **Analyze thinking** to identify gaps and patterns
6. **Revise thoughts** as understanding deepens
7. **Merge branches** to integrate best insights

## Advanced Usage

### With Environment Variables
```bash
claude mcp add sequential-thinking -e DEBUG=1 -e CACHE_DIR=/tmp -- uv run /path/to/main.py
```

### Project Team Setup
```bash
# Add to project scope for team sharing
claude mcp add sequential-thinking -s project uv run ./main.py

# Team members can then use:
claude mcp list  # Shows shared servers
```

### Integration with Other Tools
The Sequential Thinking MCP works well with:
- Database MCP servers for data-driven reasoning
- Web search MCPs for research-backed thinking
- File system MCPs for documentation integration