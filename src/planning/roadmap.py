"""Roadmap management for PersonAI"""

import json
import os
from datetime import datetime
from typing import Optional, List, Dict

ROADMAP_FILE = "/home/workspace/personai/data/roadmap.json"

class Roadmap:
    """Manages the project roadmap with phases and tasks"""
    
    def __init__(self):
        self.phases = self._load_roadmap()
    
    def _load_roadmap(self) -> list:
        """Load roadmap from file or create default"""
        if os.path.exists(ROADMAP_FILE):
            with open(ROADMAP_FILE, 'r') as f:
                return json.load(f)
        
        return [
            {
                "id": "phase1",
                "name": "Phase 1: Foundation",
                "description": "Core infrastructure and basic functionality",
                "tasks": [
                    {"id": "core", "name": "Core state management", "status": "completed"},
                    {"id": "memory", "name": "Memory system", "status": "completed"},
                    {"id": "nlp", "name": "Self-driven NLP", "status": "completed"},
                    {"id": "agents", "name": "Agent system", "status": "completed"},
                ]
            },
            {
                "id": "phase2",
                "name": "Phase 2: Planning & Roadmapping",
                "description": "Self-improvement and roadmap tracking",
                "tasks": [
                    {"id": "roadmap", "name": "Roadmap management", "status": "in_progress"},
                    {"id": "self_improvement", "name": "Self-improvement loop", "status": "pending"},
                    {"id": "personalization", "name": "User personalization", "status": "pending"},
                ]
            },
            {
                "id": "phase3",
                "name": "Phase 3: Web UI & API",
                "description": "Zo.space web interface and API",
                "tasks": [
                    {"id": "web_ui", "name": "Web chat interface", "status": "completed"},
                    {"id": "api", "name": "REST API", "status": "completed"},
                    {"id": "persistent_history", "name": "Persistent history", "status": "pending"},
                ]
            },
            {
                "id": "phase4",
                "name": "Phase 4: Advanced Features",
                "description": "Advanced NLP and autonomous capabilities",
                "tasks": [
                    {"id": "llm_integration", "name": "LLM integration", "status": "pending"},
                    {"id": "autonomous", "name": "Autonomous improvements", "status": "pending"},
                ]
            }
        ]
    
    def save(self):
        """Save roadmap to file"""
        os.makedirs(os.path.dirname(ROADMAP_FILE), exist_ok=True)
        with open(ROADMAP_FILE, 'w') as f:
            json.dump(self.phases, f, indent=2)
    
    def get_status_summary(self) -> Dict:
        """Get summary of roadmap status"""
        total = sum(len(p.get('tasks', [])) for p in self.phases)
        completed = sum(
            sum(1 for t in p.get('tasks', []) if t.get('status') == 'completed')
            for p in self.phases
        )
        in_progress = sum(
            sum(1 for t in p.get('tasks', []) if t.get('status') == 'in_progress')
            for p in self.phases
        )
        
        return {
            'total_tasks': total,
            'completed': completed,
            'in_progress': in_progress,
            'pending': total - completed - in_progress,
            'phases': self.phases
        }
    
    def mark_complete(self, task_id: str) -> bool:
        """Mark a task as completed"""
        for phase in self.phases:
            for task in phase.get("tasks", []):
                if task["id"] == task_id:
                    task["status"] = "completed"
                    self.save()
                    return True
        return False


# Global instance
_roadmap = None

def get_roadmap() -> Roadmap:
    """Get the roadmap instance"""
    global _roadmap
    if _roadmap is None:
        _roadmap = Roadmap()
    return _roadmap
