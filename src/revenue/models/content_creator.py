"""
Content Creator Revenue Model

Create and monetize content.
"""

from typing import Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
import json
import os
import random

from ..base import RevenueModel, RevenueConfig, RevenueResult, RevenueStatus


@dataclass
class Content:
    """Content piece"""
    id: str
    title: str
    platform: str  # youtube, newsletter, blog, twitter, tiktok
    type: str  # video, article, thread, short
    status: str = "draft"  # draft, scheduled, published
    views: int = 0
    engagement: float = 0.0
    monetization: float = 0.0  # Revenue from this piece


class ContentCreator(RevenueModel):
    """
    Content Creator - Create and monetize content
    
    Revenue potential: $100-$10,000 monthly
    """
    
    PLATFORMS = {
        "youtube": {"monetization": "ad revenue", "base_views": 1000},
        "newsletter": {"monetization": "subscribers", "base_views": 500},
        "blog": {"monetization": "ads/affiliate", "base_views": 800},
        "twitter": {"monetization": "sponsorships", "base_views": 5000},
        "tiktok": {"monetization": "creator fund", "base_views": 10000},
    }
    
    def __init__(self, config: RevenueConfig):
        super().__init__(config)
        self.content: List[Content] = []
        self.subscribers: Dict[str, int] = {}  # platform -> count
        self.sponsorships: List[Dict] = []
        self._load_data()
    
    def _load_data(self):
        """Load existing data"""
        data_dir = "/home/workspace/personai/data/revenue"
        
        content_file = os.path.join(data_dir, "content_creator_content.json")
        if os.path.exists(content_file):
            try:
                with open(content_file, 'r') as f:
                    data = json.load(f)
                    for c in data.get("content", []):
                        self.content.append(Content(**c))
            except Exception:
                pass  # Handle exception
                pass
        
        # Initialize subscribers
        for platform in self.PLATFORMS:
            self.subscribers[platform] = random.randint(100, 5000)
    
    def _save_data(self):
        """Save data"""
        data_dir = "/home/workspace/personai/data/revenue"
        os.makedirs(data_dir, exist_ok=True)
        
        content_file = os.path.join(data_dir, "content_creator_content.json")
        with open(content_file, 'w') as f:
            json.dump({
                "content": [vars(c) for c in self.content],
                "subscribers": self.subscribers,
                "sponsorships": self.sponsorships
            }, f, indent=2)
    
    def initialize(self) -> bool:
        """Initialize content creator"""
        self.status = RevenueStatus.INITIALIZING
        self._load_data()
        
        # Create some initial content
        if not self.content:
            initial_content = [
                ("AI Tools Review 2024", "youtube", "video"),
                ("Weekly AI Newsletter", "newsletter", "article"),
                ("Prompt Engineering Tips", "twitter", "thread"),
                ("AI Business Guide", "blog", "article"),
            ]
            
            for title, platform, ctype in initial_content:
                content = Content(
                    id=f"content_{len(self.content)}",
                    title=title,
                    platform=platform,
                    type=ctype,
                    status="published",
                    views=random.randint(100, 5000),
                    engagement=random.uniform(0.01, 0.1)
                )
                self.content.append(content)
        
        self.status = RevenueStatus.IDLE
        return True
    
    def generate_ideas(self) -> List[Dict[str, Any]]:
        """Generate content ideas"""
        ideas = {
            "youtube": [
                "AI Tools Comparison", "Tutorial: Building with AI", "AI News Weekly",
                "Interview with AI Founder", "AI Startup Behind the Scenes"
            ],
            "newsletter": [
                "AI Industry Roundup", "New AI Tools Spotlight", "AI Tips & Tricks",
                "Case Study: AI in Business", "AI Predictions"
            ],
            "twitter": [
                "10 AI Tools You Need", "Hot Takes on AI News", "AI Coding Tips",
                "Thread: AI Future", "Quick AI Wins"
            ],
            "blog": [
                "How to Use AI for Productivity", "AI Tool Reviews", "AI Implementation Guide",
                "AI vs Traditional Methods", "AI Best Practices"
            ],
            "tiktok": [
                "AI Tool Quick Demos", "Funny AI Fails", "AI Tips in 60 Seconds",
                "AI Trends TikTok", "AI Hacks"
            ]
        }
        
        all_ideas = []
        for platform, titles in ideas.items():
            for title in random.sample(titles, 2):
                all_ideas.append({
                    "platform": platform,
                    "title": title,
                    "type": random.choice(["video", "article", "thread"]),
                    "potential_views": self.PLATFORMS[platform]["base_views"] * random.uniform(0.5, 2.0)
                })
        
        return all_ideas
    
    def create_content(self, title: str, platform: str, content_type: str) -> Content:
        """Create new content"""
        content = Content(
            id=f"content_{datetime.now().timestamp()}",
            title=title,
            platform=platform,
            type=content_type,
            status="draft"
        )
        self.content.append(content)
        return content
    
    def publish_content(self, content_id: str) -> bool:
        """Publish content"""
        for c in self.content:
            if c.id == content_id:
                c.status = "published"
                c.views = random.randint(10, 100)
                self._save_data()
                return True
        return False
    
    def execute(self) -> RevenueResult:
        """Execute content creation cycle"""
        self.status = RevenueStatus.RUNNING
        self.execution_count += 1
        
        try:
            activities = []
            new_revenue = 0.0
            
            # 1. Publish pending content
            drafts = [c for c in self.content if c.status == "draft"]
            if drafts:
                for content in drafts[:3]:
                    self.publish_content(content.id)
                    activities.append(f"Published: {content.title[:30]}")
            
            # 2. Grow published content
            published = [c for c in self.content if c.status == "published"]
            if published:
                for content in published:
                    # Growth
                    growth = random.uniform(0.05, 0.3)
                    content.views = int(content.views * (1 + growth))
                    
                    # Engagement
                    content.engagement = min(0.2, content.engagement + random.uniform(-0.01, 0.02))
                    
                    # Monetization
                    if content.platform == "youtube":
                        revenue = content.views * 0.001 * random.uniform(0.5, 2)  # CPM
                    elif content.platform == "newsletter":
                        revenue = self.subscribers.get("newsletter", 0) * 0.01 * random.uniform(0.5, 1.5)
                    elif content.platform == "blog":
                        revenue = content.views * 0.0005
                    else:
                        revenue = content.views * 0.0001
                    
                    content.monetization += revenue
                    new_revenue += revenue
                
                activities.append(f"Updated {len(published)} content pieces, ${new_revenue:.2f} revenue")
            
            # 3. Grow subscribers
            for platform in self.subscribers:
                growth = random.randint(5, 50)
                self.subscribers[platform] += growth
            
            # 4. Get sponsorships
            if random.random() < 0.2:
                sponsorships = [
                    {"brand": f"Brand{i}", "value": random.randint(100, 1000)}
                    for i in range(random.randint(1, 3))
                ]
                self.sponsorships.extend(sponsorships)
                new_revenue += sum(s["value"] for s in sponsorships)
                activities.append(f"New sponsorships: ${sum(s['value'] for s in sponsorships)}")
            
            # 5. Create new content
            if random.random() < 0.5:
                ideas = self.generate_ideas()
                idea = random.choice(ideas)
                content = self.create_content(idea["title"], idea["platform"], idea["type"])
                activities.append(f"Created draft: {content.title[:30]}")
            
            result = RevenueResult(
                model="content_creator",
                amount=new_revenue,
                currency="USD",
                timestamp=datetime.now(),
                details={
                    "activities": activities,
                    "total_content": len(self.content),
                    "published": len(published),
                    "total_views": sum(c.views for c in published),
                    "subscribers": self.subscribers,
                    "sponsorships_count": len(self.sponsorships),
                    "avg_engagement": sum(c.engagement for c in published) / len(published) if published else 0
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
                model="content_creator",
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
            "total_views": sum(c.views for c in published),
            "subscribers": self.subscribers,
            "sponsorships": len(self.sponsorships),
            "total_revenue": self.total_revenue
        }
    
    def stop(self):
        """Stop the model"""
        self.is_running = False
        self.status = RevenueStatus.STOPPED
        self._save_data()
