from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.project import ProjectSummary, ProjectDetail
from app.services.project_service import get_projects, get_project_detail
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("", response_model=List[ProjectSummary])
def list_projects(
    state: Optional[str] = Query(None, description="Filter by state"),
    district: Optional[str] = Query(None, description="Filter by district"),
    project_type: Optional[str] = Query(None, description="Filter by project type"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level (HIGH, MEDIUM, LOW)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_projects(db, state=state, district=district, project_type=project_type, risk_level=risk_level)

@router.get("/{project_id}", response_model=ProjectDetail)
def get_single_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_detail(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found."
        )
    return project

@router.get("/{project_id}/risk")
def get_project_risk_factors(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_detail(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found."
        )
    return {
        "project_id": project.id,
        "project_code": project.project_code,
        "project_name": project.name,
        "risk_prediction": project.risk_prediction,
        "top_risk_factors": project.top_risk_factors,
        "estimated_cost_impact_cr": project.estimated_cost_impact_cr
    }
