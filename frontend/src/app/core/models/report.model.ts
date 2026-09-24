export interface ReportGenerateRequest {
  report_type: 'PROJECT_RISK' | 'DISTRICT_RISK' | 'STATE_RISK' | 'AI_EXPLAINABILITY';
  project_id?: number;
  district?: string;
  state?: string;
  export_format: 'json' | 'pdf';
}

export interface ReportSummaryItem {
  report_id: string;
  title: string;
  report_type: string;
  generated_at: string;
  summary: string;
  key_metrics: Record<string, any>;
  recommendations_count: number;
  high_risk_flag: boolean;
}
