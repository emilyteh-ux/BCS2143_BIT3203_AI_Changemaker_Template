# PEAS and Formal AI Problem Formulation

## PEAS
- **Performance Measure:** Maximize route safety while keeping walking distance reasonably low.

- **Environment:** City street network modeled as a graph — intersections as nodes, streets as edges, each tagged with lighting, foot traffic, and risk level.

- **Actuators:** Route (sequence of nodes), turn-by-turn directions, and a safety breakdown of the path.

- **Sensors:** Start/end location, user's safety preference, and the road graph data.

## State or variables
A state is the current intersection (node) the pedestrian is at.

## Initial state
The user's chosen starting intersection.

## Actions or domains
Move to any intersection directly connected by a street segment (edge) from the current node.

## Transition model or constraints
Taking an action moves the pedestrian from the current node to the connected node along that edge. Only edges that exist in the graph are valid moves.

## Goal test
Current node equals the user's chosen destination intersection.

## Path cost
g(n) = cumulative distance + weighted safety risk penalty (based on lighting and foot traffic) across all traversed edges.

## Heuristic, where applicable
h(n) = straight-line (Euclidean) distance from the current node to the destination node.