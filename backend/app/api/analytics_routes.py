from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.risk import DashboardKPISummary, ProjectRiskOverviewChart
from app.services.project_service import get_dashboard_kpis, get_risk_overview_chart
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Analytics & KPIs"])

@router.get("/kpis", response_model=DashboardKPISummary)
def get_kpis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_dashboard_kpis(db)

@router.get("/risk-overview", response_model=ProjectRiskOverviewChart)
def get_risk_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns Project Risk Overview distribution.
    CRITICAL SPEC: Only High Risk, Medium Risk, Low Risk.
    No Critical Risk category shown here.
    """
    return get_risk_overview_chart(db)
