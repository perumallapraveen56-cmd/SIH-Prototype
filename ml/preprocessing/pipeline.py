"""
ML Preprocessing & Feature Engineering Pipeline
Handles categorical encoding, numerical scaling, and transformation for delay prediction.
"""

import os
import joblib
import pandas as pd
from typing import Tuple, List
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

NUMERICAL_FEATURES = [
    "total_area_ha",
    "total_parcels",
    "affected_families",
    "compensation_delay_days",
    "active_legal_disputes",
    "pending_statutory_approvals",
    "rr_progress_pct",
    "documentation_deficiency_score",
    "landowner_resistance_index",
    "survey_amendments_count",
    "base_budget_cr",
    "daily_delay_cost_lakhs"
]

CATEGORICAL_FEATURES = [
    "state",
    "project_type",
    "current_stage"
]

ALL_FEATURES = CATEGORICAL_FEATURES + NUMERICAL_FEATURES

class LandAcquisitionPreprocessor:
    def __init__(self):
        self.preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
                ("num", StandardScaler(), NUMERICAL_FEATURES)
            ]
        )
        self.feature_names: List[str] = []

    def fit_transform(self, X: pd.DataFrame):
        transformed = self.preprocessor.fit_transform(X[ALL_FEATURES])
        cat_features = list(self.preprocessor.named_transformers_["cat"].get_feature_names_out(CATEGORICAL_FEATURES))
        self.feature_names = cat_features + NUMERICAL_FEATURES
        return transformed

    def transform(self, X: pd.DataFrame):
        return self.preprocessor.transform(X[ALL_FEATURES])

    def save(self, file_path: str):
        joblib.dump(self, file_path)

    @staticmethod
    def load(file_path: str) -> "LandAcquisitionPreprocessor":
        return joblib.load(file_path)

def prepare_data(csv_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series, pd.Series]:
    df = pd.read_csv(csv_path)
    X = df[ALL_FEATURES]
    y_class = df["risk_level"]
    y_reg = df["delay_days"]

    X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
        X, y_class, y_reg, test_size=0.2, random_state=42, stratify=y_class
    )
    return X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test
