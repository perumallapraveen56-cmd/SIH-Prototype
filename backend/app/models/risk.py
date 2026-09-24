from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database.session import Base

class RiskPrediction(Base):
    __tablename__ = "risk_predictions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    risk_score = Column(Float, nullable=False) # 0.0 - 100.0
    risk_level = Column(String(20), nullable=False, index=True) # HIGH, MEDIUM, LOW
    predicted_delay_days = Column(Integer, nullable=False) # In days
    delay_confidence_interval = Column(String(50), nullable=True) # e.g. "±14 days"
    confidence_score = Column(Float, nullable=False, default=0.92) # 0.0 - 1.0
    model_name = Column(String(100), nullable=False, default="CatBoost Ensembled Classifier v2.1")
    
    last_assessed = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="risk_prediction")

    def __repr__(self):
        return f"<RiskPrediction Project {self.project_id}: {self.risk_level} ({self.risk_score})>"


class RiskFactor(Base):
    __tablename__ = "risk_factors"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    factor_name = Column(String(100), nullable=False) # Compensation Delay, Legal Disputes, etc.
    contribution_pct = Column(Float, nullable=False) # e.g. 31.0 for +31%
    severity = Column(String(20), nullable=False, default="MEDIUM") # HIGH, MEDIUM, LOW
    metric_value = Column(String(100), nullable=True) # e.g. "68 days pending", "14 court cases"
    details = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="risk_factors")

    def __repr__(self):
        return f"<RiskFactor {self.factor_name} ({self.contribution_pct}%)>"
