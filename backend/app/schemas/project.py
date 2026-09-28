from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.risk import RiskPredictionItem, RiskFactorItem

class ProjectSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_code: str
    name: str
    district: str
    state: str
    project_type: str
    current_stage: str
    status: str
    acquisition_progress: float
    risk_level: str
    risk_score: float
    predicted_delay_days: int
    daily_delay_cost_lakhs: float

class ProjectDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_code: str
    name: str
    district: str
    state: str
    project_type: str
    notification_date: str
    expected_completion: str
    current_stage: str
    status: str
    
    total_area_ha: float
    acquired_area_ha: float
    acquisition_progress: float
    
    total_parcels: int
    affected_families: int
    base_budget_cr: float
    daily_delay_cost_lakhs: float
    
    latitude: float
    longitude: float
    description: Optional[str] = None
    
    # Financial impact calculation based on project's specific daily delay cost
    estimated_cost_impact_cr: float
    
    risk_prediction: Optional[RiskPredictionItem] = None
    top_risk_factors: List[RiskFactorItem] = []
