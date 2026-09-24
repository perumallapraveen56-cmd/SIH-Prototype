import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.models.project import Project
from app.schemas.alert import AlertItem, AlertPollResponse

def get_all_alerts(db: Session, severity: Optional[str] = None) -> List[AlertItem]:
    query = db.query(Alert)
    if severity:
        query = query.filter(Alert.severity == severity.upper())
    alerts = query.order_by(Alert.created_at.desc()).all()
    return [AlertItem.model_validate(a) for a in alerts]

def poll_alerts_with_sound_check(db: Session) -> AlertPollResponse:
    """
    Polls alerts and evaluates if a notification sound should be triggered.
    CRITICAL SAFETY RULES:
    1. Only plays for NEW, UNACKNOWLEDGED, HIGH severity alerts.
    2. Once an alert triggers a sound, its sound_played flag is set to True in DB.
    3. Acknowledged alerts NEVER trigger sound.
    4. Prevents duplicate audio loops.
    """
    all_alerts = db.query(Alert).order_by(Alert.created_at.desc()).all()
    
    unacked_high_count = 0
    new_alert_ids = []
    should_play = False

    for a in all_alerts:
        if a.severity == "HIGH" and not a.acknowledged:
            unacked_high_count += 1
            if not a.sound_played:
                should_play = True
                new_alert_ids.append(a.alert_id)
                a.sound_played = True

    if should_play:
        db.commit()

    return AlertPollResponse(
        alerts=[AlertItem.model_validate(a) for a in all_alerts],
        total_alerts=len(all_alerts),
        unacknowledged_high_count=unacked_high_count,
        should_play_sound=should_play,
        new_alert_ids=new_alert_ids
    )

def acknowledge_alert(db: Session, alert_id: str, acknowledged_by: str = "Officer") -> Optional[AlertItem]:
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not alert:
        return None

    alert.acknowledged = True
    alert.acknowledged_by = acknowledged_by
    alert.acknowledged_at = datetime.now(timezone.utc)
    alert.sound_played = True
    db.commit()
    db.refresh(alert)
    return AlertItem.model_validate(alert)

def trigger_live_high_risk_alert(db: Session, project_id: Optional[int] = None) -> AlertItem:
    p = None
    if project_id:
        p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        p = db.query(Project).filter(Project.project_code == "PRJ-OD-2024-08").first() or db.query(Project).first()

    unique_num = uuid.uuid4().hex[:6].upper()
    alert_code = f"ALT-LIVE-{unique_num}"

    new_alert = Alert(
        alert_id=alert_code,
        project_id=p.id,
        project_name=p.name,
        district=p.district,
        severity="HIGH",
        reason="Urgent Risk Spike: Environmental Clearance Stage-II withheld due to compliance deficiency; +45 days projected slippage.",
        recommended_action="Convene emergency taskforce review with District Magistrate and PCCF within 48 hours.",
        acknowledged=False,
        sound_played=False,
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return AlertItem.model_validate(new_alert)
