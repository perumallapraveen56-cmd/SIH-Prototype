import { RiskLevel } from './risk.model';

export interface AlertItem {
  id: number;
  alert_id: string;
  project_id: number;
  project_name: string;
  district: string;
  severity: RiskLevel;
  reason: string;
  recommended_action: string;
  acknowledged: boolean;
  acknowledged_by?: string;
  acknowledged_at?: string;
  sound_played: boolean;
  created_at: string;
}

export interface AlertPollResponse {
  alerts: AlertItem[];
  total_alerts: number;
  unacknowledged_high_count: number;
  should_play_sound: boolean;
  new_alert_ids: string[];
}
