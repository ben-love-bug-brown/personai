"""Roadmap management for PersonAI"""

import json
import os
from datetime import datetime
from typing import Dict

ROADMAP_FILE = "/home/workspace/personai/data/roadmap.json"

class Roadmap:
    """Manages the project roadmap with phases and tasks"""
    
    def __init__(self):
        self.phases = self._load_roadmap()
    
    def _load_roadmap(self):
        """Load roadmap from file or create default"""
        if os.path.exists(ROADMAP_FILE):
            with open(ROADMAP_FILE, 'r') as f:
                data = json.load(f)
                # Handle both old format (list) and new format (dict with phases key)
                if isinstance(data, dict) and 'phases' in data:
                    return data['phases']
                return data
        
        # Default roadmap
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
        ]
    
    def save(self):
        """Save roadmap to file"""
        os.makedirs(os.path.dirname(ROADMAP_FILE), exist_ok=True)
        
        # Save in new format with metadata
        data = {
            "name": "PersonAI Master Roadmap",
            "version": "2.0.0",
            "last_updated": datetime.now().isoformat(),
            "phases": self.phases
        }
        
        with open(ROADMAP_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_status_summary(self) -> Dict:
        """Get summary of roadmap status"""
        total = sum(len(p.get('tasks', [])) for p in self.phases if isinstance(p, dict))
        completed = sum(
            sum(1 for t in p.get('tasks', []) if isinstance(t, dict) and t.get('status') == 'completed')
            for p in self.phases if isinstance(p, dict)
        )
        in_progress = sum(
            sum(1 for t in p.get('tasks', []) if isinstance(t, dict) and t.get('status') == 'in_progress')
            for p in self.phases if isinstance(p, dict)
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
            if not isinstance(phase, dict):
                continue
            for task in phase.get("tasks", []):
                if not isinstance(task, dict):
                    continue
                if task.get("id") == task_id:
                    task["status"] = "completed"
                    self.save()
                    return True
        return False


def get_roadmap() -> Roadmap:
    """Get the roadmap instance"""
    return Roadmap()
