"""Dignity measurement primitives for ESPER-FORGE.

This package provides the normative v0.1 implementation of the Dignity Metric
and certificate generation system.

Public API:

State & Metrics:
- :class:`~src.dignity.state.DignityState13`
- :class:`~src.dignity.metric.MetricWeightsV01`
- :func:`~src.dignity.metric.create_metric_tensor`
- :func:`~src.dignity.metric.d_total`
- :func:`~src.dignity.metric.d_degrade`
- :func:`~src.dignity.metric.path_energy`
- :func:`~src.dignity.metric.geodesic_likeness`
- :func:`~src.dignity.metric.loop_defect`

Gates:
- :class:`~src.dignity.gates.GateConfig`
- :class:`~src.dignity.gates.GateViolation`
- :class:`~src.dignity.gates.GateReport`
- :func:`~src.dignity.gates.check_gates`

Certificates (v0.1):
- :func:`~src.dignity.certificates.build_certificate_unsigned`
- :func:`~src.dignity.certificates.attach_signature`
- :func:`~src.dignity.certificates.verify_certificate`
- :func:`~src.dignity.certificates.render_certificate_markdown`
- :class:`~src.dignity.certificates.KeyPair`
- :func:`~src.dignity.certificates.sha256_text`
- :func:`~src.dignity.certificates.sha256_bytes`
- :func:`~src.dignity.certificates.canonical_json_bytes`
- :const:`~src.dignity.certificates.DEFAULT_CONTEXT`
- :const:`~src.dignity.certificates.DEFAULT_DISCLAIMERS`
"""

# State primitives
from .state import DignityState13

# Metric functions
from .metric import (
    DEFAULT_WEIGHT_DIAG,
    MetricWeightsV01,
    create_metric_tensor,
    d_degrade,
    d_total,
    geodesic_likeness,
    loop_defect,
    path_energy,
)

# Gate enforcement
from .gates import (
    GateConfig,
    GateViolation,
    GateReport,
    check_gates,
)

# Certificate generation (v0.1)
from .certificates import (
    build_certificate_unsigned,
    attach_signature,
    verify_certificate,
    render_certificate_markdown,
    KeyPair,
    sha256_text,
    sha256_bytes,
    canonical_json_bytes,
    DEFAULT_CONTEXT,
    DEFAULT_DISCLAIMERS,
)

__all__ = [
    # State
    "DignityState13",
    
    # Metric
    "MetricWeightsV01",
    "DEFAULT_WEIGHT_DIAG",
    "create_metric_tensor",
    "d_total",
    "d_degrade",
    "path_energy",
    "geodesic_likeness",
    "loop_defect",
    
    # Gates
    "GateConfig",
    "GateViolation",
    "GateReport",
    "check_gates",
    
    # Certificates
    "build_certificate_unsigned",
    "attach_signature",
    "verify_certificate",
    "render_certificate_markdown",
    "KeyPair",
    "sha256_text",
    "sha256_bytes",
    "canonical_json_bytes",
    "DEFAULT_CONTEXT",
    "DEFAULT_DISCLAIMERS",
]

__version__ = "0.1.0"
