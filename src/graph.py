"""Graph representation and CSP structures for SafeRoute.AI."""

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class Node:
    id: str
    name: str
    alias: str
    x: float
    y: float
    is_safe_haven: bool = False


@dataclass
class Edge:
    to: str
    distance: float            # in metres
    safety_score: float        # 0.0 to 100.0
    lighting: float            # 0.0 (dark) to 5.0 (well-lit)
    has_cctv: bool = False
    foot_traffic: float = 0.5  # 0.0 (empty) to 1.0 (busy)

    def risk_score(self) -> float:
        """Calculates a normalized segment risk multiplier."""
        safety_penalty = (100.0 - self.safety_score) / 50.0
        lighting_penalty = (5.0 - self.lighting) / 5.0
        cctv_penalty = 0.0 if self.has_cctv else 0.25
        return round(1.0 + safety_penalty + lighting_penalty + cctv_penalty, 2)


class RoadNetworkGraph:
    """Represents the SafeRoute.AI spatial graph for Ipoh City Center."""
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.adjacency: Dict[str, List[Edge]] = {}

    def add_node(self, node_id: str, name: str, alias: str, x: float, y: float, is_safe_haven: bool = False) -> None:
        self.nodes[node_id] = Node(node_id, name, alias, x, y, is_safe_haven)
        self.adjacency.setdefault(node_id, [])

    def add_road_segment(self, u: str, v: str, distance: float, safety_score: float,
                         lighting: float, has_cctv: bool, foot_traffic: float = 0.5,
                         bidirectional: bool = True) -> None:
        edge_uv = Edge(to=v, distance=distance, safety_score=safety_score, 
                       lighting=lighting, has_cctv=has_cctv, foot_traffic=foot_traffic)
        self.adjacency.setdefault(u, []).append(edge_uv)

        if bidirectional:
            edge_vu = Edge(to=u, distance=distance, safety_score=safety_score, 
                           lighting=lighting, has_cctv=has_cctv, foot_traffic=foot_traffic)
            self.adjacency.setdefault(v, []).append(edge_vu)

    def neighbors(self, node_id: str) -> List[Edge]:
        return self.adjacency.get(node_id, [])

    def load_from_json_data(self, data: Dict[str, Any]) -> None:
        """Populates the road network from map data dictionary."""
        for node_id, details in data.get("nodes", {}).items():
            self.add_node(
                node_id=node_id,
                name=details["name"],
                alias=details["alias"],
                x=details["x"],
                y=details["y"],
                is_safe_haven=details.get("is_safe_haven", False)
            )
        for edge in data.get("edges", []):
            self.add_road_segment(
                u=edge["from"],
                v=edge["to"],
                distance=edge["distance_meters"],
                safety_score=edge["safety_score"],
                lighting=edge["lighting_level"],
                has_cctv=edge["has_cctv"],
                foot_traffic=edge.get("foot_traffic", 0.5),
                bidirectional=True
            )


class SafetyPatrolCSP:
    """Constraint Satisfaction Problem for patrol escort allocation."""
    def __init__(self, zones: List[str], escort_teams: Dict[str, List[Any]], adjacencies: Dict[str, List[str]]):
        self.variables = zones
        self.domains = escort_teams
        self.constraints = adjacencies

    def is_consistent(self, zone: str, team: Any, assignment: Dict[str, Any]) -> bool:
        for neighbor in self.constraints.get(zone, []):
            if neighbor in assignment and assignment[neighbor] == team:
                return False
        return True

    def select_unassigned_variable(self, assignment: Dict[str, Any]) -> str:
        """Minimum Remaining Values (MRV) heuristic."""
        unassigned = [z for z in self.variables if z not in assignment]
        return min(unassigned, key=lambda z: len(self.domains[z]))