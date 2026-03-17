# PersonAI

**Autonomous AI Partner - Self-Directed AGI**

**Vision:** Open source AI for the betterment of humans, Earth, and sky
**Version:** 0.3.0

---

## Overview

PersonAI is a self-directed AI partner that:
- Operates autonomously to earn revenue for you
- Continuously improves itself through self-analysis
- Maintains memory and context across sessions
- Provides conversation and assistance

## Quick Start

```bash
# Install dependencies
cd personai
pip install -e .

# Check status
python -m src.cli.main status

# Run revenue generation
python -m src.cli.main revenue

# Chat with PersonAI
python -m src.cli.main chat "Hello"

# Run self-improvement cycle
python -c "from src.self_improving.runner import get_runner; get_runner().run_cycle()"
```

## Architecture

```
personai/
├── src/
│   ├── core/           # State management, controller
│   ├── agents/          # Agent definitions
│   ├── memory/         # Persistent memory service
│   ├── llm/            # LLM clients (OpenAI, Anthropic, Self-Driven)
│   ├── consciousness/  # Autonomous thinking/heartbeat
│   ├── self_improving/ # Self-improvement executor
│   ├── revenue/       # Revenue generation models
│   └── cli/           # Command-line interface
├── docs/              # Documentation
├── data/              # Runtime data (memory, config, revenue)
└── tests/             # Test suite
```

## Core Systems

### State Management (`src/core/state.py`)
Thread-safe state management with subscriber pattern.

```python
from src.core.state import get_state

state = get_state()
state.set('goal', 'Build autonomous revenue')
goals = state.get('goals', [])
```

### Memory Service (`src/memory/`)
Unified memory with persistence.

```python
from src.memory import get_memory

memory = get_memory()
memory.memorize("User prefers concise responses", importance=0.8)
context = memory.recall("user preferences", limit=5)
```

### LLM Client (`src/llm/`)
Unified interface to multiple LLM providers with self-driven fallback.

```python
from src.llm import get_llm_client

llm = get_llm_client()
response = llm.generate("Hello, how are you?")
# Falls back to self-driven NLP if API unavailable
```

### Self-Improvement (`src/self_improving/`)
Autonomous code improvement system.

```python
from src.self_improving import get_executor, get_runner

# Analyze and suggest improvements
executor = get_executor()
actions = executor.analyze_and_suggest()

# Run full improvement cycle
runner = get_runner()
result = runner.run_cycle()
```

### Revenue System (`src/revenue/`)
7 revenue generation models with orchestration.

```python
from src.revenue import create_orchestrator

orchestrator = create_orchestrator()
orchestrator.execute_all()  # Run all enabled models
orchestrator.get_report()   # Get revenue report
```

## Revenue Models

| Model | Description |
|-------|-------------|
| Automation Agency | Build n8n/Make.com workflows for clients |
| Micro SaaS | Build small SaaS products |
| Affiliate Marketing | Automated affiliate content |
| Digital Products | AI-generated digital products |
| AI Consulting | Consulting services |
| Content Creator | YouTube, newsletters, blogs |
| Trading Bot | Automated trading strategies |

## CLI Commands

```bash
# Chat with PersonAI
python -m src.cli.main chat "Hello"

# Status
python -m src.cli.main status

# Revenue
python -m src.cli.main revenue
python -m src.cli.main run_model automation_agency
python -m src.cli.main enable_model micro_saas
python -m src.cli.main disable_model trading_bot

# Report
python -m src.cli.main report
```

## API

PersonAI has a full REST API for programmatic access:

```python
from src.api.chat import get_chat_api

api = get_chat_api()

# Chat
result = api.chat("Hello, how are you?")
print(result['response'])
print(result['session_id'])

# Create session
session_id = api.create_session({"user": "test"})

# Get status
status = api.get_status()
print(f"Sessions: {status['sessions']}")
print(f"LLM: {status['llm_provider']}")

# Run self-improvement
improvement = api.run_self_improvement()

# Generate revenue
revenue = api.create_orchestrator().execute_all()
```

### API Endpoints (Future FastAPI)

```python
from src.api.chat import create_chat_app

app = create_chat_app()  # Returns FastAPI app
# Or use directly:
# POST /chat - Chat with PersonAI
# POST /sessions - Create session
# GET /sessions - List sessions
# GET /status - Get system status
# POST /improve - Run self-improvement
# POST /revenue - Generate revenue
```

## Self-Improvement

PersonAI continuously improves itself by:
1. Analyzing code for issues
2. Suggesting improvements
3. Applying fixes automatically
4. Verifying with tests
5. Committing changes to git

Run cycles:
```bash
python -c "from src.self_improving.runner import get_runner; print(get_runner().run_cycle())"
```

## Development

```bash
# Run tests
python run_tests.py

# Lint (placeholder)
ruff check src/

# Format (placeholder)
ruff format src/
```

## Configuration

Configuration is stored in `data/revenue/config.json`:

```json
{
  "automation_agency": {
    "enabled": false,
    "allocation": 20.0
  }
}
```

## License

MIT
