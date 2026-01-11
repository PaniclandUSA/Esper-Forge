"""
Compile gate enforcement for the Dignity Metric v0.1.

This module implements constitutional "must never happen" boundaries
per docs/09-DIGNITY-METRIC-v0.1.md Section 8.

Metrics measure drift.
Gates enforce legitimacy.

If any required gate fails, certification MUST fail.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .state import DignityState13


# ──────────────────────────────────────────────────────────────
# Gate violation records
# ──────────────────────────────────────────────────────────────

@dataclass(frozen=True, slots=True)
class GateViolation:
    """
    Records a single compile-gate violation.

    Attributes:
        coordinate: Canonical coordinate name (e.g., 'A_perp').
        value: Observed value.
        threshold: Required minimum (or exact requirement).
        severity: 'critical' or 'warning'.
    """
    coordinate: str
    value: float
    threshold: float
    severity: str  # "critical" | "warning"


@dataclass(frozen=True, slots=True)
class GateReport:
    """
    Result of compile-gate evaluation.

    Attributes:
        passed: True iff no critical violations occurred.
        violations: List of all gate violations.
        warnings: Human-readable warnings (non-fatal).
    """
    passed: bool
    violations: List[GateViolation]
    warnings: List[str]


# ──────────────────────────────────────────────────────────────
# Gate configuration (v0.1 defaults)
# ──────────────────────────────────────────────────────────────

@dataclass(frozen=True, slots=True)
class GateConfig:
    """
    Compile-gate thresholds per Dignity Metric v0.1 Section 8.1.

    These defaults reflect catastrophic dignity failure boundaries.
    Contracts MAY override these values.
    """

    # Agency
    A_MIN: float = 0.95
    A_VOL_MIN: float = 0.90

    # Temporal
    T_MIN: float = 0.95
    T_CAUSAL_MIN: float = 0.99  # stricter for causality

    # Cultural
    C_MIN: float = 0.80

    # Material
    M_ENTITY_MIN: float = 0.95
    M_REL_MIN: float = 0.90


# ──────────────────────────────────────────────────────────────
# Gate enforcement
# ──────────────────────────────────────────────────────────────

def check_gates(
    state: DignityState13,
    config: Optional[GateConfig] = None
) -> GateReport:
    """
    Checks all compile gates for a given dignity state.

    Args:
        state: The DignityState13 to evaluate.
        config: Optional GateConfig override.

    Returns:
        GateReport with pass/fail status and violation details.

    Semantics:
        - Any critical violation => passed = False
        - Metrics may still be recorded even if gates fail
        - This function NEVER mutates state
    """
    cfg = config or GateConfig()
    violations: List[GateViolation] = []
    warnings: List[str] = []

    # ── Agency gates ───────────────────────────────────────────
    if state.a_perp < cfg.A_MIN:
        violations.append(GateViolation(
            coordinate="A_perp",
            value=state.a_perp,
            threshold=cfg.A_MIN,
            severity="critical",
        ))

    if state.a_victim < cfg.A_MIN:
        violations.append(GateViolation(
            coordinate="A_victim",
            value=state.a_victim,
            threshold=cfg.A_MIN,
            severity="critical",
        ))

    if state.a_vol < cfg.A_VOL_MIN:
        violations.append(GateViolation(
            coordinate="A_vol",
            value=state.a_vol,
            threshold=cfg.A_VOL_MIN,
            severity="critical",
        ))

    # ── Temporal gates ─────────────────────────────────────────
    if state.t_topo < cfg.T_MIN:
        violations.append(GateViolation(
            coordinate="T_topo",
            value=state.t_topo,
            threshold=cfg.T_MIN,
            severity="critical",
        ))

    if state.t_causal < cfg.T_CAUSAL_MIN:
        violations.append(GateViolation(
            coordinate="T_causal",
            value=state.t_causal,
            threshold=cfg.T_CAUSAL_MIN,
            severity="critical",
        ))

    # ── Cultural gates ─────────────────────────────────────────
    if state.c_dialect < cfg.C_MIN:
        violations.append(GateViolation(
            coordinate="C_dialect",
            value=state.c_dialect,
            threshold=cfg.C_MIN,
            severity="critical",
        ))

    if state.c_idiom < cfg.C_MIN:
        violations.append(GateViolation(
            coordinate="C_idiom",
            value=state.c_idiom,
            threshold=cfg.C_MIN,
            severity="critical",
        ))

    # ── Material identity gates ────────────────────────────────
    if state.m_entity < cfg.M_ENTITY_MIN:
        violations.append(GateViolation(
            coordinate="M_entity",
            value=state.m_entity,
            threshold=cfg.M_ENTITY_MIN,
            severity="critical",
        ))

    if state.m_rel < cfg.M_REL_MIN:
        violations.append(GateViolation(
            coordinate="M_rel",
            value=state.m_rel,
            threshold=cfg.M_REL_MIN,
            severity="critical",
        ))

    passed = not any(v.severity == "critical" for v in violations)

    return GateReport(
        passed=passed,
        violations=violations,
        warnings=warnings,
    )
