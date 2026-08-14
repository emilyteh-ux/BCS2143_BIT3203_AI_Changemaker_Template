"""Telemetry data hygiene, edge cost function, and heuristic utilities."""

import math
import numpy as np
import pandas as pd
from graph import Edge, RoadNetworkGraph


def clean_safety_telemetry(df: pd.DataFrame) -> pd.DataFrame:
    """Telemetry data hygiene pipeline."""
    df_clean = df.copy()

    if "safety_score" in df_clean.columns:
        df_clean.loc[~df_clean["safety_score"].between(0.0, 100.0), "safety_score"] = np.nan
        df_clean["safety_score"] = df_clean["safety_score"].fillna(df_clean["safety_score"].median())

    if "lighting_level" in df_clean.columns:
        df_clean.loc[~df_clean["lighting_level"].between(0, 5), "lighting_level"] = np.nan
        df_clean["lighting_level"] = df_clean["lighting_level"].fillna(df_clean["lighting_level"].median())

    if "hazard_type" in df_clean.columns:
        hazard_mode = df_clean["hazard_type"].mode()[0]
        df_clean["hazard_type"] = df_clean["hazard_type"].fillna(hazard_mode)

    return df_clean


def calculate_edge_risk_cost(edge: Edge, safety_weight: float = 1.0) -> float:
    """Computes total risk-penalized edge cost."""
    if safety_weight == 0.0:
        return edge.distance
    return round(edge.distance * edge.risk_score(), 2)


def calculate_euclidean_heuristic(graph: RoadNetworkGraph, a: str, b: str) -> float:
    """Admissible Euclidean straight-line heuristic."""
    na, nb = graph.nodes[a], graph.nodes[b]
    return round(math.hypot(nb.x - na.x, nb.y - na.y), 2)