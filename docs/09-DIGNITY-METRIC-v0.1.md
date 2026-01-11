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

For integrity coordinates (A,T,C,M) we define degradation componentwise:

\[
\Delta^- = \max(0, x - y)
\]

For Φ coordinates we retain symmetric difference.

Then:

\[
d_{\text{degrade}}(x,y)=\sqrt{(\Delta^-)^T g (\Delta^-)}
\]

This measures dignity harm risk specifically.

Implementations SHOULD compute both.

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

Metrics quantify drift; gates enforce “must never happen.”

A contract MAY specify minimum integrity thresholds:

- A_* ≥ A_min
- T_* ≥ T_min
- C_* ≥ C_min
- M_* ≥ M_min

If any required coordinate violates its gate, the transformation FAILS CERTIFICATION.

Distance computations SHOULD still be recorded for diagnostics.

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

---

## 10. Reference implementation signatures (non-normative)

Suggested API surface:

- `extract_dignity_state(artifact) -> DignityState13`
- `d_total(x,y,weights) -> float`
- `d_degrade(x,y,weights) -> float`
- `path_energy(path,weights) -> float`
- `geodesic_likeness(path,weights) -> float`
- `check_gates(state, contract) -> GateReport`
