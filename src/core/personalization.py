"""User personalization for PersonAI"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

PROFILE_FILE = "/home/workspace/personai/data/user_profile.json"

class UserProfile:
    """Manages user profile and preferences"""
    
    def __init__(self):
        self.data = self._load_profile()
    
    def _load_profile(self) -> Dict:
        """Load profile from file"""
        if os.path.exists(PROFILE_FILE):
            with open(PROFILE_FILE, 'r') as f:
                return json.load(f)
        return {
            'name': None,
            'preferences': {},
            'learned_facts': {},
            'created_at': datetime.now().isoformat()
        }
    
    def save(self):
        """Save profile to file"""
        os.makedirs(os.path.dirname(PROFILE_FILE), exist_ok=True)
        with open(PROFILE_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def learn_fact(self, key: str, value: Any):
        """Learn a fact about the user"""
        self.data['learned_facts'][key] = value
        self.save()
    
    def get_fact(self, key: str, default: Any = None) -> Any:
        """Get a learned fact"""
        return self.data['learned_facts'].get(key, default)
    
    def get_summary(self) -> Dict:
        """Get profile summary"""
        return {
            'name': self.data.get('name'),
            'facts_learned': len(self.data.get('learned_facts', {})),
            'preferences': self.data.get('preferences', {})
        }


# Global instance
_profile = None

def get_user_profile() -> UserProfile:
    """Get the user profile instance"""
    global _profile
    if _profile is None:
        _profile = UserProfile()
    return _profile
