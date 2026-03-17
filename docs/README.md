# PersonAI

**Autonomous AI Partner - Self-Directed AGI**

**Vision:** Open source AI for the betterment of humans, Earth, and sky
**Version:** 0.3.0

---

## Session Engineering Notes (Live LLM Bridge Fix)

**Date:** 2026-03-17

This session fixed a critical circular reference bug in SelfDrivenNLP and enabled live LLM testing through the web UI.

### The Problem

SelfDrivenNLP was calling `localhost:8765/chat` (the local NLP service) which would wait for itself to respond, causing a deadlock and timeout. This resulted in hardcoded fallback responses instead of real LLM responses.

### The Fix

- Changed `ZoAIBridge` to connect directly to `https://api.zo.computer/zo/ask` instead of the local service
- Added proper authorization using `ZO_CLIENT_IDENTITY_TOKEN`
- Now all chat responses use real Zo AI LLM responses

### What changed

- `src/llm/__init__.py` - ZoAIBridge now calls Zo AI API directly with auth
- Every feature can now be tested through the web UI with real LLM responses
- No more hardcoded fallback responses in the chat flow

### Validation

```bash
curl -X POST http://localhost:8765/chat -H "Content-Type: application/json" -d '{"message": "Hello!"}'
# Returns: Real LLM response from Zo AI
```

### Live Testing

You can now test PersonAI through the web UI at https://badlucksbane.zo.space/chat - every feature uses real LLM responses from Zo AI. This enables:
- Testing as the user would experience it
- Verifying all features with natural language
- No more hardcoded test inputs

---

## Session Engineering Notes (Compatibility Cleanup + Stability)

This session focused on removing leftover compatibility/dead code paths, modular cleanup, and stability/performance hardening.

### What changed

- Replaced untyped aiohttp app dict keys with typed `web.AppKey` in `src/api/nlp_service.py`.
- Removed direct private history access by introducing `MainLoop.get_history(limit=50)` and using it in API handlers.
- Improved `SelfDrivenNLP` response flow: learned-pattern cache now short-circuits before rule fallback when available.
- Cleaned dead imports and low-signal cruft across modules with safe lint auto-fixes.
- Refactored affiliate model internals for clearer variable names and easier maintenance.
- Updated roadmap verification tests to rely on stable task IDs while preserving compatibility with legacy task names.

### Validation performed

```bash
python -m ruff check src tests
python -m pytest -q tests/unit tests/integration tests/advanced
```

Result:
- Ruff: **All checks passed**
- Pytest: **41 passed**

## Quick Start

```bash
cd personai
pip install -e .

python -m src.cli.main status
python -m src.cli.main revenue
python -m src.cli.main chat "Hello"
python -c "from src.self_improving.runner import get_runner; get_runner().run_cycle()"
```

## Architecture

```
personai/
├── src/
│   ├── core/           # State management, controller
│   ├── agents/         # Agent definitions
│   ├── memory/         # Persistent memory service
│   ├── llm/            # Native self-driven NLP stack
│   ├── consciousness/  # Autonomous thinking/heartbeat
│   ├── self_improving/ # Self-improvement executor
│   ├── revenue/        # Revenue generation models
│   └── cli/            # Command-line interface
├── docs/               # Documentation
├── data/               # Runtime data (memory, config, revenue)
└── tests/              # Test suite
```

## Core Systems

### State Management (`src/core/state.py`)
Thread-safe state management with subscriber pattern.

### Memory Service (`src/memory/`)
Unified memory with persistence.

### LLM Client (`src/llm/`)
Unified interface using native self-driven NLP. Learned pattern responses are reused first where possible.

### Self-Improvement (`src/self_improving/`)
Autonomous code improvement system.

### Revenue System (`src/revenue/`)
7 revenue generation models with orchestration.

Revenue internals are modularized:
- `src/revenue/model_factory.py` builds model instances
- `src/revenue/config_store.py` loads/saves allocation config
- `src/revenue/orchestrator.py` coordinates execution/reporting

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
python -m src.cli.main chat "Hello"
python -m src.cli.main status
python -m src.cli.main revenue
python -m src.cli.main run_model automation_agency
python -m src.cli.main enable_model micro_saas
python -m src.cli.main disable_model trading_bot
python -m src.cli.main report
```

## Development

```bash
python run_tests.py
ruff check src/
ruff format src/
```
