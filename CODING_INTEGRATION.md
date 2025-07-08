# Coding Integration Guide for Sequential Thinking MCP

## Overview

The Sequential Thinking MCP now includes powerful coding integration features that help prevent code reinvention, facilitate package discovery, and track architecture decisions throughout your development process.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Coding Tools](#core-coding-tools)
3. [Package Discovery Workflow](#package-discovery-workflow)
4. [Architecture Decision Tracking](#architecture-decision-tracking)
5. [Code Reinvention Prevention](#code-reinvention-prevention)
6. [Cross-System Integration](#cross-system-integration)
7. [Real-World Examples](#real-world-examples)
8. [Performance Guidelines](#performance-guidelines)
9. [Troubleshooting](#troubleshooting)

## Quick Start

### Basic Coding Session

```python
# Start a coding session with automatic package exploration
start_coding_session(
    problem="Build a web scraper for product prices",
    success_criteria="Extract data efficiently using existing libraries",
    package_exploration_required=True
)

# Explore relevant packages
explore_packages("web scraping", "python")
# Returns: requests, beautifulsoup4, scrapy, etc.

# Add coding thoughts with package awareness
add_coding_thought(
    "Should use requests for HTTP and BeautifulSoup for HTML parsing",
    explore_packages=True
)

# Record your architecture decision
record_architecture_decision(
    decision_title="Web Scraping Tech Stack",
    context="Need to scrape e-commerce sites for price monitoring",
    options_considered="requests+bs4, scrapy, selenium",
    chosen_option="requests + beautifulsoup4",
    rationale="Simple, lightweight, good for basic scraping needs",
    consequences="May need to upgrade to scrapy for complex sites"
)
```

## Core Coding Tools

### start_coding_session()

Initialize a specialized coding session with package discovery capabilities.

**Parameters:**
- `problem` (str): The coding problem to solve
- `success_criteria` (str): Definition of success
- `constraints` (str, optional): Comma-separated constraints
- `codebase_context` (str, optional): Existing codebase information
- `package_exploration_required` (bool, default=True): Enable automatic package discovery

**Example:**
```python
start_coding_session(
    problem="Implement user authentication system",
    success_criteria="Secure, standards-compliant auth with minimal custom code",
    constraints="Must integrate with existing Django app",
    codebase_context="Django 4.2 project with PostgreSQL",
    package_exploration_required=True
)
```

### explore_packages()

Discover and rank relevant packages for a specific task.

**Parameters:**
- `task_description` (str): Description of what you want to accomplish
- `language` (str, default="python"): Programming language
- `thinking_session_id` (str, optional): Session to store results in

**Example:**
```python
packages = explore_packages(
    task_description="HTTP client with async support",
    language="python"
)
# Returns list of PackageInfo objects with relevance scores
```

### add_coding_thought()

Add a thought with coding context and optional package exploration.

**Parameters:**
- `content` (str): The thought content
- `dependencies` (str, optional): Comma-separated thought dependencies
- `confidence` (float, default=0.8): Confidence level
- `branch_id` (str, optional): Branch to add thought to
- `explore_packages` (bool, default=True): Automatically explore relevant packages

**Example:**
```python
add_coding_thought(
    content="Need to handle rate limiting for API calls",
    dependencies="previous_api_thought",
    explore_packages=True
)
```

### record_architecture_decision()

Document architectural choices with full context and rationale.

**Parameters:**
- `decision_title` (str): Short title for the decision
- `context` (str): Background and requirements
- `options_considered` (str): Comma-separated options evaluated
- `chosen_option` (str): Selected option
- `rationale` (str): Why this option was chosen
- `consequences` (str): Expected outcomes and trade-offs
- `package_dependencies` (str, optional): Related packages
- `thinking_session_id` (str, optional): Session to link decision to

### detect_code_reinvention()

Analyze proposed code to detect potential reinvention of existing solutions.

**Parameters:**
- `proposed_code` (str): Code you're considering writing
- `existing_packages_checked` (str, optional): Packages already evaluated
- `confidence_threshold` (float, default=0.8): Detection sensitivity

**Example:**
```python
result = detect_code_reinvention(
    proposed_code="def http_get(url): ...",  # Custom HTTP implementation
    existing_packages_checked="requests"
)
# Returns analysis with reinvention likelihood and recommendations
```

### query_architecture_decisions()

Search previous decisions for similar contexts and patterns.

**Parameters:**
- `technology` (str, optional): Technology filter
- `pattern` (str, optional): Pattern filter
- `package` (str, optional): Package filter
- `similarity_threshold` (float, default=0.7): Similarity threshold

## Package Discovery Workflow

### 1. Automatic Discovery

When you start a coding session, packages are automatically discovered based on your problem description:

```python
start_coding_session(
    problem="Build REST API with database integration",
    success_criteria="High performance, well-documented endpoints"
)
# Automatically discovers: FastAPI, Django, Flask, SQLAlchemy, etc.
```

### 2. Manual Discovery

Explore packages for specific tasks:

```python
# Discover web frameworks
web_frameworks = explore_packages("web framework", "python")

# Discover database ORMs
orm_packages = explore_packages("database ORM", "python")

# Discover testing frameworks
test_frameworks = explore_packages("testing framework", "python")
```

### 3. Package Evaluation

Packages are ranked by:
- **Relevance Score**: How well they match your task
- **Installation Status**: Installed packages are prioritized
- **Popularity**: Based on usage patterns and community adoption

### 4. Integration Examples

Each discovered package includes potential integration examples:

```python
packages = explore_packages("HTTP client", "python")
for package in packages:
    print(f"{package.name}: {package.description}")
    print(f"Relevance: {package.relevance_score}")
    print(f"Examples: {package.integration_examples}")
```

## Architecture Decision Tracking

### Decision Format

All architecture decisions follow the ADR (Architecture Decision Record) format:

```python
record_architecture_decision(
    decision_title="Database Selection for User Data",
    context="Need to store user profiles, preferences, and activity logs. Expected 100K+ users within first year.",
    options_considered="PostgreSQL, MongoDB, SQLite + Redis",
    chosen_option="PostgreSQL with Redis cache",
    rationale="ACID compliance for user data, mature ecosystem, excellent Django integration. Redis for session storage and caching.",
    consequences="Higher infrastructure complexity but better data consistency and performance at scale."
)
```

### Decision Queries

Search previous decisions to maintain consistency:

```python
# Find database-related decisions
db_decisions = query_architecture_decisions(technology="database")

# Find authentication decisions
auth_decisions = query_architecture_decisions(pattern="authentication")

# Find FastAPI-related decisions
api_decisions = query_architecture_decisions(package="fastapi")
```

### Decision Evolution

Decisions can be updated or superseded:

```python
# Record a new decision that supersedes a previous one
record_architecture_decision(
    decision_title="Database Migration to PostgreSQL",
    context="Original SQLite decision no longer meets performance requirements",
    options_considered="Stay with SQLite, migrate to PostgreSQL, switch to MongoDB",
    chosen_option="Migrate to PostgreSQL",
    rationale="Better performance, ACID compliance, rich feature set",
    consequences="Migration effort required, infrastructure complexity increases"
)
```

## Code Reinvention Prevention

### Automatic Detection

The system automatically detects common reinvention patterns:

```python
# This will trigger reinvention warning
detect_code_reinvention("""
def send_http_request(url, method='GET', headers=None):
    # Custom HTTP implementation
    import socket
    # ... custom HTTP code
""")
# Result: HIGH confidence reinvention detected - suggests using 'requests'
```

### Common Patterns Detected

- **HTTP Requests**: Custom HTTP vs requests/httpx
- **Data Processing**: Manual CSV parsing vs pandas
- **Database Access**: Raw SQL vs ORM libraries
- **Testing**: Custom assertions vs pytest
- **Authentication**: Custom JWT vs libraries like PyJWT
- **Logging**: Print statements vs logging module

### Integration with Workflow

```python
# 1. Start coding session
start_coding_session(problem="API client for third-party service")

# 2. Check for reinvention before implementing
result = detect_code_reinvention(
    proposed_code="Custom HTTP client implementation"
)

# 3. If reinvention detected, explore packages
if result['is_potential_reinvention']:
    packages = explore_packages("HTTP client", "python")
    
# 4. Record decision to use existing package
record_architecture_decision(
    decision_title="HTTP Client Library Selection",
    chosen_option="requests",
    rationale="Mature, well-tested, excellent documentation"
)
```

## Cross-System Integration

### Memory Bank Integration

Share package context with memory-bank-mcp:

```python
# Export context for other systems
context = get_cross_system_context()
# Context includes packages, decisions, and session metadata

# Import context from other systems
external_context = {
    "packages": {...},
    "architecture_decisions": {...}
}
set_external_context(json.dumps(external_context))
```

### Context Sharing

```python
# Get package context for sharing
context = get_cross_system_context(session_id)
# Returns:
# {
#   "packages": {"requests": {...}, "fastapi": {...}},
#   "architecture_decisions": {"dec_123": {...}},
#   "coding_session": true,
#   "last_updated": "2024-01-15T10:30:00"
# }
```

## Real-World Examples

### Example 1: Web API Development

```python
# 1. Initialize coding session
session_id = start_coding_session(
    problem="Build REST API for task management",
    success_criteria="Fast, documented, type-safe endpoints",
    codebase_context="New greenfield project"
)

# 2. Explore web frameworks
frameworks = explore_packages("web framework async", "python")
# Discovers: FastAPI, Django, Flask, Starlette

# 3. Add reasoning thought
add_coding_thought(
    "FastAPI provides automatic OpenAPI docs and type checking",
    explore_packages=False  # Already explored
)

# 4. Record framework decision
record_architecture_decision(
    decision_title="Web Framework Selection",
    context="Need REST API with automatic documentation",
    options_considered="FastAPI, Django REST, Flask-RESTful",
    chosen_option="FastAPI",
    rationale="Built-in OpenAPI, type hints, async support, high performance",
    consequences="Newer ecosystem, less third-party packages than Django"
)

# 5. Explore database options
db_packages = explore_packages("async database ORM", "python")
# Discovers: SQLAlchemy, Tortoise ORM, Databases

# 6. Record database decision
record_architecture_decision(
    decision_title="Database and ORM Selection",
    context="Need async-compatible ORM for FastAPI",
    options_considered="SQLAlchemy + asyncpg, Tortoise ORM, Raw SQL with databases",
    chosen_option="SQLAlchemy 2.0 with asyncpg",
    rationale="Mature, feature-rich, excellent async support in 2.0",
    consequences="Learning curve for SQLAlchemy 2.0 async patterns"
)
```

### Example 2: Data Processing Pipeline

```python
# 1. Start coding session
start_coding_session(
    problem="Process large CSV files for analytics",
    success_criteria="Handle 10M+ rows efficiently",
    constraints="Memory usage under 4GB"
)

# 2. Check for reinvention
reinvention_result = detect_code_reinvention(
    proposed_code="Custom CSV parser with manual memory management"
)
# Result: Suggests pandas, polars, or dask

# 3. Explore data processing libraries
data_libs = explore_packages("large dataset processing", "python")
# Discovers: pandas, polars, dask, vaex

# 4. Record processing library decision
record_architecture_decision(
    decision_title="Large Data Processing Library",
    context="Process 10M+ row CSV files within memory constraints",
    options_considered="pandas, polars, dask, custom solution",
    chosen_option="polars",
    rationale="Rust backend for speed, lazy evaluation, low memory usage",
    consequences="Newer library, smaller community than pandas"
)
```

### Example 3: Machine Learning Model

```python
# 1. Initialize ML project session
start_coding_session(
    problem="Build image classification model",
    success_criteria="90%+ accuracy on validation set",
    codebase_context="Existing data science workflow with Jupyter"
)

# 2. Explore ML frameworks
ml_frameworks = explore_packages("deep learning framework", "python")
# Discovers: PyTorch, TensorFlow, JAX, Keras

# 3. Add analysis thought
add_coding_thought(
    "Need to consider model deployment requirements and team expertise"
)

# 4. Record ML framework decision
record_architecture_decision(
    decision_title="Deep Learning Framework Selection",
    context="Image classification with deployment to REST API",
    options_considered="PyTorch, TensorFlow, Keras",
    chosen_option="PyTorch with TorchServe",
    rationale="Flexible research-friendly API, excellent deployment with TorchServe",
    consequences="Steeper learning curve than Keras, more verbose than TensorFlow"
)

# 5. Explore computer vision libraries
cv_libs = explore_packages("computer vision preprocessing", "python")
# Discovers: torchvision, albumentations, opencv-python

# 6. Record preprocessing decision
record_architecture_decision(
    decision_title="Image Preprocessing Pipeline",
    context="Need robust data augmentation for image classification",
    options_considered="torchvision transforms, albumentations, custom preprocessing",
    chosen_option="albumentations with torchvision integration",
    rationale="More extensive augmentations, faster, research-proven techniques",
    consequences="Additional dependency, learning curve for advanced augmentations"
)
```

## Performance Guidelines

### Memory Usage

- Basic thinking session: ~2-5MB
- Coding session with package registry: +5-10MB
- Each architecture decision: +1-2MB storage
- Package discovery cache: +2-5MB

### Response Times

- `start_coding_session()`: <300ms (includes package initialization)
- `explore_packages()`: 500-2000ms (network dependent, cached after first call)
- `add_coding_thought()`: <200ms (with package cache)
- `record_architecture_decision()`: <50ms
- `detect_code_reinvention()`: <100ms

### Optimization Tips

1. **Enable Caching**: Package discovery results are cached automatically
2. **Limit Discovery Scope**: Use specific task descriptions for faster results
3. **Async Operations**: Package discovery runs asynchronously when possible
4. **Batch Operations**: Group related decisions and explorations

```python
# Efficient: Specific task description
explore_packages("async HTTP client", "python")

# Less efficient: Vague description
explore_packages("networking", "python")
```

## Troubleshooting

### Common Issues

#### Package Discovery Returns No Results

**Problem**: `explore_packages()` returns empty list

**Solutions**:
1. Check internet connectivity (for PyPI search)
2. Verify package manager installation (`pip --version`)
3. Try more specific or alternative task descriptions
4. Check spelling in task description

```python
# Instead of:
explore_packages("web scrapping")  # Typo

# Use:
explore_packages("web scraping")
```

#### Performance Issues

**Problem**: Slow response times for package discovery

**Solutions**:
1. Use more specific task descriptions to reduce search scope
2. Check network connectivity for PyPI API access
3. Clear package cache if corrupted: restart the session
4. Reduce `confidence_threshold` for faster detection

#### Architecture Decisions Not Persisting

**Problem**: Decisions not available in `query_architecture_decisions()`

**Solutions**:
1. Ensure you're providing `thinking_session_id` parameter
2. Check that decision was recorded successfully (no error returned)
3. Verify session is still active
4. Check decision storage with `thinking://architecture-decisions` resource

### Debug Resources

Use MCP resources to inspect system state:

```python
# Check package registry
packages = get_resource("thinking://packages")

# Check architecture decisions
decisions = get_resource("thinking://architecture-decisions")

# Check coding analysis
analysis = get_resource("thinking://coding-analysis")

# Check cross-system context
context = get_cross_system_context()
```

### Error Handling

All tools provide detailed error messages:

```python
try:
    result = explore_packages("invalid task", "unsupported_language")
except Exception as e:
    print(f"Error: {e}")
    # Handle gracefully
```

## Best Practices

### 1. Start with Package Discovery

Always explore existing solutions before implementing:

```python
# ✅ Good: Explore first
packages = explore_packages("task automation", "python")
# Then decide whether to use existing package or implement custom

# ❌ Bad: Implement first, discover later
```

### 2. Document All Decisions

Record decisions with full context:

```python
# ✅ Good: Comprehensive decision record
record_architecture_decision(
    decision_title="Detailed title",
    context="Full business and technical context",
    options_considered="All evaluated options",
    chosen_option="Selected option",
    rationale="Clear reasoning with trade-offs",
    consequences="Expected outcomes and risks"
)

# ❌ Bad: Minimal decision record
record_architecture_decision(
    decision_title="Used FastAPI",
    chosen_option="FastAPI",
    rationale="It's fast"
)
```

### 3. Check for Reinvention Regularly

Use reinvention detection throughout development:

```python
# Before implementing any significant functionality
result = detect_code_reinvention(proposed_code)
if result['is_potential_reinvention']:
    # Explore alternatives first
    alternatives = explore_packages(functionality_description)
```

### 4. Leverage Cross-Session Learning

Query previous decisions for consistency:

```python
# Before making similar decisions
previous = query_architecture_decisions(technology="database")
# Learn from past decisions and maintain consistency
```

### 5. Use Specific Task Descriptions

Better package discovery with specific descriptions:

```python
# ✅ Good: Specific
explore_packages("async HTTP client with retry logic", "python")

# ❌ Bad: Vague
explore_packages("networking", "python")
```

## Migration from Basic Thinking

Existing users can adopt coding features gradually:

### Phase 1: Drop-in Replacement

```python
# Before: Basic thinking session
start_thinking_session(problem, criteria)

# After: Coding session (backward compatible)
start_coding_session(problem, criteria)
```

### Phase 2: Add Package Awareness

```python
# Before: Basic thoughts
add_thought(content)

# After: Package-aware thoughts
add_coding_thought(content, explore_packages=True)
```

### Phase 3: Decision Tracking

```python
# Add architecture decision tracking
record_architecture_decision(
    decision_title="Technology Choice",
    # ... full decision context
)
```

All existing tools continue to work unchanged, and new features are completely optional.