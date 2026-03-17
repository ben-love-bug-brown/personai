"""
Self-Improvement Executor

Actually executes code improvements based on analysis.
"""

import os
import re
import subprocess
import time
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import uuid

from ..llm import get_llm_client, SelfDrivenNLP
from ..memory import get_memory, MemoryCategory


@dataclass
class ImprovementAction:
    """An improvement action to be taken"""
    id: str
    file_path: str
    description: str
    old_code: str
    new_code: str
    reason: str
    priority: float
    status: str = "pending"  # pending, applied, reverted, failed


class SelfImprovementExecutor:
    """
    Executes self-improvement actions on the codebase.
    
    This is the core component that actually makes changes to improve the system.
    """
    
    def __init__(self, nlp: SelfDrivenNLP = None, memory=None):
        self.nlp = nlp or get_llm_client().self_driven
        self.memory = memory or get_memory()
        self.pending_actions: List[ImprovementAction] = []
        self.applied_actions: List[ImprovementAction] = []
        self.failed_actions: List[ImprovementAction] = []
        self.target_path = "/home/workspace/personai/src"
    
    def analyze_and_suggest(self, module_path: str = None) -> List[ImprovementAction]:
        """Analyze code and suggest improvements"""
        target = module_path or self.target_path
        
        if not os.path.exists(target):
            return []
        
        actions = []
        
        # Analyze Python files
        for root, dirs, files in os.walk(target):
            # Skip test files and __pycache__
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'tests']]
            
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    file_actions = self._analyze_file(filepath)
                    actions.extend(file_actions)
        
        # Sort by priority
        actions.sort(key=lambda x: x.priority, reverse=True)
        self.pending_actions = actions
        
        return actions
    
    def _analyze_file(self, filepath: str) -> List[ImprovementAction]:
        """Analyze a single file for improvements"""
        actions = []
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
        except Exception as e:
            return actions
        
        # Check for common issues
        issues = self._detect_issues(content, filepath)
        
        for issue in issues:
            action = ImprovementAction(
                id=str(uuid.uuid4()),
                file_path=filepath,
                description=issue['description'],
                old_code=issue.get('old_code', ''),
                new_code=issue.get('new_code', ''),
                reason=issue.get('reason', ''),
                priority=issue.get('priority', 0.5)
            )
            actions.append(action)
        
        return actions
    
    def _detect_issues(self, content: str, filepath: str) -> List[Dict]:
        """Detect issues in code"""
        issues = []
        
        lines = content.split('\n')
        
        # Issue 1: Check for TODO comments that need addressing
        for i, line in enumerate(lines):
            if 'TODO' in line.upper():
                issues.append({
                    'description': f'TODO comment found on line {i+1}',
                    'old_code': line,
                    'new_code': line.replace('TODO', 'FIXME'),  # Escalate priority
                    'reason': 'TODOs should be addressed',
                    'priority': 0.6
                })
        
        # Issue 2: Check for bare except clauses
        for i, line in enumerate(lines):
            if re.match(r'^\s*except\s*:', line):
                issues.append({
                    'description': f'Bare except on line {i+1} - should catch specific exception',
                    'old_code': line,
                    'new_code': line.replace('except:', 'except Exception as e:'),
                    'reason': 'Bare excepts catch everything including KeyboardInterrupt',
                    'priority': 0.8
                })
        
        # Issue 3: Check for print statements that should be logging
        for i, line in enumerate(lines):
            if re.match(r'^\s*print\(', line) and 'logging' not in content[:500]:
                issues.append({
                    'description': f'Print statement on line {i+1} - consider using logging',
                    'old_code': line,
                    'new_code': line,  # Keep as-is for now
                    'reason': 'Logging is more appropriate for production code',
                    'priority': 0.3
                })
        
        # Issue 4: Check for hardcoded values that should be config
        for i, line in enumerate(lines):
            # Look for hardcoded timeouts, retries, etc.
            if re.search(r'(timeout|retry|delay)\s*=\s*\d+', line):
                issues.append({
                    'description': f'Hardcoded value on line {i+1} - consider config',
                    'old_code': line,
                    'new_code': line,
                    'reason': 'Hardcoded values should be configurable',
                    'priority': 0.4
                })
        
        # Issue 5: Check for missing docstrings
        if filepath.endswith('.py'):
            if '"""' not in content and "'''" not in content:
                if len(lines) > 20:  # Only for substantial files
                    issues.append({
                        'description': 'File lacks docstrings',
                        'old_code': '',
                        'new_code': '# Add module docstring',
                        'reason': 'Documentation improves maintainability',
                        'priority': 0.3
                    })
        
        # Issue 6: Check for empty except blocks
        for i, line in enumerate(lines):
            if re.match(r'^\s*except.*:', line):
                # Check if next non-empty line is pass or another except
                for j in range(i+1, min(i+5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and not next_line.startswith('#'):
                        if next_line == 'pass':
                            issues.append({
                                'description': f'Empty except block at line {i+1}',
                                'old_code': lines[j-1] + '\n' + lines[j],
                                'new_code': lines[j-1] + '\n    # Handle exception',
                                'reason': 'Empty except blocks hide errors',
                                'priority': 0.7
                            })
                        break
        
        return issues
    
    def apply_action(self, action: ImprovementAction) -> bool:
        """Apply an improvement action"""
        try:
            with open(action.file_path, 'r') as f:
                content = f.read()
            
            if action.old_code:
                new_content = content.replace(action.old_code, action.new_code)
            else:
                # For additions at the beginning
                new_content = action.new_code + '\n' + content
            
            # Backup before applying
            backup_path = action.file_path + '.backup'
            with open(backup_path, 'w') as f:
                f.write(content)
            
            # Apply the change
            with open(action.file_path, 'w') as f:
                f.write(new_content)
            
            action.status = "applied"
            self.applied_actions.append(action)
            
            # Log to memory
            self.memory.memorize(
                content=f"Applied improvement: {action.description} to {action.file_path}",
                category=MemoryCategory.SELF_IMPROVEMENT,
                importance=0.8,
                metadata={
                    'action_id': action.id,
                    'file': action.file_path,
                    'improvement': action.description
                }
            )
            
            return True
            
        except Exception as e:
            action.status = "failed"
            action.reason = f"Failed: {str(e)}"
            self.failed_actions.append(action)
            return False
    
    def revert_action(self, action: ImprovementAction) -> bool:
        """Revert an applied action"""
        try:
            backup_path = action.file_path + '.backup'
            if os.path.exists(backup_path):
                with open(backup_path, 'r') as f:
                    content = f.read()
                
                with open(action.file_path, 'w') as f:
                    f.write(content)
                
                action.status = "reverted"
                os.remove(backup_path)
                return True
        except Exception as e:
            pass
        return False
    
    def run_improvement_cycle(self) -> Dict[str, Any]:
        """Run a complete improvement cycle"""
        cycle_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        
        results = {
            'cycle_id': cycle_id,
            'started_at': datetime.now().isoformat(),
            'analyzed_files': 0,
            'actions_suggested': 0,
            'actions_applied': 0,
            'actions_failed': 0,
            'tests_passed': False,
            'improvements': []
        }
        
        # Step 1: Analyze
        print(f"[{cycle_id}] Analyzing code...")
        actions = self.analyze_and_suggest()
        results['actions_suggested'] = len(actions)
        results['analyzed_files'] = len(set(a.file_path for a in actions))
        
        # Step 2: Apply improvements (limit to prevent runaway)
        max_apply = 3
        applied_count = 0
        
        for action in actions[:5]:  # Try top 5
            if applied_count >= max_apply:
                break
            
            print(f"[{cycle_id}] Applying: {action.description[:50]}...")
            success = self.apply_action(action)
            
            if success:
                results['actions_applied'] += 1
                applied_count += 1
                results['improvements'].append({
                    'description': action.description,
                    'file': action.file_path,
                    'status': 'applied'
                })
            else:
                results['actions_failed'] += 1
        
        # Step 3: Run tests
        print(f"[{cycle_id}] Running tests...")
        test_result = self._run_tests()
        results['tests_passed'] = test_result['passed']
        
        # Step 4: Revert if tests fail
        if not test_result['passed'] and self.applied_actions:
            print(f"[{cycle_id}] Tests failed, reverting changes...")
            for action in reversed(self.applied_actions[-applied_count:]):
                self.revert_action(action)
            results['actions_applied'] = 0
            results['improvements'] = []
        
        results['duration_seconds'] = time.time() - start_time
        results['completed_at'] = datetime.now().isoformat()
        
        return results
    
    def _run_tests(self) -> Dict[str, Any]:
        """Run tests to verify changes"""
        try:
            result = subprocess.run(
                ['python', '-m', 'pytest', self.target_path, '-v', '--tb=short', '-x'],
                cwd='/home/workspace/personai',
                capture_output=True,
                text=True,
                timeout=120
            )
            return {
                'passed': result.returncode == 0,
                'output': result.stdout[-500:] if result.stdout else '',
                'errors': result.stderr[-500:] if result.stderr else ''
            }
        except subprocess.TimeoutExpired:
            return {'passed': False, 'output': '', 'errors': 'Test timeout'}
        except Exception as e:
            return {'passed': False, 'output': '', 'errors': str(e)}
    
    def get_status(self) -> Dict[str, Any]:
        """Get executor status"""
        return {
            'pending_actions': len(self.pending_actions),
            'applied_actions': len(self.applied_actions),
            'failed_actions': len(self.failed_actions),
            'target_path': self.target_path
        }


# Global executor
_executor: Optional[SelfImprovementExecutor] = None


def get_executor() -> SelfImprovementExecutor:
    """Get the global executor"""
    global _executor
    if _executor is None:
        _executor = SelfImprovementExecutor()
    return _executor
