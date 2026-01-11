"""
Dignity metric functions per docs/09-DIGNITY-METRIC-v0.1.md.

Provides d_total, d_degrade, path_energy, geodesic_likeness computations.
"""

import numpy as np
from typing import List
from .state import DignityState13

def create_metric_tensor(weights: dict = None) -> np.ndarray:
    """Creates the 13×13 metric tensor g."""
    ...

def d_total(x: DignityState13, y: DignityState13, 
            weights: dict = None) -> float:
    """Symmetric total movement distance (Section 5.1)."""
    ...

def d_degrade(x: DignityState13, y: DignityState13, 
              weights: dict = None) -> float:
    """Asymmetric degradation distance (Section 5.2)."""
    ...

def path_energy(path: List[DignityState13], 
                weights: dict = None) -> float:
    """Computes E(γ) for discrete path (Section 6.1)."""
    ...

def geodesic_likeness(path: List[DignityState13], 
                      weights: dict = None) -> float:
    """Computes G(γ) geodesic-likeness score (Section 6.3)."""
    ...

def loop_defect(states: List[DignityState13], 
                weights: dict = None) -> float:
    """Computes Δ_loop for bias detection (Section 7)."""
    ...
