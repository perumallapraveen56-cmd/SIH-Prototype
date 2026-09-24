import { RiskLevel, RiskPredictionItem, RiskFactorItem } from './risk.model';

export interface ProjectSummary {
  id: number;
  project_code: string;
  name: string;
  district: string;
  state: string;
  project_type: string;
  current_stage: string;
  status: string;
  acquisition_progress: number;
  risk_level: RiskLevel;
  risk_score: number;
  predicted_delay_days: number;
  daily_delay_cost_lakhs: number;
}

export interface ProjectDetail {
  id: number;
  project_code: string;
  name: string;
  district: string;
  state: string;
  project_type: string;
  notification_date: string;
  expected_completion: string;
  current_stage: string;
  status: string;
  
  total_area_ha: number;
  acquired_area_ha: number;
  acquisition_progress: number;
  
  total_parcels: number;
  affected_families: number;
  base_budget_cr: number;
  daily_delay_cost_lakhs: number;
  
  latitude: number;
  longitude: number;
  description?: string;
  
  estimated_cost_impact_cr: number;
  risk_prediction?: RiskPredictionItem;
  top_risk_factors: RiskFactorItem[];
}
