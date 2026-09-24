export type RiskLevel = 'HIGH' | 'MEDIUM' | 'LOW';

export interface RiskFactorItem {
  id?: number;
  factor_name: string;
  contribution_pct: number;
  severity: RiskLevel;
  metric_value?: string;
  details?: string;
}

export interface RiskPredictionItem {
  risk_score: number;
  risk_level: RiskLevel;
  predicted_delay_days: number;
  delay_confidence_interval?: string;
  confidence_score: number;
  model_name: string;
}

export interface DashboardKPISummary {
  total_projects: number;
  land_parcels: number;
  high_risk_projects: number;
  medium_risk_projects: number;
  low_risk_projects: number;
  average_predicted_delay_days: number;
  acquisition_progress_pct: number;
}

export interface ProjectRiskOverviewChart {
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  high_risk_pct: number;
  medium_risk_pct: number;
  low_risk_pct: number;
}
