Data

`ipoh_map.json` is a simulated urban pedestrian map of Ipoh City Center (Old Town and New Town) used by the SafeRoute.AI prototype. All coordinates, distances, and safety attributes are fabricated for academic and modeling purposes, so no ethical clearance or anonymisation of real individuals is required.

Each node records:

- `x`, `y` — relative 2D Cartesian coordinates used for calculating Euclidean distance heuristics $h(n)$
- `is_safe_haven` — boolean flag indicating whether the location serves as an emergency shelter or designated safe point (e.g., police station, hospital)

Each edge records:

- `distance_meters` — approximate walking distance in metres
- `safety_score` — historical/perceived street safety index (0.0 to 100.0)
- `lighting_level` — street lighting quality scale (1 to 5)
- `has_cctv` — presence of active surveillance/CCTV coverage (true / false)
- `wheelchair_accessible` — whether the path segment can be navigated by wheelchair users (true / false)
- `surface` — road surface type (e.g., paved / cobblestone / brick_walkway)
