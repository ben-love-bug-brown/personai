# PersonAI - Self-Driven AI Assistant

A self-improving AI assistant with autonomous capabilities, built on the PersonAI framework.

## Features

- **Self-Driven NLP**: Pure Python NLP without external APIs
- **Memory System**: Persistent conversation memory
- **Self-Improvement**: Autonomous code improvement
- **User Personalization**: Learns user preferences
- **Web UI**: Zo.space chat interface at https://badlucksbane.zo.space/chat
- **REST API**: Full API at https://badlucksbane.zo.space/api/personai
- **Service Management**: Auto-start via Zo service manager

## Maintenance Update (Current Session)

- Removed leftover compatibility/dead code paths and unused imports across core modules.
- Refactored `src/api/nlp_service.py` for stronger stability using typed `aiohttp.web.AppKey` storage.
- Reduced private coupling by adding `MainLoop.get_history()` and switching API history reads to that public method.
- Improved NLP hot path in `src/llm/__init__.py` by using learned-pattern cache before rule-generation fallback.
- Cleaned and standardized code quality via Ruff-safe fixes.
- Improved readability and maintainability in affiliate model internals (`src/revenue/models/affiliate.py`) with clearer variable naming.
- Hardened roadmap verification tests by checking stable task IDs with backward-compatible name fallback.

## Roadmap Progress

| Phase | Name | Status |
|-------|------|--------|
| Phase 1 | Foundation | ✅ Complete |
| Phase 2 | Planning & Roadmapping | ✅ Complete |
| Phase 3 | Web UI & API | ✅ Complete |
| Phase 4 | Advanced Self-Driven Features | 🔄 In Progress |
| Phase 5 | Autonomous Operating System | 📋 Pending |

### Phase 3 Completed Tasks
- Web chat interface
- REST API
- Persistent history
- Service manager auto-start
- WebUI service status indicator
- WebUI restart button

### Phase 4 In Progress
- Enhanced native pattern learning
- Autonomous code analysis
- Deep personalization
- Autonomous goal setting

### Dream State
- Always-on autonomous operator (self-improves, optimizes revenue, and transfers learning across modules)
- 100% native processing without external model APIs

## Quick Start

```bash
cd /home/workspace/personai
pip install -e .
python -m src.api.nlp_service
```

## Validation

```bash
python -m ruff check src tests
python -m pytest -q tests/unit tests/integration tests/advanced
```

## API Endpoints

- `GET /api/personai` - Status + roadmap
- `GET /api/personai?action=history` - Conversation history
- `POST /api/personai` - Send message
- `POST /api/personai?action=restart` - Restart service
- `GET /api/personai?action=services` - List services

## Web Interface

Chat UI: https://badlucksbane.zo.space/chat

Features:
- Real-time chat with PersonAI
- Service status indicator
- Restart button
- Roadmap progress display

## Architecture

```
personai/
├── src/
│   ├── core/           # Core state management
│   ├── memory/         # Memory system
│   ├── llm/            # Self-driven NLP
│   ├── agents/         # Agent system
│   ├── revenue/        # Revenue models + orchestration
│   │   ├── orchestrator.py
│   │   ├── model_factory.py
│   │   └── config_store.py
│   ├── self_improving/ # Self-improvement
│   ├── planning/       # Roadmap & loop
│   └── api/            # Web API
├── data/               # Persistent data
├── tests/              # Test suite
└── docs/               # Documentation
```

## Testing

```bash
pytest tests/ -v
```

## License

MIT
