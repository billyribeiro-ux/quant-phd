"""Verifier round-3 alternative A-brute: exhaustive enumeration of working sets in float arithmetic.

Validation and the case parser are the reference's (copied unchanged below); the solver is a different method: it
enumerates every set of up to n-1 inequality rows (bounds, sector caps and the 2**n sign forms of the turnover limit),
solves the equality-constrained KKT system for each set in floats, and returns the first set whose primal point is
feasible and whose multipliers are non-negative. The certificate is recomputed with the page's definitions in floats.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from itertools import combinations, product
from typing import Any

FLOAT_TOL = 1e-10
