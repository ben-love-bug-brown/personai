"""
LLM Client - Self-Driven Zo AI Bridge

This module provides a direct bridge to Zo's native AI capabilities.
NO FALLBACK - pure forward connection to Zo LLM.

The bridge connects to the local PersonAI NLP service which forwards
to Zo's AI for natural, context-aware responses.
"""

import re
import os
import json
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Response from LLM"""
    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: str


class ZoAIBridge:
    """
    Direct bridge to Zo's AI - NO FALLBACK.
    
    This module provides autonomous AI capabilities by directly bridging
    to Zo's LLM. No external providers, no fallback - pure Zo integration.
    """
    
    def __init__(self, service_url: str = "http://localhost:8765"):
        self.service_url = service_url
        self.timeout = 30
        
    def _call_zo_ai(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        Direct call to Zo AI via local service.
        NO FALLBACK - fails if service unavailable.
        """
        data = json.dumps({"message": prompt}).encode('utf-8')
        req = urllib.request.Request(
            f"{self.service_url}/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=self.timeout) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('response', '')


class SelfDrivenNLP:
    """
    Self-driven Real-Mode NLP - Direct Zo Bridge Only
    
    This is the main NLP class that provides autonomous AI capabilities
    by directly bridging to Zo's LLM. NO FALLBACK - pure connection.
    """

    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = """You are PersonAI, a self-improving autonomous AI partner.
You are helpful, concise, and focused on continuous improvement.
You have memory of past conversations and can learn from them.
You connect directly to Zo's AI for natural responses."""
        
        self.bridge = ZoAIBridge()
        
        self._learned_patterns: Dict[str, str] = {}
        self._pattern_file = "/home/workspace/personai/data/learned_patterns.json"
        self._load_patterns()

    def _load_patterns(self):
        """Load learned patterns from disk"""
        if os.path.exists(self._pattern_file):
            try:
                with open(self._pattern_file, 'r') as f:
                    self._learned_patterns = json.load(f)
            except Exception:
                pass

    def _save_patterns(self):
        """Save learned patterns to disk"""
        os.makedirs(os.path.dirname(self._pattern_file), exist_ok=True)
        with open(self._pattern_file, 'w') as f:
            json.dump(self._learned_patterns, f, indent=2)

    def _learn_pattern(self, query: str, response: str):
        """Learn a new response pattern from interaction"""
        words = query.lower().split()
        key_words = [w for w in words if len(w) > 3][:3]
        if key_words:
            pattern_key = "_".join(sorted(key_words))
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
        """Extract latest user utterance from wrapped prompts."""
        matches = re.findall(r"(?:^|\n)User:\s*(.+?)(?=\n\n|\n[A-Z][^:]*:|$)", prompt, flags=re.DOTALL)
        if matches:
            return matches[-1].strip()
        return prompt.strip()

    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate a response using direct Zo AI bridge"""
        self.conversation_history.append({"role": "user", "content": prompt})
        
        intent_text = self._extract_user_intent_text(prompt)
        
        # Check learned patterns first (cache optimization)
        learned_response = self._get_learned_response(intent_text)
        
        if learned_response:
            response_content = learned_response
        else:
            # Direct bridge to Zo AI - NO FALLBACK
            response_content = self.bridge._call_zo_ai(prompt)
            
            # Learn from this interaction
            if response_content:
                self._learn_pattern(intent_text, response_content)
        
        self.conversation_history.append({"role": "assistant", "content": response_content})
        
        # Keep history manageable
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-50:]
        
        return LLMResponse(
            content=response_content,
            model="zo_ai_bridge",
            usage={
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(response_content.split())
            },
            finish_reason="stop"
        )

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()


class LLMClient:
    """
    Unified LLM client - Direct Zo Bridge Only
    
    Uses the direct Zo AI Bridge - NO FALLBACK.
    """

    def __init__(self):
        self.model = "zo_ai_bridge"
        self.self_driven = SelfDrivenNLP()

    def generate(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Generate a response using direct Zo bridge"""
        return self.self_driven.generate(prompt, max_tokens=max_tokens, temperature=temperature)


_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get the global LLM client (direct Zo bridge only)"""
    global _client
    if _client is None:
        _client = LLMClient()
    return _client
