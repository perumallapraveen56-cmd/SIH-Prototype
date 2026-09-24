import { RiskLevel } from './risk.model';

export interface RecommendationItem {
  id: number;
  category: string;
  title: string;
  description: string;
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  potential_delay_reduction_days: number;
  potential_cost_savings_cr: number;
  action_steps: string[];
  status: string;
}

export interface RecommendationListResponse {
  project_id: number;
  project_code: string;
  project_name: string;
  district: string;
  current_risk_level: RiskLevel;
  total_potential_delay_reduction_days: number;
  total_potential_savings_cr: number;
  recommendations: RecommendationItem[];
}
