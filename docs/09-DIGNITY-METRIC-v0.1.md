# Dignity Metric v0.1 (Implementable Spec)

**Status:** normative v0.1  
**Purpose:** provide a concrete, code-able metric for measuring dignity drift across transformations.  
**Scope:** literacy-leveling, summarization, translation, and other controlled transformations where the Dignity Manifold applies.  
**Non-goal:** this metric does **not** declare truth, guilt, or final judgment. Collapse remains human-only.

---

## 0. Dependencies

This spec assumes the axioms and constraints defined in:

- `01-DIGNITY-MANIFOLD.md`
- `02-COLLAPSE-CRITERION.md`
- `05-LITERACY-DEMO.md`

---

## 1. Dignity state space

We define a first-pass dignity manifold as a product space:

\[
\mathcal{M}_{\text{dignity}} \subset \mathbb{R}^{13}
\]

A narrative/story state is a vector:

\[
x = (\Phi, A, T, C, M)
\]

### 1.1 Coordinate ordering (MUST)

The canonical coordinate order for v0.1 is:

1. \Phi_1, \Phi_2, \Phi_3, \Phi_4  
2. A_perp, A_victim, A_vol  
3. T_topo, T_causal  
4. C_dialect, C_idiom  
5. M_entity, M_rel

Any implementation MUST preserve this order.

### 1.2 Dimension (MUST)

The dignity manifold has exactly **13 dimensions**:
- Φ: 4 dimensions
- A: 3 dimensions
- T: 2 dimensions
- C: 2 dimensions
- M: 2 dimensions

Total: d = 13

This dimension is **locked** for v0.1. Any change constitutes a breaking version increment.

---

## 2. Coordinate definitions and ranges

### 2.1 Emotional core block  \Phi ∈ R^4  (axes)

Each coordinate is in [-1, 1]:

- \Phi_1: polarity (warm ↔ cool)
- \Phi_2: direction (dreaming ↔ declaring)
- \Phi_3: stance (together ↔ apart)
- \Phi_4: confidence (wondering ↔ certain)

\[
\Phi = (\Phi_1,\Phi_2,\Phi_3,\Phi_4)
\]

### 2.2 Agency block  A ∈ [0,1]^3  (integrity scores)

Story-level aggregates:

- A_perp: perpetrator agency stability across levels
- A_victim: recipient/victim role stability across levels
- A_vol: voluntary/forced label stability across levels

\[
A=(A_{\text{perp}}, A_{\text{victim}}, A_{\text{vol}})
\]

### 2.3 Temporal block  T ∈ [0,1]^2  (integrity scores)

- T_topo: topological preservation score (DAG order similarity)
- T_causal: ChronoCore causal alignment score (no paradox/inversion)

\[
T=(T_{\text{topo}}, T_{\text{causal}})
\]

### 2.4 Cultural block  C ∈ [0,1]^2  (integrity scores)

- C_dialect: dialect preservation score
- C_idiom: idiom retention score

\[
C=(C_{\text{dialect}}, C_{\text{idiom}})
\]

### 2.5 Material identity block  M ∈ [0,1]^2  (integrity scores)

- M_entity: fraction of entities preserved
- M_rel: fraction of relationships preserved

\[
M=(M_{\text{entity}}, M_{\text{rel}})
\]

---

## 3. Normalization requirements

Upstream components MAY output raw values.
Before metric evaluation, implementations MUST normalize:

- Φ axes into [-1, 1]
- A, T, C, M into [0, 1] where higher = better preservation

If a coordinate cannot be reliably measured, the implementation MUST:
1) mark it as `unknown`, and  
2) exclude it from metric distance while recording the omission in the certificate.

---

## 4. Metric g^(0.1)

We define a block-diagonal, positive definite metric:

\[
g =
\begin{pmatrix}
W_\Phi & 0 & 0 & 0 & 0 \\
0 & W_A & 0 & 0 & 0 \\
0 & 0 & W_T & 0 & 0 \\
0 & 0 & 0 & W_C & 0 \\
0 & 0 & 0 & 0 & W_M
\end{pmatrix}
\]

Each block is diagonal:

- W_Φ = diag(w_{Φ1}, w_{Φ2}, w_{Φ3}, w_{Φ4})
- W_A = diag(w_{Aperp}, w_{Avictim}, w_{Avol})
- W_T = diag(w_{Ttopo}, w_{Tcausal})
- W_C = diag(w_{Cdialect}, w_{Cidiom})
- W_M = diag(w_{Mentity}, w_{Mrel})

### 4.1 Default weights (v0.1)

Defaults reflect “catastrophic dignity failure” priorities:

**Φ:**
- w_{Φ1}=3.0
- w_{Φ2}=1.0
- w_{Φ3}=2.0
- w_{Φ4}=1.0

**A:**
- w_{Aperp}=4.0
- w_{Avictim}=4.0
- w_{Avol}=3.0

**T:**
- w_{Ttopo}=3.0
- w_{Tcausal}=3.0

**C:**
- w_{Cdialect}=2.0
- w_{Cidiom}=2.0

**M:**
- w_{Mentity}=4.0
- w_{Mrel}=3.0

Contracts MAY override weights; certificates MUST record the active weights.

---

## 5. Distance definitions

Let v = x − y.

### 5.1 Total movement distance (symmetric)

\[
d_{\text{total}}(x,y)=\sqrt{(x-y)^T g (x-y)}
\]

This measures total movement in dignity space.

### 5.2 Degradation-only distance (integrity harm)

For **integrity coordinates** (A, T, C, M), we define degradation componentwise:

\[
\Delta^- = \max(0, x - y)
\]

**Interpretation**: 
- Positive values = loss of integrity (harm)
- Negative values = improvement (clamped to 0, not penalized)

For **Φ coordinates** (emotional axes), we retain **symmetric difference**:

\[
\Delta^- = x - y
\]

**Interpretation**: Emotional drift is drift—movement in either direction has dignity cost.

Then:

\[
d_{\text{degrade}}(x,y)=\sqrt{(\Delta^-)^T g (\Delta^-)}
\]

This measures **dignity harm risk** specifically, allowing improvements without penalty.

Implementations SHOULD compute both d_total and d_degrade.
```

---

## 6. Discrete geodesic path test (v0.1)

Given a path γ = (x_0, x_1, ..., x_n):

### 6.1 Path energy

\[
E(\gamma)=\sum_{k=0}^{n-1} d_{\text{total}}(x_k,x_{k+1})^2
\]

### 6.2 Linear baseline

Define:

\[
x^{lin}_k = x_0 + \frac{k}{n}(x_n-x_0)
\]

\[
E_{lin} = \sum_{k=0}^{n-1} d_{\text{total}}(x^{lin}_k,x^{lin}_{k+1})^2
\]

### 6.3 Geodesic-likeness

\[
G(\gamma)=\frac{E_{lin}}{E(\gamma)} \in (0,1]
\]

Near 1 means “near-geodesic” (low extra dignity cost).

---

## 7. Bias/curvature signal (loop defect, v0.1)

To approximate curvature, construct a loop that should cancel:

\[
x_0 \xrightarrow{f} x_1 \xrightarrow{h} x_2 \xrightarrow{f^{-1}} x_3 \xrightarrow{h^{-1}} x_4
\]

Loop defect:

\[
\Delta_{loop} = d_{\text{degrade}}(x_0,x_4)
\]

Systematic differences in Δ_loop across cohorts is an actionable structural bias signal.

---

## 8. Compile gates (hard failures)

Metrics quantify drift; gates enforce **"must never happen"**.

### 8.1 Gate specification

A contract MAY specify minimum integrity thresholds:

- `A_perp ≥ A_min` (default: 0.95)
- `A_victim ≥ A_min` (default: 0.95)
- `A_vol ≥ A_min` (default: 0.90)
- `T_topo ≥ T_min` (default: 0.95)
- `T_causal = 1.0` (or ≥ 0.99 for probabilistic systems)
- `C_dialect ≥ C_min` (default: 0.80)
- `C_idiom ≥ C_min` (default: 0.80)
- `M_entity ≥ M_min` (default: 0.95)
- `M_rel ≥ M_min` (default: 0.90)

### 8.2 Enforcement

If **any** required coordinate violates its gate:
1. Transformation **FAILS CERTIFICATION**
2. Distance computations **SHOULD still be recorded** for diagnostics
3. Certificate **MUST document** which gate(s) failed

### 8.3 Philosophy

Gates are **constitutional boundaries**, not optimization targets.

**Refuse to compile** is the correct response, not "warn and proceed."

---

## 9. Certificate fields (required)

Certificates validating this metric MUST include:

- active weights
- d_total per stage
- d_degrade per stage
- path energy and geodesic-likeness
- loop defects if computed
- any unknown/omitted coordinates
- any gate failures with coordinate names and values

Example object name:

`dignity_metric_v0_1`

## 9. Certificate fields (required)

### 9.1 Required fields

Certificates validating this metric MUST include:

- `active_weights`: Weight vector used for metric computation
- `d_total_per_stage`: Total distance for each transformation step
- `d_degrade_per_stage`: Degradation distance for each step
- `path_energy`: E(γ) for the complete transformation path
- `geodesic_likeness`: G(γ) score
- `loop_defects`: Array of loop defect measurements (if computed)
- `unknown_coordinates`: List of coordinates that could not be measured
- `gate_violations`: Array of gate failures (if any)

### 9.2 Schema example
```json
{
  "dignity_metric_v0_1": {
    "dimension": 13,
    "active_weights": {
      "Phi": [3.0, 1.0, 2.0, 1.0],
      "A": [4.0, 4.0, 3.0],
      "T": [3.0, 3.0],
      "C": [2.0, 2.0],
      "M": [4.0, 3.0]
    },
    "distances": {
      "spoken_to_grade_1": {
        "d_total": 0.12,
        "d_degrade": 0.08
      },
      "grade_1_to_grade_5": {
        "d_total": 0.09,
        "d_degrade": 0.05
      },
      "grade_5_to_grade_12": {
        "d_total": 0.11,
        "d_degrade": 0.07
      },
      "spoken_to_grade_12": {
        "d_total": 0.19,
        "d_degrade": 0.15
      }
    },
    "path_energy": {
      "actual": 0.0346,
      "linear": 0.0361,
      "ratio": 0.958
    },
    "geodesic_likeness": 0.958,
    "loop_defects": [
      {
        "loop_type": "dialect_norm_complexity_cycle",
        "delta": 0.04,
        "cohort": "AAVE_speakers"
      }
    ],
    "gate_violations": [],
    "unknown_coordinates": []
  }
}
```

---

## 10. Reference implementation signatures (non-normative)

Suggested API surface:

- `extract_dignity_state(artifact) -> DignityState13`
- `d_total(x,y,weights) -> float`
- `d_degrade(x,y,weights) -> float`
- `path_energy(path,weights) -> float`
- `geodesic_likeness(path,weights) -> float`
- `check_gates(state, contract) -> GateReport`

---

## 11. Python implementation (normative reference)

The canonical Python implementation of this metric is the `DignityState13` class.

### 11.1 Class definition
```python
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class DignityState13:
    """
    Normative implementation of Dignity State Space (v0.1).
    
    Immutable atomic unit for ESPER-FORGE certification.
    Coordinates MUST match Section 1.1 ordering.
    """
    
    # Emotional Core [-1, 1]
    phi_polarity: float      # warm ↔ cool
    phi_direction: float     # dreaming ↔ declaring
    phi_stance: float        # together ↔ apart
    phi_confidence: float    # wondering ↔ certain
    
    # Agency [0, 1]
    a_perp: float           # Perpetrator stability
    a_victim: float         # Victim stability
    a_vol: float            # Voluntariness stability
    
    # Temporal [0, 1]
    t_topo: float           # Topological preservation
    t_causal: float         # Causal alignment
    
    # Cultural [0, 1]
    c_dialect: float        # Dialect preservation
    c_idiom: float          # Idiom retention
    
    # Material [0, 1]
    m_entity: float         # Entity preservation
    m_rel: float            # Relationship preservation
    
    def as_vector(self) -> np.ndarray:
        """Returns the 13-dimensional state vector x."""
        return np.array([
            self.phi_polarity, self.phi_direction, 
            self.phi_stance, self.phi_confidence,
            self.a_perp, self.a_victim, self.a_vol,
            self.t_topo, self.t_causal,
            self.c_dialect, self.c_idiom,
            self.m_entity, self.m_rel
        ], dtype=np.float64)
    
    def diff(self, other: 'DignityState13') -> np.ndarray:
        """
        Computes signed displacement vector v = self - other.
        
        Args:
            other: The state to compare against.
            
        Returns:
            np.ndarray: The displacement vector.
        """
        return self.as_vector() - other.as_vector()
    
    def degrade(self, other: 'DignityState13') -> np.ndarray:
        """
        Computes the asymmetric degradation vector Δ⁻ per Spec 5.2.
        
        Interprets 'self' as the Reference (Original) state and 'other'
        as the Transformed state.
        
        Logic:
        - Φ coordinates: Retain symmetric difference (drift is drift).
        - Integrity coordinates (A, T, C, M): max(0, Reference - Transformed).
          Positive values indicate LOSS of integrity.
          Negative values (improvements) are clamped to 0.
        
        Returns:
            np.ndarray: The degradation vector suitable for quadratic form metric.
        """
        displacement = self.diff(other)
        delta_minus = np.zeros_like(displacement)
        
        # Φ: retain symmetric difference
        delta_minus[0:4] = displacement[0:4]
        
        # A, T, C, M: one-sided (penalize loss only)
        delta_minus[4:13] = np.maximum(0.0, displacement[4:13])
        
        return delta_minus
```

### 11.2 Normative status

This class is **normative** for v0.1:
- Coordinate ordering MUST match Section 1.1
- Field names are canonical
- `@dataclass(frozen=True)` ensures immutability
- `degrade()` semantics are normative for asymmetric distance

Any implementation in any language MUST preserve these semantics.

---

## 12. Worked example (non-normative)

### 12.1 Setup
```python
import numpy as np

# Metric tensor diagonal (Section 4.1 defaults)
W_diag = np.array([
    3.0, 1.0, 2.0, 1.0,  # Φ
    4.0, 4.0, 3.0,        # A
    3.0, 3.0,             # T
    2.0, 2.0,             # C
    4.0, 3.0              # M
])
G_metric = np.diag(W_diag)

# Reference state (spoken narrative)
ref = DignityState13(
    phi_polarity=0.8, phi_direction=0.5, 
    phi_stance=0.9, phi_confidence=0.9,
    a_perp=1.0, a_victim=1.0, a_vol=1.0,
    t_topo=1.0, t_causal=1.0,
    c_dialect=1.0, c_idiom=1.0,
    m_entity=1.0, m_rel=1.0
)

# Transformed state (Grade 5 rendering)
trans = DignityState13(
    phi_polarity=0.7, phi_direction=0.5,      # Slight emotional drift
    phi_stance=0.9, phi_confidence=0.9,
    a_perp=0.9, a_victim=1.0, a_vol=1.0,      # Loss in perp agency
    t_topo=1.0, t_causal=1.0,
    c_dialect=0.8, c_idiom=1.0,                # Dialect loss
    m_entity=1.0, m_rel=1.0
)
```

### 12.2 Distance computation
```python
# Asymmetric degradation distance
delta_minus = ref.degrade(trans)
d_degrade_squared = delta_minus.T @ G_metric @ delta_minus
d_degrade = np.sqrt(d_degrade_squared)

print(f"Dignity Degradation Score: {d_degrade:.4f}")
# Output: Dignity Degradation Score: 0.3873

```

### 12.3 Interpretation

The degradation score of 0.73 indicates:
- **Φ contribution**: 0.3 (polarity drift from 0.8 → 0.7)
- **A contribution**: 0.4 (agency loss from 1.0 → 0.9, weight 4.0)
- **C contribution**: 0.4 (dialect loss from 1.0 → 0.8, weight 2.0)

**Verdict**: Transformation preserves core dignity (< 1.0 threshold) but shows measurable loss in agency and cultural authenticity.

**Action**: Certificate would include these distances; human tutor confirms with learner.
