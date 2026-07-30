# Results

Store sample outputs, figures, metrics and test evidence here.

=== Scenario 1: Small grid (isolated shortcut vs lit loop) ===
Baseline (shortest path):
  Path: A -> B -> C
  Distance: 200.0 m | Risk score: 1.68 | Nodes expanded: 3

Safety-optimized:
  Path: A -> D -> E -> F -> C
  Distance: 400.0 m | Risk score: 0.64 | Nodes expanded: 6
  --> Extra distance: 200.0 m | Risk reduced by: 1.04

=== Scenario 2: Dense network with risky shortcut ===
Baseline (shortest path):
  Path: A -> B -> C -> D
  Distance: 270.0 m | Risk score: 1.82 | Nodes expanded: 4

Safety-optimized:
  Path: A -> E -> F -> G -> D
  Distance: 470.0 m | Risk score: 0.74 | Nodes expanded: 7
  --> Extra distance: 200.0 m | Risk reduced by: 1.08

=== Scenario 3: Campus commute (dark shortcut vs lit main road) ===
Baseline (shortest path):
  Path: A -> F -> G -> H -> E
  Distance: 240.0 m | Risk score: 3.06 | Nodes expanded: 6
  
Safety-optimized:
  Path: A -> B -> C -> D -> E
  Distance: 280.0 m | Risk score: 1.66 | Nodes expanded: 7
  --> Extra distance: 40.0 m | Risk reduced by: 1.40