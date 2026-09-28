def test_list_projects(client, auth_headers):
    response = client.get("/api/projects", headers=auth_headers)
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) >= 5
    # Verify risk levels are valid: HIGH, MEDIUM, LOW
    for p in projects:
        assert p["risk_level"] in ["HIGH", "MEDIUM", "LOW"]

def test_project_details_project_3(client, auth_headers):
    response = client.get("/api/projects/3", headers=auth_headers)
    assert response.status_code == 200
    p = response.json()
    assert p["id"] == 3
    assert p["project_code"] == "PRJ-JK-2023-01"
    assert "Udhampur-Srinagar-Baramulla" in p["name"]
    assert p["risk_prediction"]["risk_level"] == "HIGH"
    assert p["risk_prediction"]["predicted_delay_days"] > 0
    assert p["daily_delay_cost_lakhs"] > 0

def test_whatif_simulation_project_3(client, auth_headers):
    payload = {
        "compensation_delay_reduction_pct": 50,
        "legal_disputes_resolution_pct": 40,
        "approvals_expedited_pct": 30,
        "rr_progress_acceleration_pct": 20,
        "documentation_streamlining_pct": 10
    }
    response = client.post("/api/projects/3/what-if", json=payload, headers=auth_headers)
    assert response.status_code == 200
    sim = response.json()
    assert sim["project_id"] == 3
    assert sim["baseline_delay_days"] == 254
    assert sim["simulated_delay_days"] < sim["baseline_delay_days"]
    assert sim["delay_reduction_days"] > 0
    assert sim["cost_savings_cr"] > 0
    assert len(sim["key_drivers_addressed"]) > 0

def test_shap_explanation_project_3(client, auth_headers):
    response = client.get("/api/projects/3/shap", headers=auth_headers)
    assert response.status_code == 200
    shap_data = response.json()
    assert shap_data["project_id"] == 3
    assert len(shap_data["features"]) > 0
    assert "TreeSHAP" in shap_data["model_used"] or "CatBoost" in shap_data["model_used"]
    # Check that features have contribution percentages and sum to reasonable attribution
    top_feature = shap_data["features"][0]
    assert "feature" in top_feature
    assert top_feature["contribution_pct"] > 0
    assert "impact_label" in top_feature

def test_recommendations_project_3(client, auth_headers):
    response = client.get("/api/projects/3/recommendations", headers=auth_headers)
    assert response.status_code == 200
    rec_data = response.json()
    assert rec_data["project_id"] == 3
    assert len(rec_data["recommendations"]) > 0
    assert rec_data["total_potential_delay_reduction_days"] > 0
    assert rec_data["total_potential_savings_cr"] > 0
    rec = rec_data["recommendations"][0]
    assert rec["priority"] in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    assert len(rec["action_steps"]) > 0

def test_financial_impact_project_3(client, auth_headers):
    response = client.get("/api/projects/3/financial-impact", headers=auth_headers)
    assert response.status_code == 200
    fin_data = response.json()
    assert fin_data["project_id"] == 3
    assert fin_data["daily_delay_cost_lakhs"] == 9.2
    assert len(fin_data["scenarios"]) == 5
    for s in fin_data["scenarios"]:
        assert s["total_delay_days"] > 0
        assert s["estimated_cost_cr"] > 0
        assert s["impact_level"] in ["BASELINE", "LOW", "MODERATE", "HIGH", "SEVERE"]
