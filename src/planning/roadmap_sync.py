"""
Roadmap Sync - NLP-powered synchronization between markdown and JSON

Keeps the JSON roadmap in sync with the master markdown document.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


class RoadmapSync:
    """Synchronizes roadmap between markdown and JSON formats"""
    
    def __init__(self, markdown_path: str, json_path: str):
        self.markdown_path = Path(markdown_path)
        self.json_path = Path(json_path)
        self._load_json()
    
    def _load_json(self):
        """Load current JSON roadmap"""
        if self.json_path.exists():
            with open(self.json_path) as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.roadmap = data
                else:
                    self.roadmap = {"phases": data, "total_tasks": 0, "completed": 0}
        else:
            self.roadmap = {"phases": [], "total_tasks": 0, "completed": 0}
    
    def parse_markdown(self) -> dict:
        """Parse markdown roadmap using NLP patterns"""
        with open(self.markdown_path) as f:
            content = f.read()
        
        phases = []
        current_phase = None
        current_tasks = []
        
        # Phase patterns
        phase_pattern = r'## Phase (\d+): ([^\n]+)(?:\s+([✅🔄📋]+))?'
        task_pattern = r'- \[([ x])\] ([^\n]+)'
        
        lines = content.split('\n')
        for line in lines:
            # Check for phase header
            phase_match = re.match(phase_pattern, line)
            if phase_match:
                # Save previous phase
                if current_phase:
                    phases.append({
                        "id": f"phase{current_phase['number']}",
                        "name": current_phase['name'],
                        "description": current_phase.get('description', ''),
                        "tasks": current_tasks,
                        "status": current_phase.get('status', 'pending')
                    })
                
                phase_num = phase_match.group(1)
                phase_name = phase_match.group(2)
                phase_status = phase_match.group(3) or 'pending'
                
                # Convert emoji to status
                status_map = {'✅': 'completed', '🔄': 'in_progress', '📋': 'pending'}
                status = status_map.get(phase_status, 'pending')
                
                current_phase = {
                    'number': int(phase_num),
                    'name': phase_name,
                    'description': '',
                    'status': status
                }
                current_tasks = []
                
            # Check for task
            task_match = re.match(task_pattern, line)
            if task_match and current_phase:
                done = task_match.group(1) == 'x'
                task_name = task_match.group(2).strip()
                
                current_tasks.append({
                    "id": self._slugify(task_name),
                    "name": task_name,
                    "status": "completed" if done else "pending"
                })
        
        # Save last phase
        if current_phase:
            phases.append({
                "id": f"phase{current_phase['number']}",
                "name": current_phase['name'],
                "description": current_phase.get('description', ''),
                "tasks": current_tasks,
                "status": current_phase.get('status', 'pending')
            })
        
        return {"phases": phases}
    
    def _slugify(self, text: str) -> str:
        """Convert task name to slug ID"""
        text = re.sub(r'[-–—]', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        words = text.lower().split()[:3]
        return '_'.join(words)
    
    def calculate_progress(self, phases: list) -> dict:
        """Calculate progress statistics"""
        total = 0
        completed = 0
        in_progress = 0
        
        for phase in phases:
            tasks = phase.get('tasks', [])
            total += len(tasks)
            for task in tasks:
                if task['status'] == 'completed':
                    completed += 1
                elif task['status'] == 'in_progress':
                    in_progress += 1
        
        return {
            "total_tasks": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": total - completed - in_progress,
            "completion_percent": int((completed / total * 100)) if total > 0 else 0
        }
    
    def sync(self, llm_client=None) -> dict:
        """Sync JSON to match markdown"""
        md_data = self.parse_markdown()
        phases = md_data['phases']
        progress = self.calculate_progress(phases)
        
        synced = {
            "name": "PersonAI Master Roadmap",
            "version": "2.0.0",
            "last_synced": datetime.now().isoformat(),
            "source": str(self.markdown_path),
            "phases": phases,
            **progress
        }
        
        with open(self.json_path, 'w') as f:
            json.dump(synced, f, indent=2)
        
        return {
            "status": "synced",
            "progress": progress
        }
    
    def get_status(self) -> dict:
        """Get current sync status"""
        md_mtime = self.markdown_path.stat().st_mtime if self.markdown_path.exists() else 0
        json_mtime = self.json_path.stat().st_mtime if self.json_path.exists() else 0
        
        progress = 0
        if isinstance(self.roadmap, dict):
            progress = self.roadmap.get('completion_percent', 0)
        
        return {
            "markdown_path": str(self.markdown_path),
            "json_path": str(self.json_path),
            "markdown_modified": datetime.fromtimestamp(md_mtime).isoformat(),
            "json_modified": datetime.fromtimestamp(json_mtime).isoformat(),
            "needs_sync": md_mtime > json_mtime,
            "current_progress": progress
        }


def sync_roadmap(
    markdown_path: str = "/home/workspace/personai/docs/ROADMAP.md",
    json_path: str = "/home/workspace/personai/data/roadmap.json",
    llm_client=None
) -> dict:
    """Sync roadmap markdown to JSON"""
    sync = RoadmapSync(markdown_path, json_path)
    return sync.sync(llm_client)


def get_roadmap_status() -> dict:
    """Get roadmap sync status"""
    sync = RoadmapSync(
        "/home/workspace/personai/docs/ROADMAP.md",
        "/home/workspace/personai/data/roadmap.json"
    )
    return sync.get_status()
