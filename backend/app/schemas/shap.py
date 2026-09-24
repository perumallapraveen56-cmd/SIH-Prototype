from typing import List, Optional
from pydantic import BaseModel

class ShapFeatureItem(BaseModel):
    feature: str
    contribution_pct: float
    direction: str # increases_risk, decreases_risk
    shap_value: float
    impact_label: str
    baseline_value: Optional[str] = None

class ShapExplanationResponse(BaseModel):
    project_id: int
    project_code: str
    project_name: str
    district: str
    state: str
    base_value: float
    output_value: float
    predicted_risk_level: str
    predicted_risk_score: float
    predicted_delay_days: int
    model_used: str
    confidence_score: float
    explanation_summary: str
    features: List[ShapFeatureItem]
