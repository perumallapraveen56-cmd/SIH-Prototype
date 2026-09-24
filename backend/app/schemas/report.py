from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class ReportGenerateRequest(BaseModel):
    report_type: str # "PROJECT_RISK", "DISTRICT_RISK", "STATE_RISK", "AI_EXPLAINABILITY"
    project_id: Optional[int] = None
    district: Optional[str] = None
    state: Optional[str] = None
    export_format: str = "json" # "json" or "pdf"

class ReportSummaryItem(BaseModel):
    report_id: str
    title: str
    report_type: str
    generated_at: str
    summary: str
    key_metrics: Dict[str, Any]
    recommendations_count: int
    high_risk_flag: bool
