
# Tests

The test suite validates data preprocessing, pathfinding search algorithms, and CSP constraint handling. Tests are executed using Python's built-in `unittest` framework.

### How to Run Tests

```bash
python3 -m unittest discover -s tests
```

---

### Test Cases Summary

| Test ID         | Module            | Purpose                                                                               | Expected Outcome                                                              | Actual Outcome                                                                                   | Status         |
| --------------- | ----------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------- |
| **TC-01** | `cost.py`       | Validate IoT telemetry cleaning for out-of-bound values & NaNs.                       | All`safety_score` values normalized between `[0, 100]`, zero NaNs remain. | All out-of-bound inputs imputed via median imputation; 0 NaNs detected.                          | **PASS** |
| **TC-02** | `algorithms.py` | Verify A* search finds the safest path prioritizing safety scores over pure distance. | Route selected:`A -> C -> D -> F -> J` with optimal risk cost (`3523.5`). | Route returned:`A -> C -> D -> F -> J`, risk cost = `3523.5`.                                | **PASS** |
| **TC-03** | `algorithms.py` | Verify CSP patrol assignment prevents adjacent sector team conflicts.                 | Valid assignment with no two adjacent sectors sharing the same patrol team.   | Assignments:`Concubine_Lane` = Alpha, `Gerbang_Malam` = Bravo, `Kinta_Riverfront` = Alpha. | **PASS** |

---

### Detailed Test Cases

#### Test Case 1: IoT Telemetry Hygiene Pipeline (`test_01_telemetry_data_hygiene`)

* **Objective:** Ensure corrupted sensor data (out-of-bounds safety scores like `150.0` or `-10.0`, missing lighting values) are properly sanitized before graph loading.
* **Input Data:**

```python
safety_score: [85.0, 150.0, NaN, 60.0, -10.0]
lighting_level: [5.0, 4.0, 10.0, NaN, 2.0]
```

* **Expected Outcome:** Scores restricted to range `[0.0, 100.0]`, lighting levels restricted to `[0, 5]`, and missing entries replaced using median imputation.
* **Actual Outcome:** Clean DataFrame returned with `safety_score` values equal to `[85.0, 72.5, 72.5, 60.0, 72.5]`. Zero NaNs remain.
* **Result:** **PASS**

---

#### Test Case 2: A* Search vs. Shortest Path Strategy (`test_02_astar_pathfinding`)

* **Objective:** Ensure A* Search penalizes dark/unsafe edges and picks a high-safety alternative.
* **Input Nodes:** Origin = `ipoh_railway_station (A)`, Destination = `hospital_bainun (J)`.
* **Expected Outcome:** The algorithm avoids unlit route segment `A -> B -> D` and instead routes through `A -> C -> D` (Police Headquarters) to minimize overall path risk.
* **Actual Outcome:** Path generated: `A -> C -> D -> F -> J` with a path risk cost of `3523.5`.
* **Result:** **PASS**

---

#### Test Case 3: Emergency Patrol Escort CSP Allocation (`test_03_csp_patrol_allocation`)

* **Objective:** Verify backtracking CSP solver allocates patrol teams to sectors using the Minimum Remaining Values (MRV) heuristic without team overlaps between adjacent sectors.
* **Input Constraints:** Adjacency constraints between Concubine Lane, Gerbang Malam, and Kinta Riverfront sectors.
* **Expected Outcome:** A valid assignment mapping where `Assignment[Sector_U] != Assignment[Sector_V]` for all adjacent sectors.
* **Actual Outcome:** Assignment dictionary produced:
* `Concubine_Lane_Sector`: Alpha_Team
* `Gerbang_Malam_Sector`: Bravo_Team
* `Kinta_Riverfront_Sector`: Alpha_Team
* **Result:** **PASS**
