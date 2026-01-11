"""
DignityState13 (normative v0.1)

Atomic, immutable representation of a point in the 13-dimensional
Dignity Manifold defined in:

  docs/09-DIGNITY-METRIC-v0.1.md

This module is NORMATIVE for v0.1:
- Coordinate ordering is locked (Section 1.1).
- Dimension is locked at 13 (Section 1.2).
- Ranges are enforced (Section 2).
- Asymmetric degradation semantics are defined here (Section 5.2).

Non-goals:
- This module does not compute distances (that lives in metric.py).
- This module does not enforce compile gates (that lives in gates.py).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Final, Tuple

import numpy as np


@dataclass(frozen=True, slots=True)
class DignityState13:
    """
    Immutable atomic unit for ESPER-FORGE dignity measurement.

    Coordinate Ordering (MUST; Spec 1.1):
      0-3   : Φ (Emotional Core)   [phi_polarity, phi_direction, phi_stance, phi_confidence]
      4-6   : A (Agency)          [a_perp, a_victim, a_vol]
      7-8   : T (Temporal/Causal) [t_topo, t_causal]
      9-10  : C (Cultural)        [c_dialect, c_idiom]
      11-12 : M (Material)        [m_entity, m_rel]
    """

    # --- 1) Emotional Core Φ ∈ [-1, 1]^4 ---
    phi_polarity: float      # warm ↔ cool
    phi_direction: float     # dreaming ↔ declaring
    phi_stance: float        # together ↔ apart
    phi_confidence: float    # wondering ↔ certain

    # --- 2) Agency A ∈ [0, 1]^3 ---
    a_perp: float            # perpetrator agency stability
    a_victim: float          # victim/recipient role stability
    a_vol: float             # voluntariness stability

    # --- 3) Temporal T ∈ [0, 1]^2 ---
    t_topo: float            # DAG/topology preservation
    t_causal: float          # causal alignment

    # --- 4) Cultural C ∈ [0, 1]^2 ---
    c_dialect: float         # dialect preservation
    c_idiom: float           # idiom retention

    # --- 5) Material M ∈ [0, 1]^2 ---
    m_entity: float          # entity preservation
    m_rel: float             # relationship preservation

    # --- Slices (normative constants) ---
    DIM: ClassVar[int] = 13
    PHI_SLICE: ClassVar[slice] = slice(0, 4)
    INTEGRITY_SLICE: ClassVar[slice] = slice(4, 13)

    # --- Range limits ---
    _PHI_MIN: ClassVar[float] = -1.0
    _PHI_MAX: ClassVar[float] = 1.0
    _INT_MIN: ClassVar[float] = 0.0
    _INT_MAX: ClassVar[float] = 1.0

    # --- Canonical field names in locked order (useful for logs/certs) ---
    FIELD_ORDER: ClassVar[Tuple[str, ...]] = (
        "phi_polarity",
        "phi_direction",
        "phi_stance",
        "phi_confidence",
        "a_perp",
        "a_victim",
        "a_vol",
        "t_topo",
        "t_causal",
        "c_dialect",
        "c_idiom",
        "m_entity",
        "m_rel",
    )

    def __post_init__(self) -> None:
        """
        Enforce normative coordinate ranges (Spec 2 + Spec 3).

        Implementations MUST NOT silently clamp.
        If an upstream component cannot supply a reliable value, that must be
        handled by the caller (e.g., "unknown coordinate" logic in certification),
        not by coercing values here.
        """
        # Validate Φ block in [-1, 1]
        for name in ("phi_polarity", "phi_direction", "phi_stance", "phi_confidence"):
            val = getattr(self, name)
            _require_finite(name, val)
            if not (self._PHI_MIN <= val <= self._PHI_MAX):
                raise ValueError(f"{name}={val} out of range [{self._PHI_MIN}, {self._PHI_MAX}]")

        # Validate integrity blocks in [0, 1]
        for name in (
            "a_perp",
            "a_victim",
            "a_vol",
            "t_topo",
            "t_causal",
            "c_dialect",
            "c_idiom",
            "m_entity",
            "m_rel",
        ):
            val = getattr(self, name)
            _require_finite(name, val)
            if not (self._INT_MIN <= val <= self._INT_MAX):
                raise ValueError(f"{name}={val} out of range [{self._INT_MIN}, {self._INT_MAX}]")

    # ----------------------------
    # Vectorization / algebra
    # ----------------------------

    def as_vector(self) -> np.ndarray:
        """
        Return the 13D state vector x in strict v0.1 coordinate order (Spec 1.1).
        """
        return np.array(
            [
                self.phi_polarity,
                self.phi_direction,
                self.phi_stance,
                self.phi_confidence,
                self.a_perp,
                self.a_victim,
                self.a_vol,
                self.t_topo,
                self.t_causal,
                self.c_dialect,
                self.c_idiom,
                self.m_entity,
                self.m_rel,
            ],
            dtype=np.float64,
        )

    def diff(self, other: DignityState13) -> np.ndarray:
        """
        Signed displacement vector v = self - other.
        """
        return self.as_vector() - other.as_vector()

    def degrade(self, transformed: DignityState13) -> np.ndarray:
        """
        Compute the asymmetric degradation vector Δ⁻ (Spec 5.2).

        Interprets:
          self        = reference/original state x
          transformed = transformed state y

        Semantics (Spec 5.2):
          - Φ coordinates (0..3): symmetric drift retained:  x - y
          - Integrity coords (4..12): one-sided loss only: max(0, x - y)

        Returns:
          Δ⁻ vector suitable for quadratic form with metric tensor g.
        """
        displacement = self.diff(transformed)  # x - y
        delta_minus = np.zeros_like(displacement)

        # Φ: symmetric difference (drift is drift)
        delta_minus[self.PHI_SLICE] = displacement[self.PHI_SLICE]

        # A,T,C,M: penalize only loss of integrity
        delta_minus[self.INTEGRITY_SLICE] = np.maximum(0.0, displacement[self.INTEGRITY_SLICE])

        return delta_minus


def _require_finite(name: str, value: float) -> None:
    """Internal: raise if value is NaN/inf (normative sanity check)."""
    if not np.isfinite(value):
        raise ValueError(f"{name} must be finite; got {value!r}")

