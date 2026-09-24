from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database.session import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    category = Column(String(100), nullable=False) # Compensation, Legal, Approvals, R&R, Documentation
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(20), nullable=False, default="HIGH") # CRITICAL, HIGH, MEDIUM
    
    potential_delay_reduction_days = Column(Integer, nullable=False, default=30)
    potential_cost_savings_cr = Column(Float, nullable=False, default=12.5) # in ₹ Crores
    action_steps_json = Column(Text, nullable=True) # JSON array of specific action steps
    
    status = Column(String(50), nullable=False, default="PENDING") # PENDING, IN_PROGRESS, RESOLVED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="recommendations")

    def __repr__(self):
        return f"<Recommendation {self.title} ({self.priority})>"
