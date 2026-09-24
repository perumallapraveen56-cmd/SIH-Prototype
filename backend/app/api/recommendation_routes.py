from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.recommendation import RecommendationListResponse
from app.services.recommendation_service import get_recommendations_for_project
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["Recommendations"])

@router.get("/{project_id}/recommendations", response_model=RecommendationListResponse)
def get_recommendations(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recs = get_recommendations_for_project(db, project_id)
    if not recs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendations not found for project ID {project_id}."
        )
    return recs
