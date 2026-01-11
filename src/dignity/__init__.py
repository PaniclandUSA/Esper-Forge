"""Dignity measurement primitives for ESPER-FORGE.

This package provides the normative v0.1 implementation of the Dignity Metric.

Public API:
- :class:`~src.dignity.state.DignityState13`
- :class:`~src.dignity.metric.MetricWeightsV01`
- :func:`~src.dignity.metric.create_metric_tensor`
- :func:`~src.dignity.metric.d_total`
- :func:`~src.dignity.metric.d_degrade`
- :func:`~src.dignity.metric.path_energy`
- :func:`~src.dignity.metric.geodesic_likeness`
- :func:`~src.dignity.metric.loop_defect`
"""

from .state import DignityState13
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

__all__ = [
    "DignityState13",
    "MetricWeightsV01",
    "DEFAULT_WEIGHT_DIAG",
    "create_metric_tensor",
    "d_total",
    "d_degrade",
    "path_energy",
    "geodesic_likeness",
    "loop_defect",
]
