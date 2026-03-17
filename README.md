# PersonAI 🤖

Your personal AI assistant with self-improvement capabilities.

## Features

- **Conversational AI** - Natural language chat with memory
- **Self-Improvement** - Autonomous code analysis and improvement
- **Personalization** - Learns your preferences and facts about you
- **Roadmap Tracking** - Tracks project milestones
- **Service Management** - Auto-start with web UI control

## Web Interface

**URL**: https://badlucksbane.zo.space/chat

### Controls
- Service status indicator (Online/Offline)
- Restart button when service is down
- Real-time message history
- Roadmap progress display

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/personai` | GET | Status, roadmap, message count |
| `/api/personai?action=history` | GET | Conversation history |
| `/api/personai` | POST | Send message |
| `/api/personai?action=restart` | POST | Restart NLP service |

## Service Management

The NLP service runs as a persistent service:
- **Service ID**: `personai-nlp`
- **Port**: 8765
- **Auto-restart**: Enabled via Zo service manager

### Manual Commands
```bash
# Check service status
curl http://localhost:8765/health

# View logs
tail -f /tmp/nlp_service.log

# Restart service
curl -X POST https://badlucksbane.zo.space/api/personai?action=restart
```

## Architecture

```
┌─────────────────┐     ┌──────────────────┐
│   Web UI       │────▶│  zo.space API    │
│  (React)       │     │  (TypeScript)    │
└─────────────────┘     └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │  NLP Service     │
                        │  (Python)        │
                        │  - Memory        │
                        │  - Planning      │
                        │  - Self-Improve  │
                        └──────────────────┘
```

## Roadmap

- ✅ Phase 1: Foundation (Core, Memory, LLM)
- 🔄 Phase 2: Planning (Roadmap, Self-Improvement)  
- ✅ Phase 3: Web UI (Chat interface, API)
- ⏳ Phase 4: Advanced (Autonomous agents, Plugins)

## Development

```bash
# Run tests
cd /home/workspace/personai
pytest tests/ -v

# Start service manually
cd /home/workspace/personai
python -m src.api.nlp_service
```

## Version

0.1.0 - Service Management Update
