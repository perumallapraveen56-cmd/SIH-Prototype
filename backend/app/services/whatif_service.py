import json
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.simulation import WhatIfSimulation
from app.schemas.whatif import (
    WhatIfRequest, WhatIfResponse,
    FinancialImpactResponse, FinancialImpactScenario
)

def simulate_what_if_scenario(db: Session, project_id: int, req: WhatIfRequest) -> Optional[WhatIfResponse]:
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        return None

    rp = p.risk_prediction
    baseline_risk = rp.risk_score if rp else 75.0
    baseline_delay = rp.predicted_delay_days if rp else 180
    daily_cost_lakhs = p.daily_delay_cost_lakhs

    # Dynamic delay reduction impact weighting based on domain mechanics:
    # 1. Compensation Delay reduction (weight: 0.35 of baseline delay)
    # 2. Legal Disputes resolution (weight: 0.25 of baseline delay)
    # 3. Pending Approvals fast-tracking (weight: 0.20 of baseline delay)
    # 4. R&R Progress acceleration (weight: 0.12 of baseline delay)
    # 5. Documentation streamlining (weight: 0.08 of baseline delay)
    
    comp_impact_days = (req.compensation_delay_reduction_pct / 100.0) * (baseline_delay * 0.35)
    legal_impact_days = (req.legal_disputes_resolution_pct / 100.0) * (baseline_delay * 0.25)
    appr_impact_days = (req.approvals_expedited_pct / 100.0) * (baseline_delay * 0.20)
    rr_impact_days = (req.rr_progress_acceleration_pct / 100.0) * (baseline_delay * 0.12)
    doc_impact_days = (req.documentation_streamlining_pct / 100.0) * (baseline_delay * 0.08)

    total_delay_reduction_days = int(round(
        comp_impact_days + legal_impact_days + appr_impact_days + rr_impact_days + doc_impact_days
    ))
    
    # Cap reduction so simulated delay cannot drop below minimum physiological process timeline (10 days)
    simulated_delay = max(10, baseline_delay - total_delay_reduction_days)
    delay_reduction_achieved = baseline_delay - simulated_delay

    # Recalculate Risk Score
    risk_drop = (delay_reduction_achieved / max(1, baseline_delay)) * (baseline_risk * 0.85)
    simulated_risk = max(10.0, round(baseline_risk - risk_drop, 1))
    risk_reduction_pct = round(((baseline_risk - simulated_risk) / max(0.1, baseline_risk)) * 100.0, 1)

    # Classify simulated risk level
    if simulated_risk > 65.0:
        simulated_risk_level = "HIGH"
    elif simulated_risk >= 35.0:
        simulated_risk_level = "MEDIUM"
    else:
        simulated_risk_level = "LOW"

    # Financial impact calculation (1 Cr = 100 Lakhs)
    baseline_cost_cr = round((baseline_delay * daily_cost_lakhs) / 100.0, 2)
    simulated_cost_cr = round((simulated_delay * daily_cost_lakhs) / 100.0, 2)
    cost_savings_cr = round(baseline_cost_cr - simulated_cost_cr, 2)

    drivers_addressed = []
    if req.compensation_delay_reduction_pct > 0:
        drivers_addressed.append(f"Compensation Disbursement accelerated by {int(req.compensation_delay_reduction_pct)}%")
    if req.legal_disputes_resolution_pct > 0:
        drivers_addressed.append(f"Legal Cases resolution expedited by {int(req.legal_disputes_resolution_pct)}%")
    if req.approvals_expedited_pct > 0:
        drivers_addressed.append(f"Statutory Approvals fast-tracked by {int(req.approvals_expedited_pct)}%")
    if req.rr_progress_acceleration_pct > 0:
        drivers_addressed.append(f"R&R Resettlement accelerated by {int(req.rr_progress_acceleration_pct)}%")
    if req.documentation_streamlining_pct > 0:
        drivers_addressed.append(f"Digital Land Documentation streamlined by {int(req.documentation_streamlining_pct)}%")

    # Persist simulation log in DB for audit trail
    sim_record = WhatIfSimulation(
        project_id=p.id,
        scenario_name="Custom Intervention Simulation",
        input_params_json=json.dumps(req.dict()),
        baseline_risk=baseline_risk,
        simulated_risk=simulated_risk,
        baseline_delay_days=baseline_delay,
        simulated_delay_days=simulated_delay,
        risk_reduction_pct=risk_reduction_pct,
        delay_reduction_days=delay_reduction_achieved,
        estimated_cost_savings_cr=cost_savings_cr
    )
    db.add(sim_record)
    db.commit()

    return WhatIfResponse(
        project_id=p.id,
        project_code=p.project_code,
        project_name=p.name,
        baseline_risk_score=baseline_risk,
        baseline_risk_level=rp.risk_level if rp else "HIGH",
        baseline_delay_days=baseline_delay,
        baseline_cost_impact_cr=baseline_cost_cr,
        simulated_risk_score=simulated_risk,
        simulated_risk_level=simulated_risk_level,
        simulated_delay_days=simulated_delay,
        simulated_cost_impact_cr=simulated_cost_cr,
        risk_reduction_pct=risk_reduction_pct,
        delay_reduction_days=delay_reduction_achieved,
        cost_savings_cr=cost_savings_cr,
        key_drivers_addressed=drivers_addressed or ["Baseline parameters maintained"],
        model_confidence=0.94
    )

def get_project_financial_impact(db: Session, project_id: int) -> Optional[FinancialImpactResponse]:
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        return None

    rp = p.risk_prediction
    curr_delay = rp.predicted_delay_days if rp else 120
    daily_cost_lakhs = p.daily_delay_cost_lakhs
    base_budget = p.base_budget_cr

    curr_cost_cr = round((curr_delay * daily_cost_lakhs) / 100.0, 2)

    # Scenarios: Current, +7 Days, +15 Days, +30 Days, +60 Days
    offsets = [
        ("Current Predicted", 0, "BASELINE"),
        ("+7 Days Slippage", 7, "LOW"),
        ("+15 Days Slippage", 15, "MODERATE"),
        ("+30 Days Slippage", 30, "HIGH"),
        ("+60 Days Slippage", 60, "SEVERE")
    ]

    scenarios = []
    for label, add_days, severity in offsets:
        tot_days = curr_delay + add_days
        cost_cr = round((tot_days * daily_cost_lakhs) / 100.0, 2)
        scenarios.append(FinancialImpactScenario(
            scenario_label=label,
            additional_days=add_days,
            total_delay_days=tot_days,
            daily_cost_lakhs=daily_cost_lakhs,
            estimated_cost_cr=cost_cr,
            impact_level=severity
        ))

    return FinancialImpactResponse(
        project_id=p.id,
        project_code=p.project_code,
        project_name=p.name,
        daily_delay_cost_lakhs=daily_cost_lakhs,
        base_budget_cr=base_budget,
        current_predicted_delay_days=curr_delay,
        current_estimated_cost_cr=curr_cost_cr,
        scenarios=scenarios
    )
