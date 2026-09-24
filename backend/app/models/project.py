from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from app.database.session import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. PRJ-2026-001
    name = Column(String(255), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False, index=True)
    project_type = Column(String(100), nullable=False, index=True) # Expressway, Rail Line, Metro Corridor, Industrial Park, etc.
    
    notification_date = Column(String(50), nullable=False) # Gazette publication / Section 11 date
    expected_completion = Column(String(50), nullable=False)
    current_stage = Column(String(150), nullable=False) # Section 11, Section 19, Award Enquiry, Possession, R&R
    status = Column(String(50), nullable=False, default="In Progress") # In Progress, Critical, At Risk, On Schedule
    
    total_area_ha = Column(Float, nullable=False, default=100.0)
    acquired_area_ha = Column(Float, nullable=False, default=45.0)
    acquisition_progress = Column(Float, nullable=False, default=45.0) # Percentage 0-100
    
    total_parcels = Column(Integer, nullable=False, default=120)
    affected_families = Column(Integer, nullable=False, default=85)
    base_budget_cr = Column(Float, nullable=False, default=500.0) # In ₹ Crores
    daily_delay_cost_lakhs = Column(Float, nullable=False, default=4.5) # Specific project daily delay cost in ₹ Lakhs
    
    # Coordinates for GIS mapping
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    risk_prediction = relationship("RiskPrediction", back_populates="project", uselist=False, cascade="all, delete-orphan")
    risk_factors = relationship("RiskFactor", back_populates="project", cascade="all, delete-orphan")
    shap_explanation = relationship("ShapExplanation", back_populates="project", uselist=False, cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="project", cascade="all, delete-orphan")
    simulations = relationship("WhatIfSimulation", back_populates="project", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project {self.project_code} - {self.name}>"
