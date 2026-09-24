import { RiskLevel } from './risk.model';

export interface ShapFeatureItem {
  feature: string;
  contribution_pct: number;
  direction: string;
  shap_value: number;
  impact_label: string;
  baseline_value?: string;
}

export interface ShapExplanationResponse {
  project_id: number;
  project_code: string;
  project_name: string;
  district: string;
  state: string;
  base_value: number;
  output_value: number;
  predicted_risk_level: RiskLevel;
  predicted_risk_score: number;
  predicted_delay_days: number;
  model_used: string;
  confidence_score: number;
  explanation_summary: string;
  features: ShapFeatureItem[];
}
