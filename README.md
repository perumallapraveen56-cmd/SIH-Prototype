# Predictive Analytics System for Early Detection of Land Acquisition Delays

**Smart India Hackathon (SIH 2026)**  
**Problem Statement ID**: `SIH26017`  
**Team**: `NEXORA_TAU`  
**Prototype Reference**: *"SIH SOLUTION WORKFLOW – LAND ACQUISITION DELAY PREDICTION SYSTEM"*

---

## 🏛️ Executive Summary

Linear and mega infrastructure projects across India—spanning National Expressways (NHAI), High-Speed Rail corridors (NHSRCL), Metro rail networks, and Dedicated Freight Corridors (DFCCIL)—frequently experience catastrophic schedule overruns caused by bottlenecks in land acquisition under the **RFCTLARR Act, 2013**.

This enterprise prototype delivers an **AI-powered Early Warning & Explainability System** that predicts acquisition delays months before critical milestones lapse, quantifies project-specific daily financial cost exposure, generates real-time **TreeSHAP** attribution waterfalls across **8 canonical statutory factors**, simulates **What-If intervention scenarios**, and produces statutory PDF audit dossiers.

```
       ┌────────────────────────────────────────────────────────┐
       │             SIH26017 - NEXORA_TAU ARCHITECTURE         │
       └────────────────────────────────────────────────────────┘
                                    │
          ┌─────────────────────────┴─────────────────────────┐
          ▼                                                   ▼
┌───────────────────────────┐                       ┌───────────────────────────┐
│     ANGULAR 21 FRONTEND   │                       │      FASTAPI BACKEND      │
│  - Standalone Signals UI  │                       │  - Python 3.13 Async REST │
│  - Leaflet GIS Risk Map   │ ◄─── REST (Port 8000) ──►  - CatBoost GBDT Dual-Head│
│  - TreeSHAP Waterfall     │                       │  - TreeSHAP Explainer     │
│  - What-If Simulator      │                       │  - ReportLab PDF Engine   │
│  - Web Audio Safety Chime │                       │  - SQLite / Postgres DB   │
└───────────────────────────┘                       └───────────────────────────┘
```

---

## 🚀 Key Innovations & Statutory Compliance

1. **Dual-Head Gradient Boosted Tree Architecture**:
   - **CatBoost Classifier**: Detects delay escalation with measured **92.16% F1-Score** (92.20% accuracy, 0.9862 ROC-AUC).
   - **CatBoost Regressor**: Forecasts exact delay duration with measured **95.54% R²** (MAE = 6.92 days, RMSE = 8.54 days).
2. **8 Canonical RFCTLARR Statutory Factors**:
   - Land Dispute Litigation Index
   - Section 19 Declaration Velocity
   - Compensation Rate Disparity Ratio
   - Cadastral Discrepancy & Mutation Lag
   - Forest / Environmental Stage-II Clearances
   - R&R Entitlement Package Acceptance
   - Gram Sabha / Tribal Consent Resolution
   - Utility Shifting & Right-of-Way Obstruction
3. **Strict Ministry Governance Alignment**:
   - Project Risk Overview chart strictly adheres to the three-tier classification standard: **High Risk (Red)**, **Medium Risk (Yellow/Amber)**, and **Low Risk (Green)**. **NO Critical Risk category** is displayed in the risk overview.
4. **Single Source of Truth**:
   - Zero hardcoded numbers in Angular templates. All KPI counts, project lists, risk charts, and SHAP waterfalls are fetched dynamically from the database.
5. **Web Audio API Safety Chime**:
   - Overcomes browser autoplay blocks by synthesizing a clean dual-tone alert chime ($880\text{ Hz} \to 659.25\text{ Hz}$) via the Web Audio API. Fired **once only** per new unacknowledged high-risk alert. Never loops or repeats.

---

## 📋 Standard Judge & Evaluation Workflow

Follow this sequence to inspect all prototype capabilities matching the reference specification:

1. **Login (`/login`)**:
   - Access via the built-in one-click role selector buttons on the login screen:
     - **Revenue Officer** (Operational field monitoring & SLAO intervention)
     - **Data Analyst** (TreeSHAP explainability & What-If scenario simulations)
     - **Super Admin** (Full administrative oversight & portfolio control)
   - Single Sign-On (SSO) integration options for Jan Parichay and DigiLocker.
2. **Dashboard (`/dashboard`)**:
   - Real-time statutory KPI cards (Total Projects, Cadastral Parcels, High/Medium/Low counts).
   - Project Risk Overview Chart (Red, Yellow, Green distribution).
   - Recent Projects Table with live risk badges.
3. **GIS Risk Map (`/gis-map`)**:
   - Leaflet map displaying pan-India project coordinates.
   - Filter by State, District, Project Type, and Risk Level.
   - Click pins to view delay duration, cost impact, and inspect details.
4. **Project Risk Details (`/projects/:id`)**:
   - Metadata dossier, acquisition progress track, daily cost burn rate.
   - Primary action button **"AI Simulate"** triggers the What-If intervention optimizer.
5. **What-If Simulator & Intervention Optimizer (`/what-if?projectId=:id`)**:
   - Adjust dispute settlement, surveyor staffing, and fast-track approval sliders.
   - Backend dynamically recalculates post-intervention delay days and financial savings in ₹ Crores.
   - Dedicated navigation link to **"SHAP Explainability"**.
6. **AI Explainability (`/shap?projectId=:id`)**:
   - Interactive TreeSHAP horizontal waterfall visualization.
   - Quantifies how statutory factors contribute to the predicted delay baseline.
   - Dedicated navigation link to **"Explainable AI (Directives)"**.
7. **Explainable AI & Strategic Directives (`/explainable-ai?projectId=:id`)**:
   - High-level executive decision-support dashboard for District Magistrates & Project Directors.
   - Top SHAP-derived risk drivers, root-cause interpretation, statutory administrative delegation matrix, and SOP mitigation directives.
   - Explicit **"Return to SHAP Explainability"** button preserving project context.
8. **Alerts & Sound Chime (`/alerts`)**:
   - Automated 15-second background poller.
   - Test audio chime button.
   - "Trigger Live Delay Spike" button to simulate an escalated event with live audio notification.
9. **Statutory Reports & Land Records (`/reports` & `/land-records`)**:
   - Download official ReportLab-generated PDF compliance dossiers.
   - Filter cadastral land parcels, Khasra numbers, and dispute litigation status.

---

## 💻 Quick Start & Running Locally

### Prerequisites
- **Node.js**: v20 or higher (`node -v`)
- **Python**: v3.11, 3.12, or 3.13 (`python --version`)

---

### Step 1: Start the FastAPI Backend

Open a terminal in the project root:

```powershell
# Navigate to backend directory
cd backend

# Activate the existing virtual environment (all packages pre-installed)
.\.venv\Scripts\Activate.ps1

# Run the FastAPI server on port 8000
python -m uvicorn app.main:app --port 8000 --reload
```

- Backend API: `http://localhost:8000`
- Interactive OpenAPI / Swagger Docs: `http://localhost:8000/docs`
- Health Probe: `http://localhost:8000/api/health`

*Note: Database automatically seeds 12 realistic Indian infrastructure projects and cadastral records upon startup.*

---

### Step 2: Start the Angular Frontend

Open a second terminal:

```powershell
# Navigate to frontend directory
cd frontend

# Build or start development server
npm start
```

- Web Application: `http://localhost:4200`

---

```powershell
# Run Backend Test Suite (10/10 automated tests)
cd backend
.\.venv\Scripts\python.exe -m pytest

# Run Frontend Unit Tests (Vitest / Karma)
cd ../frontend
npm test -- --watch=false

# Run Frontend Production Build
npm run build
```

---

## 📂 Project Repository Structure

```
SIH26017/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI route handlers (auth, projects, gis, shap, whatif, alerts, reports)
│   │   ├── core/           # Security (bcrypt, JWT), configuration
│   │   ├── database/       # SQLAlchemy engine, session, and seed data
│   │   ├── models/         # Relational database models (Project, Risk, Factor, SHAP, Alert)
│   │   ├── schemas/        # Pydantic v2 validation schemas
│   │   ├── services/       # Core business logic, What-If calculator, ReportLab PDF builder
│   │   └── main.py         # Application entry point & lifespan manager
│   ├── ml/
│   │   ├── data/           # 2,500 balanced synthetic training dataset generator
│   │   ├── explainability/ # TreeSHAP explainer with float serialization
│   │   ├── models/         # Serialized CatBoost models (.cbm) & transformers (.joblib)
│   │   ├── preprocessing/  # ColumnTransformer & scalers
│   │   └── training/       # CatBoost vs LightGBM training & benchmarking script
│   └── land_acquisition.db# Local SQLite fallback database (seeded)
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/       # Guards, services (Api, Auth, Sound), models
│   │   │   ├── layout/     # Header, Sidebar, MainLayout with 15s poller & toast
│   │   │   ├── pages/      # All prototype views (Login, Dashboard, GIS, Details, SHAP, What-If, Alerts, Reports, Land Records, Settings)
│   │   │   ├── app.routes.ts
│   │   │   └── app.config.ts
│   │   ├── styles.scss     # Leaflet CSS, Google Fonts, theme variables
│   │   └── main.ts
│   ├── angular.json
│   └── package.json
├── docs/
│   ├── architecture/       # Detailed technical architecture
│   ├── api/                # Complete REST API reference
│   ├── ml/                 # CatBoost & TreeSHAP technical breakdown
│   └── workflow/           # Evaluator step-by-step verification guide
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── LICENSE
└── README.md
```

---

## 👥 Team: NEXORA_TAU
Built with ❤️ for the Smart India Hackathon (SIH 2026).
All rights reserved under the MIT License.
