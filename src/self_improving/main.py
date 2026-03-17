"""
Self-Improver Core Implementation

Main SelfImprover class and supporting components.
"""

import os
import re
import time
import subprocess
from dataclasses import dataclass, field
from typing import Optional, Callable
from datetime import datetime

from ..llm import get_llm_client, SelfDrivenNLP
from ..memory import get_memory


@dataclass
class ImprovementResult:
    """Result of a single improvement attempt"""
    modification: str
    metric_name: str
    metric_before: float
    metric_after: float
    status: str
    timestamp: float
    duration_seconds: float
    error: Optional[str] = None
    commit_hash: Optional[str] = None


@dataclass
class ExperimentConfig:
    """Configuration for an improvement experiment"""
    target_module: str
    metric_to_optimize: str = "test_pass_rate"
    time_budget_seconds: int = 60
    max_attempts: int = 10
    improvement_threshold: float = 0.01
    use_git: bool = True
    auto_commit: bool = True


@dataclass
class CodeAnalysis:
    """Analysis of a code module"""
    module_path: str
    line_count: int
    function_count: int
    class_count: int
    complexity_score: float
    test_coverage: float = 0.0
    issues: list = field(default_factory=list)
    suggestions: list = field(default_factory=list)


class CodeAnalyzer:
    """Analyzes code for improvement opportunities"""
    
    def __init__(self, nlp: SelfDrivenNLP):
        self.nlp = nlp
    
    def analyze(self, module_path: str) -> CodeAnalysis:
        """Analyze a code module"""
        if not os.path.exists(module_path):
            return CodeAnalysis(
                module_path=module_path,
                line_count=0,
                function_count=0,
                class_count=0,
                complexity_score=0.0,
                issues=["Module not found"]
            )
        
        with open(module_path, 'r') as f:
            content = f.read()
        
        line_count = len(content.split('\n'))
        functions = re.findall(r'def (\w+)\(', content)
        function_count = len(functions)
        classes = re.findall(r'class (\w+)', content)
        class_count = len(classes)
        complexity_score = self._calculate_complexity(content)
        
        return CodeAnalysis(
            module_path=module_path,
            line_count=line_count,
            function_count=function_count,
            class_count=class_count,
            complexity_score=complexity_score,
            suggestions=[]
        )
    
    def _calculate_complexity(self, content: str) -> float:
        complexity = 0.0
        complexity += content.count('if ') * 1.0
        complexity += content.count('for ') * 1.5
        complexity += content.count('while ') * 1.5
        complexity += content.count('try:') * 2.0
        complexity += content.count('except') * 2.0
        lines = len(content.split('\n'))
        if lines > 0:
            complexity = complexity / (lines / 100)
        return min(complexity, 100.0)


class ExperimentRunner:
    """Runs experiments and measures results"""
    
    def __init__(self, nlp: SelfDrivenNLP):
        self.nlp = nlp
        self.results = []
    
    def run_experiment(
        self,
        modification: str,
        run_test: Callable[[], dict],
        time_budget: int = 60
    ) -> ImprovementResult:
        start_time = time.time()
        
        try:
            result = run_test()
            duration = time.time() - start_time
            
            return ImprovementResult(
                modification=modification,
                metric_name=result.get("name", "unknown"),
                metric_before=result.get("before", 0.0),
                metric_after=result.get("after", 0.0),
                status="keep" if result.get("success", False) else "discard",
                timestamp=time.time(),
                duration_seconds=duration
            )
            
        except Exception as e:
            duration = time.time() - start_time
            return ImprovementResult(
                modification=modification,
                metric_name="error",
                metric_before=0.0,
                metric_after=0.0,
                status="crash",
                timestamp=time.time(),
                duration_seconds=duration,
                error=str(e)
            )


class KeepDiscardManager:
    """Manages the keep/discard logic"""
    
    def __init__(self):
        self.history = []
        self.best_result = None
    
    def evaluate(self, result: ImprovementResult, threshold: float = 0.01) -> str:
        self.history.append(result)
        
        if result.status == "crash":
            return "discard"
        
        if self.best_result is None:
            self.best_result = result
            return "keep"
        
        improvement = result.metric_after - self.best_result.metric_after
        
        if improvement > threshold:
            self.best_result = result
            return "keep"
        elif abs(improvement) <= threshold:
            return "keep"
        else:
            return "discard"


class GitManager:
    """Handles git operations"""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.current_branch = "main"
    
    def commit(self, message: str) -> str:
        try:
            subprocess.run(["git", "add", "-A"], cwd=self.repo_path, capture_output=True)
            subprocess.run(["git", "commit", "-m", message], cwd=self.repo_path, capture_output=True)
            result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo_path, capture_output=True, text=True)
            return result.stdout.strip()[:7]
        except Exception as e:
            return f"error: {e}"
    
    def reset(self, count: int = 1) -> bool:
        try:
            target = "HEAD" if count <= 0 else f"HEAD~{count}"
            subprocess.run(["git", "reset", "--hard", target], cwd=self.repo_path, capture_output=True)
            return True
        except Exception:
            return False
    
    def create_branch(self, branch_name: str) -> bool:
        try:
            subprocess.run(["git", "checkout", "-b", branch_name], cwd=self.repo_path, capture_output=True)
            self.current_branch = branch_name
            return True
        except Exception:
            return False


class SelfImprover:
    """Main self-improving agent"""
    
    def __init__(
        self,
        config: ExperimentConfig,
        nlp: Optional[SelfDrivenNLP] = None,
        memory = None
    ):
        self.config = config
        self.nlp = nlp or get_llm_client()
        self.memory = memory or get_memory()
        
        self.analyzer = CodeAnalyzer(self.nlp)
        self.runner = ExperimentRunner(self.nlp)
        self.keep_discard = KeepDiscardManager()
        self.git = GitManager("/home/workspace/personai") if config.use_git else None
        
        self.is_running = False
        self.experiments_run = 0
        self.improvements_made = 0
    
    def start(self):
        self.is_running = True
        if self.git:
            branch_name = f"self-improvement/{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            self.git.create_branch(branch_name)
    
    def stop(self):
        self.is_running = False
    
    def get_status(self) -> dict:
        return {
            "is_running": self.is_running,
            "experiments_run": self.experiments_run,
            "improvements_made": self.improvements_made,
            "current_branch": self.git.current_branch if self.git else "none"
        }


def create_self_improver(
    target_module: str = "/home/workspace/personai/src",
    time_budget: int = 60,
    max_attempts: int = 10
) -> SelfImprover:
    config = ExperimentConfig(
        target_module=target_module,
        time_budget_seconds=time_budget,
        max_attempts=max_attempts,
        use_git=True,
        auto_commit=True
    )
    return SelfImprover(config)


class AutonomousScheduler:
    """Autonomous scheduling for self-improvement experiments"""
    
    def __init__(self, self_improver):
        self.improver = self_improver
        self.schedule_enabled = False
        self.schedule_interval = 300  # 5 minutes
        self.max_experiments_per_cycle = 3
        self.last_run = 0
        self.total_runs = 0
    
    def enable(self, interval_seconds: int = 300):
        """Enable autonomous scheduling"""
        self.schedule_enabled = True
        self.schedule_interval = interval_seconds
        print(f'📅 Autonomous scheduling enabled (interval: {interval_seconds}s)')
    
    def disable(self):
        """Disable autonomous scheduling"""
        self.schedule_enabled = False
        print('📅 Autonomous scheduling disabled')
    
    def should_run(self) -> bool:
        """Check if it's time to run"""
        if not self.schedule_enabled:
            return False
        import time
        return (time.time() - self.last_run) >= self.schedule_interval
    
    def run_cycle(self) -> dict:
        """Run one autonomous improvement cycle"""
        import time
        self.last_run = time.time()
        self.total_runs += 1
        
        results = {
            'cycle': self.total_runs,
            'experiments': [],
            'improvements': 0,
            'discards': 0,
            'crashes': 0
        }
        
        for i in range(self.max_experiments_per_cycle):
            try:
                from .intelligence import create_advisor
                advisor = create_advisor()
                analysis = self.improver.analyzer.analyze(self.improver.config.target_module)
                analysis_dict = {
                    'line_count': analysis.line_count,
                    'function_count': analysis.function_count,
                    'class_count': analysis.class_count,
                    'complexity_score': analysis.complexity_score,
                    'issues': analysis.issues
                }
                suggestion = advisor.get_suggestion(analysis_dict)
            except Exception:
                suggestion = {
                    'focus': 'stability',
                    'action': 'Run safe static analysis and test verification only'
                }

            results['experiments'].append({
                'suggestion': suggestion,
                'status': 'proposed'
            })
        
        return results
    
    def get_status(self) -> dict:
        """Get scheduler status"""
        return {
            'enabled': self.schedule_enabled,
            'interval': self.schedule_interval,
            'last_run': self.last_run,
            'total_runs': self.total_runs
        }


# Add scheduler to SelfImprover
SelfImprover.scheduler = property(
    lambda self: getattr(self, '_scheduler', None),
    lambda self, value: setattr(self, '_scheduler', value)
)


class UserOversight:
    """User oversight and control for self-improvement"""
    
    def __init__(self):
        self.enabled = True
        self.require_approval = True
        self.auto_mode = False
        self.approved_modules = set()
        self.blocked_modules = set()
        self.approval_queue = []
        self.history = []
    
    def request_approval(self, modification: dict) -> bool:
        """Request user approval for a modification"""
        if not self.require_approval:
            return True
        
        self.approval_queue.append(modification)
        return False
    
    def approve(self, modification_id: str) -> bool:
        """Approve a pending modification"""
        for mod in self.approval_queue:
            if mod.get('id') == modification_id:
                self.approval_queue.remove(mod)
                self.history.append({**mod, 'status': 'approved'})
                return True
        return False
    
    def reject(self, modification_id: str, reason: str = None) -> bool:
        """Reject a pending modification"""
        for mod in self.approval_queue:
            if mod.get('id') == modification_id:
                self.approval_queue.remove(mod)
                self.history.append({**mod, 'status': 'rejected', 'reason': reason})
                return True
        return False
    
    def enable_auto_mode(self):
        """Enable automatic mode (no approval needed)"""
        self.auto_mode = True
        self.require_approval = False
    
    def disable_auto_mode(self):
        """Disable automatic mode (approval required)"""
        self.auto_mode = False
        self.require_approval = True
    
    def get_status(self) -> dict:
        """Get oversight status"""
        return {
            'enabled': self.enabled,
            'require_approval': self.require_approval,
            'auto_mode': self.auto_mode,
            'pending_approvals': len(self.approval_queue),
            'history_count': len(self.history)
        }


# Add to SelfImprover
SelfImprover.oversight = property(
    lambda self: getattr(self, '_oversight', None),
    lambda self, value: setattr(self, '_oversight', value)
)
