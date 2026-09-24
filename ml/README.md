# NEXORA_TAU - Machine Learning Pipeline (SIH26017)
## Predictive Analytics System for Early Detection of Land Acquisition Delays

### 1. Overview
The ML subsystem predicts land acquisition delay probability, classifies project risk levels (`LOW`, `MEDIUM`, `HIGH`), estimates expected delay duration in days, and computes SHAP (SHapley Additive exPlanations) feature attributions.

### 2. Architecture & Pipeline
```
Raw Project Data & Synthetic Seed
            ↓
Preprocessing Pipeline (Categorical Encoding + Numerical Scaling)
            ↓
Multi-Model Benchmarking:
  - Classification: CatBoost Classifier vs LightGBM Classifier
  - Regression: CatBoost Regressor vs LightGBM Regressor
            ↓
Selected Best Models:
  - Classification Best: CatBoost Classifier (F1: 0.9216, Accuracy: 92.4%)
  - Regression Best: CatBoost Regressor (R²: 0.9554, MAE: 6.42 days)
            ↓
TreeSHAP Explainer (Feature Attribution into 8 Canonical Factors)
            ↓
What-If Simulator & Recommendation Engine
```

### 3. Key Risk Factors
1. **Compensation Delay** (Disbursement timelines, title dispute clearance)
2. **Legal Disputes** (Civil suits, writ petitions)
3. **Pending Approvals** (Forest Stage-I/II, MoEF&CC, Wildlife)
4. **R&R Progress** (Resettlement & Rehabilitation execution rate)
5. **Documentation Issues** (Revenue record mutation discrepancies)
6. **Land Owner Resistance** (Consent consensus and local opposition)
7. **Survey & Amendments** (Joint measurement survey re-validations)
8. **Other Factors** (Administrative constraints, multi-agency coordination)

### 4. Running Training & Evaluation
```bash
.\backend\.venv\Scripts\python.exe -m ml.training.train
```
Model evaluation metrics are exported to `ml/evaluation/model_metrics.json`.
