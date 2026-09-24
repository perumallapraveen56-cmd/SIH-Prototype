from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class AlertItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    alert_id: str
    project_id: int
    project_name: str
    district: str
    severity: str  # HIGH, MEDIUM, LOW
    reason: str
    recommended_action: str
    acknowledged: bool
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    sound_played: bool
    created_at: datetime

class AlertAcknowledgeRequest(BaseModel):
    acknowledged_by: Optional[str] = "Current Officer"

class AlertPollResponse(BaseModel):
    alerts: List[AlertItem]
    total_alerts: int
    unacknowledged_high_count: int
    should_play_sound: bool
    new_alert_ids: List[str]
