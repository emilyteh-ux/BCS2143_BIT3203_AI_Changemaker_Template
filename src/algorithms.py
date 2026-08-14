"""Search algorithms (BFS, DFS, UCS, A*) and CSP solver."""

import heapq
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from graph import RoadNetworkGraph, SafetyPatrolCSP, Edge
from cost import calculate_edge_risk_cost, calculate_euclidean_heuristic


@dataclass(order=True)
class PQItem:
    priority: float
    node_id: str = field(compare=False)


def calculate_path_risk_cost(graph: RoadNetworkGraph, path: List[str]) -> float:
    """Calculates cumulative risk cost for a given path."""
    total_cost = 0.0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        for edge in graph.neighbors(u):
            if edge.to == v:
                total_cost += calculate_edge_risk_cost(edge, safety_weight=1.0)
                break
    return round(total_cost, 1)


def breadth_first_search(graph: RoadNetworkGraph, origin: str, destination: str) -> Tuple[Optional[List[str]], float, List[str]]:
    """Breadth-First Search (BFS)."""
    queue = deque([(origin, [origin])])
    visited = set()
    expansion_order = []

    while queue:
        node, path = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        expansion_order.append(node)

        if node == destination:
            return path, calculate_path_risk_cost(graph, path), expansion_order

        for edge in graph.neighbors(node):
            if edge.to not in visited:
                queue.append((edge.to, path + [edge.to]))

    return None, float("inf"), expansion_order


def depth_first_search(graph: RoadNetworkGraph, origin: str, destination: str) -> Tuple[Optional[List[str]], float, List[str]]:
    """Depth-First Search (DFS)."""
    stack = [(origin, [origin])]
    visited = set()
    expansion_order = []

    while stack:
        node, path = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        expansion_order.append(node)

        if node == destination:
            return path, calculate_path_risk_cost(graph, path), expansion_order

        for edge in reversed(graph.neighbors(node)):
            if edge.to not in visited:
                stack.append((edge.to, path + [edge.to]))

    return None, float("inf"), expansion_order


def uniform_cost_search(graph: RoadNetworkGraph, origin: str, destination: str) -> Tuple[Optional[List[str]], float, List[str]]:
    """Uniform Cost Search (UCS)."""
    frontier = []
    heapq.heappush(frontier, PQItem(0.0, origin))

    came_from: Dict[str, Optional[str]] = {origin: None}
    g_score: Dict[str, float] = {origin: 0.0}
    visited = set()
    expansion_order = []

    while frontier:
        current = heapq.heappop(frontier).node_id

        if current in visited:
            continue
        visited.add(current)
        expansion_order.append(current)

        if current == destination:
            break

        for edge in graph.neighbors(current):
            step_cost = calculate_edge_risk_cost(edge, safety_weight=1.0)
            tentative_g = g_score[current] + step_cost

            if edge.to not in g_score or tentative_g < g_score[edge.to]:
                g_score[edge.to] = tentative_g
                came_from[edge.to] = current
                heapq.heappush(frontier, PQItem(tentative_g, edge.to))

    if destination not in came_from:
        return None, float("inf"), expansion_order

    path = []
    curr = destination
    while curr is not None:
        path.append(curr)
        curr = came_from[curr]
    path.reverse()

    return path, round(g_score[destination], 1), expansion_order


def a_star_safe_route(graph: RoadNetworkGraph, origin: str, destination: str) -> Tuple[Optional[List[str]], float, List[str]]:
    """A* Search using Euclidean heuristic."""
    frontier = []
    heapq.heappush(frontier, PQItem(0.0, origin))

    came_from: Dict[str, Optional[str]] = {origin: None}
    g_score: Dict[str, float] = {origin: 0.0}
    visited = set()
    expansion_order = []

    while frontier:
        current = heapq.heappop(frontier).node_id

        if current in visited:
            continue
        visited.add(current)
        expansion_order.append(current)

        if current == destination:
            break

        for edge in graph.neighbors(current):
            step_cost = calculate_edge_risk_cost(edge, safety_weight=1.0)
            tentative_g = g_score[current] + step_cost

            if edge.to not in g_score or tentative_g < g_score[edge.to]:
                g_score[edge.to] = tentative_g
                came_from[edge.to] = current
                h_cost = calculate_euclidean_heuristic(graph, edge.to, destination)
                f_score = tentative_g + h_cost
                heapq.heappush(frontier, PQItem(f_score, edge.to))

    if destination not in came_from:
        return None, float("inf"), expansion_order

    path = []
    curr = destination
    while curr is not None:
        path.append(curr)
        curr = came_from[curr]
    path.reverse()

    return path, round(g_score[destination], 1), expansion_order


def allocate_patrol_csp(csp: SafetyPatrolCSP, assignment: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
    """Backtracking CSP solver with MRV Heuristic."""
    if assignment is None:
        assignment = {}

    if len(assignment) == len(csp.variables):
        return assignment

    zone = csp.select_unassigned_variable(assignment)

    for team in csp.domains[zone]:
        if csp.is_consistent(zone, team, assignment):
            assignment[zone] = team
            result = allocate_patrol_csp(csp, assignment)
            if result is not None:
                return result
            del assignment[zone]

    return None