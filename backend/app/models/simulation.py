from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database.session import Base

class WhatIfSimulation(Base):
    __tablename__ = "what_if_simulations"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    scenario_name = Column(String(255), nullable=False, default="Custom Intervention Scenario")
    input_params_json = Column(Text, nullable=False) # Parameters modified
    
    baseline_risk = Column(Float, nullable=False)
    simulated_risk = Column(Float, nullable=False)
    baseline_delay_days = Column(Integer, nullable=False)
    simulated_delay_days = Column(Integer, nullable=False)
    
    risk_reduction_pct = Column(Float, nullable=False)
    delay_reduction_days = Column(Integer, nullable=False)
    estimated_cost_savings_cr = Column(Float, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="simulations")

    def __repr__(self):
        return f"<WhatIfSimulation {self.scenario_name} (Risk -{self.risk_reduction_pct}%)>"
