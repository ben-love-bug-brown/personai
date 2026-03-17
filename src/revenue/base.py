"""
Revenue Model Base Classes

Defines the foundation for all revenue generation models.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RevenueCategory(Enum):
    """Categories of revenue generation models"""
    SERVICE = "service"           # Automation agency, consulting
    CONTENT = "content"           # YouTube, newsletters, books
    TRADING = "trading"           # Bots, arbitrage
    PRODUCT = "product"           # SaaS, digital products
    LICENSE = "license"           # Data, prompts, voice
    AGENCY = "agency"            # Freelance platforms
    EDUCATION = "education"       # Courses, tutoring
    INFRASTRUCTURE = "infrastructure"  # APIs, compute


class RevenueStatus(Enum):
    """Status of revenue generation"""
    IDLE = "idle"
    INITIALIZING = "initializing"
    RUNNING = "running"
    ERROR = "error"
    STOPPED = "stopped"


@dataclass
class RevenueResult:
    """Result of a revenue generation attempt"""
    model: str
    amount: float
    currency: str = "USD"
    timestamp: datetime = field(default_factory=datetime.now)
    details: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "amount": self.amount,
            "currency": self.currency,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
            "success": self.success,
            "error": self.error
        }


@dataclass
class RevenueConfig:
    """Configuration for a revenue model"""
    model: str
    enabled: bool = False
    allocation: float = 0.0  # % of resources to allocate
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RevenueConfig":
        return cls(
            model=data.get("model", ""),
            enabled=data.get("enabled", False),
            allocation=data.get("allocation", 0.0),
            parameters=data.get("parameters", {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "enabled": self.enabled,
            "allocation": self.allocation,
            "parameters": self.parameters
        }


class RevenueModel(ABC):
    """Base class for all revenue generation models"""
    
    def __init__(self, config: RevenueConfig):
        self.config = config
        self.status = RevenueStatus.IDLE
        self.is_running = False
        self.last_result: Optional[RevenueResult] = None
        self.execution_count = 0
        self.total_revenue = 0.0
        self.history: List[RevenueResult] = []
        
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the model. Returns True if successful."""
        pass
    
    @abstractmethod
    def execute(self) -> RevenueResult:
        """Execute revenue generation. Returns a RevenueResult."""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the model"""
        pass
    
    @abstractmethod
    def stop(self):
        """Stop the model"""
        pass
    
    def validate_config(self) -> bool:
        """Validate model configuration"""
        if self.config.allocation < 0 or self.config.allocation > 100:
            return False
        return True
    
    def save_history(self, result: RevenueResult):
        """Save result to history"""
        self.history.append(result)
        if result.success:
            self.total_revenue += result.amount
        
        # Keep only last 100 results
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def get_history(self, limit: int = 10) -> List[RevenueResult]:
        """Get recent revenue history"""
        return self.history[-limit:]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get revenue metrics"""
        if not self.history:
            return {
                "total_executions": 0,
                "total_revenue": 0.0,
                "success_rate": 0.0,
                "avg_revenue": 0.0,
                "last_execution": None
            }
        
        successful = [r for r in self.history if r.success]
        return {
            "total_executions": len(self.history),
            "total_revenue": self.total_revenue,
            "success_rate": len(successful) / len(self.history) * 100 if self.history else 0,
            "avg_revenue": self.total_revenue / len(successful) if successful else 0,
            "last_execution": self.history[-1].timestamp.isoformat() if self.history else None
        }


class RevenueModelRegistry:
    """Registry for all available revenue models"""
    
    _models: Dict[str, type] = {}
    
    @classmethod
    def register(cls, name: str, model_class: type):
        """Register a revenue model class"""
        cls._models[name] = model_class
    
    @classmethod
    def get(cls, name: str) -> Optional[type]:
        """Get a revenue model class by name"""
        return cls._models.get(name)
    
    @classmethod
    def list_models(cls) -> List[str]:
        """List all registered model names"""
        return list(cls._models.keys())
    
    @classmethod
    def create(cls, name: str, config: RevenueConfig) -> Optional[RevenueModel]:
        """Create a revenue model instance"""
        model_class = cls.get(name)
        if model_class:
            return model_class(config)
        return None


# Register base models
RevenueModelRegistry.register("automation_agency", None)  # Placeholder
RevenueModelRegistry.register("micro_saas", None)
RevenueModelRegistry.register("affiliate", None)
RevenueModelRegistry.register("digital_products", None)
RevenueModelRegistry.register("ai_consulting", None)
RevenueModelRegistry.register("content_creator", None)
RevenueModelRegistry.register("trading_bot", None)
