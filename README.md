# PersonAI - Self-Driven AI Assistant

A self-improving AI assistant with autonomous capabilities, built on the PersonAI framework.

## Features

- **Self-Driven NLP**: Pure Python NLP without external APIs
- **Memory System**: Persistent conversation memory
- **Self-Improvement**: Autonomous code improvement with test validation
- **User Personalization**: Learns user preferences
- **Web UI**: Zo.space chat interface at https://badlucksbane.zo.space/chat
- **REST API**: Full API at https://badlucksbane.zo.space/api/personai
- **Service Management**: Auto-start via Zo service manager

## Status (2026-03-17)

- **Tests**: 44/44 passing
- **Self-Improvement Cycles**: 23 completed, 22 improvements applied
- **Phase**: 4 - Deep Native Autonomy (in progress) - 62% complete

## Recent Improvements

- Enhanced NLP with dynamic semantic response generation (no hardcoded responses)
- Deep code analysis: complexity detection, duplication detection, hotspot identification
- Self-improvement executor analyzes code complexity patterns
- All improvements validated by running test suite before committing
- Failed changes automatically reverted if tests fail

## Roadmap Progress

| Phase | Name | Status |
|-------|------|--------|
| Phase 1 | Foundation | ✅ Complete |
| Phase 2 | Planning & Roadmapping | ✅ Complete |
| Phase 3 | Web UI & API | ✅ Complete |
| Phase 4 | Deep Native Autonomy | 🔄 In Progress |
| Phase 5 | Always-On Revenue Operator | 📋 Pending |
| Phase 6 | Autonomous Verification & Docs | 📋 Pending |

### Phase 3 Completed Tasks
- Web chat interface
- REST API
- Persistent history
- Service manager auto-start

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
python -m src.api.nlp_service
```

## Validation

```bash
python -m pytest -q tests/
```

## API Endpoints

- `GET /api/personai` - Status + roadmap
- `GET /api/personai?action=history` - Conversation history
- `POST /api/personai` - Send message

## Web Interface

Chat UI: https://badlucksbane.zo.space/chat

## Testing

```bash
pytest tests/ -v
```

## License

MIT
