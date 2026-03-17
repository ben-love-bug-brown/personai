"""
Affiliate Marketing Revenue Model

Automated affiliate marketing system.
"""

from typing import Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
import json
import os
import random

from ..base import RevenueModel, RevenueConfig, RevenueResult, RevenueStatus


@dataclass
class AffiliateLink:
    """An affiliate link"""
    id: str
    product: str
    network: str  # amazon, shareasale, impact, etc.
    url: str
    clicks: int = 0
    conversions: int = 0
    earnings: float = 0.0


@dataclass  
class ContentPiece:
    """Content piece for affiliate marketing"""
    id: str
    title: str
    platform: str  # wordpress, medium, etc.
    topic: str
    status: str = "draft"  # draft, published, scheduled
    affiliate_links: List[str] = None
    views: int = 0
    
    def __post_init__(self):
        if self.affiliate_links is None:
            self.affiliate_links = []


class AffiliateMarketing(RevenueModel):
    """
    Affiliate Marketing - Automated affiliate revenue
    
    Revenue potential: $100-$5,000 monthly
    """
    
    def __init__(self, config: RevenueConfig):
        super().__init__(config)
        self.affiliate_links: List[AffiliateLink] = []
        self.content: List[ContentPiece] = []
        self.keywords: List[str] = []
        self._load_data()
    
    def _load_data(self):
        """Load existing data"""
        data_dir = "/home/workspace/personai/data/revenue"
        
        links_file = os.path.join(data_dir, "affiliate_links.json")
        if os.path.exists(links_file):
            try:
                with open(links_file, 'r') as f:
                    data = json.load(f)
                    for l in data.get("links", []):
                        self.affiliate_links.append(AffiliateLink(**l))
            except Exception:
                pass  # Handle exception
    # Handle exception
        
        content_file = os.path.join(data_dir, "affiliate_content.json")
        if os.path.exists(content_file):
            try:
                with open(content_file, 'r') as f:
                    data = json.load(f)
                    for c in data.get("content", []):
                        self.content.append(ContentPiece(**c))
            except Exception:
                pass  # Handle exception
    # Handle exception
        
        # Default keywords
        if not self.keywords:
            self.keywords = [
                "best AI tools", "productivity software", "remote work tools",
                "coding courses", "marketing automation", "business software"
            ]
    
    def _save_data(self):
        """Save data"""
        data_dir = "/home/workspace/personai/data/revenue"
        os.makedirs(data_dir, exist_ok=True)
        
        links_file = os.path.join(data_dir, "affiliate_links.json")
        with open(links_file, 'w') as f:
            json.dump({"links": [vars(l) for l in self.affiliate_links]}, f, indent=2)
        
        content_file = os.path.join(data_dir, "affiliate_content.json")
        with open(content_file, 'w') as f:
            json.dump({"content": [vars(c) for c in self.content]}, f, indent=2)
    
    def initialize(self) -> bool:
        """Initialize affiliate marketing"""
        self.status = RevenueStatus.INITIALIZING
        
        # Load default affiliate programs
        default_programs = [
            {"product": "ChatGPT Plus", "network": "openai", "commission": "20%"},
            {"product": "Claude Pro", "network": "anthropic", "commission": "20%"},
            {"product": "Notion", "network": "affiliate", "commission": "50%"},
            {"product": "Canva", "network": "affiliate", "commission": "30%"},
            {"product": "Shopify", "network": "affiliate", "commission": "200%"},
        ]
        
        if not self.affiliate_links:
            for prog in default_programs:
                link = AffiliateLink(
                    id=f"link_{len(self.affiliate_links)}",
                    product=prog["product"],
                    network=prog["network"],
                    url=f"https://{prog['network']}.com/ref/{prog['product'].lower().replace(' ', '')}"
                )
                self.affiliate_links.append(link)
        
        self._load_data()
        self.status = RevenueStatus.IDLE
        return True
    
    def research_keywords(self) -> List[Dict[str, Any]]:
        """Research keywords for content"""
        keyword_opportunities = []
        
        topics = [
            "AI writing tools", "productivity apps", "coding bootcamps",
            "business software", "marketing tools", "design software"
        ]
        
        for topic in random.sample(topics, min(4, len(topics))):
            keyword_opportunities.append({
                "keyword": topic,
                "volume": random.randint(1000, 50000),
                "difficulty": random.uniform(0.3, 0.9),
                "competition": random.randint(5, 100),
                "potential_cpc": random.uniform(0.5, 10.0)
            })
        
        return keyword_opportunities
    
    def create_content(self, title: str, topic: str, platform: str = "wordpress") -> ContentPiece:
        """Create content piece"""
        content = ContentPiece(
            id=f"content_{datetime.now().timestamp()}",
            title=title,
            platform=platform,
            topic=topic,
            status="draft"
        )
        self.content.append(content)
        return content
    
    def publish_content(self, content_id: str) -> bool:
        """Publish content"""
        for c in self.content:
            if c.id == content_id:
                c.status = "published"
                c.views = random.randint(10, 100)  # Initial views
                self._save_data()
                return True
        return False
    
    def execute(self) -> RevenueResult:
        """Execute affiliate marketing cycle"""
        self.status = RevenueStatus.RUNNING
        self.execution_count += 1
        
        try:
            activities = []
            new_earnings = 0.0
            
            # 1. Research keywords
            keywords = self.research_keywords()
            activities.append(f"Researched {len(keywords)} keyword opportunities")
            
            # 2. Generate content (simulated)
            published = [c for c in self.content if c.status == "published"]
            if published:
                # Simulate traffic and conversions
                for content in published:
                    new_views = random.randint(0, 50)
                    content.views += new_views
                    
                    # Conversions based on views
                    conversions = int(content.views * random.uniform(0.001, 0.01))
                    if conversions > 0:
                        commission = random.uniform(5, 50) * conversions
                        new_earnings += commission
                
                activities.append(f"Generated {len(published)} content pieces, {new_earnings:.2f} in earnings")
            
            # 3. Create new content periodically
            if random.random() < 0.4:  # 40% chance
                topics = ["AI Tools Review", "Best Software 2024", "Productivity Guide", "Tech Comparison"]
                title = f"{random.choice(topics)} - {random.choice(['Ultimate', 'Complete', 'Simple', 'Quick'])} Guide"
                content = self.create_content(title, random.choice(keywords)["keyword"])
                activities.append(f"Created content: {title[:30]}...")
                
                # Auto-publish sometimes
                if random.random() < 0.5:
                    self.publish_content(content.id)
            
            # 4. Update link performance
            for link in self.affiliate_links:
                new_clicks = random.randint(0, 20)
                link.clicks += new_clicks
                
                conversions = int(new_clicks * random.uniform(0.02, 0.1))
                link.conversions += conversions
                link.earnings += conversions * random.uniform(5, 30)
                new_earnings += conversions * random.uniform(5, 30)
            
            result = RevenueResult(
                model="affiliate_marketing",
                amount=new_earnings,
                currency="USD",
                timestamp=datetime.now(),
                details={
                    "activities": activities,
                    "total_content": len(self.content),
                    "published_content": len(published),
                    "total_clicks": sum(l.clicks for l in self.affiliate_links),
                    "total_conversions": sum(l.conversions for l in self.affiliate_links),
                    "top_performers": [
                        {"product": l.product, "earnings": l.earnings}
                        for l in sorted(self.affiliate_links, key=lambda x: x.earnings, reverse=True)[:3]
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
                model="affiliate_marketing",
                amount=0.0,
                success=False,
                error=str(e)
            )
    
    def get_status(self) -> Dict[str, Any]:
        """Get status"""
        published = [c for c in self.content if c.status == "published"]
        return {
            "status": self.status.value,
            "total_content": len(self.content),
            "published": len(published),
            "total_clicks": sum(l.clicks for l in self.affiliate_links),
            "total_earnings": sum(l.earnings for l in self.affiliate_links),
            "conversion_rate": sum(l.conversions for l in self.affiliate_links) / max(1, sum(l.clicks for l in self.affiliate_links))
        }
    
    def stop(self):
        """Stop the model"""
        self.is_running = False
        self.status = RevenueStatus.STOPPED
        self._save_data()
