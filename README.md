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

## Roadmap Progress

| Phase | Name | Status |
|-------|------|--------|
| Phase 1 | Foundation | ✅ Complete |
| Phase 2 | Planning & Roadmapping | ✅ Complete |
| Phase 3 | Web UI & API | ✅ Complete |
| Phase 4 | Advanced Features | 🔄 In Progress |
| Phase 5 | Next Generation | 📋 Pending |

### Phase 3 Completed Tasks
- Web chat interface
- REST API
- Persistent history
- Service manager auto-start
- WebUI service status indicator
- WebUI restart button

### Phase 4 In Progress
- LLM integration
- Autonomous improvements

## Quick Start

```bash
# Install dependencies
cd /home/workspace/personai
pip install -e .

# Run the NLP service
python -m src.api.nlp_service
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
│   ├── llm/           # Self-driven NLP
│   ├── agents/         # Agent system
│   ├── revenue/       # Revenue models
│   ├── self_improving/ # Self-improvement
│   ├── planning/      # Roadmap & loop
│   └── api/           # Web API
├── data/              # Persistent data
├── tests/             # Test suite
└── docs/              # Documentation
```

## Testing

```bash
pytest tests/ -v
```

## License

MIT
