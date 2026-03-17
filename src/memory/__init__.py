"""
Memory Service

Unified memory system for PersonAI using memU integration.
"""

import json
import os
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class MemoryCategory(Enum):
    """Memory categories"""
    CONVERSATION = "conversation"
    KNOWLEDGE = "knowledge"
    PROFILE = "profile"
    SKILL = "skill"
    TOOL = "tool"
    BEHAVIOR = "behavior"
    EVENT = "event"
    REVENUE = "revenue"
    SELF_IMPROVEMENT = "self_improvement"


@dataclass
class MemoryItem:
    """A single memory item"""
    id: str
    content: str
    category: MemoryCategory
    importance: float  # 0.0 - 1.0
    created_at: datetime
    accessed_at: datetime
    access_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'content': self.content,
            'category': self.category.value,
            'importance': self.importance,
            'created_at': self.created_at.isoformat(),
            'accessed_at': self.accessed_at.isoformat(),
            'access_count': self.access_count,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MemoryItem':
        return cls(
            id=data['id'],
            content=data['content'],
            category=MemoryCategory(data['category']),
            importance=data['importance'],
            created_at=datetime.fromisoformat(data['created_at']),
            accessed_at=datetime.fromisoformat(data['accessed_at']),
            access_count=data.get('access_count', 0),
            metadata=data.get('metadata', {})
        )


class MemoryService:
    """
    Unified memory service.
    
    Provides memorization, recall, and retrieval capabilities.
    """
    
    def __init__(self, storage_path: str = "/home/workspace/personai/data/memory.json"):
        self.storage_path = storage_path
        self.memories: Dict[str, MemoryItem] = {}
        self._load()
    
    def _load(self):
        """Load memories from disk"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for item_data in data.get('memories', []):
                        item = MemoryItem.from_dict(item_data)
                        self.memories[item.id] = item
            except Exception as e:
                # Handle exception - log if needed
                import logging
                logging.warning(f"Failed to load memory data: {e}")
    
    def _save(self):
        """Save memories to disk"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            'memories': [m.to_dict() for m in self.memories.values()],
            'saved_at': datetime.now().isoformat()
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def memorize(
        self,
        content: str,
        category: MemoryCategory,
        importance: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Store a memory and return its ID"""
        now = datetime.now()
        item = MemoryItem(
            id=str(uuid.uuid4()),
            content=content,
            category=category,
            importance=importance,
            created_at=now,
            accessed_at=now,
            access_count=0,
            metadata=metadata or {}
        )
        self.memories[item.id] = item
        self._save()
        return item.id
    
    def recall(self, query: str, limit: int = 5) -> List[MemoryItem]:
        """Recall relevant memories based on query"""
        query_lower = query.lower()
        
        # Score memories by relevance
        scored = []
        for item in self.memories.values():
            score = 0.0
            
            # Text similarity (simple keyword matching)
            content_words = set(item.content.lower().split())
            query_words = set(query_lower.split())
            overlap = len(content_words & query_words)
            score += overlap * 0.3
            
            # Importance weight
            score += item.importance * 0.5
            
            # Recency weight
            hours_old = (datetime.now() - item.accessed_at).total_seconds() / 3600
            score += max(0, 1 - hours_old / 24) * 0.2
            
            scored.append((score, item))
        
        # Sort by score and return top results
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [item for _, item in scored[:limit]]
        
        # Update access stats
        for item in results:
            item.access_count += 1
            item.accessed_at = datetime.now()
        
        if results:
            self._save()
        
        return results
    
    def retrieve(
        self,
        query: str,
        category: Optional[MemoryCategory] = None,
        limit: int = 10
    ) -> List[MemoryItem]:
        """Retrieve memories with filters"""
        results = []
        
        for item in self.memories.values():
            # Filter by category if specified
            if category and item.category != category:
                continue
            
            # Simple text search
            if query.lower() in item.content.lower():
                results.append(item)
            
            if len(results) >= limit:
                break
        
        return results
    
    def get_by_id(self, memory_id: str) -> Optional[MemoryItem]:
        """Get a specific memory by ID"""
        return self.memories.get(memory_id)
    
    def update(
        self,
        memory_id: str,
        content: Optional[str] = None,
        importance: Optional[float] = None
    ) -> bool:
        """Update a memory"""
        item = self.memories.get(memory_id)
        if not item:
            return False
        
        if content is not None:
            item.content = content
        if importance is not None:
            item.importance = importance
        
        item.accessed_at = datetime.now()
        self._save()
        return True
    
    def delete(self, memory_id: str) -> bool:
        """Delete a memory"""
        if memory_id in self.memories:
            del self.memories[memory_id]
            self._save()
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        categories = {}
        for item in self.memories.values():
            cat = item.category.value
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total_memories': len(self.memories),
            'by_category': categories,
            'avg_importance': sum(m.importance for m in self.memories.values()) / max(len(self.memories), 1),
            'total_accesses': sum(m.access_count for m in self.memories.values())
        }
    
    def get_recent(self, limit: int = 10) -> List[MemoryItem]:
        """Get most recent memories"""
        sorted_memories = sorted(
            self.memories.values(),
            key=lambda m: m.created_at,
            reverse=True
        )
        return sorted_memories[:limit]


# Global memory instance
_memory: Optional[MemoryService] = None


def get_memory(storage_path: str = "/home/workspace/personai/data/memory.json") -> MemoryService:
    """Get the global memory service"""
    global _memory
    if _memory is None:
        _memory = MemoryService(storage_path)
    return _memory
