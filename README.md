# PersonAI 🤖

A self-improving AI assistant with autonomous planning capabilities.

## Features

- **Self-Driven NLP** - Pure Python LLM processing without external APIs
- **Memory System** - Unified memory with categorization and retrieval
- **Planning & Roadmapping** - Autonomous self-improvement with phase-based roadmap tracking
- **Web UI** - Zo.space chat interface at https://badlucksbane.zo.space/chat
- **REST API** - Full API at https://badlucksbane.zo.space/api/personai

## Architecture

```
personai/
├── src/
│   ├── api/          # API services (nlp_service.py)
│   ├── core/         # State management, personalization
│   ├── llm/          # Self-driven NLP
│   ├── memory/       # Unified memory system
│   ├── planning/     # Roadmap and main loop
│   ├── revenue/      # Revenue models
│   └── self_improving/  # Self-improvement logic
├── data/             # Persistent data (roadmap, profile, memory)
└── tests/           # Test suite
```

## Web Interface

Chat with PersonAI at: **https://badlucksbane.zo.space/chat**

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/personai` | POST | Send a chat message |
| `/api/personai` | GET | Get status |
| `/api/personai/history` | GET | Get conversation history |
| `/api/personai/roadmap` | GET | Get roadmap status |

## Local Development

```bash
# Start NLP service
cd /home/workspace/personai
python -m src.api.nlp_service

# Run tests
python -m pytest tests/
```

## Roadmap Progress

- Phase 1: Foundation ✅ (4/4 tasks)
- Phase 2: Planning & Roadmapping 🔄 (1/3 tasks)
- Phase 3: Web UI & API ✅ (2/3 tasks)
- Phase 4: Advanced Features ⏳ (0/2 tasks)

## Version

0.1.0 - Initial release with core functionality
