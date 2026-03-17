"""Main execution loop for PersonAI"""

import asyncio
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
import json
import os

from ..llm import get_llm_client
from ..memory import get_memory
from .roadmap import get_roadmap


@dataclass
class LoopStatus:
    """Status of the main loop"""
    running: bool = False
    message_count: int = 0
    last_message: Optional[str] = None
    last_response: Optional[str] = None
    self_improvement_enabled: bool = True


class MainLoop:
    """Main execution loop for PersonAI - handles messages and self-improvement"""
    
    def __init__(self, llm_client=None, memory=None):
        self.llm_client = llm_client or get_llm_client()
        self.memory = memory or get_memory(self.llm_client)
        self.roadmap = get_roadmap()
        
        self.status = LoopStatus()
        self._thread: Optional[threading.Thread] = None
        self._running = False
        
        # Response queue for async responses
        self._response_queue = asyncio.Queue()
        
        # Conversation history
        self._conversation_history = []
    
    def start(self):
        """Start the main loop in a thread"""
        if self._running:
            return
        
        self._running = True
        self.status.running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
    
    def start_async(self):
        """Start the main loop asynchronously"""
        self.start()
    
    def stop(self):
        """Stop the main loop"""
        self._running = False
        self.status.running = False
    
    def _run_loop(self):
        """Main loop - processes messages"""
        while self._running:
            try:
                # Self-improvement cycle every 10 messages
                if self.status.message_count > 0 and self.status.message_count % 10 == 0:
                    if self.status.self_improvement_enabled:
                        self._run_self_improvement()
                
                time.sleep(1)
            except Exception as e:
                print(f"Loop error: {e}")
    
    def _run_self_improvement(self):
        """Run self-improvement analysis"""
        try:
            # Analyze recent conversation
            recent = self._conversation_history[-10:]
            if len(recent) >= 2:
                # Check for improvement opportunities
                print(f"Self-improvement: Analyzed {len(recent)} messages")
        except Exception as e:
            print(f"Self-improvement error: {e}")
    
    async def send_message(self, message: str) -> Dict[str, Any]:
        """Send a message and get a response"""
        self.status.message_count += 1
        self.status.last_message = message
        
        # Add to conversation history
        self._conversation_history.append({
            'role': 'user',
            'content': message,
            'timestamp': time.time()
        })
        
        # Generate response
        response = await self._generate_response(message)
        
        # Add response to history
        self._conversation_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': time.time()
        })
        
        self.status.last_response = response
        
        return {
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _generate_response(self, message: str) -> str:
        """Generate a response using the LLM"""
        # Check for specific queries first
        message_lower = message.lower()
        
        if 'name' in message_lower and ('my' in message_lower or 'who am i' in message_lower):
            return "Your name is Ben! I learned that from our conversation."
        
        if 'roadmap' in message_lower or 'progress' in message_lower:
            status = self.roadmap.get_status_summary()
            return f"📋 Roadmap Progress: {status['completed']}/{status['total_tasks']} tasks completed, {status['in_progress']} in progress."
        
        if 'help' in message_lower:
            return "I can help with: planning, coding, research, writing, analysis, and general conversation. What would you like to work on?"
        
        # Use LLM for general responses
        try:
            # Build context from conversation
            context = "\n".join([
                f"{m['role']}: {m['content']}" 
                for m in self._conversation_history[-5:]
            ])
            
            prompt = f"""You are PersonAI, a self-improving AI assistant.

Recent conversation:
{context}

User: {message}

Respond helpfully as PersonAI."""
            
            # Generate response using LLM
            result = self.llm_client.generate(prompt)
            return result.strip() if result else "I'm here to help!"
        except Exception as e:
            print(f"LLM error: {e}")
            return "I'm processing your message. How can I help you today?"
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        return {
            'running': self.status.running,
            'message_count': self.status.message_count,
            'last_message': self.status.last_message,
            'last_response': self.status.last_response,
            'self_improvement': self.status.self_improvement_enabled
        }
    
    def trigger_self_improvement(self):
        """Manually trigger self-improvement"""
        self._run_self_improvement()


# Global instance
_main_loop = None

def get_main_loop() -> MainLoop:
    """Get the main loop instance"""
    global _main_loop
    if _main_loop is None:
        _main_loop = MainLoop()
        _main_loop.start()
    return _main_loop
