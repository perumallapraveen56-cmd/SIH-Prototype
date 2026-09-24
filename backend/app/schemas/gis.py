from typing import Optional
from pydantic import BaseModel

class ProjectGISMarker(BaseModel):
    id: int
    project_code: str
    name: str
    district: str
    state: str
    project_type: str
    latitude: float
    longitude: float
    risk_level: str  # HIGH (Red), MEDIUM (Yellow/Amber), LOW (Green)
    risk_score: float
    predicted_delay_days: int
    acquisition_progress: float
    status: str

    class Config:
        from_attributes = True

class GISFilterOptions(BaseModel):
    states: list[str]
    districts: list[str]
    project_types: list[str]
    risk_levels: list[str]
