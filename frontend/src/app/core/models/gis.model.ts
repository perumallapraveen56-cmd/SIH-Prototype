import { RiskLevel } from './risk.model';

export interface ProjectGISMarker {
  id: number;
  project_code: string;
  name: string;
  district: string;
  state: string;
  project_type: string;
  latitude: number;
  longitude: number;
  risk_level: RiskLevel;
  risk_score: number;
  predicted_delay_days: number;
  acquisition_progress: number;
  status: string;
}

export interface GISFilterOptions {
  states: string[];
  districts: string[];
  project_types: string[];
  risk_levels: string[];
}
