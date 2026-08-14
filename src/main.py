"""Main entry point for SafeRoute.AI."""

import numpy as np
import pandas as pd
from graph import RoadNetworkGraph, SafetyPatrolCSP
from cost import clean_safety_telemetry
from algorithms import (
    breadth_first_search,
    depth_first_search,
    uniform_cost_search,
    a_star_safe_route,
    allocate_patrol_csp
)

IPOH_MAP_DATA = {
  "nodes": {
    "ipoh_railway_station":   {"alias": "A", "name": "Ipoh Railway Station",              "x": 0,   "y": 0,   "is_safe_haven": True},
    "birch_clock_tower":      {"alias": "B", "name": "Birch Memorial Clock Tower",        "x": 25,  "y": 15,  "is_safe_haven": False},
    "central_police_station": {"alias": "C", "name": "Ipoh District Police Headquarters", "x": 40,  "y": -20, "is_safe_haven": True},
    "concubine_lane":         {"alias": "D", "name": "Concubine Lane",                    "x": 50,  "y": 20,  "is_safe_haven": False},
    "padang_ipoh":            {"alias": "E", "name": "Padang Ipoh",                       "x": 35,  "y": 40,  "is_safe_haven": False},
    "kinta_riverfront":       {"alias": "F", "name": "Kinta Riverfront Walk",             "x": 75,  "y": 45,  "is_safe_haven": False},
    "gerbang_malam":          {"alias": "G", "name": "Gerbang Malam Night Market",        "x": 100, "y": 10,  "is_safe_haven": False},
    "yau_tet_shin":           {"alias": "H", "name": "Yau Tet Shin Food District",        "x": 110, "y": 35,  "is_safe_haven": False},
    "greentown_center":       {"alias": "I", "name": "Greentown Business Centre",         "x": 150, "y": 30,  "is_safe_haven": False},
    "hospital_bainun":        {"alias": "J", "name": "Hospital Raja Permaisuri Bainun",   "x": 140, "y": 70,  "is_safe_haven": True}
  },
  "edges": [
    {"from": "ipoh_railway_station",   "to": "birch_clock_tower",      "distance_meters": 300, "safety_score": 85.0, "lighting_level": 4, "has_cctv": True},
    {"from": "ipoh_railway_station",   "to": "central_police_station", "distance_meters": 450, "safety_score": 95.0, "lighting_level": 5, "has_cctv": True},
    {"from": "birch_clock_tower",      "to": "concubine_lane",         "distance_meters": 280, "safety_score": 75.0, "lighting_level": 3, "has_cctv": True},
    {"from": "birch_clock_tower",      "to": "padang_ipoh",            "distance_meters": 320, "safety_score": 80.0, "lighting_level": 4, "has_cctv": False},
    {"from": "central_police_station", "to": "concubine_lane",         "distance_meters": 400, "safety_score": 90.0, "lighting_level": 5, "has_cctv": True},
    {"from": "padang_ipoh",            "to": "kinta_riverfront",       "distance_meters": 420, "safety_score": 60.0, "lighting_level": 2, "has_cctv": False},
    {"from": "concubine_lane",         "to": "kinta_riverfront",       "distance_meters": 350, "safety_score": 65.0, "lighting_level": 2, "has_cctv": False},
    {"from": "concubine_lane",         "to": "gerbang_malam",          "distance_meters": 600, "safety_score": 88.0, "lighting_level": 5, "has_cctv": True},
    {"from": "kinta_riverfront",       "to": "yau_tet_shin",           "distance_meters": 480, "safety_score": 70.0, "lighting_level": 3, "has_cctv": False},
    {"from": "gerbang_malam",          "to": "yau_tet_shin",           "distance_meters": 250, "safety_score": 92.0, "lighting_level": 5, "has_cctv": True},
    {"from": "yau_tet_shin",           "to": "greentown_center",       "distance_meters": 850, "safety_score": 82.0, "lighting_level": 4, "has_cctv": True},
    {"from": "kinta_riverfront",       "to": "hospital_bainun",        "distance_meters": 900, "safety_score": 78.0, "lighting_level": 3, "has_cctv": True},
    {"from": "greentown_center",       "to": "hospital_bainun",        "distance_meters": 500, "safety_score": 90.0, "lighting_level": 5, "has_cctv": True}
  ]
}


def fmt_aliases(graph: RoadNetworkGraph, path: list[str]) -> str:
    """Formats path to display ONLY node letter aliases (e.g., 'A -> B -> D')."""
    return " -> ".join([graph.nodes[node].alias for node in path])


def main() -> None:
    # -----------------------------------------------------------------------
    # [1] IoT Safety Telemetry Preprocessing
    # -----------------------------------------------------------------------
    print("[1] IoT Safety Telemetry Preprocessing...")
    raw_sensor_data = {
        "safety_score": [85.0, 120.0, np.nan, 60.0, -10.0],
        "lighting_level": [5.0, 4.0, 4.0, 4.0, 2.0],
        "hazard_type": ["Clear", "Obstacle", "Clear", "Clear", "Clear"]
    }
    df_raw = pd.DataFrame(raw_sensor_data)
    df_clean = clean_safety_telemetry(df_raw)
    print("Validated Telemetry Stream:")
    print(df_clean.to_string())
    print()

    # -----------------------------------------------------------------------
    # Graph Setup
    # -----------------------------------------------------------------------
    graph = RoadNetworkGraph()
    graph.load_from_json_data(IPOH_MAP_DATA)

    start_node = "ipoh_railway_station"
    goal_node = "hospital_bainun"

    # -----------------------------------------------------------------------
    # Node Legend
    # -----------------------------------------------------------------------
    print("Node Aliases Legend:")
    for nid, node in graph.nodes.items():
        print(f"  ({node.alias}) {nid} - {node.name}")
    print()

    # -----------------------------------------------------------------------
    # [2] Route Optimization Engine Comparison (Letters Only)
    # -----------------------------------------------------------------------
    print(f"[2] Route Optimization Engine (Start: {start_node} ({graph.nodes[start_node].alias}) -> Goal: {goal_node} ({graph.nodes[goal_node].alias}))\n")

    # BFS
    bfs_path, bfs_cost, bfs_order = breadth_first_search(graph, start_node, goal_node)
    print("--- Breadth-First Search (BFS) ---")
    print(f"Expansion Order: {fmt_aliases(graph, bfs_order)}")
    print(f"Computed Path:   {fmt_aliases(graph, bfs_path)}")
    print(f"Path Risk Cost:  {bfs_cost}\n")

    # DFS
    dfs_path, dfs_cost, dfs_order = depth_first_search(graph, start_node, goal_node)
    print("--- Depth-First Search (DFS) ---")
    print(f"Expansion Order: {fmt_aliases(graph, dfs_order)}")
    print(f"Computed Path:   {fmt_aliases(graph, dfs_path)}")
    print(f"Path Risk Cost:  {dfs_cost}\n")

    # UCS
    ucs_path, ucs_cost, ucs_order = uniform_cost_search(graph, start_node, goal_node)
    print("--- Uniform Cost Search (UCS) ---")
    print(f"Expansion Order: {fmt_aliases(graph, ucs_order)}")
    print(f"Safest Path:     {fmt_aliases(graph, ucs_path)}")
    print(f"Path Risk Cost:  {ucs_cost}\n")

    # A*
    a_star_path, a_star_cost, a_star_order = a_star_safe_route(graph, start_node, goal_node)
    print("--- A* Search (Informed Euclidean Heuristic) ---")
    print(f"Expansion Order: {fmt_aliases(graph, a_star_order)}")
    print(f"Safest Path:     {fmt_aliases(graph, a_star_path)}")
    print(f"Path Risk Cost:  {a_star_cost}\n")


if __name__ == "__main__":
    main()