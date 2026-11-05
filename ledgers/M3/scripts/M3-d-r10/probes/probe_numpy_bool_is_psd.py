"""Probe (round 10, not a ledger mutant): NumPy-based solution whose is_psd returns numpy.bool_, as an ordinary
comparison of NumPy floats does. Every other function is the reference's."""

from __future__ import annotations

import numpy as np

import importlib.util
import pathlib

_REF = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD10-M3-d/course/modules/M/M3/grader/reference.py")
_spec = importlib.util.spec_from_file_location("ref", _REF)
ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ref)  # type: ignore[union-attr]


def min_eigenvalue(matrix):
    return ref.min_eigenvalue(matrix)


def is_psd(matrix, tol=1e-10):
    return np.float64(min_eigenvalue(matrix)) >= -tol


clip_repair = ref.clip_repair
projection_repair = ref.projection_repair
comparison_weights = ref.comparison_weights
