
# SafeRoute.AI Intelligent Agent System

This repository contains the source code and documentation for **SafeRoute.AI**, an AI Changemaker Agent developed for the BCS2143/BIT3203 Artificial Intelligence individual assignment.

---

## Student Information

* **Student Name:** Emily Feriana Danish Teh
* **Student ID:** QIU-202507-008569
* **Programme:** BCS / BIT
* **Course Code:** BCS2143 / BIT3203
* **GitHub Username:** emilyteh-ux

---

## Project Title

**SafeRoute.AI:** Intelligent Safety-Aware Navigation and Emergency Patrol Agent for Urban Pedestrians

---

## Competition-Ready Project Description (150 words max)

Standard navigation tools return the shortest walking path without evaluating street lighting, CCTV coverage, or historical safety, forcing nighttime pedestrians through high-risk urban areas. SafeRoute.AI is an intelligent agent designed for Ipoh City Center that preprocesses raw IoT street telemetry and optimizes pedestrian safety. It calculates a composite path risk cost $g(n)$ and compares uninformed search baselines (BFS, DFS, UCS) against an informed A* search powered by an admissible spatial Euclidean distance heuristic $h(n)$. Additionally, a Constraint Satisfaction Problem (CSP) solver uses the Minimum Remaining Values (MRV) heuristic to assign emergency patrol escorts across high-risk sectors without coverage overlap. Automated unit testing verifies telemetry cleaning, search risk optimality, and CSP constraint enforcement. SafeRoute.AI advances SDG 3, 10, and 11 by empowering pedestrian mobility and protecting vulnerable night commuters.

---

## Problem Summary

> See `docs/problem_statement.md` for the full problem statement, evidence, and SDG alignment.

In short: pedestrians walking at night in urban centers like Ipoh need navigation that minimizes risk exposure rather than just physical distance. Standard maps lack street-level safety awareness, leading to anxiety and unnecessary exposure to crime or poorly lit hazards.

---

## AI Method

The system implements a multi-agent AI framework (see `src/algorithms.py`):

* **Uninformed Baselines:** Breadth-First Search (BFS), Depth-First Search (DFS), and Uniform Cost Search (UCS).
* **Informed Principal Search:** A* Search utilizing an admissible straight-line Euclidean distance heuristic $h(n)$ calculated dynamically from node Cartesian coordinates $(x, y)$.
* **Constraint Optimization Agent:** Backtracking Constraint Satisfaction Problem (CSP) solver using the Minimum Remaining Values (MRV) heuristic to allocate emergency response escorts without adjacent sector overlap.

---

## PEAS Framework

> See `docs/peas_and_formulation.md` for the full problem formulation.

* **Performance Measure:** Minimizes composite path risk cost $g(n)$, minimizes search node expansions, and eliminates adjacent sector patrol assignment overlaps.
* **Environment:** Simulated Ipoh City Center pedestrian graph (`data/ipoh_map.json`).
* **Actuators:** Prints validated telemetry, computed safe routes, total risk cost breakdowns, and patrol team assignments to the console using concise letter aliases.
* **Sensors:** Reads the spatial JSON map dataset and live simulated IoT safety telemetry streams.

---

## Node Aliases Legend

To optimize terminal readability, locations in Ipoh City Center are mapped to short letter aliases:

| Alias       | Node ID                    | Location Name                     |
| ----------- | -------------------------- | --------------------------------- |
| **A** | `ipoh_railway_station`   | Ipoh Railway Station              |
| **B** | `birch_clock_tower`      | Birch Memorial Clock Tower        |
| **C** | `central_police_station` | Ipoh District Police Headquarters |
| **D** | `concubine_lane`         | Concubine Lane                    |
| **E** | `padang_ipoh`            | Padang Ipoh                       |
| **F** | `kinta_riverfront`       | Kinta Riverfront Walk             |
| **G** | `gerbang_malam`          | Gerbang Malam Night Market        |
| **H** | `yau_tet_shin`           | Yau Tet Shin Food District        |
| **I** | `greentown_center`       | Greentown Business Centre         |
| **J** | `hospital_bainun`        | Hospital Raja Permaisuri Bainun   |

---

## Installation

### macOS / Linux

```bash
# 1. Create virtual environment
python3 -m venv .venv

# 2. Activate environment
source .venv/bin/activate

# 3. Upgrade pip and install dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

```

### Windows (PowerShell)

```powershell
# 1. Create virtual environment
py -V:3.13 -m venv .venv

# 2. Activate environment
.\.venv\Scripts\Activate.ps1

# 3. Upgrade pip and install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

```

---

## Running the Prototype

Make sure your virtual environment is activated (`source .venv/bin/activate`), then execute the main intelligence pipeline:

```bash
python3 src/main.py

```

This will run:

1. IoT Safety Telemetry Preprocessing pipeline (imputation and cleaning).
2. Spatial graph initialization and Node Alias Legend display.
3. Route Optimization Engine comparing **BFS**, **DFS**, **UCS**, and **A*** using letter aliases (e.g., `A -> C -> D -> F -> J`).

---

## Testing

Run the automated unit testing suite:

```bash
python3 -m unittest discover -s tests

```

Three core automated test cases are provided in `tests/test_smoke.py`:

1. **`test_01_telemetry_data_hygiene`**: Validates IoT telemetry cleaning, missing value handling, and out-of-bounds value imputation.
2. **`test_02_astar_pathfinding`**: Verifies A* search risk-cost optimality (prioritizes well-lit, CCTV-monitored routes like Police Headquarters `A -> C -> D` over darker routes `A -> B -> D`).
3. **`test_03_csp_patrol_allocation`**: Verifies backtracking CSP patrol assignment enforcement using the MRV heuristic to prevent team overlaps across adjacent sectors.

---

## Repository Structure

```text
BCS2143_BIT3203_AI_Changemaker_Template/
├── data/
│   └── ipoh_map.json            # Ipoh City spatial map dataset & edges
├── docs/
│   ├── peas_and_formulation.md  # PEAS framework and problem formulation
│   ├── problem_statement.md     # Problem statement, evidence & SDG alignment
│   └── responsible_ai.md        # Responsible AI evaluation & trade-offs
├── presentation/
│   └── slides.pptx              # Project presentation deck
├── results/
│   └── test_results.md          # Output logs, metrics, and test evidence
├── src/
│   ├── algorithms.py            # Search algorithms (BFS, DFS, UCS, A*) & CSP
│   ├── cost.py                  # Telemetry cleaning & heuristic cost functions
│   ├── graph.py                 # Graph & CSP data structures
│   └── main.py                  # Main execution entry point
├── tests/
│   └── test_smoke.py            # Automated unittest suite
├── AI_USE_DECLARATION.md        # Compulsory AI-use disclosure statement
├── DEVELOPMENT_LOG.md           # Substantive development decision log
├── requirements.txt             # Python dependencies (numpy, pandas)
└── README.md                    # System documentation

```

---

## Known Limitations

* **Simulated Map & Telemetry:** The Ipoh map and IoT sensor feeds are currently simulated; real-world deployment requires live integration with municipal traffic, CCTV, and street lighting APIs.
* **Static Graph Model:** The current graph models static road segments; real-time dynamic traffic or sudden construction hazards require live stream updating.
* **CLI Interface:** Output is text-based on the terminal console; future iterations should incorporate a mobile screen-reader interface or visual GIS map overlay.

---

## Submission

* **Final Submission Deadline:** 20 August 2026, 5:00 pm
* **Submission Portal:** eQIU (GitHub URL, final commit SHA, and ZIP archive) & Turnitin (Written Report)
