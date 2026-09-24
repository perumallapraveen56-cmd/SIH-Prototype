from typing import List, Optional
from pydantic import BaseModel

class RiskFactorItem(BaseModel):
    id: Optional[int] = None
    factor_name: str
    contribution_pct: float
    severity: str
    metric_value: Optional[str] = None
    details: Optional[str] = None

    class Config:
        from_attributes = True

class RiskPredictionItem(BaseModel):
    risk_score: float
    risk_level: str  # HIGH, MEDIUM, LOW
    predicted_delay_days: int
    delay_confidence_interval: Optional[str] = None
    confidence_score: float
    model_name: str

    class Config:
        from_attributes = True

class DashboardKPISummary(BaseModel):
    total_projects: int
    land_parcels: int
    high_risk_projects: int
    medium_risk_projects: int
    low_risk_projects: int
    average_predicted_delay_days: float
    acquisition_progress_pct: float

class ProjectRiskOverviewChart(BaseModel):
    """
    IMPORTANT: Must NOT show Critical Risk.
    Only shows:
    - High Risk (Red)
    - Medium Risk (Yellow/Amber)
    - Low Risk (Green)
    """
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    high_risk_pct: float
    medium_risk_pct: float
    low_risk_pct: float
