"""
Self-Improvement Runner

Runs autonomous self-improvement cycles.
"""

import time
import json
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from .executor import get_executor, SelfImprovementExecutor
from .roadmap import get_roadmap, RollingRoadmap
from ..memory import get_memory, MemoryCategory
from ..core.state import get_state


class SelfImprovementRunner:
    """
    Autonomous self-improvement runner.
    
    Continuously analyzes, improves, and verifies the codebase.
    """
    
    def __init__(self):
        self.executor = get_executor()
        self.roadmap = get_roadmap()
        self.memory = get_memory()
        self.state = get_state()
        
        self.is_running = False
        self.cycle_interval = 300  # 5 minutes
        self.max_cycles = 100
        self.cycles_completed = 0
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        self.results_history: List[Dict[str, Any]] = []
    
    def start(self, interval: int = 300):
        """Start autonomous self-improvement"""
        if self.is_running:
            return
        
        self.is_running = True
        self.cycle_interval = interval
        self._stop_event.clear()
        
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        
        self.state.update('self_improver_active', True)
        print(f"🚀 Self-improvement runner started (interval: {interval}s)")
    
    def stop(self):
        """Stop self-improvement"""
        self.is_running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=10)
        self.state.update('self_improver_active', False)
        print("🛑 Self-improvement runner stopped")
    
    def _run_loop(self):
        """Main improvement loop"""
        while not self._stop_event.is_set() and self.cycles_completed < self.max_cycles:
            try:
                # Run improvement cycle
                result = self.run_cycle()
                self.results_history.append(result)
                
                # Keep last 50 results
                if len(self.results_history) > 50:
                    self.results_history = self.results_history[-50:]
                
                # Update state
                self.state.update('improvements_made', 
                    sum(1 for r in self.results_history if r.get('actions_applied', 0) > 0))
                
                # Store in memory
                self.memory.memorize(
                    content=f"Improvement cycle {self.cycles_completed}: "
                           f"{result.get('actions_applied', 0)} applied, "
                           f"tests passed: {result.get('tests_passed', False)}",
                    category=MemoryCategory.SELF_IMPROVEMENT,
                    importance=0.6,
                    metadata={
                        'cycle': self.cycles_completed,
                        'actions_applied': result.get('actions_applied', 0),
                        'tests_passed': result.get('tests_passed', False)
                    }
                )
                
            except Exception as e:
                print(f"❌ Improvement cycle error: {e}")
                self.state.add_error(f"Improvement error: {e}")
            
            # Wait for next cycle
            self._stop_event.wait(self.cycle_interval)
    
    def run_cycle(self) -> Dict[str, Any]:
        """Run a single improvement cycle"""
        self.cycles_completed += 1
        cycle_id = f"cycle_{int(time.time())}_{self.cycles_completed}"
        
        print(f"\n{'='*50}")
        print(f"🔄 Self-Improvement Cycle {self.cycles_completed}")
        print(f"{'='*50}")
        
        start_time = time.time()
        
        result = {
            'cycle_id': cycle_id,
            'cycle_number': self.cycles_completed,
            'started_at': datetime.now().isoformat()
        }
        
        # Step 1: Analyze code
        print("\n📊 Step 1: Analyzing code...")
        actions = self.executor.analyze_and_suggest()
        result['actions_suggested'] = len(actions)
        print(f"   Found {len(actions)} potential improvements")
        
        # Show top suggestions
        for i, action in enumerate(actions[:3]):
            print(f"   {i+1}. {action.description[:60]}...")
        
        # Step 2: Apply improvements
        print("\n🔧 Step 2: Applying improvements...")
        applied = 0
        improvements = []
        
        max_apply = 3  # Limit to prevent runaway
        for action in actions[:5]:
            if applied >= max_apply:
                break
            
            print(f"   Applying: {action.description[:50]}...")
            success = self.executor.apply_action(action)
            
            if success:
                applied += 1
                improvements.append({
                    'description': action.description,
                    'file': action.file_path
                })
                print(f"   ✅ Applied")
            else:
                print(f"   ❌ Failed")
        
        result['actions_applied'] = applied
        result['improvements'] = improvements
        
        # Step 3: Run tests
        print("\n🧪 Step 3: Running tests...")
        test_result = self.executor._run_tests()
        result['tests_passed'] = test_result['passed']
        
        if test_result['passed']:
            print("   ✅ All tests passed!")
        else:
            print(f"   ❌ Tests failed")
            if test_result.get('errors'):
                print(f"   Error: {test_result['errors'][:200]}")
            
            # Revert changes
            print("   ↩️  Reverting changes...")
            for action in reversed(self.executor.applied_actions[-applied:]):
                self.executor.revert_action(action)
            result['actions_applied'] = 0
            result['reverted'] = True
        
        # Step 4: Update roadmap
        print("\n📋 Step 4: Updating roadmap...")
        self.roadmap.update_from_improvement_cycle(result)
        
        result['duration_seconds'] = time.time() - start_time
        result['completed_at'] = datetime.now().isoformat()
        
        print(f"\n{'='*50}")
        print(f"✅ Cycle {self.cycles_completed} Complete")
        print(f"   Applied: {applied}/{len(actions)}")
        print(f"   Tests: {'PASSED' if test_result['passed'] else 'FAILED'}")
        print(f"   Duration: {result['duration_seconds']:.1f}s")
        print(f"{'='*50}\n")
        
        return result
    
    def run_manual_cycle(self) -> Dict[str, Any]:
        """Run a manual improvement cycle (one-shot)"""
        if not self.is_running:
            return self.run_cycle()
        return {'error': 'Runner is already running'}
    
    def get_status(self) -> Dict[str, Any]:
        """Get runner status"""
        return {
            'is_running': self.is_running,
            'cycles_completed': self.cycles_completed,
            'cycle_interval': self.cycle_interval,
            'executor_status': self.executor.get_status(),
            'last_result': self.results_history[-1] if self.results_history else None
        }
    
    def get_suggestions(self) -> List[Dict[str, Any]]:
        """Get current improvement suggestions without applying"""
        actions = self.executor.analyze_and_suggest()
        return [
            {
                'id': a.id,
                'description': a.description,
                'file': a.file_path,
                'priority': a.priority,
                'reason': a.reason
            }
            for a in actions[:10]
        ]


# Global runner
_runner: Optional[SelfImprovementRunner] = None


def get_runner() -> SelfImprovementRunner:
    """Get the global runner"""
    global _runner
    if _runner is None:
        _runner = SelfImprovementRunner()
    return _runner
