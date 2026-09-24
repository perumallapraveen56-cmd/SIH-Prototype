from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.whatif import WhatIfRequest, WhatIfResponse, FinancialImpactResponse
from app.services.whatif_service import simulate_what_if_scenario, get_project_financial_impact
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["Recommendations & What-If Simulation"])

@router.post("/{project_id}/what-if", response_model=WhatIfResponse)
def run_what_if_simulation(
    project_id: int,
    request: WhatIfRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = simulate_what_if_scenario(db, project_id, request)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found."
        )
    return result

@router.get("/{project_id}/financial-impact", response_model=FinancialImpactResponse)
def get_financial_impact(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = get_project_financial_impact(db, project_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found."
        )
    return result
