"""
Self-Improvement Executor

Actually executes code improvements based on analysis.
"""

import os
import re
import subprocess
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid

from ..llm import get_llm_client, SelfDrivenNLP
from ..memory import get_memory, MemoryCategory
from .logging_utils import get_logger

logger = get_logger(__name__)


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
        except Exception:
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
        """Detect issues in code - enhanced with deeper analysis"""
        issues = []
        
        lines = content.split('\n')
        
        # Skip analyzing self (the executor) and test files
        if 'self_improving' in filepath or 'tests/' in filepath:
            return issues
        
        # Issue 1: Check for print statements that should be logging
        for i, line in enumerate(lines):
            if re.match(r'^\s*print\s*\(', line) and 'logging' not in content[:2000]:
                # Skip if in __main__ or test code
                if '__main__' not in content[:3000] and 'test' not in content[:3000].lower():
                    issues.append({
                        'description': f'Print statement on line {i+1} - consider logging for production',
                        'old_code': line,
                        'new_code': line,
                        'reason': 'Logging is more configurable for production code',
                        'priority': 0.4
                    })
        
        # Issue 2: Check for bare except clauses - SAFE to auto-fix
        for i, line in enumerate(lines):
            if re.match(r'^\s*except\s*:', line):
                issues.append({
                    'description': f'Bare except on line {i+1} - should catch specific exception',
                    'old_code': line,
                    'new_code': line.replace('except:', 'except Exception as e:'),
                    'reason': 'Bare excepts catch everything including KeyboardInterrupt',
                    'priority': 0.7
                })
        
        # Issue 3: Deep complexity analysis - detect functions with high complexity
        complexity_issues = self._analyze_complexity(content, filepath)
        issues.extend(complexity_issues)
        
        # Issue 4: Detect code duplication patterns
        duplication_issues = self._detect_duplication(content, filepath)
        issues.extend(duplication_issues)
        
        # Issue 5: Detect hotspots (large files with many functions)
        hotspot_issues = self._detect_hotspots(filepath, len(lines), content)
        issues.extend(hotspot_issues)
        
        return issues
    
    def _analyze_complexity(self, content: str, filepath: str) -> List[Dict]:
        """Analyze code complexity - detect functions with high complexity"""
        issues = []
        lines = content.split('\n')
        
        # Find all function definitions
        in_function = False
        function_name = ""
        function_start = 0
        complexity_score = 0
        
        # Count decision points (if, for, while, and, or, except, with)
        decision_keywords = ['if ', 'elif ', 'for ', 'while ', ' and ', ' or ', 'except', 'with ']
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Detect function start
            if stripped.startswith('def ') or stripped.startswith('async def '):
                if in_function and function_name:
                    # Analyze previous function
                    if complexity_score > 7:  # Threshold for high complexity
                        issues.append({
                            'description': f'High complexity function "{function_name}" (score: {complexity_score}) - consider refactoring',
                            'old_code': '',
                            'new_code': '',
                            'reason': f'Function has {complexity_score} decision points - consider splitting',
                            'priority': 0.6
                        })
                in_function = True
                function_start = i
                # Extract function name
                match = re.match(r'def (\w+)', stripped)
                if match:
                    function_name = match.group(1)
                complexity_score = 0
                continue
            
            if in_function:
                # Skip docstrings and comments
                if stripped.startswith('"""') or stripped.startswith("'''") or stripped.startswith('#'):
                    continue
                # Count decision points
                for kw in decision_keywords:
                    complexity_score += line.count(kw)
        
        return issues
    
    def _detect_duplication(self, content: str, filepath: str) -> List[Dict]:
        """Detect code duplication patterns"""
        issues = []
        
        # Skip small files
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        if len(lines) < 20:
            return issues
        
        # Find repeated code blocks (3+ lines repeated)
        code_blocks = {}
        current_block = []
        
        for line in lines:
            # Skip trivial lines
            if len(line) < 20 or line.startswith('#') or line.startswith('"""'):
                if current_block and len(current_block) >= 3:
                    block_text = '\n'.join(current_block)
                    code_blocks[block_text] = code_blocks.get(block_text, 0) + 1
                current_block = []
            else:
                current_block.append(line)
        
        # Report duplicated blocks
        for block, count in code_blocks.items():
            if count >= 2 and len(block) > 50:
                issues.append({
                    'description': f'Code duplication detected: {len(block)} chars repeated {count} times',
                    'old_code': block[:100] + '...' if len(block) > 100 else block,
                    'new_code': '',
                    'reason': 'Repeated code should be extracted to a function',
                    'priority': 0.5
                })
                break  # Report one at a time
        
        return issues
    
    def _detect_hotspots(self, filepath: str, line_count: int, content: str) -> List[Dict]:
        """Detect code hotspots - large files or files with many functions"""
        issues = []
        
        # Count functions/classes
        function_count = len(re.findall(r'^\s*(def |class |async def )', content, re.MULTILINE))
        
        # Hotspot: Large file with many functions
        if line_count > 200 and function_count > 10:
            issues.append({
                'description': f'Hotspot: Large file ({line_count} lines, {function_count} functions) - consider splitting',
                'old_code': '',
                'new_code': '',
                'reason': 'Large files are harder to maintain - consider modularization',
                'priority': 0.4
            })
        
        # Hotspot: Many exports but no docstrings
        if function_count > 5 and '"""' not in content[:1000]:
            issues.append({
                'description': f'File has {function_count} functions but no module docstring',
                'old_code': '',
                'new_code': '',
                'reason': 'Module documentation improves maintainability',
                'priority': 0.3
            })
        
        return issues
    
    def apply_action(self, action: ImprovementAction) -> bool:
        """Apply an improvement action"""
        try:
            with open(action.file_path, 'r') as f:
                content = f.read()

            if action.old_code:
                if action.old_code not in content:
                    action.status = "failed"
                    action.reason = "Failed: target code snippet not found"
                    self.failed_actions.append(action)
                    return False
                new_content = content.replace(action.old_code, action.new_code, 1)
            else:
                new_content = action.new_code + '\n' + content

            backup_path = action.file_path + '.backup'
            with open(backup_path, 'w') as f:
                f.write(content)

            with open(action.file_path, 'w') as f:
                f.write(new_content)

            action.status = "applied"
            self.applied_actions.append(action)

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
            logger.error(f"Revert failed: {e}")
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
        logger.info(f"[{cycle_id}] Analyzing code...")
        actions = self.analyze_and_suggest()
        results['actions_suggested'] = len(actions)
        results['analyzed_files'] = len(set(a.file_path for a in actions))
        
        # Step 2: Apply improvements (limit to prevent runaway)
        max_apply = 3
        applied_count = 0
        
        for action in actions[:5]:  # Try top 5
            if applied_count >= max_apply:
                break
            
            logger.info(f"[{cycle_id}] Applying: {action.description[:50]}...")
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
        logger.info(f"[{cycle_id}] Running tests...")
        test_result = self._run_tests()
        results['tests_passed'] = test_result['passed']
        
        # Step 4: Revert if tests fail
        if not test_result['passed'] and self.applied_actions:
            logger.warning(f"[{cycle_id}] Tests failed, reverting changes...")
            for action in reversed(self.applied_actions[-applied_count:]):
                self.revert_action(action)
            results['actions_applied'] = 0
            results['improvements'] = []
        
        results['duration_seconds'] = time.time() - start_time
        results['completed_at'] = datetime.now().isoformat()
        
        return results
    
    def _run_tests(self) -> Dict[str, Any]:
        """Run tests to verify changes"""
        # Check if there are any test files
        has_tests = False
        for root, dirs, files in os.walk('/home/workspace/personai'):
            # Skip non-test dirs
            if any(x in root for x in ['node_modules', '.git', '__pycache__', 'data']):
                continue
            if any(f.startswith('test_') and f.endswith('.py') for f in files):
                has_tests = True
                break

        if not has_tests:
            # No tests - skip verification
            return {'passed': True, 'output': 'No tests found, skipping verification', 'errors': ''}

        try:
            # Create clean environment without problematic terminal settings
            env = os.environ.copy()
            env['TERM'] = 'dumb'
            env['COLORTERM'] = ''
            
            result = subprocess.run(
                ['python', '-m', 'pytest', '/home/workspace/personai/tests', '-v', '--tb=short', '-x', '--no-header'],
                cwd='/home/workspace/personai',
                capture_output=True,
                text=True,
                timeout=120,
                env=env
            )
            # Check for actual test failures - look for "FAILED" in stdout (not stderr warnings)
            stdout = result.stdout
            # Filter out terminal warnings from check
            has_failures = 'FAILED' in stdout or result.returncode != 0
            return {
                'passed': not has_failures,
                'output': stdout[-500:] if stdout else '',
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
