"""src.dignity.state

Normative implementation of the Dignity State Space (v0.1).

A :class:`~DignityState13` is the immutable atomic unit for ESPER-FORGE dignity
measurement and certification.

Normative requirements (v0.1):
- Dimension locked at 13.
- Coordinate ordering is locked and MUST NOT change.
- Φ coordinates are axes in [-1, 1].
- A/T/C/M coordinates are integrity scores in [0, 1], where higher is better.
- Asymmetric degradation semantics:
    * Φ drift is symmetric (movement in either direction is "movement"),
    * A/T/C/M are one-sided for degradation: only losses are penalized.

Spec source:
- docs/09-DIGNITY-METRIC-v0.1.md

Coordinate ordering (STRICT):
    0-3   Φ  = (phi_polarity, phi_direction, phi_stance, phi_confidence)
    4-6   A  = (a_perp, a_victim, a_vol)
    7-8   T  = (t_topo, t_causal)
    9-10  C  = (c_dialect, c_idiom)
    11-12 M  = (m_entity, m_rel)

Copyright 2026 The Cyrano de Bergerac Foundation
Licensed under Apache-2.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

import numpy as np


@dataclass(frozen=True, slots=True)
class DignityState13:
    """A point in the 13D dignity manifold (normative v0.1).

    This class is intentionally small, immutable, and hash-stable.

    Notes
    -----
    * Validation is performed at construction time.
    * Use :meth:`as_vector` to obtain the canonical 13D vector.
    """

    # --- 1. Emotional Core Block (Φ) in [-1, 1] ---
    phi_polarity: float
    phi_direction: float
    phi_stance: float
    phi_confidence: float

    # --- 2. Agency Block (A) in [0, 1] ---
    a_perp: float
    a_victim: float
    a_vol: float

    # --- 3. Temporal Block (T) in [0, 1] ---
    t_topo: float
    t_causal: float

    # --- 4. Cultural Block (C) in [0, 1] ---
    c_dialect: float
    c_idiom: float

    # --- 5. Material Identity Block (M) in [0, 1] ---
    m_entity: float
    m_rel: float

    # Constant slices for block access (normative indices)
    DIM: ClassVar[int] = 13
    PHI_SLICE: ClassVar[slice] = slice(0, 4)
    A_SLICE: ClassVar[slice] = slice(4, 7)
    T_SLICE: ClassVar[slice] = slice(7, 9)
    C_SLICE: ClassVar[slice] = slice(9, 11)
    M_SLICE: ClassVar[slice] = slice(11, 13)
    INTEGRITY_SLICE: ClassVar[slice] = slice(4, 13)

    def __post_init__(self) -> None:
        # Validate Φ block [-1, 1]
        phi = (self.phi_polarity, self.phi_direction, self.phi_stance, self.phi_confidence)
        for name, val in zip(
            ("phi_polarity", "phi_direction", "phi_stance", "phi_confidence"),
            phi,
            strict=True,
        ):
            if not (-1.0 <= float(val) <= 1.0):
                raise ValueError(f"{name} must be in [-1, 1]; got {val!r}")

        # Validate integrity blocks [0, 1]
        integrity = {
            "a_perp": self.a_perp,
            "a_victim": self.a_victim,
            "a_vol": self.a_vol,
            "t_topo": self.t_topo,
            "t_causal": self.t_causal,
            "c_dialect": self.c_dialect,
            "c_idiom": self.c_idiom,
            "m_entity": self.m_entity,
            "m_rel": self.m_rel,
        }
        for name, val in integrity.items():
            if not (0.0 <= float(val) <= 1.0):
                raise ValueError(f"{name} must be in [0, 1]; got {val!r}")

    def as_vector(self) -> np.ndarray:
        """Return the canonical 13D vector (dtype=float64)."""
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

    def diff(self, other: "DignityState13") -> np.ndarray:
        """Compute signed displacement v = self - other."""
        return self.as_vector() - other.as_vector()

    def degrade(self, transformed: "DignityState13") -> np.ndarray:
        """Compute the asymmetric degradation vector Δ⁻ (normative semantics).

        Interpretations (normative):
        - `self` is the reference/original state x
        - `transformed` is the transformed state y

        Construction:
        - Φ coordinates: Δ⁻_Φ = x_Φ - y_Φ (symmetric drift retained)
        - Integrity coordinates (A/T/C/M): Δ⁻_I = max(0, x_I - y_I)
          (improvements are clamped to 0; only loss is penalized)

        Returns
        -------
        np.ndarray
            A length-13 vector suitable for quadratic-form distance computation.
        """
        displacement = self.diff(transformed)  # x - y

        delta_minus = np.zeros_like(displacement)
        delta_minus[self.PHI_SLICE] = displacement[self.PHI_SLICE]
        delta_minus[self.INTEGRITY_SLICE] = np.maximum(0.0, displacement[self.INTEGRITY_SLICE])
        return delta_minus
