from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database.session import Base

class ShapExplanation(Base):
    __tablename__ = "shap_explanations"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    base_value = Column(Float, nullable=False, default=0.25)
    output_value = Column(Float, nullable=False, default=0.78)
    model_used = Column(String(100), nullable=False, default="CatBoost + TreeSHAP Kernel v2.4")
    confidence_score = Column(Float, nullable=False, default=0.94)
    explanation_summary = Column(Text, nullable=False)
    
    # JSON serialized list of feature contributions:
    # [{"feature": "Compensation Delay", "percentage": 31.0, "direction": "increases_risk", "shap_value": 0.28, "impact_label": "High Delay in Award Disbursement"}, ...]
    features_json = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="shap_explanation")

    def __repr__(self):
        return f"<ShapExplanation Project {self.project_id}>"
