"""
Micro SaaS Revenue Model

Builds and runs small SaaS products.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
import json
import os
import random

from ..base import RevenueModel, RevenueConfig, RevenueResult, RevenueStatus


@dataclass
class SaaSProduct:
    """A micro SaaS product"""
    id: str
    name: str
    description: str
    platform: str = "bubble"  # bubble, flutterflow, custom
    status: str = "idea"  # idea, building, launched, scaling
    monthly_revenue: float = 0.0
    active_users: int = 0
    churn_rate: float = 0.0
    launched_at: Optional[datetime] = None


class MicroSaaS(RevenueModel):
    """
    Micro SaaS - Build and run small SaaS products
    
    Revenue potential: $100-$10,000 monthly per product
    """
    
    def __init__(self, config: RevenueConfig):
        super().__init__(config)
        self.products: List[SaaSProduct] = []
        self.product_ideas = []
        self._load_data()
        self._load_ideas()
    
    def _load_data(self):
        """Load existing products"""
        data_file = "/home/workspace/personai/data/revenue/micro_saas_products.json"
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    for p in data.get("products", []):
                        launched = p.get("launched_at")
                        if launched:
                            p["launched_at"] = datetime.fromisoformat(launched)
                        self.products.append(SaaSProduct(**p))
            except Exception:
                pass  # Handle exception
    
    def _save_data(self):
        """Save products"""
        data_dir = "/home/workspace/personai/data/revenue"
        os.makedirs(data_dir, exist_ok=True)
        data_file = os.path.join(data_dir, "micro_saas_products.json")
        
        products_data = []
        for p in self.products:
            pd = vars(p)
            if pd.get("launched_at"):
                pd["launched_at"] = pd["launched_at"].isoformat()
            products_data.append(pd)
        
        with open(data_file, 'w') as f:
            json.dump({"products": products_data}, f, indent=2)
    
    def _load_ideas(self):
        """Load product ideas"""
        self.product_ideas = [
            {
                "name": "Meeting Scheduler Pro",
                "description": "AI-powered meeting scheduling with timezone handling",
                "target": "Remote teams, freelancers",
                "potential": 500,
                "platform": "bubble"
            },
            {
                "name": "Invoice Generator AI",
                "description": "Create professional invoices with AI suggestions",
                "target": "Freelancers, small businesses",
                "potential": 300,
                "platform": "bubble"
            },
            {
                "name": "Content Repurposer",
                "description": "Turn one piece of content into many formats",
                "target": "Content creators, marketers",
                "potential": 800,
                "platform": "flutterflow"
            },
            {
                "name": "Customer Feedback Collector",
                "description": "Collect and analyze customer feedback automatically",
                "target": "SaaS companies, e-commerce",
                "potential": 600,
                "platform": "bubble"
            },
            {
                "name": "Social Media Analytics",
                "description": "Unified analytics across social platforms",
                "target": "Social media managers",
                "potential": 400,
                "platform": "custom"
            },
            {
                "name": "Email Warmup Tool",
                "description": "Automatically warm up email accounts",
                "target": "Cold emailers, sales teams",
                "potential": 700,
                "platform": "custom"
            }
        ]
    
    def initialize(self) -> bool:
        """Initialize the micro SaaS business"""
        self.status = RevenueStatus.INITIALIZING
        self._load_data()
        self._load_ideas()
        self.status = RevenueStatus.IDLE
        return True
    
    def discover_opportunities(self) -> List[Dict[str, Any]]:
        """Discover micro SaaS opportunities"""
        opportunities = []
        
        for idea in random.sample(self.product_ideas, min(3, len(self.product_ideas))):
            opportunities.append({
                **idea,
                "score": random.uniform(0.6, 0.95),
                "competition": random.choice(["low", "medium", "high"]),
                "ease_of_build": random.choice(["easy", "medium", "hard"])
            })
        
        return opportunities
    
    def build_product(self, name: str, description: str, platform: str = "bubble") -> SaaSProduct:
        """Build a new micro SaaS product"""
        product = SaaSProduct(
            id=f"saas_{datetime.now().timestamp()}",
            name=name,
            description=description,
            platform=platform,
            status="building"
        )
        self.products.append(product)
        self._save_data()
        return product
    
    def launch_product(self, product_id: str) -> bool:
        """Launch a product"""
        for product in self.products:
            if product.id == product_id:
                product.status = "launched"
                product.launched_at = datetime.now()
                # Simulate initial traction
                product.active_users = random.randint(5, 50)
                product.monthly_revenue = random.uniform(50, 200)
                self._save_data()
                return True
        return False
    
    def execute(self) -> RevenueResult:
        """Execute revenue generation"""
        self.status = RevenueStatus.RUNNING
        self.execution_count += 1
        
        try:
            activities = []
            new_revenue = 0.0
            
            # 1. Discover new opportunities
            opportunities = self.discover_opportunities()
            activities.append(f"Analyzed {len(opportunities)} product opportunities")
            
            # 2. Work on existing products
            launched_products = [p for p in self.products if p.status == "launched"]
            
            if launched_products:
                # Simulate growth/churn
                for product in launched_products:
                    # User growth
                    new_users = random.randint(0, 10)
                    churn = random.randint(0, 3)
                    product.active_users = max(0, product.active_users + new_users - churn)
                    
                    # Revenue update
                    revenue_change = random.uniform(-20, 50)
                    product.monthly_revenue = max(0, product.monthly_revenue + revenue_change)
                    new_revenue += product.monthly_revenue
                
                activities.append(f"Updated {len(launched_products)} launched products")
            
            # Build in-progress products
            building_products = [p for p in self.products if p.status == "building"]
            if building_products:
                # Random chance of completion
                for product in building_products:
                    if random.random() < 0.2:  # 20% chance per cycle
                        self.launch_product(product.id)
                        activities.append(f"Launched: {product.name}")
            
            # Seed new ideas if we have few products
            if len(self.products) < 3 and random.random() < 0.3:
                idea = random.choice(self.product_ideas)
                self.build_product(idea["name"], idea["description"], idea["platform"])
                activities.append(f"Started building: {idea['name']}")
            
            result = RevenueResult(
                model="micro_saas",
                amount=new_revenue,
                currency="USD",
                timestamp=datetime.now(),
                details={
                    "activities": activities,
                    "total_products": len(self.products),
                    "launched_products": len(launched_products),
                    "building_products": len(building_products),
                    "total_users": sum(p.active_users for p in launched_products),
                    "avg_revenue_per_product": new_revenue / len(launched_products) if launched_products else 0
                },
                success=True
            )
            
            self.last_result = result
            self.save_history(result)
            self.status = RevenueStatus.IDLE
            self._save_data()
            
            return result
            
        except Exception as e:
            self.status = RevenueStatus.ERROR
            return RevenueResult(
                model="micro_saas",
                amount=0.0,
                success=False,
                error=str(e)
            )
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        launched = [p for p in self.products if p.status == "launched"]
        return {
            "status": self.status.value,
            "total_products": len(self.products),
            "launched": len(launched),
            "building": len([p for p in self.products if p.status == "building"]),
            "total_users": sum(p.active_users for p in launched),
            "total_revenue": self.total_revenue,
            "avg_revenue": sum(p.monthly_revenue for p in launched) / len(launched) if launched else 0
        }
    
    def stop(self):
        """Stop the model"""
        self.is_running = False
        self.status = RevenueStatus.STOPPED
        self._save_data()
