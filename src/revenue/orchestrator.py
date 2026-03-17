"""
Revenue Orchestrator

Coordinates multiple revenue generation models.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

from .base import RevenueModel, RevenueResult
from .config_store import RevenueConfigStore
from .model_factory import build_models


@dataclass
class RevenueReport:
    """Overall revenue report"""
    timestamp: datetime
    total_revenue: float
    active_models: int
    results: List[RevenueResult]
    summary: Dict[str, Any]


class RevenueOrchestrator:
    """
    Orchestrates multiple revenue generation models
    
    Coordinates execution, allocation, and reporting across all revenue streams.
    """
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = "/home/workspace/personai/data/revenue/config.json"
        
        self.config_path = config_path
        self.models: Dict[str, RevenueModel] = {}
        self.allocation: Dict[str, float] = {}
        self.total_revenue = 0.0
        self.history: List[RevenueResult] = []
        self.config_store = RevenueConfigStore(config_path)
        
        self._load_config()
        self._initialize_models()
    
    def _load_config(self):
        """Load configuration"""
        self.allocation = self.config_store.load_allocation()
    
    def _save_config(self):
        """Save configuration"""
        self.config_store.save_allocation(self.allocation)
    
    def _initialize_models(self):
        """Initialize all revenue models"""
        self.models = build_models(self.allocation)
        
        # Initialize all models
        for name, model in self.models.items():
            try:
                model.initialize()
            except Exception as e:
                logging.error(f"Failed to initialize {name}: {e}")
    
    def register_model(self, name: str, model: RevenueModel):
        """Register a revenue model"""
        self.models[name] = model
    
    def set_allocation(self, allocations: Dict[str, float]):
        """Set resource allocation per model"""
        self.allocation = allocations
        
        # Update model configs
        for name, allocation in allocations.items():
            if name in self.models:
                self.models[name].config.allocation = allocation
                self.models[name].config.enabled = allocation > 0
        
        self._save_config()
    
    def execute_all(self) -> List[RevenueResult]:
        """Execute all enabled models"""
        results = []
        
        for name, model in self.models.items():
            if model.config.enabled:
                try:
                    result = model.execute()
                    results.append(result)
                    self.total_revenue += result.amount
                    self.history.append(result)
                    
                    # Keep history manageable
                    if len(self.history) > 1000:
                        self.history = self.history[-1000:]
                        
                except Exception as e:
                    logging.error(f"Error executing {name}: {e}")
                    results.append(RevenueResult(
                        model=name,
                        amount=0.0,
                        success=False,
                        error=str(e)
                    ))
        
        return results
    
    def execute_model(self, name: str) -> Optional[RevenueResult]:
        """Execute a specific model"""
        if name not in self.models:
            return None
        
        try:
            result = self.models[name].execute()
            self.total_revenue += result.amount
            self.history.append(result)
            return result
        except Exception as e:
            return RevenueResult(
                model=name,
                amount=0.0,
                success=False,
                error=str(e)
            )
    
    def get_report(self) -> RevenueReport:
        """Generate revenue report"""
        results = []
        for model in self.models.values():
            if model.config.enabled:
                results.extend(model.get_history(limit=5))
        
        model_status = {}
        for name, model in self.models.items():
            model_status[name] = {
                "enabled": model.config.enabled,
                "allocation": model.config.allocation,
                "status": model.status.value,
                "total_revenue": model.total_revenue,
                "execution_count": model.execution_count,
                "metrics": model.get_metrics()
            }
        
        return RevenueReport(
            timestamp=datetime.now(),
            total_revenue=self.total_revenue,
            active_models=len([m for m in self.models.values() if m.config.enabled]),
            results=results,
            summary={
                "total_models": len(self.models),
                "enabled_models": len([m for m in self.models.values() if m.config.enabled]),
                "total_allocation": sum(self.allocation.values()),
                "model_status": model_status
            }
        )
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status"""
        return {
            "total_revenue": self.total_revenue,
            "total_models": len(self.models),
            "enabled_models": len([m for m in self.models.values() if m.config.enabled]),
            "allocation": self.allocation,
            "models": {
                name: {
                    "enabled": model.config.enabled,
                    "allocation": model.config.allocation,
                    "status": model.status.value,
                    "total_revenue": model.total_revenue,
                    "last_result": model.last_result.to_dict() if model.last_result else None
                }
                for name, model in self.models.items()
            }
        }
    
    def stop_all(self):
        """Stop all models"""
        for model in self.models.values():
            try:
                model.stop()
            except Exception as e:
                logging.error(f"Error stopping model: {e}")


def create_orchestrator() -> RevenueOrchestrator:
    """Factory function to create orchestrator"""
    return RevenueOrchestrator()
