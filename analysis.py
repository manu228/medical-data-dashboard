"""Reproducible descriptive analysis of Wisconsin Diagnostic Breast Cancer data.

Dataset: scikit-learn's bundled copy of the UCI WDBC dataset.
The observations are fine-needle aspirate image features, not patients over time.
This software is educational and is not a medical device.
"""
from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_breast_cancer

DISPLAY_FEATURES = {
    "mean radius": "Mean radius",
    "mean texture": "Mean texture",
    "mean perimeter": "Mean perimeter",
    "mean area": "Mean area",
    "mean smoothness": "Mean smoothness",
    "mean concavity": "Mean concavity",
    "mean concave points": "Mean concave points",
    "worst radius": "Worst radius",
    "worst area": "Worst area",
    "worst concave points": "Worst concave points",
}


def get_data() -> pd.DataFrame:
    """Load bundled, non-identifying digitized-image features, no downloads/API keys."""
    raw = load_breast_cancer(as_frame=True)
    df = raw.data.copy()
    # sklearn target encoding: 0 = malignant, 1 = benign.
    df.insert(0, "diagnosis", raw.target.map({0: "Malignant", 1: "Benign"}))
    df.insert(0, "sample_id", [f"WDBC-{i:03d}" for i in range(1, len(df) + 1)])
    return df


def summary(df: pd.DataFrame) -> dict:
    n = len(df)
    benign = int((df["diagnosis"] == "Benign").sum())
    malignant = int((df["diagnosis"] == "Malignant").sum())
    return {"total": n, "benign": benign, "malignant": malignant,
            "malignant_pct": (100 * malignant / n if n else 0),
            "mean_radius": float(df["mean radius"].mean()) if n else None}


def grouped_feature_stats(df: pd.DataFrame, feature: str) -> pd.DataFrame:
    if feature not in DISPLAY_FEATURES:
        raise ValueError("Unsupported feature")
    return (df.groupby("diagnosis")[feature]
            .agg(count="count", mean="mean", median="median", std="std")
            .round(3).reset_index())
