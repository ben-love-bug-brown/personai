"""
Chat API

REST API endpoints for PersonAI chat functionality.
"""

import os
import json
import uuid
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ..llm import get_llm_client
from ..memory import get_memory, MemoryCategory
from ..core.state import get_state
from ..self_improving.roadmap import get_roadmap
from ..self_improving.runner import get_runner
from ..revenue import create_orchestrator


class MessageRole(Enum):
    """Message roles"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class ChatMessage:
    """A chat message"""
    role: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatSession:
    """A chat session"""
    id: str
    created_at: str
    messages: List[ChatMessage] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ChatAPI:
    """
    PersonAI Chat API
    
    Provides chat functionality with memory and self-improvement integration.
    """
    
    def __init__(self):
        self.llm = get_llm_client()
        self.memory = get_memory()
        self.state = get_state()
        self.roadmap = get_roadmap()
        self.runner = get_runner()
        self.orchestrator = create_orchestrator()
        
        self.sessions: Dict[str, ChatSession] = {}
        self.current_session_id: Optional[str] = None
    
    def create_session(self, context: Dict[str, Any] = None) -> str:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())[:12]
        session = ChatSession(
            id=session_id,
            created_at=datetime.now().isoformat(),
            context=context or {},
            messages=[
                ChatMessage(
                    role="system",
                    content="You are PersonAI, a self-improving autonomous AI partner. "
                            "You are helpful, concise, and focused on continuous improvement."
                )
            ]
        )
        self.sessions[session_id] = session
        self.current_session_id = session_id
        return session_id
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a session by ID"""
        return self.sessions.get(session_id)
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions"""
        return [
            {
                "id": s.id,
                "created_at": s.created_at,
                "message_count": len(s.messages),
                "context": s.context
            }
            for s in self.sessions.values()
        ]
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            if self.current_session_id == session_id:
                self.current_session_id = None
            return True
        return False
    
    def chat(
        self,
        message: str,
        session_id: Optional[str] = None,
        use_memory: bool = True,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Chat with PersonAI
        
        Args:
            message: The user's message
            session_id: Optional session ID to continue
            use_memory: Whether to use memory for context
            stream: Whether to stream the response
            
        Returns:
            Dict with response, session_id, and metadata
        """
        # Use existing session or create new one
        if session_id and session_id in self.sessions:
            session = self.sessions[session_id]
        else:
            session_id = self.create_session()
            session = self.sessions[session_id]
        
        # Add user message
        session.messages.append(ChatMessage(role="user", content=message))
        
        # Build context from multiple sources
        context_parts = []
        
        # Add conversation history context (last 3 messages)
        recent_msgs = [m for m in session.messages[-5:] if m.role != "system"]
        if recent_msgs:
            context_parts.append("Recent conversation:")
            for m in recent_msgs[-3:]:
                context_parts.append(f"  {m.role}: {m.content[:80]}")
        
        # Add relevant memories if enabled
        if use_memory:
            memories = self.memory.recall(message, limit=3)
            if memories:
                context_parts.append("Relevant memories:")
                for m in memories:
                    context_parts.append(f"- {m.content[:100]}")
        
        # Add roadmap context for awareness
        next_items = self.roadmap.get_next_items(2)
        if next_items:
            context_parts.append("Current priorities:")
            for item in next_items:
                context_parts.append(f"- {item.task[:80]}")
        
        # Build the full prompt with rich context
        system_context = "\n".join(context_parts) if context_parts else ""
        
        if system_context:
            full_prompt = f"""Current context:
{system_context}

User: {message}

Respond as PersonAI - be concise, helpful, and contextually aware."""
        else:
            full_prompt = message
        
        # Generate response
        response = self.llm.generate(full_prompt)
        response_content = response.content
        
        # Add assistant message
        session.messages.append(ChatMessage(
            role="assistant",
            content=response_content,
            metadata={
                "model": response.model,
                "usage": response.usage
            }
        ))
        
        # Store important info in memory
        if use_memory and len(message.split()) > 5:
            self.memory.memorize(
                content=f"User discussed: {message[:200]}",
                category=MemoryCategory.CONVERSATION,
                importance=0.3
            )
        
        return {
            "session_id": session_id,
            "response": response_content,
            "model": response.model,
            "usage": response.usage,
            "message_count": len(session.messages),
            "context_sources": {
                "conversation_history": len(recent_msgs),
                "memories": len(memories) if use_memory else 0,
                "roadmap_items": len(next_items)
            }
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            "sessions": len(self.sessions),
            "current_session": self.current_session_id,
            "llm_provider": "self_driven_real_mode",
            "self_improver_active": self.runner.is_running,
            "cycles_completed": self.runner.cycles_completed,
            "roadmap_progress": self.roadmap.get_progress(),
            "revenue_status": self.orchestrator.get_status()
        }
    
    def run_self_improvement(self) -> Dict[str, Any]:
        """Run a self-improvement cycle"""
        result = self.runner.run_cycle()
        return {
            "cycle_id": result.get("cycle_id"),
            "actions_applied": result.get("actions_applied", 0),
            "tests_passed": result.get("tests_passed", False),
            "duration": result.get("duration_seconds", 0)
        }
    
    def generate_revenue(self) -> Dict[str, Any]:
        """Generate revenue from all models"""
        results = self.orchestrator.execute_all()
        return {
            "total": sum(r.amount for r in results),
            "results": [
                {
                    "model": r.model,
                    "amount": r.amount,
                    "success": r.success,
                    "error": r.error
                }
                for r in results
            ]
        }


# Global API instance
_api: Optional[ChatAPI] = None


def get_chat_api() -> ChatAPI:
    """Get the global chat API"""
    global _api
    if _api is None:
        _api = ChatAPI()
    return _api


def create_chat_app():
    """Create a FastAPI app (optional - for future HTTP server)"""
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel
        
        app = FastAPI(title="PersonAI API")
        api = get_chat_api()
        
        class ChatRequest(BaseModel):
            message: str
            session_id: Optional[str] = None
            use_memory: bool = True
        
        class SessionCreate(BaseModel):
            context: Optional[Dict[str, Any]] = None
        
        @app.post("/chat")
        async def chat(req: ChatRequest):
            return api.chat(req.message, req.session_id, req.use_memory)
        
        @app.post("/sessions")
        def create_session(req: SessionCreate):
            return {"session_id": api.create_session(req.context)}
        
        @app.get("/sessions")
        def list_sessions():
            return {"sessions": api.list_sessions()}
        
        @app.get("/status")
        def status():
            return api.get_status()
        
        @app.post("/improve")
        def improve():
            return api.run_self_improvement()
        
        @app.post("/revenue")
        def revenue():
            return api.generate_revenue()
        
        return app
        
    except ImportError:
        return None
