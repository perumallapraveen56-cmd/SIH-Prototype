from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.gis import ProjectGISMarker, GISFilterOptions
from app.services.gis_service import get_gis_markers, get_gis_filter_options
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/gis", tags=["GIS Risk Map"])

@router.get("/projects", response_model=List[ProjectGISMarker])
def list_gis_markers(
    state: Optional[str] = Query(None),
    district: Optional[str] = Query(None),
    project_type: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_gis_markers(db, state=state, district=district, project_type=project_type, risk_level=risk_level)

@router.get("/filters", response_model=GISFilterOptions)
def get_filter_dropdowns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_gis_filter_options(db)
