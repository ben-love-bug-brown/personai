from dataclasses import dataclass
from typing import Dict, Type

from .base import RevenueConfig, RevenueModel
from .models.automation_agency import AutomationAgency
from .models.micro_saas import MicroSaaS
from .models.affiliate import AffiliateMarketing
from .models.digital_products import DigitalProducts
from .models.ai_consulting import AIConsulting
from .models.content_creator import ContentCreator
from .models.trading_bot import TradingBot


@dataclass(frozen=True)
class ModelSpec:
    name: str
    cls: Type[RevenueModel]


MODEL_SPECS = (
    ModelSpec("automation_agency", AutomationAgency),
    ModelSpec("micro_saas", MicroSaaS),
    ModelSpec("affiliate_marketing", AffiliateMarketing),
    ModelSpec("digital_products", DigitalProducts),
    ModelSpec("ai_consulting", AIConsulting),
    ModelSpec("content_creator", ContentCreator),
    ModelSpec("trading_bot", TradingBot),
)


def build_models(allocation: Dict[str, float]) -> Dict[str, RevenueModel]:
    models: Dict[str, RevenueModel] = {}
    for spec in MODEL_SPECS:
        model_config = RevenueConfig(
            model=spec.name,
            enabled=allocation.get(spec.name, 0) > 0,
            allocation=allocation.get(spec.name, 0),
        )
        models[spec.name] = spec.cls(model_config)
    return models


def default_allocation() -> Dict[str, float]:
    return {
        "automation_agency": 20.0,
        "micro_saas": 15.0,
        "affiliate_marketing": 15.0,
        "digital_products": 15.0,
        "ai_consulting": 15.0,
        "content_creator": 10.0,
        "trading_bot": 10.0,
    }
