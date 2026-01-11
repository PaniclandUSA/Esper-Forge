"""src.dignity.metric

Dignity metric functions (normative v0.1).

This module implements the metric and distances defined in:
- docs/09-DIGNITY-METRIC-v0.1.md

Key functions:
- :func:`d_total` (Section 5.1)
- :func:`d_degrade` (Section 5.2)
- :func:`path_energy` (Section 6.1)
- :func:`geodesic_likeness` (Section 6.3)
- :func:`loop_defect` (Section 7)

Notes
-----
* The metric is block-diagonal and diagonal within each block in v0.1.
* Contracts may override weights; certificates MUST record active weights.
* This module only measures drift/harm; it does not authorize "collapse".

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np

from .state import DignityState13


# Canonical v0.1 diagonal weights, in locked coordinate order.
# (Φ1, Φ2, Φ3, Φ4, A_perp, A_victim, A_vol, T_topo, T_causal,
#  C_dialect, C_idiom, M_entity, M_rel)
DEFAULT_WEIGHT_DIAG: np.ndarray = np.array(
    [
        3.0,
        1.0,
        2.0,
        1.0,
        4.0,
        4.0,
        3.0,
        3.0,
        3.0,
        2.0,
        2.0,
        4.0,
        3.0,
    ],
    dtype=np.float64,
)


@dataclass(frozen=True)
class MetricWeightsV01:
    """Typed weight container (v0.1).

    This is a convenience wrapper; the normative requirement is that the
    resulting diagonal weight vector matches the locked coordinate ordering.
    """

    Phi: Tuple[float, float, float, float] = (3.0, 1.0, 2.0, 1.0)
    A: Tuple[float, float, float] = (4.0, 4.0, 3.0)
    T: Tuple[float, float] = (3.0, 3.0)
    C: Tuple[float, float] = (2.0, 2.0)
    M: Tuple[float, float] = (4.0, 3.0)

    def as_diag(self) -> np.ndarray:
        """Return the canonical 13-length diagonal vector in spec order."""

        diag = np.array(
            [
                *self.Phi,
                *self.A,
                *self.T,
                *self.C,
                *self.M,
            ],
            dtype=np.float64,
        )
        if diag.shape != (13,):
            raise ValueError("MetricWeightsV01 must produce a 13-length diag")
        return diag


def _weights_to_diag(
    weights: Optional[Mapping[str, Sequence[float]]] = None,
) -> np.ndarray:
    """Normalize user-provided weights into a 13-length diagonal array.

    Parameters
    ----------
    weights:
        Optional mapping with keys "Phi", "A", "T", "C", "M".
        If omitted, defaults are used.

    Returns
    -------
    numpy.ndarray
        Shape (13,) float64 diagonal weights in locked coordinate order.

    Raises
    ------
    ValueError
        If provided weights are malformed.
    """

    if weights is None:
        return DEFAULT_WEIGHT_DIAG.copy()

    required = {
        "Phi": 4,
        "A": 3,
        "T": 2,
        "C": 2,
        "M": 2,
    }

    diag_parts: List[float] = []
    for key, n in required.items():
        if key not in weights:
            raise ValueError(f"weights missing required key: {key}")
        vals = list(weights[key])
        if len(vals) != n:
            raise ValueError(f"weights[{key}] must have length {n}, got {len(vals)}")
        diag_parts.extend(float(v) for v in vals)

    diag = np.array(diag_parts, dtype=np.float64)
    if diag.shape != (13,):
        raise ValueError("weights must yield a 13-length diagonal")
    if np.any(diag <= 0):
        raise ValueError("all metric weights must be positive")
    return diag


def create_metric_tensor(
    weights: Optional[Mapping[str, Sequence[float]]] = None,
) -> np.ndarray:
    """Create the 13×13 metric tensor *g* for v0.1.

    In v0.1, g is diagonal (block-diagonal with diagonal blocks).

    Parameters
    ----------
    weights:
        Optional mapping with keys "Phi", "A", "T", "C", "M".

    Returns
    -------
    numpy.ndarray
        13×13 diagonal matrix.
    """

    diag = _weights_to_diag(weights)
    return np.diag(diag)


def d_total(
    x: DignityState13,
    y: DignityState13,
    weights: Optional[Mapping[str, Sequence[float]]] = None,
) -> float:
    """Compute symmetric total movement distance d_total(x, y).

    Spec: Section 5.1
        d_total(x,y) = sqrt( (x-y)^T g (x-y) )

    Parameters
    ----------
    x, y:
        Dignity states.
    weights:
        Optional contract weights.

    Returns
    -------
    float
        Non-negative distance.
    """

    v = x.diff(y)
    diag = _weights_to_diag(weights)
    # Since g is diagonal: v^T g v = sum_i (w_i * v_i^2)
    d2 = float(np.dot(diag, v * v))
    return float(np.sqrt(max(d2, 0.0)))


def d_degrade(
    reference: DignityState13,
    transformed: DignityState13,
    weights: Optional[Mapping[str, Sequence[float]]] = None,
) -> float:
    """Compute asymmetric degradation-only distance d_degrade(reference, transformed).

    Spec: Section 5.2

    Interpretation:
    - Φ coordinates: symmetric drift (movement in either direction has cost)
    - Integrity coords (A,T,C,M): penalize only LOSS (reference - transformed),
      improvements are clamped to 0.

    Parameters
    ----------
    reference:
        Original state x.
    transformed:
        Transformed state y.
    weights:
        Optional contract weights.

    Returns
    -------
    float
        Non-negative degradation distance.
    """

    delta_minus = reference.degrade(transformed)
    diag = _weights_to_diag(weights)
    d2 = float(np.dot(diag, delta_minus * delta_minus))
    return float(np.sqrt(max(d2, 0.0)))


def path_energy(
    path: Sequence[DignityState13],
    weights: Optional[Mapping[str, Sequence[float]]] = None,
) -> float:
    """Compute discrete path energy E(γ).

    Spec: Section 6.1
        E(γ) = sum_{k=0}^{n-1} d_total(x_k, x_{k+1})^2

    Parameters
    ----------
    path:
        Sequence of >= 2 states.
    weights:
        Optional contract weights.

    Returns
    -------
    float
        Non-negative energy.

    Raises
    ------
    ValueError
        If path has fewer than 2 states.
    """

    if len(path) < 2:
        raise ValueError("path must contain at least 2 states")

    diag = _weights_to_diag(weights)
    energy = 0.0
    for a, b in zip(path[:-1], path[1:]):
        v = a.diff(b)
        energy += float(np.dot(diag, v * v))
    return float(max(energy, 0.0))


def _linear_interpolants(
    start: DignityState13,
    end: DignityState13,
    n_segments: int,
) -> List[np.ndarray]:
    """Return vectors for a linear baseline path with n_segments.

    Returns n_segments+1 vectors including endpoints.
    """

    if n_segments < 1:
        raise ValueError("n_segments must be >= 1")

    x0 = start.as_vector()
    xn = end.as_vector()
    vecs: List[np.ndarray] = []
    for k in range(n_segments + 1):
        alpha = k / n_segments
        vecs.append((1.0 - alpha) * x0 + alpha * xn)
    return vecs


def _energy_on_vectors(vecs: Sequence[np.ndarray], diag: np.ndarray) -> float:
    if len(vecs) < 2:
        raise ValueError("need at least 2 vectors")
    energy = 0.0
    for a, b in zip(vecs[:-1], vecs[1:]):
        v = a - b
        energy += float(np.dot(diag, v * v))
    return float(max(energy, 0.0))


def geodesic_likeness(
    path: Sequence[DignityState13],
    weights: Optional[Mapping[str, Sequence[float]]] = None,
) -> float:
    """Compute geodesic-likeness score G(γ) for a discrete path.

    Spec: Section 6.3
        G(γ) = E_lin / E_actual  in (0, 1]

    Where E_lin is the energy of a linear interpolation baseline between x_0 and x_n
    sampled into the same number of segments as the provided path.

    Parameters
    ----------
    path:
        Sequence of >= 2 states.
    weights:
        Optional contract weights.

    Returns
    -------
    float
        Score in (0, 1], where values near 1 indicate near-geodesic.

    Notes
    -----
    If E_actual == 0 (identical states), returns 1.0.
    """

    if len(path) < 2:
        raise ValueError("path must contain at least 2 states")

    diag = _weights_to_diag(weights)

    e_actual = path_energy(path, weights=weights)
    if e_actual <= 0.0:
        return 1.0

    n_segments = len(path) - 1
    lin_vecs = _linear_interpolants(path[0], path[-1], n_segments=n_segments)
    e_lin = _energy_on_vectors(lin_vecs, diag)

    # Ratio should be <= 1 if the path is at least as efficient as linear.
    # Floating tolerances can push slightly above 1; clamp.
    g_score = float(e_lin / e_actual)
    return float(min(max(g_score, 0.0), 1.0))


def loop_defect(
    loop_states: Sequence[DignityState13],
    weights: Optional[Mapping[str, Sequence[float]]] = None,
) -> float:
    """Compute loop defect Δ_loop for bias/curvature signal (v0.1).

    Spec: Section 7

    In v0.1 we report the degradation-only distance between the loop start and end.

    Parameters
    ----------
    loop_states:
        A sequence containing at least [x0, ..., x_end].
        Conventionally x_end is x_4 in the spec loop, but this function accepts
        any length >= 2 and compares first to last.
    weights:
        Optional contract weights.

    Returns
    -------
    float
        Non-negative loop defect.
    """

    if len(loop_states) < 2:
        raise ValueError("loop_states must contain at least 2 states")
    x0 = loop_states[0]
    x_end = loop_states[-1]
    return d_degrade(x0, x_end, weights=weights)
