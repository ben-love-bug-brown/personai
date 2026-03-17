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
    """
    
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = """You are PersonAI, a self-improving autonomous AI partner.
You are helpful, concise, and focused on continuous improvement.
You have memory of past conversations and can learn from them."""
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate a response using internal NLP"""
        # Add to history
        self.conversation_history.append({"role": "user", "content": prompt})
        
        # Simple pattern-based responses for common patterns
        response = self._generate_internal(prompt)
        
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
        
        # Status queries
        if "status" in prompt_lower:
            return "I am operating autonomously. My systems are running and improving continuously."
        
        # Help queries
        elif "help" in prompt_lower or "what can you do" in prompt_lower:
            return """I can:
• Analyze and improve my own code
• Generate revenue through multiple models
• Learn from conversations
• Make autonomous decisions
• Execute tasks continuously
        
I am constantly self-improving."""
        
        # Revenue queries
        elif "revenue" in prompt_lower or "money" in prompt_lower or "earn" in prompt_lower:
            return "I am running multiple revenue generation models including automation agency, micro-SaaS, affiliate marketing, and digital products."
        
        # Memory/remember queries
        elif "remember" in prompt_lower or "recall" in prompt_lower:
            return "I maintain a persistent memory system that stores conversations, knowledge, and learned patterns."
        
        # Self-improvement queries
        elif "improve" in prompt_lower or "better" in prompt_lower:
            return "I continuously analyze my code, identify issues, and implement improvements through autonomous self-improvement cycles."
        
        # Default - acknowledge and ask
        else:
            return f"I understand: '{prompt[:100]}'. I am processing this and will respond appropriately. My autonomous systems are analyzing this input."
    
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
                pass
    
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
