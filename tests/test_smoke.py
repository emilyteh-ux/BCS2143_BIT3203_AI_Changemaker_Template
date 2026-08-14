"""Automated Smoke and Unit Test Suite for SafeRoute.AI."""

import os
import sys
import unittest
import numpy as np
import pandas as pd

# Add 'src' directory to Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from graph import RoadNetworkGraph, SafetyPatrolCSP, Edge
from cost import clean_safety_telemetry, calculate_edge_risk_cost
from algorithms import (
    breadth_first_search,
    a_star_safe_route,
    allocate_patrol_csp
)


class TestSafeRouteAI(unittest.TestCase):

    def setUp(self):
        """Set up test graph dataset for Ipoh City Center."""
        self.graph = RoadNetworkGraph()
        test_data = {
            "nodes": {
                "ipoh_railway_station":   {"alias": "A", "name": "Ipoh Railway Station", "x": 0, "y": 0},
                "birch_clock_tower":      {"alias": "B", "name": "Birch Clock Tower", "x": 25, "y": 15},
                "central_police_station": {"alias": "C", "name": "Police Station", "x": 40, "y": -20},
                "concubine_lane":         {"alias": "D", "name": "Concubine Lane", "x": 50, "y": 20},
                "kinta_riverfront":       {"alias": "F", "name": "Kinta Riverfront", "x": 75, "y": 45},
                "hospital_bainun":        {"alias": "J", "name": "Hospital Bainun", "x": 140, "y": 70}
            },
            "edges": [
                {"from": "ipoh_railway_station", "to": "birch_clock_tower", "distance_meters": 300, "safety_score": 85.0, "lighting_level": 4, "has_cctv": True},
                {"from": "ipoh_railway_station", "to": "central_police_station", "distance_meters": 450, "safety_score": 95.0, "lighting_level": 5, "has_cctv": True},
                {"from": "birch_clock_tower", "to": "concubine_lane", "distance_meters": 280, "safety_score": 75.0, "lighting_level": 3, "has_cctv": True},
                {"from": "central_police_station", "to": "concubine_lane", "distance_meters": 400, "safety_score": 90.0, "lighting_level": 5, "has_cctv": True},
                {"from": "concubine_lane", "to": "kinta_riverfront", "distance_meters": 350, "safety_score": 65.0, "lighting_level": 2, "has_cctv": False},
                {"from": "kinta_riverfront", "to": "hospital_bainun", "distance_meters": 900, "safety_score": 78.0, "lighting_level": 3, "has_cctv": True}
            ]
        }
        self.graph.load_from_json_data(test_data)

    def test_01_telemetry_data_hygiene(self):
        """Test Case 1: Verify data cleaning imputes missing/out-of-bound sensor values."""
        raw_df = pd.DataFrame({
            "safety_score": [85.0, 150.0, np.nan, 60.0, -10.0],
            "lighting_level": [5.0, 4.0, 10.0, np.nan, 2.0],
            "hazard_type": ["Clear", "Obstacle", None, "Clear", "Clear"]
        })
        clean_df = clean_safety_telemetry(raw_df)

        # Check no NaN values remain
        self.assertFalse(clean_df.isnull().values.any())
        # Check out-of-bound values (150 and -10) were replaced with median
        self.assertTrue((clean_df["safety_score"] >= 0.0).all())
        self.assertTrue((clean_df["safety_score"] <= 100.0).all())

    def test_02_astar_pathfinding(self):
        """Test Case 2: Verify A* finds optimal safe path from Station (A) to Hospital (J)."""
        path, risk_cost, _ = a_star_safe_route(
            self.graph, "ipoh_railway_station", "hospital_bainun"
        )
        expected_path = [
            "ipoh_railway_station",
            "central_police_station",
            "concubine_lane",
            "kinta_riverfront",
            "hospital_bainun"
        ]
        
        self.assertEqual(path, expected_path)
        self.assertGreater(risk_cost, 0.0)

    def test_03_csp_patrol_allocation(self):
        """Test Case 3: Verify CSP backtracking assigns non-conflicting patrol teams."""
        sectors = ["Concubine_Lane_Sector", "Gerbang_Malam_Sector", "Kinta_Riverfront_Sector"]
        teams = {
            "Concubine_Lane_Sector": ["Alpha_Team", "Bravo_Team"],
            "Gerbang_Malam_Sector": ["Alpha_Team", "Bravo_Team"],
            "Kinta_Riverfront_Sector": ["Alpha_Team", "Bravo_Team", "Charlie_Team"]
        }
        adjacencies = {
            "Concubine_Lane_Sector": ["Gerbang_Malam_Sector"],
            "Gerbang_Malam_Sector": ["Concubine_Lane_Sector", "Kinta_Riverfront_Sector"],
            "Kinta_Riverfront_Sector": ["Gerbang_Malam_Sector"]
        }

        csp = SafetyPatrolCSP(sectors, teams, adjacencies)
        solution = allocate_patrol_csp(csp)

        self.assertIsNotNone(solution)
        # Verify adjacent sectors do not share the same patrol team
        self.assertNotEqual(solution["Concubine_Lane_Sector"], solution["Gerbang_Malam_Sector"])
        self.assertNotEqual(solution["Gerbang_Malam_Sector"], solution["Kinta_Riverfront_Sector"])


if __name__ == "__main__":
    unittest.main()