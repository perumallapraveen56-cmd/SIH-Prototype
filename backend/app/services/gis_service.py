from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from app.models.project import Project
from app.models.risk import RiskPrediction
from app.schemas.gis import ProjectGISMarker, GISFilterOptions

def get_gis_markers(
    db: Session,
    state: Optional[str] = None,
    district: Optional[str] = None,
    project_type: Optional[str] = None,
    risk_level: Optional[str] = None
) -> List[ProjectGISMarker]:
    query = db.query(Project).join(Project.risk_prediction)

    if state and state.strip():
        query = query.filter(Project.state.ilike(f"%{state.strip()}%"))
    if district and district.strip():
        query = query.filter(Project.district.ilike(f"%{district.strip()}%"))
    if project_type and project_type.strip():
        query = query.filter(Project.project_type.ilike(f"%{project_type.strip()}%"))
    if risk_level and risk_level.strip():
        query = query.filter(RiskPrediction.risk_level == risk_level.strip().upper())

    projects = query.all()
    markers = []
    for p in projects:
        rp = p.risk_prediction
        markers.append(ProjectGISMarker(
            id=p.id,
            project_code=p.project_code,
            name=p.name,
            district=p.district,
            state=p.state,
            project_type=p.project_type,
            latitude=p.latitude,
            longitude=p.longitude,
            risk_level=rp.risk_level if rp else "LOW",
            risk_score=rp.risk_score if rp else 0.0,
            predicted_delay_days=rp.predicted_delay_days if rp else 0,
            acquisition_progress=p.acquisition_progress,
            status=p.status
        ))
    return markers

def get_gis_filter_options(db: Session) -> GISFilterOptions:
    states = [s[0] for s in db.query(distinct(Project.state)).order_by(Project.state).all() if s[0]]
    districts = [d[0] for d in db.query(distinct(Project.district)).order_by(Project.district).all() if d[0]]
    types = [t[0] for t in db.query(distinct(Project.project_type)).order_by(Project.project_type).all() if t[0]]
    risk_levels = ["HIGH", "MEDIUM", "LOW"]

    return GISFilterOptions(
        states=states,
        districts=districts,
        project_types=types,
        risk_levels=risk_levels
    )
