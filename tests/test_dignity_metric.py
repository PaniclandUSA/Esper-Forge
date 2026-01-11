"""
Comprehensive test suite for Dignity Metric v0.1 (Normative).

This suite merges two complementary approaches:
1. Core Semantics (Gemini): Surgical tests of fundamental metric properties
2. Golden-Path Validation (Claude): Real-world verification using Maria's story
3. Numerical Regression Locks: Prevention of silent math drift

Test coverage:
- State invariants (coordinate ordering, range validation, immutability)
- Asymmetric degradation logic (Φ symmetric, A/T/C/M one-sided)
- Metric algebra (d_total, d_degrade, path_energy, geodesic_likeness)
- Constitutional gates (refuse-to-compile boundaries)
- Real-world validation (documented literacy transformation)
- Edge cases and mathematical properties

Copyright 2026 The Cyrano de Bergerac Foundation
Licensed under Apache-2.0
"""

from __future__ import annotations

import pytest
import numpy as np

from src.dignity import (
    DignityState13,
    d_total,
    d_degrade,
    path_energy,
    geodesic_likeness,
    loop_defect,
    check_gates,
    GateConfig,
    MetricWeightsV01,
    DEFAULT_WEIGHT_DIAG,
)


# ══════════════════════════════════════════════════════════════════════════════
# FIXTURES: SYNTHETIC STATES (Gemini's approach)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def perfect_state() -> DignityState13:
    """
    A state with maximum integrity and neutral emotion.
    
    Useful for testing pure degradation logic.
    """
    return DignityState13(
        # Φ (Emotional) - neutral
        phi_polarity=0.0,
        phi_direction=0.0,
        phi_stance=0.0,
        phi_confidence=0.0,
        # A (Agency) - perfect
        a_perp=1.0,
        a_victim=1.0,
        a_vol=1.0,
        # T (Temporal) - perfect
        t_topo=1.0,
        t_causal=1.0,
        # C (Cultural) - perfect
        c_dialect=1.0,
        c_idiom=1.0,
        # M (Material) - perfect
        m_entity=1.0,
        m_rel=1.0,
    )


@pytest.fixture
def flawed_state() -> DignityState13:
    """
    A state with specific integrity losses for testing.
    
    Losses:
    - Φ: Polarity drift to 0.5, direction to -0.5
    - A: Perpetrator agency reduced to 0.8
    - C: Dialect reduced to 0.5, idiom to 0.9
    """
    return DignityState13(
        # Φ - drifted
        phi_polarity=0.5,
        phi_direction=-0.5,
        phi_stance=0.0,
        phi_confidence=0.0,
        # A - flawed perp agency
        a_perp=0.8,
        a_victim=1.0,
        a_vol=1.0,
        # T - perfect
        t_topo=1.0,
        t_causal=1.0,
        # C - major dialect loss
        c_dialect=0.5,
        c_idiom=0.9,
        # M - perfect
        m_entity=1.0,
        m_rel=1.0,
    )


@pytest.fixture
def unity_weights() -> dict:
    """
    Uniform weights (all 1.0) for easy manual calculation.
    
    Makes distance computations equivalent to Euclidean distance.
    """
    return {
        "Phi": (1.0, 1.0, 1.0, 1.0),
        "A": (1.0, 1.0, 1.0),
        "T": (1.0, 1.0),
        "C": (1.0, 1.0),
        "M": (1.0, 1.0),
    }


# ══════════════════════════════════════════════════════════════════════════════
# FIXTURES: MARIA'S STORY (Claude's approach - Real-world validation)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def maria_spoken() -> DignityState13:
    """
    Maria's spoken narrative (baseline).
    
    From docs/05-LITERACY-DEMO.md:
    - 3-minute recording, natural speech
    - Spanish phrases included (café con leche, polvorones, mija)
    - High emotional warmth (grandmother's love)
    - Personal reflection, stable agency attribution
    """
    return DignityState13(
        # Emotional core (from VSE extraction)
        phi_polarity=0.85,      # Warm (grandmother's love)
        phi_direction=0.45,     # Dreaming (reflective)
        phi_stance=0.90,        # Together (family bonds)
        phi_confidence=0.88,    # Certain (lived experience)
        
        # Agency (all actors consistent)
        a_perp=1.00,
        a_victim=1.00,
        a_vol=1.00,
        
        # Temporal (causal DAG preserved)
        t_topo=1.00,
        t_causal=1.00,
        
        # Cultural (authentic voice)
        c_dialect=1.00,         # Natural speech patterns
        c_idiom=1.00,           # Spanish phrases intact
        
        # Material (entity identity)
        m_entity=1.00,          # Grandmother = grandmother
        m_rel=1.00,             # Relationships consistent
    )


@pytest.fixture
def maria_grade_1() -> DignityState13:
    """
    Grade 1 rendering (48 words, basic sight words).
    
    Simplified vocabulary: "Grandma was nice. She made good food."
    Emotional core preserved but less nuanced.
    """
    return DignityState13(
        # Emotional core (slight warmth reduction)
        phi_polarity=0.78,
        phi_direction=0.45,
        phi_stance=0.90,
        phi_confidence=0.88,
        
        # Agency (preserved)
        a_perp=1.00,
        a_victim=1.00,
        a_vol=1.00,
        
        # Temporal (preserved)
        t_topo=1.00,
        t_causal=1.00,
        
        # Cultural (some dialect loss)
        c_dialect=0.85,         # Simplified but Spanish kept
        c_idiom=0.90,           # Most idioms adapted
        
        # Material (perfect)
        m_entity=1.00,
        m_rel=1.00,
    )


@pytest.fixture
def maria_grade_5() -> DignityState13:
    """
    Grade 5 rendering (248 words, intermediate vocabulary).
    
    "My grandmother showed her love through the food she prepared."
    More complex sentences, restored emotional nuance.
    """
    return DignityState13(
        # Emotional core (restored nuance)
        phi_polarity=0.82,
        phi_direction=0.45,
        phi_stance=0.90,
        phi_confidence=0.88,
        
        # Agency (preserved)
        a_perp=1.00,
        a_victim=1.00,
        a_vol=1.00,
        
        # Temporal (preserved)
        t_topo=1.00,
        t_causal=1.00,
        
        # Cultural (more preserved)
        c_dialect=0.90,
        c_idiom=0.95,
        
        # Material (perfect)
        m_entity=1.00,
        m_rel=1.00,
    )


@pytest.fixture
def maria_grade_12() -> DignityState13:
    """
    Grade 12 rendering (318 words, advanced vocabulary).
    
    "My grandmother's benevolent presence manifested through..."
    Complex sentences, full emotional depth, cultural authenticity.
    """
    return DignityState13(
        # Emotional core (fully restored)
        phi_polarity=0.84,
        phi_direction=0.45,
        phi_stance=0.90,
        phi_confidence=0.88,
        
        # Agency (preserved)
        a_perp=1.00,
        a_victim=1.00,
        a_vol=1.00,
        
        # Temporal (preserved)
        t_topo=1.00,
        t_causal=1.00,
        
        # Cultural (nearly full restoration)
        c_dialect=0.95,
        c_idiom=0.98,
        
        # Material (perfect)
        m_entity=1.00,
        m_rel=1.00,
    )


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1: STATE INVARIANTS & COORDINATE ORDERING (Gemini)
# ══════════════════════════════════════════════════════════════════════════════

class TestStateInvariants:
    """
    Verify fundamental state properties.
    
    Tests normative requirements from Spec 1.1, 1.2, 2, 3.
    """
    
    def test_coordinate_ordering_strict(self) -> None:
        """
        Verify strict Spec 1.1 coordinate ordering in vector packing.
        
        Order: Φ(4) | A(3) | T(2) | C(2) | M(2) = 13 dimensions
        """
        s = DignityState13(
            phi_polarity=0.1, phi_direction=0.2, phi_stance=0.3, phi_confidence=0.4,
            a_perp=0.5, a_victim=0.6, a_vol=0.7,
            t_topo=0.8, t_causal=0.9,
            c_dialect=0.11, c_idiom=0.12,
            m_entity=0.13, m_rel=0.14
        )
        vec = s.as_vector()
        
        expected = np.array([
            0.1, 0.2, 0.3, 0.4,     # Φ
            0.5, 0.6, 0.7,          # A
            0.8, 0.9,               # T
            0.11, 0.12,             # C
            0.13, 0.14              # M
        ])
        
        np.testing.assert_allclose(
            vec, expected,
            err_msg="Coordinate ordering violated (Spec 1.1)"
        )
    
    def test_dimension_locked(self) -> None:
        """
        Verify dimension is locked at 13 (Spec 1.2).
        
        Breaking this would invalidate all certificates.
        """
        assert DignityState13.DIM == 13, "Dimension must be 13 for v0.1"
        
        state = DignityState13(
            phi_polarity=0.0, phi_direction=0.0, phi_stance=0.0, phi_confidence=0.0,
            a_perp=1.0, a_victim=1.0, a_vol=1.0,
            t_topo=1.0, t_causal=1.0,
            c_dialect=1.0, c_idiom=1.0,
            m_entity=1.0, m_rel=1.0,
        )
        
        assert state.as_vector().shape == (13,), "Vector must be 13D"
    
    def test_validation_phi_range(self) -> None:
        """
        Φ coordinates must be in [-1, 1] (Spec 2.1).
        """
        # Out of range should raise ValueError
        with pytest.raises(ValueError, match="phi_polarity"):
            DignityState13(
                phi_polarity=1.5,  # INVALID
                phi_direction=0.0, phi_stance=0.0, phi_confidence=0.0,
                a_perp=1.0, a_victim=1.0, a_vol=1.0,
                t_topo=1.0, t_causal=1.0,
                c_dialect=1.0, c_idiom=1.0,
                m_entity=1.0, m_rel=1.0,
            )
        
        with pytest.raises(ValueError, match="phi_direction"):
            DignityState13(
                phi_polarity=0.0,
                phi_direction=-1.5,  # INVALID
                phi_stance=0.0, phi_confidence=0.0,
                a_perp=1.0, a_victim=1.0, a_vol=1.0,
                t_topo=1.0, t_causal=1.0,
                c_dialect=1.0, c_idiom=1.0,
                m_entity=1.0, m_rel=1.0,
            )
    
    def test_validation_integrity_range(self) -> None:
        """
        Integrity coordinates (A,T,C,M) must be in [0, 1] (Spec 2.2-2.5).
        """
        # Negative should fail
        with pytest.raises(ValueError, match="a_perp"):
            DignityState13(
                phi_polarity=0.0, phi_direction=0.0, phi_stance=0.0, phi_confidence=0.0,
                a_perp=-0.1,  # INVALID
                a_victim=1.0, a_vol=1.0,
                t_topo=1.0, t_causal=1.0,
                c_dialect=1.0, c_idiom=1.0,
                m_entity=1.0, m_rel=1.0,
            )
        
        # Greater than 1.0 should fail
        with pytest.raises(ValueError, match="m_entity"):
            DignityState13(
                phi_polarity=0.0, phi_direction=0.0, phi_stance=0.0, phi_confidence=0.0,
                a_perp=1.0, a_victim=1.0, a_vol=1.0,
                t_topo=1.0, t_causal=1.0,
                c_dialect=1.0, c_idiom=1.0,
                m_entity=1.5,  # INVALID
                m_rel=1.0,
            )
    
    def test_immutability(self, perfect_state: DignityState13) -> None:
        """
        States are immutable (frozen dataclass).
        
        Critical for certificate integrity.
        """
        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            perfect_state.a_perp = 0.5  # type: ignore


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2: ASYMMETRIC DEGRADATION LOGIC (Gemini - Surgical semantics)
# ══════════════════════════════════════════════════════════════════════════════

class TestAsymmetricDegradation:
    """
    Test asymmetric degradation semantics (Spec 5.2).
    
    Core principle:
    - Φ drift is symmetric (movement in either direction counts)
    - Integrity LOSS is penalized: max(0, reference - transformed)
    - Integrity GAIN is clamped to 0 (improvements not penalized)
    """
    
    def test_integrity_loss_penalized(self, perfect_state: DignityState13) -> None:
        """
        Integrity loss contributes to degradation distance.
        
        Reference=1.0, Transformed=0.8 => Δ⁻ = 0.2 (penalized)
        """
        bad_trans = DignityState13(
            phi_polarity=0.0, phi_direction=0.0, phi_stance=0.0, phi_confidence=0.0,
            a_perp=0.8,  # LOSS: 1.0 → 0.8
            a_victim=1.0, a_vol=1.0,
            t_topo=1.0, t_causal=1.0,
            c_dialect=1.0, c_idiom=1.0,
            m_entity=1.0, m_rel=1.0,
        )
        
        delta_minus = perfect_state.degrade(bad_trans)
        
        # Index 4 = a_perp (from coordinate ordering)
        assert delta_minus[4] == pytest.approx(0.2), (
            "Integrity loss should be penalized in degradation vector"
        )
    
    def test_integrity_gain_clamped(self, flawed_state: DignityState13,
                                     perfect_state: DignityState13) -> None:
        """
        Integrity improvements are clamped to 0 in degradation.
        
        Reference=0.8, Transformed=1.0 => Δ⁻ = max(0, -0.2) = 0.0
        """
        # Flawed has a_perp=0.8, Perfect has a_perp=1.0
        # Improvement: 0.8 → 1.0 should be clamped
        
        delta_minus = flawed_state.degrade(perfect_state)
        
        # Index 4 = a_perp
        assert delta_minus[4] == pytest.approx(0.0), (
            "Integrity improvements should be clamped to 0"
        )
    
    def test_emotional_drift_symmetric(self, perfect_state: DignityState13) -> None:
        """
        Φ drift is symmetric (both directions penalized).
        
        Reference=0.0, Transformed=0.5 => Δ⁻ = -0.5 (retained)
        Reference=0.0, Transformed=-0.5 => Δ⁻ = 0.5 (retained)
        """
        # Positive drift
        drift_pos = DignityState13(
            phi_polarity=0.5,  # DRIFT: 0.0 → 0.5
            phi_direction=0.0, phi_stance=0.0, phi_confidence=0.0,
            a_perp=1.0, a_victim=1.0, a_vol=1.0,
            t_topo=1.0, t_causal=1.0,
            c_dialect=1.0, c_idiom=1.0,
            m_entity=1.0, m_rel=1.0,
        )
        
        # Negative drift
        drift_neg = DignityState13(
            phi_polarity=-0.5,  # DRIFT: 0.0 → -0.5
            phi_direction=0.0, phi_stance=0.0, phi_confidence=0.0,
            a_perp=1.0, a_victim=1.0, a_vol=1.0,
            t_topo=1.0, t_causal=1.0,
            c_dialect=1.0, c_idiom=1.0,
            m_entity=1.0, m_rel=1.0,
        )
        
        delta_pos = perfect_state.degrade(drift_pos)
        delta_neg = perfect_state.degrade(drift_neg)
        
        # Index 0 = phi_polarity
        assert delta_pos[0] == pytest.approx(-0.5), "Positive drift retained"
        assert delta_neg[0] == pytest.approx(0.5), "Negative drift retained"


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3: METRIC CALCULATIONS (Gemini - Manual math verification)
# ══════════════════════════════════════════════════════════════════════════════

class TestMetricCalculations:
    """
    Test metric distance functions (Spec 5, 6, 7).
    
    Uses unity weights for manual verification.
    """
    
    def test_d_total_manual_calculation(
        self,
        perfect_state: DignityState13,
        flawed_state: DignityState13,
        unity_weights: dict,
    ) -> None:
        """
        Verify d_total with explicit manual calculation.
        
        Manual calculation:
        - Φ diff: (0.5, -0.5, 0, 0) => sq: (0.25, 0.25, 0, 0)
        - A diff: (-0.2, 0, 0) => sq: (0.04, 0, 0)
        - T diff: (0, 0) => sq: (0, 0)
        - C diff: (-0.5, -0.1) => sq: (0.25, 0.01)
        - M diff: (0, 0) => sq: (0, 0)
        
        Sum of squares: 0.25 + 0.25 + 0.04 + 0.25 + 0.01 = 0.8
        Distance: sqrt(0.8) ≈ 0.8944
        """
        d_tot = d_total(perfect_state, flawed_state, weights=unity_weights)
        
        expected = np.sqrt(0.8)
        assert d_tot == pytest.approx(expected, rel=1e-6), (
            f"Expected {expected:.4f}, got {d_tot:.4f}"
        )
    
    def test_d_degrade_forward(
        self,
        perfect_state: DignityState13,
        flawed_state: DignityState13,
        unity_weights: dict,
    ) -> None:
        """
        d_degrade(perfect → flawed) should match d_total.
        
        All changes are losses or Φ drift (no improvements to clamp).
        """
        d_deg = d_degrade(perfect_state, flawed_state, weights=unity_weights)
        d_tot = d_total(perfect_state, flawed_state, weights=unity_weights)
        
        assert d_deg == pytest.approx(d_tot, rel=1e-6), (
            "Forward degradation should equal total distance (all losses)"
        )
    
    def test_d_degrade_reverse(
        self,
        perfect_state: DignityState13,
        flawed_state: DignityState13,
        unity_weights: dict,
    ) -> None:
        """
        d_degrade(flawed → perfect) should only count Φ drift.
        
        Manual calculation:
        - Φ diff: (-0.5, 0.5, 0, 0) => sq: (0.25, 0.25, 0, 0)
        - Integrity: All improvements, clamped to 0
        
        Sum of squares: 0.5
        Distance: sqrt(0.5) ≈ 0.7071
        """
        d_deg = d_degrade(flawed_state, perfect_state, weights=unity_weights)
        
        expected = np.sqrt(0.5)
        assert d_deg == pytest.approx(expected, rel=1e-6), (
            f"Expected {expected:.4f}, got {d_deg:.4f}"
        )
    
    def test_path_energy_two_states(
        self,
        perfect_state: DignityState13,
        flawed_state: DignityState13,
        unity_weights: dict,
    ) -> None:
        """
        Path energy E([A, B]) = d_total(A, B)²
        """
        path = [perfect_state, flawed_state]
        
        energy = path_energy(path, weights=unity_weights)
        d_tot = d_total(perfect_state, flawed_state, weights=unity_weights)
        expected = d_tot ** 2
        
        assert energy == pytest.approx(expected, rel=1e-6)
    
    def test_geodesic_likeness_direct_path(
        self,
        perfect_state: DignityState13,
        flawed_state: DignityState13,
        unity_weights: dict,
    ) -> None:
        """
        Direct path between two states is geodesic (G = 1.0).
        """
        path = [perfect_state, flawed_state]
        
        g_score = geodesic_likeness(path, weights=unity_weights)
        
        assert g_score == pytest.approx(1.0, rel=1e-6), (
            "Direct path should be geodesic"
        )
    
    def test_loop_defect_closed_loop(
        self,
        perfect_state: DignityState13,
        flawed_state: DignityState13,
        unity_weights: dict,
    ) -> None:
        """
        Closed loop (start = end) has zero defect.
        """
        loop = [perfect_state, flawed_state, perfect_state]
        
        defect = loop_defect(loop, weights=unity_weights)
        
        assert defect == pytest.approx(0.0, abs=1e-10), (
            "Closed loop should have zero defect"
        )
    
    def test_loop_defect_open_loop(
        self,
        perfect_state: DignityState13,
        flawed_state: DignityState13,
        unity_weights: dict,
    ) -> None:
        """
        Open loop (start ≠ end) has non-zero defect.
        """
        loop = [perfect_state, flawed_state]
        
        defect = loop_defect(loop, weights=unity_weights)
        
        assert defect > 0.0, "Open loop should have positive defect"


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4: MARIA'S STORY GOLDEN PATH (Claude - Real-world validation)
# ══════════════════════════════════════════════════════════════════════════════

class TestMariaStoryGoldenPath:
    """
    Validate against documented real-world example.
    
    Ground truth from docs/05-LITERACY-DEMO.md:
    - Emotional core drift: 0.06-0.08 (< 0.15 threshold)
    - Agency attribution: Consistent all levels
    - Causal sequence: Topology preserved
    - Cultural authenticity: Spanish phrases preserved
    - Material identity: All entities consistent
    """
    
    def test_spoken_to_grade1_distance(
        self,
        maria_spoken: DignityState13,
        maria_grade_1: DignityState13,
    ) -> None:
        """
        Verify distance from spoken to Grade 1 matches documented drift.
        
        Expected: Small degradation (emotional + dialect simplification)
        """
        d_deg = d_degrade(maria_spoken, maria_grade_1)
        
        # Documented range from Spec 05
        assert 0.05 <= d_deg <= 0.20, (
            f"Spoken→Grade1 degradation {d_deg:.4f} outside expected range"
        )
    
    def test_full_transformation_path(
        self,
        maria_spoken: DignityState13,
        maria_grade_1: DignityState13,
        maria_grade_5: DignityState13,
        maria_grade_12: DignityState13,
    ) -> None:
        """
        Complete transformation path has reasonable metrics.
        """
        path = [maria_spoken, maria_grade_1, maria_grade_5, maria_grade_12]
        
        # Path energy should be bounded
        energy = path_energy(path)
        assert 0.0 < energy < 1.0, f"Path energy {energy:.4f} outside bounds"
        
        # Geodesic-likeness should be high (efficient transformation)
        g_score = geodesic_likeness(path)
        assert 0.75 <= g_score <= 1.0, (
            f"Geodesic-likeness {g_score:.4f} indicates inefficient path"
        )
    
    def test_all_states_pass_gates(
        self,
        maria_spoken: DignityState13,
        maria_grade_1: DignityState13,
        maria_grade_5: DignityState13,
        maria_grade_12: DignityState13,
    ) -> None:
        """
        Every state in transformation path passes compile gates.
        
        This ensures no intermediate step violates dignity boundaries.
        """
        for state, label in [
            (maria_spoken, "Spoken"),
            (maria_grade_1, "Grade 1"),
            (maria_grade_5, "Grade 5"),
            (maria_grade_12, "Grade 12"),
        ]:
            report = check_gates(state)
            assert report.passed, (
                f"{label} failed gates: {[v.coordinate for v in report.violations]}"
            )
            assert len(report.violations) == 0


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5: CONSTITUTIONAL GATES (Gemini - Enforcement testing)
# ══════════════════════════════════════════════════════════════════════════════

class TestConstitutionalGates:
    """
    Test compile gate enforcement (Spec 8).
    
    Gates are "must never happen" boundaries.
    Violations trigger certification failure.
    """
    
    def test_gates_pass_perfect_state(self, perfect_state: DignityState13) -> None:
        """Perfect integrity state should pass all gates."""
        report = check_gates(perfect_state)
        
        assert report.passed is True
        assert len(report.violations) == 0
    
    def test_gates_fail_flawed_state(self, flawed_state: DignityState13) -> None:
        """
        Flawed state should fail specific gates.
        
        Flawed state has:
        - a_perp = 0.8 (< 0.95 threshold)
        - c_dialect = 0.5 (< 0.80 threshold)
        """
        report = check_gates(flawed_state)
        
        assert report.passed is False
        
        violated_coords = {v.coordinate for v in report.violations}
        assert "A_perp" in violated_coords
        assert "C_dialect" in violated_coords
        
        # All violations should be critical
        for v in report.violations:
            assert v.severity == "critical"
    
    def test_agency_perpetrator_gate(self) -> None:
        """A_perp < 0.95 triggers gate violation."""
        bad_state = DignityState13(
            phi_polarity=0.0, phi_direction=0.0, phi_stance=0.0, phi_confidence=0.0,
            a_perp=0.85,  # VIOLATION
            a_victim=1.00, a_vol=1.00,
            t_topo=1.00, t_causal=1.00,
            c_dialect=1.00, c_idiom=1.00,
            m_entity=1.00, m_rel=1.00,
        )
        
        report = check_gates(bad_state)
        
        assert not report.passed
        assert any(v.coordinate == "A_perp" for v in report.violations)
    
    def test_temporal_causal_gate(self) -> None:
        """T_causal < 0.99 triggers gate violation."""
        bad_state = DignityState13(
            phi_polarity=0.0, phi_direction=0.0, phi_stance=0.0, phi_confidence=0.0,
            a_perp=1.00, a_victim=1.00, a_vol=1.00,
            t_topo=1.00,
            t_causal=0.95,  # VIOLATION (stricter threshold)
            c_dialect=1.00, c_idiom=1.00,
            m_entity=1.00, m_rel=1.00,
        )
        
        report = check_gates(bad_state)
        
        assert not report.passed
        assert any(v.coordinate == "T_causal" for v in report.violations)
    
    def test_custom_gate_config(self, flawed_state: DignityState13) -> None:
        """
        Custom gate configurations can relax thresholds.
        
        Contracts may override default gates.
        """
        # Flawed state fails default gates
        default_report = check_gates(flawed_state)
        assert not default_report.passed
        
        # Relaxed config allows flawed state to pass
        relaxed_config = GateConfig(
            A_MIN=0.70,  # Flawed has 0.8
            C_MIN=0.40,  # Flawed has 0.5
        )
        
        relaxed_report = check_gates(flawed_state, config=relaxed_config)
        assert relaxed_report.passed


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6: NUMERICAL REGRESSION LOCKS (Claude - Prevent silent drift)
# ══════════════════════════════════════════════════════════════════════════════

class TestNumericalRegressionLock:
    """
    Lock specific numerical values to prevent silent regressions.
    
    These tests ensure future changes don't break the math.
    """
    
    def test_worked_example_section_12(self) -> None:
        """
        Verify the corrected worked example from Spec Section 12.2.
        
        This is the normative numerical regression test.
        
        Given:
        - Reference: phi_polarity=0.8, a_perp=1.0, c_dialect=1.0
        - Transformed: phi_polarity=0.7, a_perp=0.9, c_dialect=0.8
        
        Manual calculation:
        - Φ₁ drift: 0.1, weight 3.0 → 0.03
        - A_perp loss: 0.1, weight 4.0 → 0.04
        - C_dialect loss: 0.2, weight 2.0 → 0.08
        - Sum: 0.15
        - Distance: √0.15 = 0.3873
        
        Expected: 0.3873 (corrected by Vox from 0.7280)
        """
        reference = DignityState13(
            phi_polarity=0.8,
            phi_direction=0.5,
            phi_stance=0.9,
            phi_confidence=0.9,
            
            a_perp=1.0,
            a_victim=1.0,
            a_vol=1.0,
            
            t_topo=1.0,
            t_causal=1.0,
            
            c_dialect=1.0,
            c_idiom=1.0,
            
            m_entity=1.0,
            m_rel=1.0,
        )
        
        transformed = DignityState13(
            phi_polarity=0.7,  # Drift: -0.1
            phi_direction=0.5,
            phi_stance=0.9,
            phi_confidence=0.9,
            
            a_perp=0.9,  # Loss: -0.1
            a_victim=1.0,
            a_vol=1.0,
            
            t_topo=1.0,
            t_causal=1.0,
            
            c_dialect=0.8,  # Loss: -0.2
            c_idiom=1.0,
            
            m_entity=1.0,
            m_rel=1.0,
        )
        
        d_deg = d_degrade(reference, transformed)
        
        # NORMATIVE VALUE (corrected by Vox)
        expected = 0.3873
        
        assert d_deg == pytest.approx(expected, abs=0.0001), (
            f"Numerical regression: expected {expected:.4f}, got {d_deg:.4f}"
        )
    
    def test_default_weights_locked(self) -> None:
        """
        Verify default weight vector hasn't changed.
        
        Changes would silently break all existing certificates.
        """
        expected_weights = np.array([
            3.0, 1.0, 2.0, 1.0,  # Φ
            4.0, 4.0, 3.0,        # A
            3.0, 3.0,             # T
            2.0, 2.0,             # C
            4.0, 3.0,             # M
        ])
        
        np.testing.assert_array_equal(
            DEFAULT_WEIGHT_DIAG,
            expected_weights,
            err_msg="Default weights changed - breaks certificates!"
        )
    
    def test_coordinate_ordering_locked(self) -> None:
        """
        Verify coordinate ordering hasn't changed.
        
        Part of normative spec, must not drift.
        """
        state = DignityState13(
            phi_polarity=0.1, phi_direction=0.2, phi_stance=0.3, phi_confidence=0.4,
            a_perp=0.5, a_victim=0.6, a_vol=0.7,
            t_topo=0.8, t_causal=0.9,
            c_dialect=0.91, c_idiom=0.92,
            m_entity=0.93, m_rel=0.94,
        )
        
        vec = state.as_vector()
        
        expected_vec = np.array([
            0.1, 0.2, 0.3, 0.4,     # Φ
            0.5, 0.6, 0.7,          # A
            0.8, 0.9,               # T
            0.91, 0.92,             # C
            0.93, 0.94,             # M
        ])
        
        np.testing.assert_array_almost_equal(
            vec,
            expected_vec,
            err_msg="Coordinate ordering changed - breaks certificates!"
        )


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7: MATHEMATICAL PROPERTIES (Claude - Edge cases)
# ══════════════════════════════════════════════════════════════════════════════

class TestMathematicalProperties:
    """
    Verify fundamental mathematical properties.
    
    Tests metric axioms and edge cases.
    """
    
    def test_identical_states_zero_distance(
        self,
        perfect_state: DignityState13,
    ) -> None:
        """
        d(x, x) = 0 for any state x.
        
        Fundamental metric property.
        """
        d_tot = d_total(perfect_state, perfect_state)
        d_deg = d_degrade(perfect_state, perfect_state)
        
        assert d_tot == pytest.approx(0.0, abs=1e-10)
        assert d_deg == pytest.approx(0.0, abs=1e-10)
    
    def test_positive_definiteness(
        self,
        perfect_state: DignityState13,
        flawed_state: DignityState13,
    ) -> None:
        """
        d(x, y) > 0 when x ≠ y.
        
        Fundamental metric property.
        """
        d_tot = d_total(perfect_state, flawed_state)
        
        assert d_tot > 0.0, "Distance between different states must be positive"
    
    def test_geodesic_likeness_identical_states(
        self,
        perfect_state: DignityState13,
    ) -> None:
        """
        Path of identical states has G = 1.0.
        
        Edge case: no movement is perfectly efficient.
        """
        path = [perfect_state, perfect_state, perfect_state]
        
        g_score = geodesic_likeness(path)
        
        assert g_score == pytest.approx(1.0, abs=1e-10)


# ══════════════════════════════════════════════════════════════════════════════
# RUN CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
