"""
Digital Products Revenue Model

Create and sell digital products.
"""

from typing import Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
import json
import os
import random

from ..base import RevenueModel, RevenueConfig, RevenueResult, RevenueStatus


@dataclass
class DigitalProduct:
    """A digital product"""
    id: str
    name: str
    type: str  # template, course, ebook, prompt_pack, tool
    description: str
    price: float
    marketplace: str  # gumroad, etsy, own_site
    status: str = "created"  # created, published, sold
    sales_count: int = 0
    rating: float = 0.0


class DigitalProducts(RevenueModel):
    """
    Digital Products - Create and sell digital products
    
    Revenue potential: $100-$10,000 monthly
    """
    
    PRODUCT_TYPES = {
        "template": {
            "examples": ["Notion Dashboard", "Business Plan Template", "Social Media Calendar"],
            "base_price": 19.99,
            "marketplaces": ["gumroad", "etsy"]
        },
        "course": {
            "examples": ["AI Fundamentals", "Prompt Engineering Masterclass", "Automation 101"],
            "base_price": 99.99,
            "marketplaces": ["teachable", "own_site"]
        },
        "ebook": {
            "examples": ["AI Business Guide", "The Freelancer's Handbook", "Tech Trends 2024"],
            "base_price": 9.99,
            "marketplaces": ["gumroad", "amazon"]
        },
        "prompt_pack": {
            "examples": ["500+ ChatGPT Prompts", "Midjourney Prompts Collection", "Claude Templates"],
            "base_price": 29.99,
            "marketplaces": ["gumroad", "own_site"]
        },
        "tool": {
            "examples": ["SEO Analyzer", "Content Generator", "Image Background Remover"],
            "base_price": 49.99,
            "marketplaces": ["gumroad", "own_site"]
        }
    }
    
    def __init__(self, config: RevenueConfig):
        super().__init__(config)
        self.products: List[DigitalProduct] = []
        self._load_data()
    
    def _load_data(self):
        """Load existing products"""
        data_file = "/home/workspace/personai/data/revenue/digital_products.json"
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    for p in data.get("products", []):
                        self.products.append(DigitalProduct(**p))
            except Exception:
                pass
    
    def _save_data(self):
        """Save products"""
        data_dir = "/home/workspace/personai/data/revenue"
        os.makedirs(data_dir, exist_ok=True)
        data_file = os.path.join(data_dir, "digital_products.json")
        
        with open(data_file, 'w') as f:
            json.dump({"products": [vars(p) for p in self.products]}, f, indent=2)
    
    def initialize(self) -> bool:
        """Initialize digital products business"""
        self.status = RevenueStatus.INITIALIZING
        self._load_data()
        
        # Create some initial products if none exist
        if not self.products:
            self._create_initial_products()
        
        self.status = RevenueStatus.IDLE
        return True
    
    def _create_initial_products(self):
        """Create initial product lineup"""
        product_ideas = [
            ("AI Prompt Master Bundle", "prompt_pack", "Ultimate collection of AI prompts"),
            ("Notion Productivity Pack", "template", "Complete workspace templates"),
            ("ChatGPT for Business", "course", "Video course on AI for business"),
            ("2024 AI Trends Ebook", "ebook", "Comprehensive guide to AI trends"),
        ]
        
        for name, ptype, desc in product_ideas:
            price = self.PRODUCT_TYPES[ptype]["base_price"]
            product = DigitalProduct(
                id=f"dp_{len(self.products)}",
                name=name,
                type=ptype,
                description=desc,
                price=price,
                marketplace="gumroad",
                status="published"
            )
            self.products.append(product)
        
        self._save_data()
    
    def generate_product_ideas(self) -> List[Dict[str, Any]]:
        """Generate new product ideas"""
        ideas = []
        
        for ptype, info in self.PRODUCT_TYPES.items():
            for example in random.sample(info["examples"], 2):
                ideas.append({
                    "type": ptype,
                    "name": example,
                    "estimated_price": info["base_price"],
                    "marketplaces": info["marketplaces"],
                    "score": random.uniform(0.5, 0.95)
                })
        
        return ideas
    
    def create_product(self, name: str, product_type: str, description: str, price: float = None) -> DigitalProduct:
        """Create a new digital product"""
        if price is None:
            price = self.PRODUCT_TYPES.get(product_type, {}).get("base_price", 29.99)
        
        product = DigitalProduct(
            id=f"dp_{datetime.now().timestamp()}",
            name=name,
            type=product_type,
            description=description,
            price=price,
            marketplace=random.choice(self.PRODUCT_TYPES.get(product_type, {}).get("marketplaces", ["gumroad"])),
            status="created"
        )
        self.products.append(product)
        self._save_data()
        return product
    
    def publish_product(self, product_id: str) -> bool:
        """Publish a product"""
        for p in self.products:
            if p.id == product_id:
                p.status = "published"
                self._save_data()
                return True
        return False
    
    def execute(self) -> RevenueResult:
        """Execute digital products revenue cycle"""
        self.status = RevenueStatus.RUNNING
        self.execution_count += 1
        
        try:
            activities = []
            new_revenue = 0.0
            
            # 1. Analyze performance
            published = [p for p in self.products if p.status == "published"]
            activities.append(f"Analyzing {len(published)} published products")
            
            # 2. Generate sales (simulated)
            if published:
                for product in published:
                    # Random sales
                    new_sales = random.randint(0, 5)
                    product.sales_count += new_sales
                    
                    # Revenue
                    revenue = new_sales * product.price
                    new_revenue += revenue
                    
                    # Update rating
                    if new_sales > 0:
                        rating_change = random.uniform(-0.1, 0.2)
                        product.rating = min(5.0, max(1.0, product.rating + rating_change))
                
                activities.append(f"Generated {new_revenue:.2f} from {sum(p.sales_count for p in published)} total sales")
            
            # 3. Create new products
            if random.random() < 0.3 and len(self.products) < 10:
                ideas = self.generate_product_ideas()
                best_idea = max(ideas, key=lambda x: x["score"])
                
                product = self.create_product(
                    name=best_idea["name"],
                    product_type=best_idea["type"],
                    description=f"High-quality {best_idea['type']}",
                    price=best_idea["estimated_price"]
                )
                
                # Publish immediately
                self.publish_product(product.id)
                activities.append(f"Created and published: {product.name}")
            
            # 4. Improve existing products
            if published and random.random() < 0.2:
                product = random.choice(published)
                # Simulate update
                activities.append(f"Updated product: {product.name}")
            
            result = RevenueResult(
                model="digital_products",
                amount=new_revenue,
                currency="USD",
                timestamp=datetime.now(),
                details={
                    "activities": activities,
                    "total_products": len(self.products),
                    "published": len(published),
                    "total_sales": sum(p.sales_count for p in published),
                    "avg_rating": sum(p.rating for p in published) / len(published) if published else 0,
                    "top_products": [
                        {"name": p.name, "sales": p.sales_count, "revenue": p.sales_count * p.price}
                        for p in sorted(published, key=lambda x: x.sales_count, reverse=True)[:3]
                    ]
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
                model="digital_products",
                amount=0.0,
                success=False,
                error=str(e)
            )
    
    def get_status(self) -> Dict[str, Any]:
        """Get status"""
        published = [p for p in self.products if p.status == "published"]
        return {
            "status": self.status.value,
            "total_products": len(self.products),
            "published": len(published),
            "total_sales": sum(p.sales_count for p in published),
            "total_revenue": self.total_revenue,
            "avg_price": sum(p.price for p in published) / len(published) if published else 0,
            "avg_rating": sum(p.rating for p in published) / len(published) if published else 0
        }
    
    def stop(self):
        """Stop the model"""
        self.is_running = False
        self.status = RevenueStatus.STOPPED
        self._save_data()
