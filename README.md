# PersonAI - Self-Driven AI Assistant

A self-improving AI assistant with autonomous capabilities, built on the PersonAI framework.

## Core Features

### 🎯 Direct Zo AI Bridge (CORE)
**The heart of PersonAI** - SelfDrivenNLP is a direct bridge to Zo's native AI:

- **NO FALLBACK**: Pure forward connection to Zo LLM - if the service is down, requests fail
- **Self-Hosted**: Only connects to local Zo services - no external APIs
- **Real Intelligence**: Uses Zo's AI for natural language understanding - not hardcoded responses
- **Pattern Learning**: Remembers conversation patterns for faster responses

```
User Query → SelfDrivenNLP → Local NLP Service → Zo AI
                                    ↓
                              NO FALLBACK
```

### 🧠 Memory System
Persistent conversation memory with semantic recall.

### 🔄 Self-Improvement
Autonomous code analysis, improvement, and test validation.

### 👤 User Personalization
Learns and adapts to user preferences over time.

### 🌐 Interfaces
- **Web UI**: https://badlucksbane.zo.space/chat
- **REST API**: https://badlucksbane.zo.space/api/personai
- **Service**: Auto-started via Zo service manager

## Status (2026-03-17)

- **Tests**: 44/44 passing
- **Self-Improvement Cycles**: 27 completed
- **Phase**: 4 - Deep Native Autonomy (in progress) - 65% complete

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
- `POST /api/personai` - Send message (body: {"message": "your text"})
- `GET /api/personai?action=history` - Conversation history

## Web Interface

Chat UI: https://badlucksbane.zo.space/chat

## Testing

```bash
pytest tests/ -v
```

## License

MIT
