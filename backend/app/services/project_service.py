from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.project import Project
from app.models.risk import RiskPrediction, RiskFactor
from app.schemas.project import ProjectSummary, ProjectDetail
from app.schemas.risk import DashboardKPISummary, ProjectRiskOverviewChart, RiskFactorItem, RiskPredictionItem

def get_dashboard_kpis(db: Session) -> DashboardKPISummary:
    total_projects = db.query(func.count(Project.id)).scalar() or 0
    total_parcels = db.query(func.sum(Project.total_parcels)).scalar() or 0
    avg_progress = db.query(func.avg(Project.acquisition_progress)).scalar() or 0.0

    # Risk level counts
    high_risk_count = db.query(func.count(RiskPrediction.id)).filter(RiskPrediction.risk_level == "HIGH").scalar() or 0
    med_risk_count = db.query(func.count(RiskPrediction.id)).filter(RiskPrediction.risk_level == "MEDIUM").scalar() or 0
    low_risk_count = db.query(func.count(RiskPrediction.id)).filter(RiskPrediction.risk_level == "LOW").scalar() or 0
    avg_delay = db.query(func.avg(RiskPrediction.predicted_delay_days)).scalar() or 0.0

    return DashboardKPISummary(
        total_projects=total_projects,
        land_parcels=int(total_parcels),
        high_risk_projects=high_risk_count,
        medium_risk_projects=med_risk_count,
        low_risk_projects=low_risk_count,
        average_predicted_delay_days=round(float(avg_delay), 1),
        acquisition_progress_pct=round(float(avg_progress), 1)
    )

def get_risk_overview_chart(db: Session) -> ProjectRiskOverviewChart:
    """
    Project Risk Overview Chart:
    IMPORTANT: Must NOT show Critical Risk.
    Only shows:
    - HIGH RISK (Red)
    - MEDIUM RISK (Yellow/Amber)
    - LOW RISK (Green)
    """
    high = db.query(func.count(RiskPrediction.id)).filter(RiskPrediction.risk_level == "HIGH").scalar() or 0
    med = db.query(func.count(RiskPrediction.id)).filter(RiskPrediction.risk_level == "MEDIUM").scalar() or 0
    low = db.query(func.count(RiskPrediction.id)).filter(RiskPrediction.risk_level == "LOW").scalar() or 0
    total = max(1, high + med + low)

    return ProjectRiskOverviewChart(
        high_risk_count=high,
        medium_risk_count=med,
        low_risk_count=low,
        high_risk_pct=round((high / total) * 100.0, 1),
        medium_risk_pct=round((med / total) * 100.0, 1),
        low_risk_pct=round((low / total) * 100.0, 1)
    )

def get_projects(
    db: Session,
    state: Optional[str] = None,
    district: Optional[str] = None,
    project_type: Optional[str] = None,
    risk_level: Optional[str] = None
) -> List[ProjectSummary]:
    query = db.query(Project).join(Project.risk_prediction)

    if state:
        query = query.filter(Project.state.ilike(f"%{state}%"))
    if district:
        query = query.filter(Project.district.ilike(f"%{district}%"))
    if project_type:
        query = query.filter(Project.project_type.ilike(f"%{project_type}%"))
    if risk_level:
        query = query.filter(RiskPrediction.risk_level == risk_level.upper())

    projects = query.order_by(RiskPrediction.risk_score.desc()).all()

    results = []
    for p in projects:
        rp = p.risk_prediction
        results.append(ProjectSummary(
            id=p.id,
            project_code=p.project_code,
            name=p.name,
            district=p.district,
            state=p.state,
            project_type=p.project_type,
            current_stage=p.current_stage,
            status=p.status,
            acquisition_progress=p.acquisition_progress,
            risk_level=rp.risk_level if rp else "LOW",
            risk_score=rp.risk_score if rp else 0.0,
            predicted_delay_days=rp.predicted_delay_days if rp else 0,
            daily_delay_cost_lakhs=p.daily_delay_cost_lakhs
        ))
    return results

def get_project_detail(db: Session, project_id: int) -> Optional[ProjectDetail]:
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        return None

    rp = p.risk_prediction
    risk_pred_item = None
    delay_days = 0
    if rp:
        delay_days = rp.predicted_delay_days
        risk_pred_item = RiskPredictionItem(
            risk_score=rp.risk_score,
            risk_level=rp.risk_level,
            predicted_delay_days=rp.predicted_delay_days,
            delay_confidence_interval=rp.delay_confidence_interval,
            confidence_score=rp.confidence_score,
            model_name=rp.model_name
        )

    # Top risk factors ordered by contribution pct
    factors = db.query(RiskFactor).filter(RiskFactor.project_id == project_id).order_by(RiskFactor.contribution_pct.desc()).all()
    risk_factors_items = [
        RiskFactorItem(
            id=f.id,
            factor_name=f.factor_name,
            contribution_pct=f.contribution_pct,
            severity=f.severity,
            metric_value=f.metric_value,
            details=f.details
        )
        for f in factors
    ]

    # Calculate project-specific estimated cost impact in Crores:
    # (predicted_delay_days * daily_delay_cost_lakhs) / 100.0 (1 Cr = 100 Lakhs)
    cost_impact_cr = round((delay_days * p.daily_delay_cost_lakhs) / 100.0, 2)

    return ProjectDetail(
        id=p.id,
        project_code=p.project_code,
        name=p.name,
        district=p.district,
        state=p.state,
        project_type=p.project_type,
        notification_date=p.notification_date,
        expected_completion=p.expected_completion,
        current_stage=p.current_stage,
        status=p.status,
        total_area_ha=p.total_area_ha,
        acquired_area_ha=p.acquired_area_ha,
        acquisition_progress=p.acquisition_progress,
        total_parcels=p.total_parcels,
        affected_families=p.affected_families,
        base_budget_cr=p.base_budget_cr,
        daily_delay_cost_lakhs=p.daily_delay_cost_lakhs,
        latitude=p.latitude,
        longitude=p.longitude,
        description=p.description,
        estimated_cost_impact_cr=cost_impact_cr,
        risk_prediction=risk_pred_item,
        top_risk_factors=risk_factors_items
    )

def get_land_parcels(
    db: Session,
    project_id: Optional[int] = None,
    stage: Optional[str] = None,
    dispute_status: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Returns granular cadastral land parcel records across monitored infrastructure projects.
    """
    projects_query = db.query(Project)
    if project_id:
        projects_query = projects_query.filter(Project.id == project_id)
    projects = projects_query.all()

    parcels: List[Dict[str, Any]] = []

    # Deterministic generation of 3-4 realistic cadastral parcels per project
    villages_pool = [
        "Sultanpur Khurd", "Bhowapur", "Navi Vasti", "Khed Shivapur",
        "Bidadi Hobli", "Kalasipalya", "Sanand Rural", "Manesar Village",
        "Sriperumbudur", "Singur Purba", "Shamshabad", "Mandhana"
    ]
    owners_pool = [
        "Rameshwar Dayal & Brothers", "Smt. Shanti Devi", "Kisan Sahakari Samiti",
        "Mahesh Chandra Sharma", "Gram Panchayat / Gaon Sabha", "Satish Kumar Patel",
        "Lakshmana Gowda & Heirs", "Murugan Chettiar", "Tapan Roy & Sons"
    ]
    categories = [
        "Agricultural (Double Cropped)", "Agricultural (Rainfed)",
        "Commercial / Roadside Abadi", "Residential Plot", "Gram Sabha Common Land"
    ]
    stages_list = [
        "Section 11 (Preliminary Notification)",
        "Section 19 (Declaration of Acquisition)",
        "Section 21 (Notice to Persons Interested)",
        "Section 23/30 (Enquiry & Award Declaration)",
        "Section 38 (Possession Taken)",
        "R&R Compensation Disbursed"
    ]
    disputes_pool = [
        "Clear / No Dispute",
        "Clear / Compensation Agreed",
        "Title Injunction in Civil Court",
        "High Court Compensation Enhancement Writ",
        "Gram Sabha Boundary Demarcation Dispute",
        "Family Partition Suit Pending"
    ]

    for p in projects:
        num_parcels = min(5, max(3, p.total_parcels // 30))
        for idx in range(1, num_parcels + 1):
            seed_val = (p.id * 17 + idx * 23)
            khasra_no = f"{100 + (seed_val % 450)}/{idx + (seed_val % 7)}"
            parcel_code = f"PC-{p.project_code.replace('PRJ-', '')}-{idx:02d}"
            village = villages_pool[(p.id + idx) % len(villages_pool)]
            owner = owners_pool[(p.id * 2 + idx) % len(owners_pool)]
            category = categories[(p.id + idx) % len(categories)]
            area = round(0.45 + ((seed_val % 85) / 20.0), 2)
            
            p_stage = stages_list[(p.id + idx) % len(stages_list)]
            disp = disputes_pool[(p.id + idx) % len(disputes_pool)]
            
            # Risk determination based on dispute & stage
            is_high_risk = "Court" in disp or "Writ" in disp or "Dispute" in disp
            p_risk_level = "HIGH" if is_high_risk else ("MEDIUM" if "Section 11" in p_stage else "LOW")
            delay_est = 120 if is_high_risk else (45 if "Section 11" in p_stage else 10)

            compensation_amt = round(area * 45.5, 2) # in Lakhs
            comp_status = "Disbursed via PFMS/DBT" if p_stage in ["Section 38 (Possession Taken)", "R&R Compensation Disbursed"] else (
                "Deposited in Civil Court (Sec 77)" if "Court" in disp else "Under Verification / SLAO Scrutiny"
            )

            # Apply filters if specified
            if stage and stage.lower() not in p_stage.lower():
                continue
            if dispute_status and dispute_status.lower() not in disp.lower():
                continue

            parcels.append({
                "parcel_id": parcel_code,
                "khasra_no": khasra_no,
                "project_id": p.id,
                "project_code": p.project_code,
                "project_name": p.name,
                "village": village,
                "district": p.district,
                "state": p.state,
                "khatedar_owner": owner,
                "land_category": category,
                "area_ha": area,
                "acquisition_stage": p_stage,
                "dispute_status": disp,
                "compensation_status": comp_status,
                "compensation_amount_lakhs": compensation_amt,
                "risk_level": p_risk_level,
                "predicted_delay_days": delay_est
            })

    return parcels

