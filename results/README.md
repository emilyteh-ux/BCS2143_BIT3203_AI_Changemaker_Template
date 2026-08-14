
# Results

### Node Alias Legend

> `A`: Ipoh Railway Station | `B`: Birch Clock Tower | `C`: Central Police Station | `D`: Concubine Lane | `E`: Padang Ipoh | `F`: Kinta Riverfront | `G`: Gerbang Malam | `H`: Yau Tet Shin | `I`: Greentown Center | `J`: Hospital Bainun

---

### === Scenario 1: Ipoh Railway Station (A) to Hospital Bainun (J) ===

**Baseline (shortest path):**

* **Path:** `A -> B -> D -> F -> J`
* **Metrics:** Distance: 1830.0 m | Risk score: 1.93 | Nodes expanded: 9

**Safety-optimized:**

* **Path:** `A -> C -> D -> F -> J`
* **Metrics:** Distance: 2100.0 m | Risk score: 1.68 | Nodes expanded: 10
* **Trade-off:** Extra distance: +270.0 m | Risk reduced by: -0.25

---

### === Scenario 2: Ipoh Railway Station (A) to Yau Tet Shin District (H) ===

**Baseline (shortest path):**

* **Path:** `A -> B -> D -> F -> H`
* **Metrics:** Distance: 1410.0 m | Risk score: 2.10 | Nodes expanded: 8

**Safety-optimized:**

* **Path:** `A -> C -> D -> G -> H`
* **Metrics:** Distance: 1700.0 m | Risk score: 1.18 | Nodes expanded: 8
* **Trade-off:** Extra distance: +290.0 m | Risk reduced by: -0.92

---

### === Scenario 3: Birch Clock Tower (B) to Greentown Business Centre (I) ===

**Baseline (shortest path):**

* **Path:** `B -> D -> F -> H -> I`
* **Metrics:** Distance: 1960.0 m | Risk score: 1.95 | Nodes expanded: 10

**Safety-optimized:**

* **Path:** `B -> D -> G -> H -> I`
* **Metrics:** Distance: 1980.0 m | Risk score: 1.46 | Nodes expanded: 9
* **Trade-off:** Extra distance: +20.0 m | Risk reduced by: -0.49
