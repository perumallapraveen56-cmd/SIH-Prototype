from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database.session import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(50), unique=True, index=True, nullable=False) # e.g. ALT-2026-001
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    project_name = Column(String(255), nullable=False)
    district = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False, index=True) # HIGH, MEDIUM, LOW
    reason = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=False)
    
    acknowledged = Column(Boolean, default=False, nullable=False)
    acknowledged_by = Column(String(100), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    
    # Flag to prevent repeated audio notification on poll
    sound_played = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    project = relationship("Project", back_populates="alerts")

    def __repr__(self):
        return f"<Alert {self.alert_id} [{self.severity}] - {self.project_name}>"
