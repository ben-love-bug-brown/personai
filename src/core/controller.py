"""
PersonAI Controller

Main controller that orchestrates all PersonAI components.
"""

import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime

from .state import get_state, AgentState
from ..revenue.orchestrator import RevenueOrchestrator
from ..self_improving.main import SelfImprover, create_self_improver


class PersonAIController:
    """
    Main controller for PersonAI.
    
    Orchestrates all subsystems: memory, LLM, consciousness, revenue, self-improvement.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.state = get_state()
        self.is_running = False
        self.orchestrator: Optional[RevenueOrchestrator] = None
        self.improver: Optional[SelfImprover] = None
        self._tasks: List[asyncio.Task] = []
    
    async def initialize(self):
        """Initialize all subsystems"""
        self.state.update('agent_state', AgentState.INITIALIZING)
        
        # Initialize revenue orchestrator
        try:
            from ..revenue import create_orchestrator
            self.orchestrator = create_orchestrator()
            self.state.update('revenue_initialized', True)
        except Exception as e:
            self.state.add_error(f"Revenue init failed: {e}")
        
        # Initialize self-improver
        try:
            self.improver = create_self_improver(
                target_module="/home/workspace/personai/src",
                time_budget=60,
                max_attempts=10
            )
            self.state.update('improver_initialized', True)
        except Exception as e:
            self.state.add_error(f"Improver init failed: {e}")
        
        self.state.update('agent_state', AgentState.IDLE)
        return self
    
    async def start_autonomous(self):
        """Start autonomous operation"""
        self.is_running = True
        self.state.update('agent_state', AgentState.THINKING)
        
        # Start background tasks
        if self.improver:
            loop = asyncio.get_event_loop()
            improver_task = loop.create_task(self._run_improvement_loop())
            self._tasks.append(improver_task)
        
        if self.orchestrator:
            loop = asyncio.get_event_loop()
            revenue_task = loop.create_task(self._run_revenue_loop())
            self._tasks.append(revenue_task)
    
    async def stop(self):
        """Stop all operations"""
        self.is_running = False
        self.state.update('agent_state', AgentState.IDLE)
        
        # Cancel all tasks
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()
    
    async def _run_improvement_loop(self):
        """Run self-improvement cycles"""
        while self.is_running:
            try:
                self.state.update('agent_state', AgentState.IMPROVING)
                # Run improvement cycle
                await asyncio.sleep(60)  # Run every minute
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.state.add_error(f"Improvement cycle error: {e}")
    
    async def _run_revenue_loop(self):
        """Run revenue generation cycles"""
        while self.is_running:
            try:
                self.state.update('agent_state', AgentState.EXECUTING)
                if self.orchestrator:
                    results = self.orchestrator.execute_all()
                    total = sum(r.amount for r in results if r.success)
                    self.state.add_revenue(total)
                await asyncio.sleep(300)  # Run every 5 minutes
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.state.add_error(f"Revenue cycle error: {e}")
    
    async def chat(self, message: str) -> str:
        """Process a chat message"""
        self.state.update('agent_state', AgentState.THINKING)
        self.state.update('conversations_count', 
                         self.state.get('conversations_count', 0) + 1)
        
        try:
            # Simple response for now - can be expanded with LLM
            response = await self._generate_response(message)
            return response
        finally:
            self.state.update('agent_state', AgentState.IDLE)
    
    async def _generate_response(self, message: str) -> str:
        """Generate a response to user message"""
        message_lower = message.lower()
        
        if "status" in message_lower:
            return self._get_status_response()
        elif "revenue" in message_lower:
            return self._get_revenue_response()
        elif "help" in message_lower:
            return self._get_help_response()
        elif "improve" in message_lower:
            return self._run_manual_improvement()
        else:
            return f"I heard: {message}. My autonomous systems are running. Say 'status' for details."
    
    def _get_status_response(self) -> str:
        """Get status report"""
        state = self.state.get_all()
        uptime = datetime.now() - state.get('uptime_start', datetime.now())
        
        return f"""PersonAI Status:
━━━━━━━━━━━━━━━━━━━━
State: {state.get('agent_state', 'unknown')}
Uptime: {uptime.total_seconds():.0f}s
Revenue Today: ${state.get('revenue_today', 0):.2f}
Revenue Total: ${state.get('revenue_total', 0):.2f}
Improvements Made: {state.get('improvements_made', 0)}
Conversations: {state.get('conversations_count', 0)}
Goals Active: {len([g for g in state.get('goals', []) if not g.get('completed', False)])}"""
    
    def _get_revenue_response(self) -> str:
        """Get revenue report"""
        if not self.orchestrator:
            return "Revenue system not initialized"
        
        status = self.orchestrator.get_status()
        return f"""Revenue Status:
━━━━━━━━━━━━━━━━━━━━
Total Revenue: ${status['total_revenue']:.2f}
Active Models: {status['enabled_models']}/{status['total_models']}"""
    
    def _get_help_response(self) -> str:
        """Get help text"""
        return """Available Commands:
━━━━━━━━━━━━━━━━━━
• status - View PersonAI status
• revenue - View revenue report
• improve - Run manual improvement cycle
• goals - List active goals
• help - Show this message"""
    
    def _run_manual_improvement(self) -> str:
        """Manually trigger improvement cycle"""
        if not self.improver:
            return "Improver not initialized"
        
        # Run improvement
        self.state.update('agent_state', AgentState.IMPROVING)
        
        # For now, just acknowledge
        return "Improvement cycle triggered. Check logs for details."
    
    def get_status(self) -> Dict[str, Any]:
        """Get full status dict"""
        return {
            'is_running': self.is_running,
            'state': self.state.get_all(),
            'revenue': self.orchestrator.get_status() if self.orchestrator else {},
            'improver': self.improver.get_status() if self.improver else {}
        }


# Global controller instance
_controller: Optional[PersonAIController] = None


def get_controller(config: Optional[Dict[str, Any]] = None) -> PersonAIController:
    """Get the global controller"""
    global _controller
    if _controller is None:
        _controller = PersonAIController(config)
    return _controller
