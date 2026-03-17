# PersonAI Master Roadmap

## Autonomous AI Partner - Implementation Guide & TODO

**Project:** PersonAI - A self-directed AGI partner that earns and cares for you\
**Vision:** Open source AI for the betterment of humans, Earth, and sky\
**Version:** 1.0.0

---

## Phase 1: Project Foundation & Organization

### 1.1 Directory Structure Setup

**Objective:** Create unified single-repo structure consolidating agi-framework, axe, memU

```markdown
/personai/
├── src/
│   ├── core/                    # Central nervous system
│   │   ├── agent_executor.py   # Unified agent execution
│   │   ├── routing.py          # Request routing
│   │   ├── state.py            # State management
│   │   └── controller.py       # Main controller
│   │
│   ├── agents/                  # Agent definitions (TOML + SKILL.md)
│   │   ├── supervisor/         # Orchestration agent
│   │   ├── researcher/         # Research tasks
│   │   ├── coder/              # Code generation
│   │   ├── writer/             # Content creation
│   │   ├── analyzer/           # Analysis tasks
│   │   └── revenue/            # Revenue generation agents
│   │
│   ├── memory/                  # Unified memory system (memU integration)
│   │   ├── __init__.py
│   │   ├── service.py
│   │   ├── memorize.py
│   │   ├── retrieve.py
│   │   └── profiles/
│   │
│   ├── llm/                     # Self-driven NLP (from agi-framework)
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── providers/
│   │   └── self_driven/
│   │
│   ├── consciousness/           # Autonomous thinking (from agi-framework)
│   │   ├── __init__.py
│   │   ├── heartbeat.py
│   │   └── decision.py
│   │
│   ├── self_improving/          # Self-improvement engine
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   ├── runner.py
│   │   └── intelligence.py
│   │
│   ├── revenue/                 # Revenue generation system
│   │   ├── __init__.py
│   │   ├── models/             # 26 revenue model implementations
│   │   ├── strategies/         # Strategy selection & allocation
│   │   ├── execution/          # Execution engines
│   │   └── tracking/           # Revenue tracking & reporting
│   │
│   ├── cli/                     # CLI interface
│   │   ├── __init__.py
│   │   └── commands/
│   │
│   └── tests/                   # Test suite
│       ├── unit/
│       ├── integration/
│       └── e2e/
│
├── docs/                        # Documentation
│   ├── architecture.md
│   ├── api_reference.md
│   ├── revenue_models.md
│   └── guides/
│
├── config/                      # Configuration
│   ├── default.toml
│   ├── development.toml
│   └── production.toml
│
├── pyproject.toml
├── Makefile
├── README.md
└── LICENSE
```

### 1.2 Move & Organize Existing Code

**Task List:**

- [ ]  1.2.1 Create new directory structure

- [ ]  1.2.2 Move `agi-framework/src/` → `src/core/`, `src/llm/`, `src/consciousness/`, `src/self_improving/`

- [ ]  1.2.3 Integrate `axe/` as agent execution layer in `src/agents/`

- [ ]  1.2.4 Integrate `memU/` as memory backend in `src/memory/`

- [ ]  1.2.5 Consolidate revenue docs → `src/revenue/models/`

- [ ]  1.2.6 Update all import paths

- [ ]  1.2.7 Verify basic imports work

- [ ]  1.2.8 Archive original directories (rename to `.backup/`)

### 1.3 Coding Standards & Configuration

**Task List:**

- [ ]  1.3.1 Define `file pyproject.toml` with dependencies

- [ ]  1.3.2 Configure `Makefile` with targets:

  - `make install` - Install dependencies
  - `make test` - Run tests
  - `make lint` - Run linters
  - `make format` - Format code
  - `make check` - Full quality check
  - `make dev` - Development server

- [ ]  1.3.3 Set up `ruff` or `black` + `isort` for formatting

- [ ]  1.3.4 Configure `mypy` for type checking

- [ ]  1.3.5 Create `.gitignore` (Python, Go, Rust patterns)

---

## Phase 2: Core System Integration

### 2.1 Agent Execution Layer (Axe Integration)

**Objective:** Fix broken agent code and integrate axe as execution engine

**Spec - AgentExecutor:**

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum

class AgentType(Enum):
    SUPERVISOR = "supervisor"
    RESEARCHER = "researcher"
    CODER = "coder"
    WRITER = "writer"
    ANALYZER = "analyzer"
    REVENUE = "revenue"

@dataclass
class AgentConfig:
    type: AgentType
    model: str  # e.g., "anthropic/claude-3-opus"
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 300
    max_iterations: int = 10
    tools: List[str] = None  # Tool names to enable
    memory_enabled: bool = True

class AgentExecutor:
    """Unified agent execution engine"""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.llm = get_llm_client(config.model)
        self.memory = get_memory()
        self.tools = self._load_tools(config.tools or [])

    def execute(self, task: str, context: Dict[str, Any] = None) -> AgentResult:
        """Execute a task and return result"""
        # 1. Load relevant memory
        # 2. Build prompt with context
        # 3. Execute with tools
        # 4. Store results to memory
        # 5. Return result
        pass

    def execute_with_subagents(
        self, 
        task: str, 
        subagent_configs: List[AgentConfig]
    ) -> AgentResult:
        """Execute with sub-agents for complex tasks"""
        pass

    def stream(self, task: str) -> Iterator[str]:
        """Stream execution results"""
        pass
```

**Task List:**

- [ ]  2.1.1 Create `file src/agent_executor.py` with AgentExecutor class

- [ ]  2.1.2 Define AgentConfig dataclass

- [ ]  2.1.3 Implement `execute()` method with memory integration

- [ ]  2.1.4 Implement `execute_with_subagents()`

- [ ]  2.1.5 Add streaming support

- [ ]  2.1.6 Create agent TOML definitions in `src/agents/`

- [ ]  2.1.7 Create SKILL.md files for each agent

- [ ]  2.1.8 Write unit tests for AgentExecutor

- [ ]  2.1.9 Run integration test with real LLM

### 2.2 Memory System (memU Integration)

**Objective:** Integrate memU as unified memory backend

**Spec - MemoryService:**

```python
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class MemoryCategory(Enum):
    CONVERSATION = "conversation"
    KNOWLEDGE = "knowledge"
    PROFILE = "profile"
    SKILL = "skill"
    TOOL = "tool"
    BEHAVIOR = "behavior"
    EVENT = "event"
    REVENUE = "revenue"

@dataclass
class MemoryItem:
    id: str
    content: str
    category: MemoryCategory
    importance: float  # 0.0 - 1.0
    created_at: datetime
    accessed_at: datetime
    access_count: int
    metadata: Dict[str, Any]

class MemoryService:
    """Unified memory service wrapping memU"""

    def __init__(self, backend: str = "sqlite"):
        self.backend = backend
        self.client = self._init_client(backend)

    def memorize(
        self, 
        content: str, 
        category: MemoryCategory,
        importance: float = 0.5,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Store a memory and return its ID"""
        pass

    def recall(self, query: str, limit: int = 5) -> List[MemoryItem]:
        """Recall relevant memories"""
        pass

    def retrieve(
        self, 
        query: str, 
        category: Optional[MemoryCategory] = None,
        limit: int = 10
    ) -> List[MemoryItem]:
        """Retrieve memories with filters"""
        pass

    def update(self, memory_id: str, content: str = None, importance: float = None):
        """Update a memory"""
        pass

    def delete(self, memory_id: str):
        """Delete a memory"""
        pass

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        pass
```

**Task List:**

- [ ]  2.2.1 Create `file src/memory/service.py` with MemoryService

- [ ]  2.2.2 Implement `memorize()` with memU backend

- [ ]  2.2.3 Implement `recall()` with relevance ranking

- [ ]  2.2.4 Implement `retrieve()` with filters

- [ ]  2.2.5 Add category management

- [ ]  2.2.6 Create profile-based LLM routing

- [ ]  2.2.7 Write unit tests for memory operations

- [ ]  2.2.8 Test with SQLite backend

- [ ]  2.2.9 Test with PostgreSQL backend (optional)

### 2.3 Self-Driven NLP Integration

**Objective:** Integrate agi-framework's self-driven NLP as LLM layer

**Spec - LLMClient:**

```python
from typing import Optional, List, Dict, Any, Iterator
from dataclasses import dataclass
from enum import Enum

class Provider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    GROK = "grok"
    OPENROUTER = "openrouter"
    SELF_DRIVEN = "self_driven"  # Fallback - no API

@dataclass
class LLMResponse:
    content: str
    model: str
    usage: Dict[str, int]  # prompt_tokens, completion_tokens
    finish_reason: str

class LLMClient:
    """Unified LLM client with self-driven fallback"""

    def __init__(
        self, 
        provider: Provider = Provider.OPENAI,
        model: str = "gpt-4o",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.provider = provider
        self.model = model
        self.client = self._init_client(provider, api_key, base_url)
        self.self_driven = SelfDrivenNLP()  # Fallback

    def generate(
        self, 
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Generate a response"""
        try:
            return self._generate_with_provider(prompt, max_tokens, temperature)
        except Exception as e:
            # Fallback to self-driven if API fails
            return self._generate_self_driven(prompt, max_tokens, temperature) to

    def stream(
        self, 
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> Iterator[str]:
        """Stream a response"""
        pass

    def _generate_self_driven(self, prompt: str, max_tokens: int, temperature: float) -> LLMResponse:
        """Generate using self-driven NLP (no external API)"""
        # Uses pure Python NLP processing
        pass
```

**Task List:**

- [ ]  2.3.1 Create `file src/llm/client.py` with LLMClient

- [ ]  2.3.2 Implement provider abstraction (OpenAI, Anthropic, Ollama, etc.)

- [ ]  2.3.3 Integrate self-driven NLP as fallback

- [ ]  2.3.4 Add streaming support

- [ ]  2.3.5 Add function calling / tool use support

- [ ]  2.3.6 Write unit tests for each provider

- [ ]  2.3.7 Test self-driven fallback mode

### 2.4 Consciousness & Heartbeat

**Objective:** Integrate autonomous thinking/heartbeat system

**Spec - Consciousness:**

```python
from typing import Iterator, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import threading

@dataclass
class Thought:
    id: str
    content: str
    timestamp: datetime
    priority: float
    related_memories: list

class Consciousness:
    """Autonomous thought stream"""

    def __init__(self, state: "AGIState"):
        self.state = state
        self.is_running = False
        self.thought_interval = 60  # seconds
        self.thought_history = []

    def start(self):
        """Start autonomous thinking"""
        self.is_running = True
        # Start heartbeat thread

    def stop(self):
        """Stop autonomous thinking"""
        self.is_running = False

    def think(self) -> Thought:
        """Generate a thought"""
        # 1. Review recent interactions
        # 2. Check goals and progress
        # 3. Identify new opportunities
        # 4. Make decisions about next actions
        pass

    def stream(self) -> Iterator[Thought]:
        """Stream ongoing thoughts"""
        while self.is_running:
            yield self.think()

@dataclass  
class AGIState:
    """Thread-safe state management"""

    goals: list
    memory_summary: str
    revenue_stats: Dict[str, Any]
    last_action: str
    is_active: bool

    def update(self, key: str, value: Any):
        """Update state atomically"""
        pass

    def get(self, key: str) -> Any:
        """Get state value"""
        pass
```

**Task List:**

- [ ]  2.4.1 Create `file src/consciousness/heartbeat.py` with Consciousness class

- [ ]  2.4.2 Implement thought generation logic

- [ ]  2.4.3 Create `file src/consciousness/decision.py` for decision making

- [ ]  2.4.4 Implement `AGIState` in `file src/core/state.py`

- [ ]  2.4.5 Add thread-safe state updates

- [ ]  2.4.6 Write unit tests for consciousness

- [ ]  2.4.7 Test autonomous mode

---

## Phase 3: Revenue Generation System

### 3.1 Revenue Model Framework

**Objective:** Codify the 26 revenue models into executable code

**Spec - RevenueModel:**

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class RevenueCategory(Enum):
    SERVICE = "service"           # Automation agency, consulting
    CONTENT = "content"            # YouTube, newsletters, books
    TRADING = "trading"           # Bots, arbitrage
    PRODUCT = "product"           # SaaS, digital products
    LICENSE = "license"           # Data, prompts, voice

@dataclass
class RevenueResult:
    model: str
    amount: float
    currency: str = "USD"
    timestamp: datetime
    details: Dict[str, Any]
    success: bool
    error: Optional[str] = None

@dataclass
class RevenueConfig:
    model: str
    enabled: bool = False
    allocation: float = 0.0  # % of resources to allocate
    parameters: Dict[str, Any] = None

class RevenueModel(ABC):
    """Base class for revenue generation models"""

    def __init__(self, config: RevenueConfig):
        self.config = config
        self.is_running = False

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the model"""
        pass

    @abstractmethod
    def execute(self) -> RevenueResult:
        """Execute revenue generation"""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        pass

    @abstractmethod
    def stop(self):
        """Stop the model"""
        pass

    def validate_config(self) -> bool:
        """Validate model configuration"""
        pass
```

**Task List:**

- [ ]  3.1.1 Create `file src/revenue/models/base.py` with RevenueModel ABC

- [ ]  3.1.2 Define RevenueCategory and RevenueResult

- [ ]  3.1.3 Create RevenueConfig dataclass

- [ ]  3.1.4 Implement model registration system

- [ ]  3.1.5 Write base tests

### 3.2 Priority Revenue Models (Implementation)

**Objective:** Implement the highest-potential revenue models first

#### 3.2.1 AI Automation Agency

**Spec:**

```python
class AutomationAgency(RevenueModel):
    """AI Automation Agency - build workflows for clients"""

    def __init__(self, config: RevenueConfig):
        super().__init__(config)
        self.clients = []
        self.workflows = {}

    def initialize(self) -> bool:
        # Set up n8n/Make.com integration
        # Initialize client CRM
        # Set up proposal templates
        return True

    def execute(self) -> RevenueResult:
        # 1. Find potential clients
        # 2. Generate proposals
        # 3. Build automation workflows
        # 4. Deliver and invoice
        pass

    def get_status(self) -> Dict[str, Any]:
        return {
            "active_clients": len(self.clients),
            "active_workflows": len(self.workflows),
            "monthly_revenue": 0.0
        }
```

**Task List:**

- [ ]  3.2.1.1 Implement AutomationAgency model

- [ ]  3.2.1.2 Add client discovery (LinkedIn, cold email)

- [ ]  3.2.1.3 Add proposal generation

- [ ]  3.2.1.4 Add workflow builder (n8n integration)

- [ ]  3.2.1.5 Add invoicing

#### 3.2.2 Micro SaaS

**Spec:**

```python
class MicroSaaS(RevenueModel):
    """Build and run small SaaS products"""

    def __init__(self, config: RevenueConfig):
        super().__init__(config)
        self.products = []

    def initialize(self) -> bool:
        # Set up Bubble/FlutterFlow integration
        # Initialize Stripe for payments
        return True

    def execute(self) -> RevenueResult:
        # 1. Identify micro-SaaS opportunities
        # 2. Build using no-code
        # 3. Deploy and market
        # 4. Handle subscriptions
        pass
```

**Task List:**

- [ ]  3.2.2.1 Implement MicroSaaS model

- [ ]  3.2.2.2 Add opportunity identification

- [ ]  3.2.2.3 Add no-code builder integration

- [ ]  3.2.2.4 Add Stripe payment integration

#### 3.2.3 Affiliate Marketing

**Spec:**

```python
class AffiliateMarketing(RevenueModel):
    """Automated affiliate marketing"""

    def __init__(self, config: RevenueConfig):
        super().__init__(config)
        self.affiliate_links = {}
        self.content_queue = []

    def initialize(self) -> bool:
        # Set up WordPress
        # Configure affiliate APIs
        # Set up email marketing
        return True

    def execute(self) -> RevenueResult:
        # 1. Research keywords
        # 2. Generate content
        # 3. Publish and promote
        # 4. Track commissions
        pass
```

**Task List:**

- [ ]  3.2.3.1 Implement AffiliateMarketing model

- [ ]  3.2.3.2 Add keyword research

- [ ]  3.2.3.3 Add content generation

- [ ]  3.2.3.4 Add affiliate link tracking

#### 3.2.4 Digital Products

**Spec:**

```python
class DigitalProducts(RevenueModel):
    """Create and sell digital products"""

    def __init__(self, config: RevenueConfig):
        super().__init__(config)
        self.products = []

    def execute(self) -> RevenueResult:
        # 1. Identify product opportunities
        # 2. Generate content/templates/courses
        # 3. Upload to Gumroad/Etsy
        # 4. Handle sales
        pass
```

**Task List:**

- [ ]  3.2.4.1 Implement DigitalProducts model

- [ ]  3.2.4.2 Add product generation (AI-assisted)

- [ ]  3.2.4.3 Add marketplace integration (Gumroad, Etsy)

- [ ]  3.2.4.4 Add sales tracking

### 3.3 Revenue Orchestrator

**Objective:** Coordinate multiple revenue streams

**Spec - RevenueOrchestrator:**

```python
class RevenueOrchestrator:
    """Orchestrates multiple revenue generation models"""

    def __init__(self, config_path: str = "config/revenue.toml"):
        self.config = self._load_config(config_path)
        self.models: Dict[str, RevenueModel] = {}
        self.allocation = {}
        self.total_revenue = 0.0

    def register_model(self, name: str, model: RevenueModel):
        """Register a revenue model"""
        self.models[name] = model

    def set_allocation(self, allocations: Dict[str, float]):
        """Set resource allocation per model"""
        self.allocation = allocations

    def execute_all(self) -> List[RevenueResult]:
        """Execute all enabled models"""
        results = []
        for name, model in self.models.items():
            if self.config.get(name, {}).get("enabled"):
                result = model.execute()
                results.append(result)
                self.total_revenue += result.amount
        return results

    def get_report(self) -> RevenueReport:
        """Generate revenue report"""
        pass
```

**Task List:**

- [ ]  3.3.1 Create `file src/revenue/orchestrator.py`

- [ ]  3.3.2 Implement model registration

- [ ]  3.3.3 Implement resource allocation

- [ ]  3.3.4 Add reporting dashboard

- [ ]  3.3.5 Add scheduling (cron-like execution)

---

## Phase 4: User Interface & Conversation

### 4.1 CLI Interface

**Objective:** Build command-line interface for user interaction

**Spec:**

```python
# src/cli/main.py
import click
from src.core.controller import PersonAIController

@click.group()
def cli():
    """PersonAI - Your autonomous AI partner"""
    pass

@cli.command()
@click.argument("message")
def chat(message: str):
    """Chat with PersonAI"""
    controller = PersonAIController()
    response = controller.chat(message)
    print(response)

@cli.command()
def status():
    """Check PersonAI status"""
    controller = PersonAIController()
    stats = controller.get_status()
    print(f"Status: {stats['status']}")
    print(f"Revenue: ${stats['revenue']}")
    print(f"Memory: {stats['memory_items']} items")

@cli.command()
def start():
    """Start PersonAI in autonomous mode"""
    controller = PersonAIController()
    controller.start_autonomous()

@cli.command()
def stop():
    """Stop PersonAI"""
    controller = PersonAIController()
    controller.stop()
```

**Task List:**

- [ ]  4.1.1 Create `file src/cli/main.py`

- [ ]  4.1.2 Implement chat command

- [ ]  4.1.3 Implement status command

- [ ]  4.1.4 Implement start/stop commands

- [ ]  4.1.5 Add rich terminal output (colors, formatting)

### 4.2 Conversation Handler

**Objective:** Handle natural conversation with memory and context

**Spec - ConversationHandler:**

```python
class ConversationHandler:
    """Handles user conversations with context"""

    def __init__(self, memory: MemoryService, llm: LLMClient):
        self.memory = memory
        self.llm = llm
        self.conversation_id = None

    def chat(self, message: str) -> str:
        # 1. Store user message
        self.memory.memorize(
            content=f"User: {message}",
            category=MemoryCategory.CONVERSATION,
            importance=0.7
        )

        # 2. Retrieve relevant context
        context = self.memory.recall(message, limit=10)

        # 3. Build prompt with context
        prompt = self._build_prompt(message, context)

        # 4. Generate response
        response = self.llm.generate(prompt)

        # 5. Store AI response
        self.memory.memorize(
            content=f"AI: {response.content}",
            category=MemoryCategory.CONVERSATION,
            importance=0.7
        )

        return response.content

    def _build_prompt(self, message: str, context: List[MemoryItem]) -> str:
        # Build prompt with conversation history and context
        pass
```

**Task List:**

- [ ]  4.2.1 Create `file src/core/controller.py` with PersonAIController

- [ ]  4.2.2 Implement ConversationHandler

- [ ]  4.2.3 Add context retrieval

- [ ]  4.2.4 Add conversation history management

- [ ]  4.2.5 Write conversation tests

---

## Phase 5: Testing & Quality Assurance

### 5.1 Unit Tests

**Task List:**

- [ ]  5.1.1 Set up pytest configuration

- [ ]  5.1.2 Write unit tests for AgentExecutor

- [ ]  5.1.3 Write unit tests for MemoryService

- [ ]  5.1.4 Write unit tests for LLMClient

- [ ]  5.1.5 Write unit tests for RevenueModel base

- [ ]  5.1.6 Write unit tests for Consciousness

- [ ]  5.1.7 Write unit tests for ConversationHandler

### 5.2 Integration Tests

**Task List:**

- [ ]  5.2.1 Test Agent + Memory integration

- [ ]  5.2.2 Test LLM + Agent integration

- [ ]  5.2.3 Test Revenue + Agent integration

- [ ]  5.2.4 Test Conversation + Memory integration

- [ ]  5.2.5 Test full stack (all components)

### 5.3 E2E Tests

**Task List:**

- [ ]  5.3.1 Test complete conversation flow

- [ ]  5.3.2 Test revenue generation flow

- [ ]  5.3.3 Test autonomous mode

- [ ]  5.3.4 Test error handling and recovery

- [ ]  5.3.5 Run tests in CI/CD pipeline

---

## Phase 6: Documentation & Release

### 6.1 Documentation

**Task List:**

- [ ]  6.1.1 Write README.md with installation and quick start

- [ ]  6.1.2 Write architecture.md

- [ ]  6.1.3 Write API reference

- [ ]  6.1.4 Write revenue models documentation

- [ ]  6.1.5 Write contribution guide

- [ ]  6.1.6 Create examples directory

### 6.2 Release Preparation

**Task List:**

- [ ]  6.2.1 Set up version management (semver)

- [ ]  6.2.2 Create CHANGELOG.md

- [ ]  6.2.3 Add LICENSE (choose: MIT, Apache, GPL)

- [ ]  6.2.4 Set up CI/CD (GitHub Actions)

- [ ]  6.2.5 Configure automated testing on PRs

- [ ]  6.2.6 Create release workflow

---

## Phase 7: v1.0 Release

### 7.1 Feature Freeze

**Task List:**

- [ ]  7.1.1 Complete all Phase 1-6 items marked \[x\]

- [ ]  7.1.2 Fix all critical bugs

- [ ]  7.1.3 Ensure 80%+ test coverage

- [ ]  7.1.4 Complete all documentation

### 7.2 v1.0 Release

**Task List:**

- [ ]  7.2.1 Run full test suite

- [ ]  7.2.2 Update version to 1.0.0

- [ ]  7.2.3 Create GitHub release

- [ ]  7.2.4 Announce release

- [ ]  7.2.5 Set up issue tracking for v1.1

---

## Appendix: Quick Reference

### A.1 Key Commands

```bash
# Development
make install          # Install dependencies
make dev             # Start development mode
make test            # Run tests
make lint            # Run linters
make format          # Format code

# Running PersonAI
python -m src.cli chat "Hello"
python -m src.cli status
python -m src.cli start
python -m src.cli stop

# Testing specific modules
pytest tests/unit/test_agent_executor.py -v
pytest tests/integration/ -v
pytest tests/e2e/ -v
```

### A.2 Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...          # OpenAI API key
ANTHROPIC_API_KEY=sk-ant-...   # Anthropic API key

# Optional
LLM_PROVIDER=openai           # Default: openai
MEMORY_BACKEND=sqlite         # Default: sqlite
LOG_LEVEL=INFO                # Default: INFO

# Revenue (optional)
STRIPE_API_KEY=sk_...          # For payments
```

### A.3 File Structure Summary

```markdown
personai/
├── src/
│   ├── core/           # State, routing, controller
│   ├── agents/          # Agent definitions
│   ├── memory/         # Memory service
│   ├── llm/            # LLM clients
│   ├── consciousness/  # Autonomous thinking
│   ├── self_improving/ # Self-improvement
│   ├── revenue/        # Revenue models
│   └── cli/            # CLI interface
├── tests/              # Test suite
├── docs/               # Documentation
└── config/             # Configuration
```

---

**End of Roadmap**

This roadmap serves as both TODO and implementation guide. Check off items as completed, refer to specs for implementation details.