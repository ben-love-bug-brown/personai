"""
Revenue Orchestrator

Coordinates multiple revenue generation models.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import os
import random

from .base import RevenueModel, RevenueConfig, RevenueResult, RevenueStatus, RevenueCategory
from .models.automation_agency import AutomationAgency
from .models.micro_saas import MicroSaaS
from .models.affiliate import AffiliateMarketing
from .models.digital_products import DigitalProducts
from .models.ai_consulting import AIConsulting
from .models.content_creator import ContentCreator
from .models.trading_bot import TradingBot


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
        
        self._load_config()
        self._initialize_models()
    
    def _load_config(self):
        """Load configuration"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.allocation = config.get("allocation", {})
            except Exception:
                self.allocation = {}
        else:
            self.allocation = {
                "automation_agency": 20.0,
                "micro_saas": 15.0,
                "affiliate_marketing": 15.0,
                "digital_products": 15.0,
                "ai_consulting": 15.0,
                "content_creator": 10.0,
                "trading_bot": 10.0,
            }
            self._save_config()
    
    def _save_config(self):
        """Save configuration"""
        data_dir = os.path.dirname(self.config_path)
        if data_dir:
            os.makedirs(data_dir, exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            json.dump({
                "allocation": self.allocation,
                "updated_at": datetime.now().isoformat()
            }, f, indent=2)
    
    def _initialize_models(self):
        """Initialize all revenue models"""
        # Automation Agency
        config = RevenueConfig(
            model="automation_agency",
            enabled=self.allocation.get("automation_agency", 0) > 0,
            allocation=self.allocation.get("automation_agency", 0)
        )
        self.models["automation_agency"] = AutomationAgency(config)
        
        # Micro SaaS
        config = RevenueConfig(
            model="micro_saas",
            enabled=self.allocation.get("micro_saas", 0) > 0,
            allocation=self.allocation.get("micro_saas", 0)
        )
        self.models["micro_saas"] = MicroSaaS(config)
        
        # Affiliate Marketing
        config = RevenueConfig(
            model="affiliate_marketing",
            enabled=self.allocation.get("affiliate_marketing", 0) > 0,
            allocation=self.allocation.get("affiliate_marketing", 0)
        )
        self.models["affiliate_marketing"] = AffiliateMarketing(config)
        
        # Digital Products
        config = RevenueConfig(
            model="digital_products",
            enabled=self.allocation.get("digital_products", 0) > 0,
            allocation=self.allocation.get("digital_products", 0)
        )
        self.models["digital_products"] = DigitalProducts(config)
        
        # AI Consulting
        config = RevenueConfig(
            model="ai_consulting",
            enabled=self.allocation.get("ai_consulting", 0) > 0,
            allocation=self.allocation.get("ai_consulting", 0)
        )
        self.models["ai_consulting"] = AIConsulting(config)
        
        # Content Creator
        config = RevenueConfig(
            model="content_creator",
            enabled=self.allocation.get("content_creator", 0) > 0,
            allocation=self.allocation.get("content_creator", 0)
        )
        self.models["content_creator"] = ContentCreator(config)
        
        # Trading Bot
        config = RevenueConfig(
            model="trading_bot",
            enabled=self.allocation.get("trading_bot", 0) > 0,
            allocation=self.allocation.get("trading_bot", 0)
        )
        self.models["trading_bot"] = TradingBot(config)
        
        # Initialize all models
        for name, model in self.models.items():
            try:
                model.initialize()
            except Exception as e:
                print(f"Failed to initialize {name}: {e}")
    
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
                    print(f"Error executing {name}: {e}")
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
                print(f"Error stopping model: {e}")


def create_orchestrator() -> RevenueOrchestrator:
    """Factory function to create orchestrator"""
    return RevenueOrchestrator()
