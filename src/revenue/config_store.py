import json
import os
from datetime import datetime
from typing import Dict

from .model_factory import default_allocation


class RevenueConfigStore:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def load_allocation(self) -> Dict[str, float]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                return config.get("allocation", {})
            except Exception:
                return {}

        allocation = default_allocation()
        self.save_allocation(allocation)
        return allocation

    def save_allocation(self, allocation: Dict[str, float]) -> None:
        data_dir = os.path.dirname(self.config_path)
        if data_dir:
            os.makedirs(data_dir, exist_ok=True)

        with open(self.config_path, "w") as f:
            json.dump(
                {
                    "allocation": allocation,
                    "updated_at": datetime.now().isoformat(),
                },
                f,
                indent=2,
            )
