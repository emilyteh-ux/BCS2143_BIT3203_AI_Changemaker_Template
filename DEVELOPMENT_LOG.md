
# Development Log

Record substantive decisions, implementation progress, testing and debugging. Do not list trivial file saves.

## 24 July 2026 — Concept checkpoint

* **Problem and target users:** Nighttime pedestrian safety in urban areas like Ipoh City Center. Target users include evening commuters, tourists walking around night districts (e.g., Concubine Lane, Gerbang Malam), and students navigating between transit hubs and commercial centers.
* **Evidence and social value:** Pedestrians often default to standard shortest-path navigation apps that route through unlit alleys, areas lacking CCTV, or low-foot-traffic streets. SafeRoute.AI balances physical distance with path safety metrics, improving urban walkability and personal safety.
* **Draft PEAS:**
  * **Performance Measure:** Path safety score optimization, distance penalty minimization, computational efficiency (nodes expanded).
  * **Environment:** Ipoh City street network (nodes A–J), ambient lighting levels (0–5), CCTV coverage, safety ratings (0–100).
  * **Actuators:** Optimal safety path rendering, patrol escort allocation output.
  * **Sensors:** Simulated IoT street sensor telemetry, environmental crime/safety telemetry data.
* **Proposed AI method:**
  1. **Graph Search:** Comparison of BFS, DFS, UCS, and A* Search with an admissible Euclidean heuristic and safety risk penalty multiplier.
  2. **CSP Assignment:** Constraint Satisfaction Problem solver using Minimum Remaining Values (MRV) heuristic for non-overlapping emergency patrol escort dispatch.
* **Risks or questions:** Ensuring the heuristic function remains admissible when combined with safety multipliers; handling missing or corrupted IoT sensor data safely.

## 30 July 2026 — Technical checkpoint

* **Formal problem formulation:**
  * **State Space:** Set of spatial graph nodes **$V = \{A, B, \dots, J\}$** representing key Ipoh landmarks.
  * **Step Cost **$g(n)$**:** **$\text{distance} \times \text{risk\_score}(e)$**, where **$\text{risk\_score}$** incorporates safety rating, lighting level, and CCTV presence.
  * **Heuristic **$h(n)$**:** Euclidean straight-line distance between current node **$(x_1, y_1)$** and target destination **$(x_2, y_2)$**.
  * **CSP Formulation:** Variables = Patrol Sectors, Domains = Escort Teams (Alpha, Bravo, Charlie), Constraints = Adjacent sectors cannot share the same patrol team.
* **Working baseline:** Implemented unweighted BFS and pure distance Uniform Cost Search (UCS) as shortest-path baselines.
* **Algorithm or heuristic decisions:**
  * Selected Euclidean distance as **$h(n)$** to maintain admissibility.
  * Structured segment risk formula: **$\text{Risk Multiplier} = 1.0 + \frac{100 - \text{Safety}}{50} + \frac{5 - \text{Lighting}}{5} + \text{CCTV Penalty}$**.
* **Testing completed:** Successfully built and parsed the spatial graph of 10 key nodes and 13 bidirectional edges for Ipoh City Center.
* **Problems found and corrections:** Out-of-bounds sensor readings (**$>100$** safety score or negative values) caused distorted path cost calculations. Resolved by implementing `clean_safety_telemetry()` in `cost.py` using median/mode imputation via `pandas` and `numpy`.

## 12 August 2026 — Readiness checkpoint

* **Three test cases and results:**
  1. **TC-01 (Data Hygiene):** Verified out-of-bounds/missing sensor data cleanups via `clean_safety_telemetry`. **[PASS]**
  2. **TC-02 (A* Optimal Safety Path):* * Verified A* routing from Station (A) to Hospital (J) chooses police station route `A -> C -> D -> F -> J` over dark route `A -> B -> D -> F -> J`. **[PASS]**
  3. **TC-03 (CSP Patrol Allocation):** Verified MRV backtracking solver assigns distinct teams to adjacent sectors with zero constraint violations. **[PASS]**
* **Responsible AI reflection:** Addressed potential neighborhood stigmatization by weighting real-time objective infrastructure metrics (lighting, CCTV) rather than demographic factors. Evaluated user trade-offs between added walking distance (+270m) and overall risk reduction (-0.25 risk score).
* **Limitations:** Static graph representation; current model uses simulated batch telemetry rather than live real-time API feeds.
* **Slides and video status:** Presentation slide deck completed; video demo script structured for algorithm comparison and system execution walk-through.
* **Remaining work:** Final repository cleanup, letter alias formatting for concise terminal output, and final submission tagging.

## 20 August 2026 — Final submission

* **Final commit SHA:** `7f3a9d2`
* **Final tag:** `v1.0.0-final`
* **Summary of final changes:**
  * Cleaned terminal console formatting to use concise node letter aliases (`A -> C -> D -> F -> J`).
  * Finalized full search comparison suite ( **BFS** ,  **DFS** ,  **UCS** ,  **A** *) across 3 real-world Ipoh commute scenarios.
  * Verified automated test suite execution via `python -m unittest discover -s tests`.
  * Completed documentation, slide deck, video recording, and repository distribution package.
