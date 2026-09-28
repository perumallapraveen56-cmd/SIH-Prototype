from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class RecommendationItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: str
    title: str
    description: str
    priority: str  # CRITICAL, HIGH, MEDIUM
    potential_delay_reduction_days: int
    potential_cost_savings_cr: float
    action_steps: List[str]
    status: str

class RecommendationListResponse(BaseModel):
    project_id: int
    project_code: str
    project_name: str
    district: str
    current_risk_level: str
    total_potential_delay_reduction_days: int
    total_potential_savings_cr: float
    recommendations: List[RecommendationItem]
