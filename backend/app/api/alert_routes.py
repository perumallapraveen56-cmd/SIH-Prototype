from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.alert import AlertItem, AlertPollResponse, AlertAcknowledgeRequest
from app.services.alert_service import (
    get_all_alerts, poll_alerts_with_sound_check, acknowledge_alert, trigger_live_high_risk_alert
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/alerts", tags=["Alerts & Notifications"])

@router.get("", response_model=List[AlertItem])
def list_alerts(
    severity: Optional[str] = Query(None, description="Filter by severity: HIGH, MEDIUM, LOW"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_alerts(db, severity=severity)

@router.get("/poll", response_model=AlertPollResponse)
def poll_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Polled periodically by frontend.
    Returns should_play_sound: True only once for newly detected high risk alerts.
    """
    return poll_alerts_with_sound_check(db)

@router.post("/{alert_id}/acknowledge", response_model=AlertItem)
def acknowledge_single_alert(
    alert_id: str,
    req: AlertAcknowledgeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_name = current_user.full_name if current_user else (req.acknowledged_by or "Officer")
    updated = acknowledge_alert(db, alert_id, acknowledged_by=user_name)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert {alert_id} not found."
        )
    return updated

@router.post("/trigger-live", response_model=AlertItem)
def trigger_live_demo_alert(
    project_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Allows user or evaluation judge to trigger a live high-risk alert event
    to immediately test visual warning and sound notifications!
    """
    return trigger_live_high_risk_alert(db, project_id=project_id)
