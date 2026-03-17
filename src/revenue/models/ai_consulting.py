"""
AI Consulting Revenue Model

Provide AI consulting services.
"""

from typing import Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
import json
import os
import random

from ..base import RevenueModel, RevenueConfig, RevenueResult, RevenueStatus


@dataclass
class Consultant:
    """A consultant or expertise area"""
    id: str
    name: str
    expertise: str
    hourly_rate: float
    projects_completed: int = 0
    rating: float = 0.0


@dataclass
class Project:
    """A consulting project"""
    id: str
    client: str
    description: str
    status: str = "proposal"  # proposal, active, completed
    value: float = 0.0
    hours_billed: float = 0.0
    consultant_id: str = ""


class AIConsulting(RevenueModel):
    """
    AI Consulting - Provide AI expertise
    
    Revenue potential: $1,000-$20,000 monthly
    """
    
    EXPERTISE_AREAS = [
        ("AI Strategy", 200),
        ("Machine Learning Implementation", 250),
        ("NLP Solutions", 225),
        ("Computer Vision", 275),
        ("Process Automation", 175),
        ("AI Ethics & Governance", 200),
        ("Data Strategy", 225),
        ("LLM Implementation", 300),
    ]
    
    def __init__(self, config: RevenueConfig):
        super().__init__(config)
        self.consultants: List[Consultant] = []
        self.projects: List[Project] = []
        self._load_data()
    
    def _load_data(self):
        """Load existing data"""
        data_dir = "/home/workspace/personai/data/revenue"
        
        consultants_file = os.path.join(data_dir, "ai_consulting_consultants.json")
        if os.path.exists(consultants_file):
            try:
                with open(consultants_file, 'r') as f:
                    data = json.load(f)
                    for c in data.get("consultants", []):
                        self.consultants.append(Consultant(**c))
            except Exception:
                pass
        
        projects_file = os.path.join(data_dir, "ai_consulting_projects.json")
        if os.path.exists(projects_file):
            try:
                with open(projects_file, 'r') as f:
                    data = json.load(f)
                    for p in data.get("projects", []):
                        self.projects.append(Project(**p))
            except Exception:
                pass
    
    def _save_data(self):
        """Save data"""
        data_dir = "/home/workspace/personai/data/revenue"
        os.makedirs(data_dir, exist_ok=True)
        
        consultants_file = os.path.join(data_dir, "ai_consulting_consultants.json")
        with open(consultants_file, 'w') as f:
            json.dump({"consultants": [vars(c) for c in self.consultants]}, f, indent=2)
        
        projects_file = os.path.join(data_dir, "ai_consulting_projects.json")
        with open(projects_file, 'w') as f:
            json.dump({"projects": [vars(p) for p in self.projects]}, f, indent=2)
    
    def initialize(self) -> bool:
        """Initialize consulting business"""
        self.status = RevenueStatus.INITIALIZING
        
        # Create default consultants (expertise areas)
        if not self.consultants:
            for area, rate in self.EXPERTISE_AREAS:
                consultant = Consultant(
                    id=f"consultant_{len(self.consultants)}",
                    name=area,
                    expertise=area,
                    hourly_rate=rate,
                    rating=4.5 + random.uniform(0, 0.5)
                )
                self.consultants.append(consultant)
        
        self._load_data()
        self.status = RevenueStatus.IDLE
        return True
    
    def find_prospects(self) -> List[Dict[str, Any]]:
        """Find potential clients"""
        companies = [
            "TechCorp Inc", "FinanceFirst", "HealthPlus", "RetailMax",
            "EduSmart", "LogiTech", "MediaGroup", "ManufacturingCo"
        ]
        
        prospects = []
        for company in random.sample(companies, min(4, len(companies))):
            prospects.append({
                "company": company,
                "industry": random.choice(["tech", "finance", "healthcare", "retail"]),
                "budget": random.randint(5000, 50000),
                "need": random.choice(self.EXPERTISE_AREAS)[0],
                "timeline": random.choice(["immediate", "1-3 months", "3-6 months"])
            })
        
        return prospects
    
    def create_proposal(self, client: str, description: str, value: float, consultant_id: str = "") -> Project:
        """Create a consulting proposal"""
        project = Project(
            id=f"project_{datetime.now().timestamp()}",
            client=client,
            description=description,
            status="proposal",
            value=value,
            consultant_id=consultant_id or (self.consultants[0].id if self.consultants else "")
        )
        self.projects.append(project)
        self._save_data()
        return project
    
    def start_project(self, project_id: str) -> bool:
        """Start a project"""
        for p in self.projects:
            if p.id == project_id and p.status == "proposal":
                p.status = "active"
                self._save_data()
                return True
        return False
    
    def complete_project(self, project_id: str) -> bool:
        """Complete a project"""
        for p in self.projects:
            if p.id == project_id and p.status == "active":
                p.status = "completed"
                
                # Update consultant stats
                for c in self.consultants:
                    if c.id == p.consultant_id:
                        c.projects_completed += 1
                
                self._save_data()
                return True
        return False
    
    def execute(self) -> RevenueResult:
        """Execute consulting revenue cycle"""
        self.status = RevenueStatus.RUNNING
        self.execution_count += 1
        
        try:
            activities = []
            new_revenue = 0.0
            
            # 1. Find prospects
            prospects = self.find_prospects()
            activities.append(f"Found {len(prospects)} potential clients")
            
            # 2. Create proposals
            if prospects and random.random() < 0.5:
                prospect = random.choice(prospects)
                consultant = random.choice(self.consultants) if self.consultants else None
                
                project = self.create_proposal(
                    client=prospect["company"],
                    description=f"{prospect['need']} implementation",
                    value=prospect["budget"],
                    consultant_id=consultant.id if consultant else ""
                )
                activities.append(f"Created proposal: {prospect['company']} - ${prospect['budget']}")
                
                # Sometimes convert to active
                if random.random() < 0.3:
                    self.start_project(project.id)
            
            # 3. Work on active projects
            active = [p for p in self.projects if p.status == "active"]
            if active:
                for project in active:
                    # Bill hours
                    hours = random.uniform(0.5, 5.0)
                    project.hours_billed += hours
                    
                    # Get rate
                    rate = 200  # Default
                    for c in self.consultants:
                        if c.id == project.consultant_id:
                            rate = c.hourly_rate
                            break
                    
                    revenue = hours * rate
                    new_revenue += revenue
                    
                    # Sometimes complete
                    if random.random() < 0.2:
                        self.complete_project(project.id)
                        activities.append(f"Completed project: {project.client}")
                
                activities.append(f"Active projects: {len(active)}, Revenue: ${new_revenue:.2f}")
            
            # 4. Generate new prospects
            if random.random() < 0.4:
                prospects = self.find_prospects()
                activities.append(f"Generated {len(prospects)} new prospect leads")
            
            result = RevenueResult(
                model="ai_consulting",
                amount=new_revenue,
                currency="USD",
                timestamp=datetime.now(),
                details={
                    "activities": activities,
                    "total_projects": len(self.projects),
                    "active_projects": len(active),
                    "completed_projects": len([p for p in self.projects if p.status == "completed"]),
                    "proposals": len([p for p in self.projects if p.status == "proposal"]),
                    "total_billed": sum(p.hours_billed for p in self.projects if p.status == "completed"),
                    "consultants": len(self.consultants)
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
                model="ai_consulting",
                amount=0.0,
                success=False,
                error=str(e)
            )
    
    def get_status(self) -> Dict[str, Any]:
        """Get status"""
        active = [p for p in self.projects if p.status == "active"]
        completed = [p for p in self.projects if p.status == "completed"]
        
        return {
            "status": self.status.value,
            "total_projects": len(self.projects),
            "active": len(active),
            "completed": len(completed),
            "proposals": len([p for p in self.projects if p.status == "proposal"]),
            "total_revenue": self.total_revenue,
            "consultants": len(self.consultants),
            "avg_project_value": sum(p.value for p in completed) / len(completed) if completed else 0
        }
    
    def stop(self):
        """Stop the model"""
        self.is_running = False
        self.status = RevenueStatus.STOPPED
        self._save_data()
