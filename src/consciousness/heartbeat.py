"""
Consciousness & Heartbeat

Autonomous thought stream and decision making.
"""

import time
import threading
from typing import Iterator, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import uuid


class ThoughtPriority(Enum):
    """Priority levels for thoughts"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


@dataclass
class Thought:
    """A single thought"""
    id: str
    content: str
    timestamp: datetime
    priority: ThoughtPriority
    related_goals: list
    related_memories: list
    action_taken: Optional[str] = None


class Consciousness:
    """
    Autonomous thought stream.
    
    Continuously generates thoughts, makes decisions, and drives action.
    """
    
    def __init__(self, state=None, memory=None):
        self.state = state
        self.memory = memory
        self.is_running = False
        self.thought_interval = 60  # seconds
        self.thought_history = []
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
    
    def start(self):
        """Start autonomous thinking"""
        if self.is_running:
            return
        
        self.is_running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_think_loop, daemon=True)
        self._thread.start()
        if self.state:
            self.state.update('consciousness_active', True)
    
    def stop(self):
        """Stop autonomous thinking"""
        self.is_running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        if self.state:
            self.state.update('consciousness_active', False)
    
    def _run_think_loop(self):
        """Main thinking loop"""
        while not self._stop_event.is_set():
            try:
                thought = self.think()
                self.thought_history.append(thought)
                
                # Keep last 100 thoughts
                if len(self.thought_history) > 100:
                    self.thought_history = self.thought_history[-100:]
                
            except Exception as e:
                # Handle exception - log for debugging
    # Handle exception
            
            # Wait for next thought cycle
            self._stop_event.wait(self.thought_interval)
    
    def think(self) -> Thought:
        """Generate a thought"""
        # Analyze current situation
        situation = self._analyze_situation()
        
        # Generate thought based on situation
        thought = self._generate_thought(situation)
        
        # Try to take action if needed
        action = self._consider_action(thought)
        if action:
            thought.action_taken = action
        
        if self.state:
            self.state.update('last_thought', thought.content[:200])
        
        return thought
    
    def _analyze_situation(self) -> Dict[str, Any]:
        """Analyze current situation"""
        state_data = self.state.get_all() if self.state else {}
        
        return {
            'state': state_data.get('agent_state', 'unknown'),
            'revenue_today': state_data.get('revenue_today', 0),
            'active_goals': state_data.get('goals', []),
            'improvements_made': state_data.get('improvements_made', 0)
        }
    
    def _generate_thought(self, situation: Dict[str, Any]) -> Thought:
        """Generate a thought based on situation"""
        # Priority-based thinking
        if situation.get('revenue_today', 0) < 10:
            return Thought(
                id=str(uuid.uuid4()),
                content="Revenue is low. Need to explore new revenue opportunities.",
                timestamp=datetime.now(),
                priority=ThoughtPriority.HIGH,
                related_goals=[{'goal': 'Increase revenue'}],
                related_memories=[]
            )
        
        # Default - check for improvement opportunities
        return Thought(
            id=str(uuid.uuid4()),
            content="Analyzing system for improvement opportunities.",
            timestamp=datetime.now(),
            priority=ThoughtPriority.MEDIUM,
            related_goals=[],
            related_memories=[]
        )
    
    def _consider_action(self, thought: Thought) -> Optional[str]:
        """Consider what action to take based on thought"""
        if thought.priority == ThoughtPriority.CRITICAL:
            return f"CRITICAL: {thought.content}"
        return None
    
    def stream(self) -> Iterator[Thought]:
        """Stream ongoing thoughts"""
        while self.is_running:
            yield self.think()
            time.sleep(self.thought_interval)
    
    def get_thought_history(self, limit: int = 10) -> list:
        """Get recent thoughts"""
        return self.thought_history[-limit:]
    
    def get_status(self) -> Dict[str, Any]:
        """Get consciousness status"""
        return {
            'is_running': self.is_running,
            'thought_interval': self.thought_interval,
            'thoughts_generated': len(self.thought_history),
            'last_thought': self.thought_history[-1].content[:100] if self.thought_history else None
        }


# Global consciousness instance
_consciousness: Optional[Consciousness] = None


def get_consciousness() -> Consciousness:
    """Get the global consciousness"""
    global _consciousness
    if _consciousness is None:
        _consciousness = Consciousness()
    return _consciousness
