"""
LLM Client

Unified LLM client with self-driven NLP fallback.
"""

import os
import re
from typing import Optional, List, Dict, Any, Iterator
from dataclasses import dataclass
from enum import Enum
import json


class Provider(Enum):
    """LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    GROK = "grok"
    OPENROUTER = "openrouter"
    SELF_DRIVEN = "self_driven"


@dataclass
class LLMResponse:
    """Response from LLM"""
    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: str


class SelfDrivenNLP:
    """
    Self-driven NLP - no external API required.
    
    Uses rule-based and pattern-matching approaches for core functionality.
    Now with pattern learning for improved responses.
    """
    
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = """You are PersonAI, a self-improving autonomous AI partner.
You are helpful, concise, and focused on continuous improvement.
You have memory of past conversations and can learn from them."""
        
        # Pattern learning: learned response patterns
        self._learned_patterns: Dict[str, str] = {}
        self._pattern_file = "/home/workspace/personai/data/learned_patterns.json"
        self._load_patterns()
    
    def _load_patterns(self):
        """Load learned patterns from disk"""
        import os
        if os.path.exists(self._pattern_file):
            try:
                with open(self._pattern_file, 'r') as f:
                    self._learned_patterns = json.load(f)
            except Exception:
                pass
    
    def _save_patterns(self):
        """Save learned patterns to disk"""
        import os
        os.makedirs(os.path.dirname(self._pattern_file), exist_ok=True)
        with open(self._pattern_file, 'w') as f:
            json.dump(self._learned_patterns, f, indent=2)
    
    def _learn_pattern(self, query: str, response: str):
        """Learn a new response pattern from interaction"""
        # Extract key words as pattern key
        words = query.lower().split()
        key_words = [w for w in words if len(w) > 3][:3]
        if key_words:
            pattern_key = "_".join(sorted(key_words))
            # Only learn if response was substantive
            if len(response) > 20:
                self._learned_patterns[pattern_key] = response
                self._save_patterns()
    
    def _get_learned_response(self, query: str) -> Optional[str]:
        """Get response from learned patterns"""
        words = query.lower().split()
        key_words = [w for w in words if len(w) > 3][:3]
        if key_words:
            pattern_key = "_".join(sorted(key_words))
            return self._learned_patterns.get(pattern_key)
        return None

    def _extract_user_intent_text(self, prompt: str) -> str:
        """Extract latest user utterance from wrapped prompts when available."""
        matches = re.findall(r"(?:^|\n)User:\s*(.+?)(?=\n\n|\n[A-Z][^\n]*:|$)", prompt, flags=re.DOTALL)
        if matches:
            return matches[-1].strip()
        return prompt.strip()
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate a response using internal NLP"""
        # Add to history
        self.conversation_history.append({"role": "user", "content": prompt})
        
        # Check for learned pattern first
        intent_text = self._extract_user_intent_text(prompt)
        learned = self._get_learned_response(intent_text)
        
        # Simple pattern-based responses for common patterns
        response = self._generate_internal(prompt)
        
        # Learn from this interaction
        self._learn_pattern(intent_text, response)
        
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return LLMResponse(
            content=response,
            model="self_driven",
            usage={
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(response.split())
            },
            finish_reason="stop"
        )
    
    def _generate_internal(self, prompt: str) -> str:
        """Generate response using internal processing"""
        prompt_lower = prompt.lower()
        intent_text = self._extract_user_intent_text(prompt)
        intent_lower = intent_text.lower()
        
        # Check memory context first
        memory_context = ""
        if hasattr(self, 'memory') and self.memory:
            try:
                memories = self.memory.recall(prompt, limit=2)
                if memories:
                    memory_context = " [From memory: " + "; ".join([m.content[:50] for m in memories]) + "]"
            except Exception as e:
                # Log error but continue without memory context
                import logging
                logging.debug(f"Memory recall failed: {e}")
        
        # Status queries
        if "status" in intent_lower:
            return "I am operating autonomously. My systems are running and improving continuously." + memory_context
        
        # Help queries
        elif "help" in intent_lower or "what can you do" in intent_lower:
            return """I can:
• Analyze and improve my own code
• Generate revenue through multiple models
• Learn from conversations
• Make autonomous decisions
• Execute tasks continuously
• Provide chat conversation via API

I am constantly self-improving.""" + memory_context
        
        # Revenue queries
        elif "revenue" in intent_lower or "money" in intent_lower or "earn" in intent_lower:
            return "I am running multiple revenue generation models including automation agency, micro-SaaS, affiliate marketing, digital products, AI consulting, content creation, and trading bots." + memory_context
        
        # Memory/remember queries
        elif "remember" in intent_lower or "recall" in intent_lower:
            return "I maintain a persistent memory system that stores conversations, knowledge, and learned patterns." + memory_context
        
        # Self-improvement queries
        elif "improve" in intent_lower or "better" in intent_lower:
            return "I continuously analyze my code, identify issues, and implement improvements through autonomous self-improvement cycles. My self-improvement executor detects bugs and applies fixes safely." + memory_context
        
        # API queries
        elif "api" in intent_lower or "/chat" in intent_lower:
            return "I have a REST API at src/api/chat.py. Use get_chat_api().chat(message) to chat, get_chat_api().get_status() for system status." + memory_context
        
        # What are you queries
        elif "what are you" in intent_lower or "who are you" in intent_lower:
            return "I am PersonAI, a self-directed autonomous AI partner. I can think, learn, improve myself, generate revenue, and have conversations. I operate continuously." + memory_context
        
        # Default - acknowledge and respond thoughtfully
        else:
            response = f"I understand: '{intent_text[:100]}'. "
            if memory_context:
                response += f"I recall relevant context:{memory_context} "
            response += "I am processing this and will respond appropriately. My autonomous systems are analyzing this input."
            return response
    
    def stream(self, prompt: str, **kwargs) -> Iterator[str]:
        """Stream response word by word"""
        response = self.generate(prompt, **kwargs)
        words = response.content.split()
        for word in words:
            yield word + " "
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()


class LLMClient:
    """
    Unified LLM client with fallback to self-driven.
    """
    
    def __init__(
        self,
        provider: Provider = Provider.SELF_DRIVEN,
        model: str = "gpt-4o",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.provider = provider
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.base_url = base_url
        self.self_driven = SelfDrivenNLP()
        self._client = None
        
        if provider != Provider.SELF_DRIVEN:
            self._init_provider_client()
    
    def _init_provider_client(self):
        """Initialize the external provider client"""
        if self.provider == Provider.OPENAI:
            try:
                import openai
                self._client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
            except ImportError:
                pass  # Handle exception
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Generate a response"""
        try:
            if self.provider == Provider.SELF_DRIVEN or not self._client:
                return self.self_driven.generate(prompt, max_tokens=max_tokens, temperature=temperature)
            
            # Try external provider
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                model=response.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens
                },
                finish_reason=response.choices[0].finish_reason
            )
        except Exception as e:
            # Fallback to self-driven
            return self.self_driven.generate(prompt, max_tokens=max_tokens, temperature=temperature)
    
    def stream(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> Iterator[str]:
        """Stream a response"""
        if self.provider == Provider.SELF_DRIVEN or not self._client:
            yield from self.self_driven.stream(prompt, max_tokens=max_tokens, temperature=temperature)
            return
        
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception:
            # Fallback
            yield from self.self_driven.stream(prompt, max_tokens=max_tokens, temperature=temperature)


# Global client instance
_client: Optional[LLMClient] = None


def get_llm_client(
    provider: Provider = Provider.SELF_DRIVEN,
    model: str = "gpt-4o",
    api_key: Optional[str] = None
) -> LLMClient:
    """Get the global LLM client"""
    global _client
    if _client is None:
        _client = LLMClient(provider, model, api_key)
    return _client
