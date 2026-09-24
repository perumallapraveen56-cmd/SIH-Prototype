import { RiskLevel } from './risk.model';

export interface WhatIfRequest {
  compensation_delay_reduction_pct: number;
  legal_disputes_resolution_pct: number;
  approvals_expedited_pct: number;
  rr_progress_acceleration_pct: number;
  documentation_streamlining_pct: number;
}

export interface WhatIfResponse {
  project_id: number;
  project_code: string;
  project_name: string;
  
  baseline_risk_score: number;
  baseline_risk_level: RiskLevel;
  baseline_delay_days: number;
  baseline_cost_impact_cr: number;
  
  simulated_risk_score: number;
  simulated_risk_level: RiskLevel;
  simulated_delay_days: number;
  simulated_cost_impact_cr: number;
  
  risk_reduction_pct: number;
  delay_reduction_days: number;
  cost_savings_cr: number;
  
  key_drivers_addressed: string[];
  model_confidence: number;
}

export interface FinancialImpactScenario {
  scenario_label: string;
  additional_days: number;
  total_delay_days: number;
  daily_cost_lakhs: number;
  estimated_cost_cr: number;
  impact_level: string;
}

export interface FinancialImpactResponse {
  project_id: number;
  project_code: string;
  project_name: string;
  daily_delay_cost_lakhs: number;
  base_budget_cr: number;
  current_predicted_delay_days: number;
  current_estimated_cost_cr: number;
  scenarios: FinancialImpactScenario[];
}
