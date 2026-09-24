"""
Database Seeding Script for Land Acquisition Delay Prediction System
PS ID: SIH26017 | Team: NEXORA_TAU
Populates relational data for Users, Projects, Risk Predictions, SHAP Explanations,
Recommendations, and Alerts.
"""

import json
from datetime import datetime, timezone, timedelta
from app.core.security import get_password_hash
from app.database.session import Base, engine, SessionLocal
from app.models.user import User
from app.models.project import Project
from app.models.risk import RiskPrediction, RiskFactor
from app.models.shap import ShapExplanation
from app.models.recommendation import Recommendation
from app.models.alert import Alert

def seed_database():
    # Ensure all tables exist in database
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if users already seeded
        if db.query(User).first() is not None:
            print("Database already contains records. Skipping seed.")
            return

        print("Seeding Users for RBAC (Admin, Officer, Analyst)...")
        users = [
            User(
                email="officer@nexora.gov.in",
                hashed_password=get_password_hash("Officer@123"),
                full_name="Rajesh Kumar, IAS",
                role="Officer",
                department="District Land Acquisition & Revenue Cell",
                is_active=True
            ),
            User(
                email="analyst@nexora.gov.in",
                hashed_password=get_password_hash("Analyst@123"),
                full_name="Dr. Sneha Verma",
                role="Analyst",
                department="Infrastructure Analytics & Risk Division",
                is_active=True
            ),
            User(
                email="admin@nexora.gov.in",
                hashed_password=get_password_hash("Admin@123"),
                full_name="Vikramaditya Sharma",
                role="Admin",
                department="National Infrastructure Pipeline PMU",
                is_active=True
            )
        ]
        db.add_all(users)
        db.commit()

        print("Seeding Infrastructure Land Acquisition Projects...")
        projects_data = [
            {
                "code": "PRJ-OD-2024-08",
                "name": "Khurda Road-Bolangir Rail Line (BhoomiRashi-linked)",
                "district": "Balangir",
                "state": "Odisha",
                "type": "Railway Dedicated Freight",
                "notification_date": "2023-04-18",
                "expected_completion": "2026-12-31",
                "current_stage": "Section 19 (Declaration of Acquisition)",
                "status": "At Risk",
                "total_area_ha": 385.0,
                "acquired_area_ha": 132.8,
                "progress": 34.5,
                "total_parcels": 480,
                "affected_families": 395,
                "budget_cr": 1450.0,
                "daily_cost_lakhs": 6.8,
                "lat": 20.7144,
                "lng": 83.4889,
                "desc": "Critical railway corridor connecting coastal Odisha with western hinterlands, experiencing severe forest diversion delays and compensation title verification bottlenecks.",
                "risk_score": 88.5,
                "risk_level": "HIGH",
                "predicted_delay": 213,
                "factors": [
                    {"name": "Compensation Delay", "pct": 31.0, "sev": "HIGH", "val": "85 days pending disbursement", "details": "District treasury disbursement backlog across 4 revenue circles."},
                    {"name": "Legal Disputes", "pct": 22.0, "sev": "HIGH", "val": "18 civil & writ petitions", "details": "High Court interim stay orders regarding ancestral land tenancy rights."},
                    {"name": "Pending Approvals", "pct": 18.0, "sev": "HIGH", "val": "3 statutory clearances", "details": "MoEF&CC Stage-II forest clearance awaiting wildlife warden compliance."},
                    {"name": "R&R Progress", "pct": 11.0, "sev": "MEDIUM", "val": "34.5% completed", "details": "Rehabilitation housing colony handover pending in Bolangir Tehsil."},
                    {"name": "Documentation Issues", "pct": 7.0, "sev": "MEDIUM", "val": "42 disputed mutations", "details": "Discrepancies in legacy RoR records and joint measurement surveys."},
                    {"name": "Land Owner Resistance", "pct": 6.0, "sev": "MEDIUM", "val": "Agitation in 3 villages", "details": "Demand for enhanced ex-gratia compensation in rural agricultural plots."},
                    {"name": "Survey & Amendments", "pct": 3.0, "sev": "LOW", "val": "2 alignment changes", "details": "Joint measurement survey alignment re-validations at river bridge piers."},
                    {"name": "Other Factors", "pct": 2.0, "sev": "LOW", "val": "Minor inter-departmental", "details": "Sub-registrar office staffing constraints."}
                ],
                "shap_factors": [
                    {"feature": "Compensation Delay", "contribution_pct": 31.0, "direction": "increases_risk", "shap_value": 0.312, "impact_label": "High delay in award disbursement and treasury release"},
                    {"feature": "Legal Disputes", "contribution_pct": 22.0, "direction": "increases_risk", "shap_value": 0.224, "impact_label": "Multiple High Court land title writ petitions"},
                    {"feature": "Pending Approvals", "contribution_pct": 18.0, "direction": "increases_risk", "shap_value": 0.181, "impact_label": "Pending MoEF&CC Stage-II forest diversion clearance"},
                    {"feature": "R&R Progress", "contribution_pct": 11.0, "direction": "increases_risk", "shap_value": 0.113, "impact_label": "Rehabilitation housing colony handover pending"},
                    {"feature": "Documentation Issues", "contribution_pct": 7.0, "direction": "increases_risk", "shap_value": 0.071, "impact_label": "Unregistered legacy inheritances & boundary mismatches"},
                    {"feature": "Land Owner Resistance", "contribution_pct": 6.0, "direction": "increases_risk", "shap_value": 0.062, "impact_label": "Demand for enhanced ex-gratia compensation in rural pockets"},
                    {"feature": "Survey & Amendments", "contribution_pct": 3.0, "direction": "increases_risk", "shap_value": 0.031, "impact_label": "Re-survey of canal intersection parcels"},
                    {"feature": "Other Factors", "contribution_pct": 2.0, "direction": "increases_risk", "shap_value": 0.021, "impact_label": "Sub-registrar office staffing constraints"}
                ],
                "recommendations": [
                    {
                        "category": "Compensation",
                        "title": "Establish Fast-Track Special Treasury Disbursement Counter",
                        "desc": "Constitute a dedicated camp office in Bolangir with state treasury and SLAO officers to clear pending award disbursements within 21 days.",
                        "priority": "CRITICAL",
                        "delay_red": 55,
                        "savings_cr": 37.4,
                        "steps": ["Issue mandate for weekly sub-treasury clearing camps", "Authorize direct DBT to verified farmer bank accounts", "Deploy 4 revenue data operators to expedite title verification"]
                    },
                    {
                        "category": "Approvals",
                        "title": "Escalate MoEF&CC Stage-II Forest Diversion to State Apex Committee",
                        "desc": "Submit compensatory afforestation compliance report to Principal Chief Conservator of Forests to expedite Stage-II forest clearance clearance.",
                        "priority": "HIGH",
                        "delay_red": 40,
                        "savings_cr": 27.2,
                        "steps": ["Finalize non-forest CA land demarcation with GPS coordinates", "Convene bilateral coordination session with State Forest Dept", "Submit compliance certificate on Parivesh 2.0 portal"]
                    },
                    {
                        "category": "Legal",
                        "title": "Initiate Lok Adalat & Alternate Dispute Resolution for Tenancy Claims",
                        "desc": "Partner with District Legal Services Authority (DLSA) to conduct Lok Adalat proceedings for 18 pending civil disputes.",
                        "priority": "HIGH",
                        "delay_red": 35,
                        "savings_cr": 23.8,
                        "steps": ["Schedule dedicated Lok Adalat bench for land title compromise", "Provide immediate solatium advance to consenting claimants", "Appoint senior government standing counsel for daily hearings"]
                    }
                ]
            },
            {
                "code": "PRJ-AP-2024-12",
                "name": "Kotipalli-Narasapur Rail Line Corridor",
                "district": "East Godavari",
                "state": "Andhra Pradesh",
                "type": "Railway Dedicated Freight",
                "notification_date": "2023-01-10",
                "expected_completion": "2026-11-15",
                "current_stage": "Section 23 (Award Enquiry & Valuation)",
                "status": "At Risk",
                "total_area_ha": 310.0,
                "acquired_area_ha": 130.2,
                "progress": 42.0,
                "total_parcels": 350,
                "affected_families": 280,
                "budget_cr": 1120.0,
                "daily_cost_lakhs": 5.4,
                "lat": 16.7107,
                "lng": 81.8040,
                "desc": "Godavari delta rail link crucial for regional agricultural and cargo transit facing coastal regulation and private aquaculture land resistance.",
                "risk_score": 84.0,
                "risk_level": "HIGH",
                "predicted_delay": 216,
                "factors": [
                    {"name": "Compensation Delay", "pct": 29.0, "sev": "HIGH", "val": "72 days pending", "details": "Aquaculture pond valuation methodology dispute."},
                    {"name": "Legal Disputes", "pct": 24.0, "sev": "HIGH", "val": "14 writ petitions", "details": "Coastal zone land ownership boundary litigations."},
                    {"name": "Pending Approvals", "pct": 19.0, "sev": "HIGH", "val": "CRZ clearance pending", "details": "Coastal Zone Management Authority approval awaited."},
                    {"name": "R&R Progress", "pct": 12.0, "sev": "MEDIUM", "val": "40% completed", "details": "Alternative fishing jetty rehabilitation works ongoing."},
                    {"name": "Documentation Issues", "pct": 6.0, "sev": "MEDIUM", "val": "28 revenue mismatches", "details": "Survey number overlapping in tidal areas."},
                    {"name": "Land Owner Resistance", "pct": 5.0, "sev": "LOW", "val": "Local fishermen committee", "details": "Concerns regarding boat passage near bridge."},
                    {"name": "Survey & Amendments", "pct": 3.0, "sev": "LOW", "val": "Bridge approach survey", "details": "Hydrological re-survey for approach embankment."},
                    {"name": "Other Factors", "pct": 2.0, "sev": "LOW", "val": "General coordination", "details": "State electricity line shifting."}
                ],
                "shap_factors": [
                    {"feature": "Compensation Delay", "contribution_pct": 29.0, "direction": "increases_risk", "shap_value": 0.285, "impact_label": "Valuation of aquaculture ponds delayed"},
                    {"feature": "Legal Disputes", "contribution_pct": 24.0, "direction": "increases_risk", "shap_value": 0.238, "impact_label": "Delta land boundary title litigations"},
                    {"feature": "Pending Approvals", "contribution_pct": 19.0, "direction": "increases_risk", "shap_value": 0.192, "impact_label": "CRZ coastal clearance backlog"},
                    {"feature": "R&R Progress", "contribution_pct": 12.0, "direction": "increases_risk", "shap_value": 0.120, "impact_label": "Fishermen jetty rehabilitation progress"},
                    {"feature": "Documentation Issues", "contribution_pct": 6.0, "direction": "increases_risk", "shap_value": 0.061, "impact_label": "Tidal survey boundary overlaps"},
                    {"feature": "Land Owner Resistance", "contribution_pct": 5.0, "direction": "increases_risk", "shap_value": 0.051, "impact_label": "Local community livelihood concerns"},
                    {"feature": "Survey & Amendments", "contribution_pct": 3.0, "direction": "increases_risk", "shap_value": 0.032, "impact_label": "Hydrological survey amendments"},
                    {"feature": "Other Factors", "contribution_pct": 2.0, "direction": "increases_risk", "shap_value": 0.021, "impact_label": "Utility shifting coordination"}
                ],
                "recommendations": [
                    {
                        "category": "Approvals",
                        "title": "Expedite State Coastal Zone Management Authority (CZMA) Clearance",
                        "desc": "Convene emergency appraisal meeting with State CZMA to review environmental mitigation measures for bridge approaches.",
                        "priority": "CRITICAL",
                        "delay_red": 50,
                        "savings_cr": 27.0,
                        "steps": ["Submit updated mangrove conservation plan", "Engage National Institute of Oceanography for technical endorsement", "Conduct joint site visit with District Collector"]
                    }
                ]
            },
            {
                "code": "PRJ-JK-2023-01",
                "name": "Udhampur-Srinagar-Baramulla Rail Link (USBRL Sector 4)",
                "district": "Reasi",
                "state": "Jammu & Kashmir",
                "type": "Railway Dedicated Freight",
                "notification_date": "2022-08-15",
                "expected_completion": "2026-10-30",
                "current_stage": "Section 30 (Physical Possession Taken)",
                "status": "Critical",
                "total_area_ha": 490.0,
                "acquired_area_ha": 284.2,
                "progress": 58.0,
                "total_parcels": 520,
                "affected_families": 410,
                "budget_cr": 2800.0,
                "daily_cost_lakhs": 9.2,
                "lat": 33.0811,
                "lng": 74.8322,
                "desc": "National strategic project connecting Kashmir valley with national railway grid traversing complex Himalayan geological strata and deep gorges.",
                "risk_score": 92.0,
                "risk_level": "HIGH",
                "predicted_delay": 254,
                "factors": [
                    {"name": "Compensation Delay", "pct": 28.0, "sev": "HIGH", "val": "92 days", "details": "Hill slope terrace land compensation revision petitions."},
                    {"name": "Legal Disputes", "pct": 26.0, "sev": "HIGH", "val": "22 cases", "details": "Community forest rights & shrine board access litigation."},
                    {"name": "Pending Approvals", "pct": 20.0, "sev": "HIGH", "val": "4 approvals", "details": "Geotechnical slope stability clearance and explosives permit."},
                    {"name": "R&R Progress", "pct": 10.0, "sev": "MEDIUM", "val": "52% done", "details": "Winterized transit shelters handover in progress."},
                    {"name": "Documentation Issues", "pct": 6.0, "sev": "MEDIUM", "val": "35 discrepancies", "details": "Mountainous terrain boundary mutations."},
                    {"name": "Land Owner Resistance", "pct": 5.0, "sev": "MEDIUM", "val": "Slope stability concerns", "details": "Villagers protesting blasting proximity."},
                    {"name": "Survey & Amendments", "pct": 3.0, "sev": "LOW", "val": "Tunnel portal shift", "details": "Re-alignment of portal 3 due to thrust fault."},
                    {"name": "Other Factors", "pct": 2.0, "sev": "LOW", "val": "Snow clearance", "details": "Seasonal weather downtime."}
                ],
                "shap_factors": [
                    {"feature": "Compensation Delay", "contribution_pct": 28.0, "direction": "increases_risk", "shap_value": 0.282, "impact_label": "Hill terraced parcel valuation claims"},
                    {"feature": "Legal Disputes", "contribution_pct": 26.0, "direction": "increases_risk", "shap_value": 0.261, "impact_label": "Community access right litigations"},
                    {"feature": "Pending Approvals", "contribution_pct": 20.0, "direction": "increases_risk", "shap_value": 0.203, "impact_label": "Explosive and forest slope clearance"},
                    {"feature": "R&R Progress", "contribution_pct": 10.0, "direction": "increases_risk", "shap_value": 0.102, "impact_label": "High-altitude winter shelter handover"},
                    {"feature": "Documentation Issues", "contribution_pct": 6.0, "direction": "increases_risk", "shap_value": 0.062, "impact_label": "Legacy mountain land survey records"},
                    {"feature": "Land Owner Resistance", "contribution_pct": 5.0, "direction": "increases_risk", "shap_value": 0.051, "impact_label": "Vibration and blasting safety demands"},
                    {"feature": "Survey & Amendments", "contribution_pct": 3.0, "direction": "increases_risk", "shap_value": 0.029, "impact_label": "Tunnel portal fault re-survey"},
                    {"feature": "Other Factors", "contribution_pct": 2.0, "direction": "increases_risk", "shap_value": 0.020, "impact_label": "Seasonal extreme climate constraints"}
                ],
                "recommendations": [
                    {
                        "category": "Legal",
                        "title": "Constitute Special High Court Land Acquisition Bench",
                        "desc": "Move Hon'ble High Court of J&K for expeditious day-to-day hearing of 22 tunnel alignment land petitions.",
                        "priority": "CRITICAL",
                        "delay_red": 60,
                        "savings_cr": 55.2,
                        "steps": ["File urgent mention memo before Chief Justice", "Submit government indemnity bond for interim possession", "Deposit contested compensation amount into court registry"]
                    }
                ]
            },
            {
                "code": "PRJ-KA-2024-09",
                "name": "Bengaluru Suburban Rail Corridor-2",
                "district": "Bengaluru Urban",
                "state": "Karnataka",
                "type": "Metro Rail Corridor",
                "notification_date": "2023-09-01",
                "expected_completion": "2027-03-31",
                "current_stage": "Section 11 (Preliminary Notification)",
                "status": "At Risk",
                "total_area_ha": 165.0,
                "acquired_area_ha": 46.2,
                "progress": 28.0,
                "total_parcels": 410,
                "affected_families": 350,
                "budget_cr": 1850.0,
                "daily_cost_lakhs": 8.1,
                "lat": 13.0827,
                "lng": 77.5877,
                "desc": "High-density urban transit corridor connecting Chikkabanavara and Baiyappanahalli, challenged by multi-storey commercial encroachments and high land acquisition prices.",
                "risk_score": 78.5,
                "risk_level": "HIGH",
                "predicted_delay": 165,
                "factors": [
                    {"name": "Compensation Delay", "pct": 33.0, "sev": "HIGH", "val": "High guidance value", "details": "Commercial property owners demanding 3x guidance value."},
                    {"name": "Legal Disputes", "pct": 21.0, "sev": "HIGH", "val": "16 urban civil suits", "details": "Title challenges regarding BBMP lake buffer zone parcels."},
                    {"name": "Pending Approvals", "pct": 17.0, "sev": "HIGH", "val": "Railway defense clearance", "details": "Ministry of Defence clearance for cantonment flyover cross."},
                    {"name": "R&R Progress", "pct": 12.0, "sev": "MEDIUM", "val": "25% R&R package", "details": "Slum rehabilitation housing allotments in Yelahanka."},
                    {"name": "Documentation Issues", "pct": 8.0, "sev": "MEDIUM", "val": "Khata bifurcations", "details": "Pending A-Khata vs B-Khata verification with BBMP."},
                    {"name": "Land Owner Resistance", "pct": 5.0, "sev": "LOW", "val": "Shopkeeper associations", "details": "Demand for alternate market complex spaces."},
                    {"name": "Survey & Amendments", "pct": 2.5, "sev": "LOW", "val": "Station footprint", "details": "Optimization of station entry/exit stairs."},
                    {"name": "Other Factors", "pct": 1.5, "sev": "LOW", "val": "Utility lines", "details": "BESCOM power cable and BWSSB water mains diversion."}
                ],
                "shap_factors": [
                    {"feature": "Compensation Delay", "contribution_pct": 33.0, "direction": "increases_risk", "shap_value": 0.334, "impact_label": "Urban commercial market value negotiation impasse"},
                    {"feature": "Legal Disputes", "contribution_pct": 21.0, "direction": "increases_risk", "shap_value": 0.215, "impact_label": "BBMP buffer zone encroachment litigations"},
                    {"feature": "Pending Approvals", "contribution_pct": 17.0, "direction": "increases_risk", "shap_value": 0.174, "impact_label": "Railway safety and defence land clearance"},
                    {"feature": "R&R Progress", "contribution_pct": 12.0, "direction": "increases_risk", "shap_value": 0.122, "impact_label": "Commercial tenant relocation scheme execution"},
                    {"feature": "Documentation Issues", "contribution_pct": 8.0, "direction": "increases_risk", "shap_value": 0.081, "impact_label": "A/B Khata municipal property title disputes"},
                    {"feature": "Land Owner Resistance", "contribution_pct": 5.0, "direction": "increases_risk", "shap_value": 0.052, "impact_label": "Retail business associations resistance"},
                    {"feature": "Survey & Amendments", "contribution_pct": 2.5, "direction": "increases_risk", "shap_value": 0.026, "impact_label": "Station entrance footprint revision"},
                    {"feature": "Other Factors", "contribution_pct": 1.5, "direction": "increases_risk", "shap_value": 0.016, "impact_label": "Underground utilities shifting backlog"}
                ],
                "recommendations": [
                    {
                        "category": "Compensation",
                        "title": "Offer TDR (Transferable Development Rights) Incentive Package",
                        "desc": "Implement BMRCL-style TDR plus cash combo compensation framework to break deadlock with commercial property owners along corridor.",
                        "priority": "HIGH",
                        "delay_red": 45,
                        "savings_cr": 36.4,
                        "steps": ["Draft TDR guideline notification in coordination with Urban Dev Dept", "Hold structured stakeholder conciliation meetings", "Open single-window TDR certificate issuance counter"]
                    }
                ]
            },
            {
                "code": "PRJ-AP-2024-14",
                "name": "Visakhapatnam Port Dedicated Connectivity Highway",
                "district": "Visakhapatnam",
                "state": "Andhra Pradesh",
                "type": "Port Connectivity Highway",
                "notification_date": "2023-05-20",
                "expected_completion": "2026-08-30",
                "current_stage": "Section 19 (Declaration of Acquisition)",
                "status": "At Risk",
                "total_area_ha": 175.0,
                "acquired_area_ha": 66.5,
                "progress": 38.0,
                "total_parcels": 290,
                "affected_families": 220,
                "budget_cr": 670.0,
                "daily_cost_lakhs": 3.8,
                "lat": 17.6868,
                "lng": 83.2185,
                "desc": "Heavy vehicle dedicated port corridor facing naval land clearance delays and municipal slum rehabilitation resistance.",
                "risk_score": 81.0,
                "risk_level": "HIGH",
                "predicted_delay": 182,
                "factors": [
                    {"name": "Compensation Delay", "pct": 30.0, "sev": "HIGH", "val": "65 days", "details": "Valuation of semi-permanent port handling godowns."},
                    {"name": "Legal Disputes", "pct": 23.0, "sev": "HIGH", "val": "11 cases", "details": "Port leasehold vs freehold title disputes."},
                    {"name": "Pending Approvals", "pct": 18.0, "sev": "HIGH", "val": "Eastern Naval Command", "details": "Security clearance for elevated flyover adjacent to naval docks."},
                    {"name": "R&R Progress", "pct": 12.0, "sev": "MEDIUM", "val": "35% complete", "details": "Relocation of 140 dock worker families."},
                    {"name": "Documentation Issues", "pct": 7.0, "sev": "MEDIUM", "val": "22 records", "details": "Port trust vs state revenue title records reconciliation."},
                    {"name": "Land Owner Resistance", "pct": 6.0, "sev": "MEDIUM", "val": "Dock transport unions", "details": "Concerns regarding access roads during civil works."},
                    {"name": "Survey & Amendments", "pct": 2.5, "sev": "LOW", "val": "Underground pipeline", "details": "Alignment adjustment around HPCL crude oil pipeline."},
                    {"name": "Other Factors", "pct": 1.5, "sev": "LOW", "val": "Traffic diversion", "details": "Night-time civil construction permission."}
                ],
                "shap_factors": [
                    {"feature": "Compensation Delay", "contribution_pct": 30.0, "direction": "increases_risk", "shap_value": 0.301, "impact_label": "Port warehouse commercial compensation backlog"},
                    {"feature": "Legal Disputes", "contribution_pct": 23.0, "direction": "increases_risk", "shap_value": 0.232, "impact_label": "Port trust leasehold litigation in High Court"},
                    {"feature": "Pending Approvals", "contribution_pct": 18.0, "direction": "increases_risk", "shap_value": 0.183, "impact_label": "Eastern Naval Command security clearance"},
                    {"feature": "R&R Progress", "contribution_pct": 12.0, "direction": "increases_risk", "shap_value": 0.121, "impact_label": "Dock worker housing allotment in Gajuwaka"},
                    {"feature": "Documentation Issues", "contribution_pct": 7.0, "direction": "increases_risk", "shap_value": 0.072, "impact_label": "Port boundary revenue record anomalies"},
                    {"feature": "Land Owner Resistance", "contribution_pct": 6.0, "direction": "increases_risk", "shap_value": 0.061, "impact_label": "Transport union operational access resistance"},
                    {"feature": "Survey & Amendments", "contribution_pct": 2.5, "direction": "increases_risk", "shap_value": 0.025, "impact_label": "HPCL crude pipeline setback revision"},
                    {"feature": "Other Factors", "contribution_pct": 1.5, "direction": "increases_risk", "shap_value": 0.015, "impact_label": "Night civil work traffic permissions"}
                ],
                "recommendations": [
                    {
                        "category": "Approvals",
                        "title": "Convene Bilateral Working Group with Eastern Naval Command",
                        "desc": "Joint committee with Ministry of Defence and NHAI to approve structural security wall design and grant flyover clearance.",
                        "priority": "HIGH",
                        "delay_red": 40,
                        "savings_cr": 15.2,
                        "steps": ["Submit blast-resistant parapet structural blueprint", "Sign MoU on perimeter surveillance CCTV sharing", "Obtain provisional NoC for foundation piling works"]
                    }
                ]
            },
            # MEDIUM RISK PROJECTS (Yellow/Amber)
            {
                "code": "PRJ-MH-2024-03",
                "name": "Mumbai-Pune Expressway Missing Link Project",
                "district": "Pune",
                "state": "Maharashtra",
                "type": "Highway Expansion",
                "notification_date": "2023-03-12",
                "expected_completion": "2026-06-30",
                "current_stage": "Section 23 (Award Enquiry & Valuation)",
                "status": "In Progress",
                "total_area_ha": 210.0,
                "acquired_area_ha": 143.8,
                "progress": 68.5,
                "total_parcels": 210,
                "affected_families": 145,
                "budget_cr": 980.0,
                "daily_cost_lakhs": 4.8,
                "lat": 18.7533,
                "lng": 73.4067,
                "desc": "Capacity augmentation bypassing Khandala ghat hairpin bends with high-speed viaducts and twin tunnels.",
                "risk_score": 58.0,
                "risk_level": "MEDIUM",
                "predicted_delay": 98,
                "factors": [
                    {"name": "Compensation Delay", "pct": 22.0, "sev": "MEDIUM", "val": "35 days", "details": "Forest fringe agricultural land title clearance."},
                    {"name": "Legal Disputes", "pct": 20.0, "sev": "MEDIUM", "val": "5 petitions", "details": "Lonavala eco-sensitive zone tribunal inquiries."},
                    {"name": "Pending Approvals", "pct": 19.0, "sev": "MEDIUM", "val": "Forest NOC", "details": "Stage-I forest compliance audit."},
                    {"name": "R&R Progress", "pct": 15.0, "sev": "MEDIUM", "val": "68% complete", "details": "Resettlement compensation 80% disbursed."},
                    {"name": "Documentation Issues", "pct": 10.0, "sev": "LOW", "val": "14 corrections", "details": "Talathi record minor errors."},
                    {"name": "Land Owner Resistance", "pct": 6.0, "sev": "LOW", "val": "Resolved", "details": "Ex-gratia rate settled with Khopoli panchayat."},
                    {"name": "Survey & Amendments", "pct": 5.0, "sev": "LOW", "val": "Slope survey", "details": "Viaduct pier geotechnical adjustments."},
                    {"name": "Other Factors", "pct": 3.0, "sev": "LOW", "val": "Rain downtime", "details": "Monsoon rain schedule buffer."}
                ],
                "shap_factors": [
                    {"feature": "Compensation Delay", "contribution_pct": 22.0, "direction": "increases_risk", "shap_value": 0.221, "impact_label": "Ghat margin plot compensation checks"},
                    {"feature": "Legal Disputes", "contribution_pct": 20.0, "direction": "increases_risk", "shap_value": 0.201, "impact_label": "NGT eco-sensitive zone buffer hearings"},
                    {"feature": "Pending Approvals", "contribution_pct": 19.0, "direction": "increases_risk", "shap_value": 0.192, "impact_label": "Forest advisory committee compliance"},
                    {"feature": "R&R Progress", "contribution_pct": 15.0, "direction": "decreases_risk", "shap_value": -0.150, "impact_label": "Steady resettlement execution rate"},
                    {"feature": "Documentation Issues", "contribution_pct": 10.0, "direction": "increases_risk", "shap_value": 0.101, "impact_label": "Talathi 7/12 extract rectifications"},
                    {"feature": "Land Owner Resistance", "contribution_pct": 6.0, "direction": "decreases_risk", "shap_value": -0.061, "impact_label": "Local consent achieved through gram sabha"},
                    {"feature": "Survey & Amendments", "contribution_pct": 5.0, "direction": "increases_risk", "shap_value": 0.051, "impact_label": "Tunnel portal safety setback verification"},
                    {"feature": "Other Factors", "contribution_pct": 3.0, "direction": "increases_risk", "shap_value": 0.031, "impact_label": "Monsoon landslide prevention works"}
                ],
                "recommendations": [
                    {
                        "category": "Approvals",
                        "title": "Complete NGT Eco-Sensitive Zone Compliance Submission",
                        "desc": "File compliance status with National Green Tribunal Western Zone Bench regarding tunnel muck disposal site safeguards.",
                        "priority": "MEDIUM",
                        "delay_red": 25,
                        "savings_cr": 12.0,
                        "steps": ["Install silt traps at identified muck dump yard", "Submit hydrogeological impact monitoring report", "Request disposal of environmental application"]
                    }
                ]
            },
            {
                "code": "PRJ-UP-2024-05",
                "name": "Ganga Expressway Phase-II Land Package 6",
                "district": "Prayagraj",
                "state": "Uttar Pradesh",
                "type": "Highway Expansion",
                "notification_date": "2023-06-01",
                "expected_completion": "2026-09-30",
                "current_stage": "Section 19 (Declaration of Acquisition)",
                "status": "In Progress",
                "total_area_ha": 320.0,
                "acquired_area_ha": 195.2,
                "progress": 61.0,
                "total_parcels": 320,
                "affected_families": 260,
                "budget_cr": 1350.0,
                "daily_cost_lakhs": 5.9,
                "lat": 25.4358,
                "lng": 81.8463,
                "desc": "High-speed greenfield expressway connecting Meerut to Prayagraj across fertile Gangetic alluvial belt.",
                "risk_score": 64.0,
                "risk_level": "MEDIUM",
                "predicted_delay": 112,
                "factors": [
                    {"name": "Compensation Delay", "pct": 25.0, "sev": "MEDIUM", "val": "42 days", "details": "Multi-heir agricultural land title mutations."},
                    {"name": "Legal Disputes", "pct": 21.0, "sev": "MEDIUM", "val": "8 civil suits", "details": "Family partition disputes among co-owners."},
                    {"name": "Pending Approvals", "pct": 18.0, "sev": "MEDIUM", "val": "Irrigation canal NOC", "details": "State Irrigation Dept approval for 3 canal syphons."},
                    {"name": "R&R Progress", "pct": 14.0, "sev": "MEDIUM", "val": "62% done", "details": "Rural artisan livelihood grant disbursement."},
                    {"name": "Documentation Issues", "pct": 9.0, "sev": "LOW", "val": "18 revenue records", "details": "Khasra number cross-referencing."},
                    {"name": "Land Owner Resistance", "pct": 6.0, "sev": "LOW", "val": "Minor", "details": "Demands for cattle underpasses."},
                    {"name": "Survey & Amendments", "pct": 4.0, "sev": "LOW", "val": "Underpass locations", "details": "Incorporation of two additional rural underpasses."},
                    {"name": "Other Factors", "pct": 3.0, "sev": "LOW", "val": "Admin buffer", "details": "Gram Panchayat meeting calendar sync."}
                ],
                "shap_factors": [
                    {"feature": "Compensation Delay", "contribution_pct": 25.0, "direction": "increases_risk", "shap_value": 0.251, "impact_label": "Multi-owner ancestral farmland inheritance checks"},
                    {"feature": "Legal Disputes", "contribution_pct": 21.0, "direction": "increases_risk", "shap_value": 0.210, "impact_label": "Civil court title partition dispute backlog"},
                    {"feature": "Pending Approvals", "contribution_pct": 18.0, "direction": "increases_risk", "shap_value": 0.182, "impact_label": "State irrigation department canal crossing NoC"},
                    {"feature": "R&R Progress", "contribution_pct": 14.0, "direction": "decreases_risk", "shap_value": -0.141, "impact_label": "Steady artisan and tenant rehabilitation payments"},
                    {"feature": "Documentation Issues", "contribution_pct": 9.0, "direction": "increases_risk", "shap_value": 0.092, "impact_label": "Khasra-Khatauni digitisation reconciliation"},
                    {"feature": "Land Owner Resistance", "contribution_pct": 6.0, "direction": "decreases_risk", "shap_value": -0.060, "impact_label": "Consensus on cattle crossing locations"},
                    {"feature": "Survey & Amendments", "contribution_pct": 4.0, "direction": "increases_risk", "shap_value": 0.041, "impact_label": "Underpass alignment amendment notice"},
                    {"feature": "Other Factors", "contribution_pct": 3.0, "direction": "increases_risk", "shap_value": 0.031, "impact_label": "Tehsil land revenue administrative roster"}
                ],
                "recommendations": [
                    {
                        "category": "Documentation",
                        "title": "Deploy Revenue Mutation Camp in Soraon Tehsil",
                        "desc": "Organize 3-day special revenue camp with Lekhpals to clear pending family partition mutations on spot.",
                        "priority": "MEDIUM",
                        "delay_red": 28,
                        "savings_cr": 16.5,
                        "steps": ["Issue public notice across participating village gram sabhas", "Authorize Sub-Divisional Magistrate to execute summary attestations", "Update digital Bhulekh database in real time"]
                    }
                ]
            },
            {
                "code": "PRJ-TN-2024-11",
                "name": "Chennai-Bengaluru Industrial Corridor Node A",
                "district": "Tiruvallur",
                "state": "Tamil Nadu",
                "type": "Industrial Park",
                "notification_date": "2023-07-15",
                "expected_completion": "2026-12-15",
                "current_stage": "Section 23 (Award Enquiry & Valuation)",
                "status": "In Progress",
                "total_area_ha": 260.0,
                "acquired_area_ha": 187.2,
                "progress": 72.0,
                "total_parcels": 260,
                "affected_families": 175,
                "budget_cr": 890.0,
                "daily_cost_lakhs": 4.1,
                "lat": 13.3328,
                "lng": 80.1983,
                "desc": "Manufacturing mega-cluster and multi-modal logistics hub near Ponneri port node.",
                "risk_score": 52.0,
                "risk_level": "MEDIUM",
                "predicted_delay": 88,
                "factors": [
                    {"name": "Compensation Delay", "pct": 24.0, "sev": "MEDIUM", "val": "28 days", "details": "Commercial guideline rate verification."},
                    {"name": "Legal Disputes", "pct": 21.0, "sev": "MEDIUM", "val": "6 cases", "details": "Salt pan leased land ownership claims."},
                    {"name": "Pending Approvals", "pct": 19.0, "sev": "MEDIUM", "val": "Salt Commissioner NOC", "details": "Central Salt Commissioner land surrender protocol."},
                    {"name": "R&R Progress", "pct": 14.0, "sev": "MEDIUM", "val": "74% complete", "details": "Housing vouchers issued to eligible families."},
                    {"name": "Documentation Issues", "pct": 9.0, "sev": "LOW", "val": "11 mutations", "details": "Patta transfer streamlining in progress."},
                    {"name": "Land Owner Resistance", "pct": 6.0, "sev": "LOW", "val": "Minimal", "details": "Employment commitment agreement reached."},
                    {"name": "Survey & Amendments", "pct": 4.0, "sev": "LOW", "val": "Storm drain line", "details": "Drainage canal setback adjustment."},
                    {"name": "Other Factors", "pct": 3.0, "sev": "LOW", "val": "TNEB shifting", "details": "High tension tower relocation."}
                ],
                "shap_factors": [
                    {"feature": "Compensation Delay", "contribution_pct": 24.0, "direction": "increases_risk", "shap_value": 0.241, "impact_label": "Salt pan commercial valuation verification"},
                    {"feature": "Legal Disputes", "contribution_pct": 21.0, "direction": "increases_risk", "shap_value": 0.211, "impact_label": "Leaseholder compensation litigation in Madras HC"},
                    {"feature": "Pending Approvals", "contribution_pct": 19.0, "direction": "increases_risk", "shap_value": 0.191, "impact_label": "Central Salt Commissionerate relinquishment NoC"},
                    {"feature": "R&R Progress", "contribution_pct": 14.0, "direction": "decreases_risk", "shap_value": -0.141, "impact_label": "High compliance in industrial training quota"},
                    {"feature": "Documentation Issues", "contribution_pct": 9.0, "direction": "increases_risk", "shap_value": 0.091, "impact_label": "Patta conversion and digital FMB updates"},
                    {"feature": "Land Owner Resistance", "contribution_pct": 6.0, "direction": "decreases_risk", "shap_value": -0.061, "impact_label": "MoU with local panchayat on youth employment"},
                    {"feature": "Survey & Amendments", "contribution_pct": 4.0, "direction": "increases_risk", "shap_value": 0.041, "impact_label": "Industrial feeder road width re-alignment"},
                    {"feature": "Other Factors", "contribution_pct": 3.0, "direction": "increases_risk", "shap_value": 0.031, "impact_label": "Power grid line rerouting permissions"}
                ],
                "recommendations": [
                    {
                        "category": "Approvals",
                        "title": "Expedite Salt Commissionerate Land Relinquishment",
                        "desc": "Execute tripartite deed with Ministry of Commerce & Industry and SIPCOT for transfer of 42 hectares of salt manufacturing leasehold land.",
                        "priority": "MEDIUM",
                        "delay_red": 30,
                        "savings_cr": 12.3,
                        "steps": ["Reconcile annual ground rent dues with Central Salt Dept", "Execute standard surrender agreement", "Issue Section 30 possession order"]
                    }
                ]
            },
            {
                "code": "PRJ-MH-2024-15",
                "name": "Pune Ring Road (Eastern Alignment Package 4)",
                "district": "Pune",
                "state": "Maharashtra",
                "type": "Highway Expansion",
                "notification_date": "2023-10-05",
                "expected_completion": "2027-01-30",
                "current_stage": "Section 11 (Preliminary Notification)",
                "status": "In Progress",
                "total_area_ha": 310.0,
                "acquired_area_ha": 148.8,
                "progress": 48.0,
                "total_parcels": 310,
                "affected_families": 230,
                "budget_cr": 1200.0,
                "daily_cost_lakhs": 5.2,
                "lat": 18.5204,
                "lng": 73.8567,
                "desc": "Strategic outer bypass highway to decongest Pune metropolitan freight traffic.",
                "risk_score": 62.0,
                "risk_level": "MEDIUM",
                "predicted_delay": 105,
                "factors": [
                    {"name": "Compensation Delay", "pct": 26.0, "sev": "MEDIUM", "val": "38 days", "details": "Peri-urban plot boundary determinations."},
                    {"name": "Legal Disputes", "pct": 22.0, "sev": "MEDIUM", "val": "7 cases", "details": "Agricultural to non-agricultural status claims."},
                    {"name": "Pending Approvals", "pct": 18.0, "sev": "MEDIUM", "val": "MSRDC clearance", "details": "Interchange geometry approval."},
                    {"name": "R&R Progress", "pct": 13.0, "sev": "MEDIUM", "val": "55% done", "details": "Rehabilitation township identification in Haveli."},
                    {"name": "Documentation Issues", "pct": 9.0, "sev": "LOW", "val": "16 issues", "details": "Gunthewari regularisation verifications."},
                    {"name": "Land Owner Resistance", "pct": 6.0, "sev": "LOW", "val": "Controlled", "details": "Panchayat consultation completed."},
                    {"name": "Survey & Amendments", "pct": 4.0, "sev": "LOW", "val": "Interchange arm", "details": "Toll plaza arm setback revision."},
                    {"name": "Other Factors", "pct": 2.0, "sev": "LOW", "val": "Routine", "details": "Local traffic management."}
                ],
                "shap_factors": [
                    {"feature": "Compensation Delay", "contribution_pct": 26.0, "direction": "increases_risk", "shap_value": 0.261, "impact_label": "Peri-urban land valuation disparity"},
                    {"feature": "Legal Disputes", "contribution_pct": 22.0, "direction": "increases_risk", "shap_value": 0.222, "impact_label": "Non-agricultural status validation petitions"},
                    {"feature": "Pending Approvals", "contribution_pct": 18.0, "direction": "increases_risk", "shap_value": 0.182, "impact_label": "MSRDC interchange structural approval"},
                    {"feature": "R&R Progress", "contribution_pct": 13.0, "direction": "decreases_risk", "shap_value": -0.131, "impact_label": "Haveli tehsil rehabilitation site demarcated"},
                    {"feature": "Documentation Issues", "contribution_pct": 9.0, "direction": "increases_risk", "shap_value": 0.091, "impact_label": "Gunthewari layout regularisation checks"},
                    {"feature": "Land Owner Resistance", "contribution_pct": 6.0, "direction": "decreases_risk", "shap_value": -0.061, "impact_label": "Village sarpanch consent consensus established"},
                    {"feature": "Survey & Amendments", "contribution_pct": 4.0, "direction": "increases_risk", "shap_value": 0.041, "impact_label": "Service lane geometry amendment"},
                    {"feature": "Other Factors", "contribution_pct": 2.0, "direction": "increases_risk", "shap_value": 0.021, "impact_label": "Local ring road connectivity links"}
                ],
                "recommendations": [
                    {
                        "category": "Compensation",
                        "title": "Streamline Gunthewari Property Valuation Protocol",
                        "desc": "Apply Maharashtra Government GR on standard compensation multipliers for peri-urban Gunthewari plots.",
                        "priority": "MEDIUM",
                        "delay_red": 32,
                        "savings_cr": 16.6,
                        "steps": ["Notify town planning officer valuation benchmarks", "Hold Lok Samvad camp with Haveli land holders", "Disburse 50% advance compensation upon title verification"]
                    }
                ]
            },
            # LOW RISK PROJECTS (Green)
            {
                "code": "PRJ-RJ-2024-02",
                "name": "Bhadla Mega Solar Park Phase-IV Transmission Corridor",
                "district": "Jodhpur",
                "state": "Rajasthan",
                "type": "Solar Energy Park",
                "notification_date": "2023-11-10",
                "expected_completion": "2025-10-31",
                "current_stage": "Section 30 (Physical Possession Taken)",
                "status": "On Schedule",
                "total_area_ha": 140.0,
                "acquired_area_ha": 127.4,
                "progress": 91.0,
                "total_parcels": 140,
                "affected_families": 65,
                "budget_cr": 420.0,
                "daily_cost_lakhs": 2.2,
                "lat": 27.5385,
                "lng": 71.9168,
                "desc": "Clean green energy evacuation transmission corridor in Thar desert region with minimal settlements and fast-track government wasteland allotment.",
                "risk_score": 24.0,
                "risk_level": "LOW",
                "predicted_delay": 32,
                "factors": [
                    {"name": "Compensation Delay", "pct": 18.0, "sev": "LOW", "val": "12 days", "details": "Government revenue wasteland lease payment on schedule."},
                    {"name": "Legal Disputes", "pct": 16.0, "sev": "LOW", "val": "1 case", "details": "Boundary delineation with neighboring pastoral grazing land."},
                    {"name": "Pending Approvals", "pct": 15.0, "sev": "LOW", "val": "Completed", "details": "PowerGrid RoW approvals in hand."},
                    {"name": "R&R Progress", "pct": 14.0, "sev": "LOW", "val": "94% done", "details": "Fencing and water point compensation disbursed."},
                    {"name": "Documentation Issues", "pct": 14.0, "sev": "LOW", "val": "Resolved", "details": "All revenue records digitized under Apna Khata portal."},
                    {"name": "Land Owner Resistance", "pct": 10.0, "sev": "LOW", "val": "Nil", "details": "High local support for clean solar infrastructure."},
                    {"name": "Survey & Amendments", "pct": 8.0, "sev": "LOW", "val": "Tower footings", "details": "Micro-siting of 12 transmission towers complete."},
                    {"name": "Other Factors", "pct": 5.0, "sev": "LOW", "val": "Desert terrain", "details": "Sand dune stabilization works."}
                ],
                "shap_factors": [
                    {"feature": "Compensation Delay", "contribution_pct": 18.0, "direction": "decreases_risk", "shap_value": -0.180, "impact_label": "Immediate government wasteland lease execution"},
                    {"feature": "Legal Disputes", "contribution_pct": 16.0, "direction": "decreases_risk", "shap_value": -0.160, "impact_label": "Negligible litigation across arid desert tracts"},
                    {"feature": "Pending Approvals", "contribution_pct": 15.0, "direction": "decreases_risk", "shap_value": -0.150, "impact_label": "Transmission corridor clearances granted ahead of schedule"},
                    {"feature": "R&R Progress", "contribution_pct": 14.0, "direction": "decreases_risk", "shap_value": -0.140, "impact_label": "Zero residential displacements required"},
                    {"feature": "Documentation Issues", "contribution_pct": 14.0, "direction": "decreases_risk", "shap_value": -0.140, "impact_label": "100% digital land registry verification"},
                    {"feature": "Land Owner Resistance", "contribution_pct": 10.0, "direction": "decreases_risk", "shap_value": -0.100, "impact_label": "Active community engagement & CSR commitments"},
                    {"feature": "Survey & Amendments", "contribution_pct": 8.0, "direction": "decreases_risk", "shap_value": -0.080, "impact_label": "Transmission pylon GPS coordinates locked"},
                    {"feature": "Other Factors", "contribution_pct": 5.0, "direction": "decreases_risk", "shap_value": -0.050, "impact_label": "Favorable environmental conditions"}
                ],
                "recommendations": [
                    {
                        "category": "Documentation",
                        "title": "Complete Final Section 30 Gazette Award Publication",
                        "desc": "Publish statutory completion certificate in Rajasthan State Gazette to formally close acquisition proceeding.",
                        "priority": "LOW",
                        "delay_red": 10,
                        "savings_cr": 2.2,
                        "steps": ["Verify final handover receipt from PowerGrid Corporation", "Issue formal closure notice to District Revenue Officer", "Archive digital survey records in state GIS database"]
                    }
                ]
            },
            {
                "code": "PRJ-GJ-2024-07",
                "name": "Dholera SIR Dedicated Expressway Corridor",
                "district": "Ahmedabad",
                "state": "Gujarat",
                "type": "Industrial Park",
                "notification_date": "2023-08-20",
                "expected_completion": "2026-04-15",
                "current_stage": "Section 30 (Physical Possession Taken)",
                "status": "On Schedule",
                "total_area_ha": 180.0,
                "acquired_area_ha": 158.4,
                "progress": 88.0,
                "total_parcels": 180,
                "affected_families": 95,
                "budget_cr": 750.0,
                "daily_cost_lakhs": 3.5,
                "lat": 22.2475,
                "lng": 72.1932,
                "desc": "High-capacity multi-modal transport corridor linking Ahmedabad with Dholera Special Investment Region.",
                "risk_score": 28.5,
                "risk_level": "LOW",
                "predicted_delay": 38,
                "factors": [
                    {"name": "Compensation Delay", "pct": 19.0, "sev": "LOW", "val": "15 days", "details": "Town planning scheme (TPS) land pooling model executed."},
                    {"name": "Legal Disputes", "pct": 17.0, "sev": "LOW", "val": "2 cases", "details": "Minor boundary demarcations in salt flat margins."},
                    {"name": "Pending Approvals", "pct": 16.0, "sev": "LOW", "val": "All clear", "details": "State highway clearance and railway overbridge approvals in place."},
                    {"name": "R&R Progress", "pct": 14.0, "sev": "LOW", "val": "91% done", "details": "Re-constituted final plots handed over to farmers."},
                    {"name": "Documentation Issues", "pct": 13.0, "sev": "LOW", "val": "Minimal", "details": "AnyROR Gujarat digital title verification completed."},
                    {"name": "Land Owner Resistance", "pct": 9.0, "sev": "LOW", "val": "High support", "details": "Farmers benefited from developed commercial plot return."},
                    {"name": "Survey & Amendments", "pct": 7.0, "sev": "LOW", "val": "Completed", "details": "Final demarcation stone pillars fixed."},
                    {"name": "Other Factors", "pct": 5.0, "sev": "LOW", "val": "Routine", "details": "Standard construction handover."}
                ],
                "shap_factors": [
                    {"feature": "Compensation Delay", "contribution_pct": 19.0, "direction": "decreases_risk", "shap_value": -0.191, "impact_label": "Gujarat town planning land pooling success"},
                    {"feature": "Legal Disputes", "contribution_pct": 17.0, "direction": "decreases_risk", "shap_value": -0.171, "impact_label": "Consensual plot reconstitution avoided court stays"},
                    {"feature": "Pending Approvals", "contribution_pct": 16.0, "direction": "decreases_risk", "shap_value": -0.161, "impact_label": "High-level single window state clearance approval"},
                    {"feature": "R&R Progress", "contribution_pct": 14.0, "direction": "decreases_risk", "shap_value": -0.141, "impact_label": "Developed plot return model accepted by land owners"},
                    {"feature": "Documentation Issues", "contribution_pct": 13.0, "direction": "decreases_risk", "shap_value": -0.131, "impact_label": "Seamless AnyROR digital mutation record updates"},
                    {"feature": "Land Owner Resistance", "contribution_pct": 9.0, "direction": "decreases_risk", "shap_value": -0.091, "impact_label": "High farmer cooperation through land appreciation"},
                    {"feature": "Survey & Amendments", "contribution_pct": 7.0, "direction": "decreases_risk", "shap_value": -0.071, "impact_label": "DGPS survey boundaries finalized without objection"},
                    {"feature": "Other Factors", "contribution_pct": 5.0, "direction": "decreases_risk", "shap_value": -0.051, "impact_label": "Adequate contractor mobilisation and site access"}
                ],
                "recommendations": [
                    {
                        "category": "Approvals",
                        "title": "Complete Right of Way Handover for Package 2 Interchange",
                        "desc": "Sign final joint possession memo between Dholera SIR Development Authority and NHAI contractors.",
                        "priority": "LOW",
                        "delay_red": 12,
                        "savings_cr": 4.2,
                        "steps": ["Verify physical fence removal on residual parcel 84", "Sign formal site possession protocol", "Commence sub-grade earthworks"]
                    }
                ]
            },
            {
                "code": "PRJ-DL-2024-04",
                "name": "Delhi-Varanasi High Speed Rail Sector 1 (Noida Link)",
                "district": "Gautam Buddha Nagar",
                "state": "Uttar Pradesh",
                "type": "Railway Dedicated Freight",
                "notification_date": "2023-12-01",
                "expected_completion": "2026-02-28",
                "current_stage": "Section 30 (Physical Possession Taken)",
                "status": "On Schedule",
                "total_area_ha": 120.0,
                "acquired_area_ha": 112.8,
                "progress": 94.0,
                "total_parcels": 120,
                "affected_families": 50,
                "budget_cr": 1600.0,
                "daily_cost_lakhs": 7.5,
                "lat": 28.5355,
                "lng": 77.3910,
                "desc": "High-speed rail right-of-way corridor parallel to Yamuna Expressway connecting Jewar International Airport terminal.",
                "risk_score": 22.0,
                "risk_level": "LOW",
                "predicted_delay": 26,
                "factors": [
                    {"name": "Compensation Delay", "pct": 18.0, "sev": "LOW", "val": "10 days", "details": "Direct DBT disbursement completed by YEIDA."},
                    {"name": "Legal Disputes", "pct": 17.0, "sev": "LOW", "val": "0 cases", "details": "No pending stays or injunctions."},
                    {"name": "Pending Approvals", "pct": 16.0, "sev": "LOW", "val": "All clear", "details": "Airport authority and railway board green clearances."},
                    {"name": "R&R Progress", "pct": 15.0, "sev": "LOW", "val": "96% done", "details": "All eligible beneficiaries settled in Model Village Jewar."},
                    {"name": "Documentation Issues", "pct": 13.0, "sev": "LOW", "val": "Resolved", "details": "Zero pending mutation claims."},
                    {"name": "Land Owner Resistance", "pct": 9.0, "sev": "LOW", "val": "Nil", "details": "Full stakeholder consensus."},
                    {"name": "Survey & Amendments", "pct": 7.0, "sev": "LOW", "val": "Locked", "details": "Elevated track centerline benchmarked."},
                    {"name": "Other Factors", "pct": 5.0, "sev": "LOW", "val": "On schedule", "details": "Piling rigs already mobilized."}
                ],
                "shap_factors": [
                    {"feature": "Compensation Delay", "contribution_pct": 18.0, "direction": "decreases_risk", "shap_value": -0.180, "impact_label": "Direct DBT release with YEIDA institutional support"},
                    {"feature": "Legal Disputes", "contribution_pct": 17.0, "direction": "decreases_risk", "shap_value": -0.170, "impact_label": "Zero active litigations along express right-of-way"},
                    {"feature": "Pending Approvals", "contribution_pct": 16.0, "direction": "decreases_risk", "shap_value": -0.160, "impact_label": "Integrated airport corridor master plan clearances"},
                    {"feature": "R&R Progress", "contribution_pct": 15.0, "direction": "decreases_risk", "shap_value": -0.150, "impact_label": "Exemplary model resettlement colony handover complete"},
                    {"feature": "Documentation Issues", "contribution_pct": 13.0, "direction": "decreases_risk", "shap_value": -0.130, "impact_label": "Complete digital revenue map reconciliation"},
                    {"feature": "Land Owner Resistance", "contribution_pct": 9.0, "direction": "decreases_risk", "shap_value": -0.090, "impact_label": "Proactive land purchase agreement at mutual terms"},
                    {"feature": "Survey & Amendments", "contribution_pct": 7.0, "direction": "decreases_risk", "shap_value": -0.070, "impact_label": "High-precision LiDAR railway alignment finalized"},
                    {"feature": "Other Factors", "contribution_pct": 5.0, "direction": "decreases_risk", "shap_value": -0.050, "impact_label": "Optimal institutional inter-agency governance"}
                ],
                "recommendations": [
                    {
                        "category": "Documentation",
                        "title": "Finalize Right of Way Title Transfer to NHSRCL",
                        "desc": "Execute lease deed transfer from YEIDA to National High Speed Rail Corporation Limited.",
                        "priority": "LOW",
                        "delay_red": 8,
                        "savings_cr": 6.0,
                        "steps": ["Issue formal mutation in favor of NHSRCL", "Record RoW benchmark coordinates", "Archive documentation on PM GatiShakti portal"]
                    }
                ]
            }
        ]

        # Insert Projects, Risk, SHAP, and Recommendations
        for pdata in projects_data:
            proj = Project(
                project_code=pdata["code"],
                name=pdata["name"],
                district=pdata["district"],
                state=pdata["state"],
                project_type=pdata["type"],
                notification_date=pdata["notification_date"],
                expected_completion=pdata["expected_completion"],
                current_stage=pdata["current_stage"],
                status=pdata["status"],
                total_area_ha=pdata["total_area_ha"],
                acquired_area_ha=pdata["acquired_area_ha"],
                acquisition_progress=pdata["progress"],
                total_parcels=pdata["total_parcels"],
                affected_families=pdata["affected_families"],
                base_budget_cr=pdata["budget_cr"],
                daily_delay_cost_lakhs=pdata["daily_cost_lakhs"],
                latitude=pdata["lat"],
                longitude=pdata["lng"],
                description=pdata["desc"]
            )
            db.add(proj)
            db.flush() # Populate proj.id

            # Risk Prediction
            rp = RiskPrediction(
                project_id=proj.id,
                risk_score=pdata["risk_score"],
                risk_level=pdata["risk_level"],
                predicted_delay_days=pdata["predicted_delay"],
                delay_confidence_interval="±14 days",
                confidence_score=0.94,
                model_name="CatBoost Delay Classifier & Regressor v2.1"
            )
            db.add(rp)

            # Risk Factors
            for f in pdata["factors"]:
                rf = RiskFactor(
                    project_id=proj.id,
                    factor_name=f["name"],
                    contribution_pct=f["pct"],
                    severity=f["sev"],
                    metric_value=f["val"],
                    details=f["details"]
                )
                db.add(rf)

            # SHAP Explanation
            top_factors = pdata["shap_factors"]
            summary_text = (
                f"SHAP local attribution reveals {top_factors[0]['feature']} ({top_factors[0]['contribution_pct']}%) "
                f"and {top_factors[1]['feature']} ({top_factors[1]['contribution_pct']}%) as the dominant bottleneck drivers. "
                f"Targeted administrative intervention on these factors can significantly mitigate delay risk."
            )
            se = ShapExplanation(
                project_id=proj.id,
                base_value=28.5,
                output_value=pdata["risk_score"],
                model_used="CatBoost Regressor + TreeSHAP v0.45",
                confidence_score=0.94,
                explanation_summary=summary_text,
                features_json=json.dumps(pdata["shap_factors"])
            )
            db.add(se)

            # Recommendations
            for r in pdata["recommendations"]:
                rec = Recommendation(
                    project_id=proj.id,
                    category=r["category"],
                    title=r["title"],
                    description=r["desc"],
                    priority=r["priority"],
                    potential_delay_reduction_days=r["delay_red"],
                    potential_cost_savings_cr=r["savings_cr"],
                    action_steps_json=json.dumps(r["steps"]),
                    status="PENDING"
                )
                db.add(rec)

        db.commit()

        # Seed Alerts (Triggering high risk events for sound notification verification)
        print("Seeding Alerts and Sound Notification Events...")
        now = datetime.now(timezone.utc)
        alerts_data = [
            {
                "alert_id": "ALT-2026-001",
                "project_code": "PRJ-OD-2024-08",
                "project_name": "Khurda Road-Bolangir Rail Line",
                "district": "Balangir",
                "severity": "HIGH",
                "reason": "Compensation disbursement delayed by 85 days; multiple land title writs pending in High Court.",
                "recommended_action": "Establish Fast-Track Special Treasury Disbursement Counter & convene DLSA Lok Adalat.",
                "acknowledged": False,
                "sound_played": False, # Will trigger sound notification on first frontend load!
                "time_offset_min": 10
            },
            {
                "alert_id": "ALT-2026-002",
                "project_code": "PRJ-AP-2024-12",
                "project_name": "Kotipalli-Narasapur Rail Line Corridor",
                "district": "East Godavari",
                "severity": "HIGH",
                "reason": "CRZ clearance pending past statutory deadline (180 days); aquaculture pond valuation dispute.",
                "recommended_action": "Escalate to State Coastal Zone Management Authority & convene District Magistrate conciliation.",
                "acknowledged": False,
                "sound_played": False,
                "time_offset_min": 25
            },
            {
                "alert_id": "ALT-2026-003",
                "project_code": "PRJ-JK-2023-01",
                "project_name": "USBRL Sector 4 (Udhampur-Srinagar-Baramulla)",
                "district": "Reasi",
                "severity": "HIGH",
                "reason": "Tunnel portal 3 realignment pending geological stability audit; community compensation dispute.",
                "recommended_action": "Constitute Special High Court Land Acquisition Bench for daily hearings.",
                "acknowledged": True, # Acknowledged alert - does NOT trigger sound!
                "acknowledged_by": "Rajesh Kumar, IAS",
                "acknowledged_at": now - timedelta(hours=2),
                "sound_played": True,
                "time_offset_min": 120
            },
            {
                "alert_id": "ALT-2026-004",
                "project_code": "PRJ-KA-2024-09",
                "project_name": "Bengaluru Suburban Rail Corridor-2",
                "district": "Bengaluru Urban",
                "severity": "HIGH",
                "reason": "Commercial property owners demanding 3x guidance value; BBMP buffer zone litigation.",
                "recommended_action": "Offer Transferable Development Rights (TDR) incentive package.",
                "acknowledged": False,
                "sound_played": False,
                "time_offset_min": 40
            },
            {
                "alert_id": "ALT-2026-005",
                "project_code": "PRJ-MH-2024-03",
                "project_name": "Mumbai-Pune Expressway Missing Link",
                "district": "Pune",
                "severity": "MEDIUM",
                "reason": "Eco-sensitive zone tribunal hearing scheduled regarding tunnel muck disposal site.",
                "recommended_action": "Submit updated hydrogeological impact monitoring report to NGT Pune.",
                "acknowledged": False,
                "sound_played": True,
                "time_offset_min": 180
            }
        ]

        for a in alerts_data:
            # find project id
            proj = db.query(Project).filter(Project.project_code == a["project_code"]).first()
            if proj:
                alert = Alert(
                    alert_id=a["alert_id"],
                    project_id=proj.id,
                    project_name=a["project_name"],
                    district=a["district"],
                    severity=a["severity"],
                    reason=a["reason"],
                    recommended_action=a["recommended_action"],
                    acknowledged=a["acknowledged"],
                    acknowledged_by=a.get("acknowledged_by"),
                    acknowledged_at=a.get("acknowledged_at"),
                    sound_played=a["sound_played"],
                    created_at=now - timedelta(minutes=a["time_offset_min"])
                )
                db.add(alert)

        db.commit()
        print("Database successfully seeded with realistic Indian land acquisition data!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
