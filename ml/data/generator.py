"""
Synthetic Land Acquisition Delay Dataset Generator for Prototype & Benchmarking
Team: NEXORA_TAU (SIH26017)
Generates statistically realistic tabular dataset reflecting Indian land acquisition dynamics:
- RFCTLARR Act 2013 provisions (Section 11, 19, 23, 30)
- Statutory clearances (Forest Stage I & II, MoEF&CC, Wildlife)
- Resettlement & Rehabilitation (R&R) scheme implementation
- Compensation disbursement timelines and court litigations
"""

import numpy as np
import pandas as pd
import os

STATES = ["Andhra Pradesh", "Maharashtra", "Odisha", "Rajasthan", "Uttar Pradesh", "Karnataka", "Tamil Nadu", "Gujarat", "Madhya Pradesh", "Bihar"]
PROJECT_TYPES = ["Highway Expansion", "Railway Dedicated Freight", "Metro Rail Corridor", "Industrial Park", "Solar Energy Park", "Port Connectivity Highway"]
STAGES = [
    "Section 11 (Preliminary Notification)",
    "Section 19 (Declaration of Acquisition)",
    "Section 23 (Award Enquiry & Valuation)",
    "Section 30 (Physical Possession Taken)",
    "R&R Scheme Implementation"
]

def generate_land_acquisition_dataset(n_samples: int = 2500, random_seed: int = 42) -> pd.DataFrame:
    np.random.seed(random_seed)
    
    states = np.random.choice(STATES, size=n_samples)
    project_types = np.random.choice(PROJECT_TYPES, size=n_samples, p=[0.30, 0.25, 0.15, 0.15, 0.10, 0.05])
    stages = np.random.choice(STAGES, size=n_samples)
    
    total_area_ha = np.round(np.random.exponential(scale=100.0, size=n_samples) + 15.0, 1)
    total_parcels = np.maximum(20, (total_area_ha * np.random.uniform(0.8, 2.2)).astype(int))
    affected_families = np.maximum(10, (total_parcels * np.random.uniform(0.5, 1.2)).astype(int))
    
    # Key risk driving features
    compensation_delay_days = np.round(np.random.exponential(scale=45.0, size=n_samples)).astype(int)
    active_legal_disputes = np.random.poisson(lam=2.5, size=n_samples)
    pending_statutory_approvals = np.random.binomial(n=4, p=0.35, size=n_samples)
    rr_progress_pct = np.round(np.clip(np.random.beta(a=3.0, b=2.0, size=n_samples) * 100, 5, 100), 1)
    documentation_deficiency_score = np.random.randint(1, 10, size=n_samples) # 1 - 9
    landowner_resistance_index = np.random.randint(1, 10, size=n_samples) # 1 - 9
    survey_amendments_count = np.random.poisson(lam=1.5, size=n_samples)
    base_budget_cr = np.round(total_area_ha * np.random.uniform(2.5, 6.5), 1)
    daily_delay_cost_lakhs = np.round(np.clip(base_budget_cr * 0.007 + np.random.normal(1.0, 0.2, size=n_samples), 1.5, 20.0), 2)
    
    # Calibrated realistic delay model
    latent_delay = (
        compensation_delay_days * 0.55 +
        active_legal_disputes * 14.0 +
        pending_statutory_approvals * 18.0 +
        (100.0 - rr_progress_pct) * 0.45 +
        documentation_deficiency_score * 3.2 +
        landowner_resistance_index * 4.0 +
        survey_amendments_count * 5.0 +
        np.random.normal(0, 8.0, size=n_samples)
    )
    predicted_delay_days = np.maximum(5, np.round(latent_delay)).astype(int)
    
    # Tri-class Risk Level Classification:
    # LOW: < 75 days (On Track / Minimal Risk) -> Green
    # MEDIUM: 75 - 145 days (Moderate Delay Concern) -> Yellow/Amber
    # HIGH: > 145 days (Significant Delay Drivers) -> Red
    risk_level = []
    for d in predicted_delay_days:
        if d > 145:
            risk_level.append("HIGH")
        elif d >= 75:
            risk_level.append("MEDIUM")
        else:
            risk_level.append("LOW")
            
    # Risk Score (0.0 - 100.0 scale)
    risk_score = np.round(np.clip(predicted_delay_days * 0.42, 5.0, 99.0), 1)

    df = pd.DataFrame({
        "state": states,
        "project_type": project_types,
        "current_stage": stages,
        "total_area_ha": total_area_ha,
        "total_parcels": total_parcels,
        "affected_families": affected_families,
        "compensation_delay_days": compensation_delay_days,
        "active_legal_disputes": active_legal_disputes,
        "pending_statutory_approvals": pending_statutory_approvals,
        "rr_progress_pct": rr_progress_pct,
        "documentation_deficiency_score": documentation_deficiency_score,
        "landowner_resistance_index": landowner_resistance_index,
        "survey_amendments_count": survey_amendments_count,
        "base_budget_cr": base_budget_cr,
        "daily_delay_cost_lakhs": daily_delay_cost_lakhs,
        "delay_days": predicted_delay_days,
        "risk_score": risk_score,
        "risk_level": risk_level
    })
    
    return df

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    df = generate_land_acquisition_dataset()
    out_path = os.path.join(out_dir, "land_acquisition_dataset.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} records at {out_path}")
    print("Class balance:\n", df["risk_level"].value_counts())
