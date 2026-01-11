"""
Compile gate enforcement per docs/09-DIGNITY-METRIC-v0.1.md Section 8.

Gates enforce "must never happen" boundaries.
"""

from dataclasses import dataclass
from typing import List, Optional
from .state import DignityState13

@dataclass
class GateViolation:
    """Records a single gate violation."""
    coordinate: str
    value: float
    threshold: float
    severity: str  # "critical" | "warning"

@dataclass
class GateReport:
    """Complete gate check report."""
    passed: bool
    violations: List[GateViolation]
    warnings: List[str]

class GateConfig:
    """Gate thresholds per Section 8.1 defaults."""
    A_MIN: float = 0.95
    T_MIN: float = 0.95
    T_CAUSAL_MIN: float = 0.99  # Stricter for causality
    C_MIN: float = 0.80
    M_MIN: float = 0.95

def check_gates(state: DignityState13, 
                config: Optional[GateConfig] = None) -> GateReport:
    """Checks all compile gates (Section 8.2)."""
    ...
