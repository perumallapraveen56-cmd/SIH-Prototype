# REST API Specification (SIH26017)
**Team**: NEXORA_TAU  
**Base URL**: `http://localhost:8000/api`

---

## 1. Authentication (`/auth`)

### `POST /auth/login`
Authenticates a user session with username and password.
- **Request Body**:
  ```json
  {
    "email": "user@domain.gov.in",
    "password": "<AUTHENTICATED_CREDENTIAL>"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "email": "officer@gov.in",
      "full_name": "Rajeshwar Sharma",
      "role": "OFFICER",
      "department": "State Land Acquisition Department"
    }
  }
  ```

---

## 2. Infrastructure Projects (`/projects`)

### `GET /projects`
Fetches all monitored infrastructure projects with filters.
- **Query Parameters**:
  - `state` (optional string): e.g. "Uttar Pradesh"
  - `district` (optional string): e.g. "Gautam Buddha Nagar"
  - `project_type` (optional string): e.g. "Highways"
  - `risk_level` (optional string): `HIGH`, `MEDIUM`, `LOW`
- **Response** (`200 OK`): List of `ProjectSummary`.

### `GET /projects/{project_id}`
Returns complete project dossier, current acquisition stage, and top 8 canonical risk factors.

### `GET /projects/{project_id}/risk`
Returns risk prediction, top 8 risk factors, and project-specific estimated cost impact in ₹ Crores.

### `GET /projects/parcels/all`
Returns granular cadastral survey land parcels across all projects with Khasra numbers, landowner records, dispute status, and compensation values.

---

## 3. Spatial & GIS Analytics (`/gis`)

### `GET /gis/projects`
Returns GeoJSON / Map markers with latitude, longitude, and risk color coding:
- 🔴 **High Risk**: Red marker
- 🟡 **Medium Risk**: Yellow / Amber marker
- 🟢 **Low Risk**: Green marker

### `GET /gis/filters`
Returns available filter options (states, districts, project types, risk levels).

---

## 4. AI & TreeSHAP Attribution (`/projects/{project_id}/shap`)

### `GET /projects/{project_id}/shap`
Calculates real-time TreeSHAP waterfall feature attributions across the 8 canonical statutory factors.

---

## 5. What-If Simulator & Recommendations (`/projects/{project_id}/what-if`)

### `GET /projects/{project_id}/recommendations`
Fetches project-specific Standard Operating Procedure (SOP) mitigation actions.

### `POST /projects/{project_id}/what-if`
Recalculates delay duration and risk probability given hypothetical intervention parameters:
- **Request Body**:
  ```json
  {
    "dispute_resolution_pct": 50.0,
    "additional_staff_assigned": 3,
    "compensation_rate_increase_pct": 10.0,
    "forest_clearance_fasttracked": true,
    "r_and_r_enhanced": true
  }
  ```
- **Response** (`200 OK`): Recalculated delay days, days saved, new risk score, and cost reduction.

---

## 6. Alerts & 15s Safety Poller (`/alerts`)

### `GET /alerts`
Returns unacknowledged and historical system alerts.

### `GET /alerts/poll`
High-performance poll endpoint called by client every 15 seconds:
- **Response** (`200 OK`):
  ```json
  {
    "unacknowledged_high_count": 2,
    "should_play_sound": false,
    "new_alert_ids": [],
    "alerts": [...]
  }
  ```
- **Sound Rule**: `should_play_sound` is `true` **only** when a new, unacknowledged high-risk alert is created during the current interval.

### `POST /alerts/{alert_id}/acknowledge`
Acknowledges an alert, preventing repeated notifications.

### `POST /alerts/trigger-live`
Live demo delay spike simulator.

---

## 7. Statutory Reports (`/reports`)

### `POST /reports/generate`
Generates statutory PDF or JSON compliance reports.

### `GET /reports/download-pdf/{project_id}`
Direct streaming download of official ReportLab-generated project risk report PDF.
