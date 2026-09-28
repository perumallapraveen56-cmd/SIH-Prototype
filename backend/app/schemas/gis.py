from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class ProjectGISMarker(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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

class GISFilterOptions(BaseModel):
    states: List[str]
    districts: List[str]
    project_types: List[str]
    risk_levels: List[str]
