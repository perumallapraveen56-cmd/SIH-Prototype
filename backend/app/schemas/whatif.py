from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class WhatIfRequest(BaseModel):
    # Reduction / Improvement interventions (0 to 100 percent)
    compensation_delay_reduction_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    legal_disputes_resolution_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    approvals_expedited_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    rr_progress_acceleration_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    documentation_streamlining_pct: float = Field(default=0.0, ge=0.0, le=100.0)

class WhatIfResponse(BaseModel):
    project_id: int
    project_code: str
    project_name: str
    
    # Baseline (Current)
    baseline_risk_score: float
    baseline_risk_level: str
    baseline_delay_days: int
    baseline_cost_impact_cr: float
    
    # Simulated (After intervention)
    simulated_risk_score: float
    simulated_risk_level: str
    simulated_delay_days: int
    simulated_cost_impact_cr: float
    
    # Reductions / Improvements achieved
    risk_reduction_pct: float
    delay_reduction_days: int
    cost_savings_cr: float
    
    key_drivers_addressed: List[str]
    model_confidence: float

class FinancialImpactScenario(BaseModel):
    scenario_label: str
    additional_days: int
    total_delay_days: int
    daily_cost_lakhs: float
    estimated_cost_cr: float
    impact_level: str # LOW, MODERATE, HIGH, SEVERE

class FinancialImpactResponse(BaseModel):
    project_id: int
    project_code: str
    project_name: str
    daily_delay_cost_lakhs: float
    base_budget_cr: float
    current_predicted_delay_days: int
    current_estimated_cost_cr: float
    scenarios: List[FinancialImpactScenario]
