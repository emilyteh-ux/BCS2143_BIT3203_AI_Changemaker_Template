"""Main entry point for the AI Changemaker assignment.

Safety-Aware Pedestrian Navigation using A* Search.

Compares a baseline shortest-path route against a safety-optimized route
across three test map scenarios, evaluating the trade-off between
added distance, path safety, and computational efficiency (nodes expanded).
"""

import heapq
import math
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Graph representation
# ---------------------------------------------------------------------------

@dataclass
class Node:
    id: str
    x: float
    y: float


@dataclass
class Edge:
    to: str
    distance: float       # in metres
    lighting: float        # 0.0 (dark) to 1.0 (well-lit)
    foot_traffic: float    # 0.0 (empty) to 1.0 (busy)

    def risk_score(self) -> float:
        """Higher = riskier. Combines lack of lighting and low foot traffic."""
        return (1 - self.lighting) * 0.6 + (1 - self.foot_traffic) * 0.4


class Graph:
    def __init__(self):
        self.nodes: dict[str, Node] = {}
        self.adjacency: dict[str, list[Edge]] = {}

    def add_node(self, node_id: str, x: float, y: float) -> None:
        self.nodes[node_id] = Node(node_id, x, y)
        self.adjacency.setdefault(node_id, [])

    def add_edge(self, a: str, b: str, distance: float,
                 lighting: float, foot_traffic: float, bidirectional=True) -> None:
        self.adjacency[a].append(Edge(b, distance, lighting, foot_traffic))
        if bidirectional:
            self.adjacency[b].append(Edge(a, distance, lighting, foot_traffic))

    def neighbors(self, node_id: str) -> list[Edge]:
        return self.adjacency.get(node_id, [])


# ---------------------------------------------------------------------------
# A* Search
# ---------------------------------------------------------------------------

@dataclass(order=True)
class PQItem:
    priority: float
    node_id: str = field(compare=False)


def euclidean(graph: Graph, a: str, b: str) -> float:
    na, nb = graph.nodes[a], graph.nodes[b]
    return math.hypot(na.x - nb.x, na.y - nb.y)


def a_star(graph: Graph, start: str, goal: str, safety_weight: float,
           risk_penalty_scale: float = 300.0) -> tuple[list[str], float, float, int]:
    """
    Runs A* search from start to goal.

    safety_weight: 0.0 = pure shortest-path baseline.
                   >0.0 = safety-optimized (penalizes risky edges).

    Returns: (path, total_distance, total_risk_penalty, nodes_expanded)
    """
    frontier: list[PQItem] = []
    heapq.heappush(frontier, PQItem(0, start))

    came_from: dict[str, str | None] = {start: None}
    g_score: dict[str, float] = {start: 0.0}
    edge_used: dict[str, Edge | None] = {start: None}

    nodes_expanded = 0

    while frontier:
        current = heapq.heappop(frontier).node_id
        nodes_expanded += 1

        if current == goal:
            break

        for edge in graph.neighbors(current):
            step_cost = edge.distance + safety_weight * edge.risk_score() * risk_penalty_scale
            tentative_g = g_score[current] + step_cost

            if edge.to not in g_score or tentative_g < g_score[edge.to]:
                g_score[edge.to] = tentative_g
                came_from[edge.to] = current
                edge_used[edge.to] = edge
                f_score = tentative_g + euclidean(graph, edge.to, goal)
                heapq.heappush(frontier, PQItem(f_score, edge.to))

    # Reconstruct path
    if goal not in came_from:
        return [], float("inf"), float("inf"), nodes_expanded

    path = []
    total_distance = 0.0
    total_risk = 0.0
    node = goal
    while node is not None:
        path.append(node)
        edge = edge_used[node]
        if edge is not None:
            total_distance += edge.distance
            total_risk += edge.risk_score()
        node = came_from[node]
    path.reverse()

    return path, total_distance, total_risk, nodes_expanded


# ---------------------------------------------------------------------------
# Test scenario builders
# ---------------------------------------------------------------------------

def build_scenario_1() -> Graph:
    """Small grid: one short route is fast but poorly lit/isolated."""
    g = Graph()
    coords = {
        "A": (0, 0), "B": (100, 0), "C": (200, 0),
        "D": (0, 100), "E": (100, 100), "F": (200, 100),
    }
    for nid, (x, y) in coords.items():
        g.add_node(nid, x, y)

    g.add_edge("A", "B", 100, lighting=0.2, foot_traffic=0.1)   # short, unsafe
    g.add_edge("B", "C", 100, lighting=0.2, foot_traffic=0.1)   # short, unsafe
    g.add_edge("A", "D", 100, lighting=0.9, foot_traffic=0.8)   # safe
    g.add_edge("D", "E", 100, lighting=0.9, foot_traffic=0.8)   # safe
    g.add_edge("E", "F", 100, lighting=0.9, foot_traffic=0.7)   # safe
    g.add_edge("F", "C", 100, lighting=0.9, foot_traffic=0.7)   # safe
    return g


def build_scenario_2() -> Graph:
    """Denser network with a mix of moderately safe shortcuts."""
    g = Graph()
    coords = {
        "A": (0, 0), "B": (80, 40), "C": (160, 0), "D": (240, 40),
        "E": (0, 120), "F": (120, 120), "G": (240, 120),
    }
    for nid, (x, y) in coords.items():
        g.add_node(nid, x, y)

    g.add_edge("A", "B", 90, lighting=0.4, foot_traffic=0.3)
    g.add_edge("B", "C", 90, lighting=0.4, foot_traffic=0.3)
    g.add_edge("C", "D", 90, lighting=0.5, foot_traffic=0.4)
    g.add_edge("A", "E", 120, lighting=0.8, foot_traffic=0.9)
    g.add_edge("E", "F", 130, lighting=0.9, foot_traffic=0.9)
    g.add_edge("F", "G", 130, lighting=0.9, foot_traffic=0.8)
    g.add_edge("G", "D", 90, lighting=0.7, foot_traffic=0.6)
    g.add_edge("B", "F", 90, lighting=0.3, foot_traffic=0.2)  # risky shortcut
    return g


def build_scenario_3() -> Graph:
    """Larger sparse network simulating a campus-to-home commute."""
    g = Graph()
    coords = {
        "A": (0, 0), "B": (50, 50), "C": (100, 100), "D": (150, 50),
        "E": (200, 0), "F": (50, -80), "G": (150, -80), "H": (200, -20),
    }
    for nid, (x, y) in coords.items():
        g.add_node(nid, x, y)

    g.add_edge("A", "B", 70, lighting=0.6, foot_traffic=0.5)
    g.add_edge("B", "C", 70, lighting=0.7, foot_traffic=0.6)
    g.add_edge("C", "D", 70, lighting=0.6, foot_traffic=0.5)
    g.add_edge("D", "E", 70, lighting=0.6, foot_traffic=0.5)
    g.add_edge("A", "F", 60, lighting=0.2, foot_traffic=0.1)  # dark shortcut
    g.add_edge("F", "G", 60, lighting=0.2, foot_traffic=0.1)
    g.add_edge("G", "H", 60, lighting=0.3, foot_traffic=0.2)
    g.add_edge("H", "E", 60, lighting=0.4, foot_traffic=0.3)
    return g


SCENARIOS = {
    "Scenario 1: Small grid (isolated shortcut vs lit loop)": (build_scenario_1(), "A", "C"),
    "Scenario 2: Dense network with risky shortcut": (build_scenario_2(), "A", "D"),
    "Scenario 3: Campus commute (dark shortcut vs lit main road)": (build_scenario_3(), "A", "E"),
}


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_scenario(name: str, graph: Graph, start: str, goal: str) -> None:
    print(f"\n=== {name} ===")

    base_path, base_dist, base_risk, base_expanded = a_star(
        graph, start, goal, safety_weight=0.0
    )
    safe_path, safe_dist, safe_risk, safe_expanded = a_star(
        graph, start, goal, safety_weight=1.0
    )

    print(f"Baseline (shortest path):")
    print(f"  Path: {' -> '.join(base_path)}")
    print(f"  Distance: {base_dist:.1f} m | Risk score: {base_risk:.2f} | Nodes expanded: {base_expanded}")

    print(f"Safety-optimized:")
    print(f"  Path: {' -> '.join(safe_path)}")
    print(f"  Distance: {safe_dist:.1f} m | Risk score: {safe_risk:.2f} | Nodes expanded: {safe_expanded}")

    extra_distance = safe_dist - base_dist
    risk_reduction = base_risk - safe_risk
    print(f"  --> Extra distance: {extra_distance:.1f} m | Risk reduced by: {risk_reduction:.2f}")


def main() -> None:
    print("AI Changemaker: Safety-Aware Pedestrian Navigation (A* Search)")
    for name, (graph, start, goal) in SCENARIOS.items():
        run_scenario(name, graph, start, goal)


if __name__ == "__main__":
    main()