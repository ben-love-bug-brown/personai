"""
Rolling Roadmap

Self-improving roadmap that tracks progress and identifies next improvements.
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
import uuid


@dataclass
class RoadmapItem:
    """A single roadmap item"""
    id: str
    phase: str
    task: str
    status: str  # pending, in_progress, completed, blocked
    priority: int
    completed_at: Optional[str] = None
    notes: str = ""
    blockers: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)


class RollingRoadmap:
    """
    Rolling self-improving roadmap that:
    1. Tracks current progress
    2. Identifies next improvements
    3. Updates based on self-improvement cycles
    """
    
    def __init__(self, data_path: str = "/home/workspace/personai/data/roadmap_progress.json"):
        self.data_path = data_path
        self.items: List[RoadmapItem] = []
        self.cycles_completed = 0
        self.improvements_made = 0
        self._load()
    
    def _load(self):
        """Load roadmap data"""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r') as f:
                    data = json.load(f)
                    self.cycles_completed = data.get('cycles_completed', 0)
                    self.improvements_made = data.get('improvements_made', 0)
            except Exception as e:
                # Handle exception - silently fail for now
                pass
    
    def _save(self):
        """Save roadmap data"""
        data = {
            'cycles_completed': self.cycles_completed,
            'improvements_made': self.improvements_made,
            'last_updated': datetime.now().isoformat(),
            'items': [
                {
                    'id': item.id,
                    'phase': item.phase,
                    'task': item.task,
                    'status': item.status,
                    'priority': item.priority,
                    'completed_at': item.completed_at,
                    'notes': item.notes,
                    'blockers': item.blockers,
                    'dependencies': item.dependencies
                }
                for item in self.items
            ]
        }
        
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        with open(self.data_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_item(self, phase: str, task: str, priority: int = 5) -> str:
        """Add a new roadmap item"""
        item = RoadmapItem(
            id=str(uuid.uuid4()),
            phase=phase,
            task=task,
            status="pending",
            priority=priority
        )
        self.items.append(item)
        self._save()
        return item.id
    
    def complete_item(self, item_id: str, notes: str = "") -> bool:
        """Mark an item as completed"""
        for item in self.items:
            if item.id == item_id:
                item.status = "completed"
                item.completed_at = datetime.now().isoformat()
                item.notes = notes
                self.improvements_made += 1
                self._save()
                return True
        return False
    
    def get_next_items(self, limit: int = 5) -> List[RoadmapItem]:
        """Get next items to work on"""
        pending = [i for i in self.items if i.status == "pending"]
        pending.sort(key=lambda x: x.priority, reverse=True)
        return pending[:limit]
    
    def update_from_improvement_cycle(self, cycle_results: Dict[str, Any]):
        """Update roadmap based on improvement cycle results"""
        self.cycles_completed += 1
        
        if cycle_results.get('tests_passed') and cycle_results.get('actions_applied', 0) > 0:
            # Success - mark improvements
            for improvement in cycle_results.get('improvements', []):
                self.add_item(
                    phase="Self-Improvement",
                    task=improvement.get('description', 'Applied improvement'),
                    priority=8
                )
        
        # Add next improvements based on cycle results
        if cycle_results.get('actions_suggested', 0) > cycle_results.get('actions_applied', 0):
            remaining = cycle_results['actions_suggested'] - cycle_results['actions_applied']
            self.add_item(
                phase="Self-Improvement",
                task=f"Continue improvements ({remaining} remaining)",
                priority=7
            )
        
        # Add testing task if tests failed
        if not cycle_results.get('tests_passed'):
            self.add_item(
                phase="Quality Assurance",
                task="Fix test failures",
                priority=9
            )
        
        self._save()
    
    def generate_rolling_improvements(self) -> List[str]:
        """Generate rolling list of improvements to achieve"""
        improvements = []
        
        # Phase 1: Core Infrastructure
        improvements.append("Implement core state management")
        improvements.append("Implement memory service with persistence")
        improvements.append("Implement LLM client with self-driven fallback")
        improvements.append("Implement consciousness/heartbeat system")
        
        # Phase 2: Integration
        improvements.append("Integrate agent executor with memory")
        improvements.append("Integrate revenue orchestrator with state")
        improvements.append("Integrate self-improvement with consciousness")
        
        # Phase 3: Capabilities
        improvements.append("Add real conversation handling to CLI")
        improvements.append("Add autonomous mode to controller")
        improvements.append("Add revenue generation automation")
        
        # Phase 4: Self-Improvement
        improvements.append("Execute self-improvement cycles")
        improvements.append("Apply code fixes from analysis")
        improvements.append("Verify fixes with tests")
        
        # Phase 5: Completion
        improvements.append("Complete Phase 5: Live Operations")
        improvements.append("Run full system test")
        improvements.append("Commit all changes to git")
        
        return improvements
    
    def get_progress(self) -> Dict[str, Any]:
        """Get roadmap progress"""
        status_counts = {}
        for item in self.items:
            status_counts[item.status] = status_counts.get(item.status, 0) + 1
        
        return {
            'total_items': len(self.items),
            'cycles_completed': self.cycles_completed,
            'improvements_made': self.improvements_made,
            'by_status': status_counts,
            'next_items': [
                {'task': i.task, 'phase': i.phase, 'priority': i.priority}
                for i in self.get_next_items(3)
            ],
            'rolling_improvements': self.generate_rolling_improvements()[:5]
        }


# Global roadmap
_roadmap: Optional[RollingRoadmap] = None


def get_roadmap() -> RollingRoadmap:
    """Get the global roadmap"""
    global _roadmap
    if _roadmap is None:
        _roadmap = RollingRoadmap()
    return _roadmap
