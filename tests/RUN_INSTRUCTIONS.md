# Install pytest if needed
pip install pytest numpy

# Run all tests
pytest tests/test_dignity_metric.py -v

# Run specific section
pytest tests/test_dignity_metric.py::TestMariaStoryGoldenPath -v

# Run with coverage
pytest tests/test_dignity_metric.py --cov=src.dignity --cov-report=html
```

---

## Expected Output
```
tests/test_dignity_metric.py::TestMariaStoryGoldenPath::test_spoken_to_grade1_distance PASSED
tests/test_dignity_metric.py::TestMariaStoryGoldenPath::test_grade1_to_grade5_improvement PASSED
tests/test_dignity_metric.py::TestMariaStoryGoldenPath::test_grade5_to_grade12_refinement PASSED
tests/test_dignity_metric.py::TestMariaStoryGoldenPath::test_full_path_energy PASSED
tests/test_dignity_metric.py::TestMariaStoryGoldenPath::test_geodesic_likeness_high PASSED
tests/test_dignity_metric.py::TestMariaStoryGoldenPath::test_no_gate_violations_grade12 PASSED
tests/test_dignity_metric.py::TestMariaStoryGoldenPath::test_all_intermediate_states_pass_gates PASSED
tests/test_dignity_metric.py::TestGateViolations::test_agency_perpetrator_violation PASSED
tests/test_dignity_metric.py::TestGateViolations::test_temporal_causal_violation PASSED
tests/test_dignity_metric.py::TestGateViolations::test_material_entity_violation PASSED
tests/test_dignity_metric.py::TestGateViolations::test_multiple_violations_reported PASSED
tests/test_dignity_metric.py::TestGateViolations::test_custom_gate_config PASSED
tests/test_dignity_metric.py::TestMathematicalInvariants::test_identical_states_zero_distance PASSED
tests/test_dignity_metric.py::TestMathematicalInvariants::test_identical_states_perfect_geodesic PASSED
tests/test_dignity_metric.py::TestMathematicalInvariants::test_integrity_improvements_not_penalized PASSED
tests/test_dignity_metric.py::TestMathematicalInvariants::test_emotional_drift_symmetric PASSED
tests/test_dignity_metric.py::TestMathematicalInvariants::test_metric_positive_definiteness PASSED
tests/test_dignity_metric.py::TestMathematicalInvariants::test_triangle_inequality_sketch PASSED
tests/test_dignity_metric.py::TestMathematicalInvariants::test_path_energy_additive PASSED
tests/test_dignity_metric.py::TestNumericalRegressionLock::test_worked_example_section_12 PASSED
tests/test_dignity_metric.py::TestNumericalRegressionLock::test_default_weights_locked PASSED
tests/test_dignity_metric.py::TestNumericalRegressionLock::test_coordinate_ordering_locked PASSED
tests/test_dignity_metric.py::TestWeightVariations::test_custom_weights_accepted PASSED
tests/test_dignity_metric.py::TestWeightVariations::test_all_equal_weights_behaves_sensibly PASSED

========================= 24 passed in 0.15s ==========================
