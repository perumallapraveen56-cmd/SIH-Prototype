from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.shap import ShapExplanationResponse
from app.services.shap_service import get_shap_for_project
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["AI Insights & SHAP Explainability"])

@router.get("/{project_id}/shap", response_model=ShapExplanationResponse)
def get_project_shap_analysis(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    shap_data = get_shap_for_project(db, project_id)
    if not shap_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"SHAP attribution not found for project ID {project_id}."
        )
    return shap_data
