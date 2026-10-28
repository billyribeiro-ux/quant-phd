"""Acceptance suite for the M3 project: the covariance-matrix doctor (covariance_doctor.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your covariance_doctor.py next to this file. Warnings are failures, as in the browser.

Each test checks a property or a number. Only the four conditions that project.html names as ValueError cases
are asserted as ValueError: a matrix that is not square, a matrix that is not symmetric to 1e-9, a volatility that
is not strictly positive, and a volatility list whose length differs from the correlation matrix's. Every other
test asserts a property of a correct answer. Positive semidefiniteness of a result is checked by an independent
Cholesky bisection, not by the eigenvalue routine under test. A failing test names the property it checks and
never prints the value it expected.
"""

from __future__ import annotations

import contextlib
import copy
import io
import math
import os
from collections.abc import Callable
from typing import Any

import covariance_doctor as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(
    SEED + 7_919
)  # a second instance, so a fixed answer for one seed must also match another
K: int = INST["k"]
K2: int = INST2["k"]
Matrix = list[list[float]]


# --- helpers: independent checks, no use of the routine under test


def _is_pd(m: Matrix) -> bool:
    """True when the symmetric matrix is positive definite, by Cholesky with strictly positive pivots."""
    n = len(m)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            total = sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                pivot = m[i][i] - total
                if not pivot > 0.0:
                    return False
                low[i][i] = math.sqrt(pivot)
            else:
                low[i][j] = (m[i][j] - total) / low[j][j]
    return True


def min_eig(m: Matrix) -> float:
    """The smallest eigenvalue, by bisection on the sign of Cholesky pivots of m - t I (no eigenvalue routine)."""
    n = len(m)
    radius = math.sqrt(sum(x * x for row in m for x in row)) + 1.0
    lo, hi = -radius, radius
    for _ in range(200):
        mid = (lo + hi) / 2.0
        shifted = [[m[i][j] - (mid if i == j else 0.0) for j in range(n)] for i in range(n)]
        if _is_pd(shifted):
            lo = mid
        else:
            hi = mid
    return lo


def frob(a: Matrix, b: Matrix) -> float:
    return math.sqrt(sum((a[i][j] - b[i][j]) ** 2 for i in range(len(a)) for j in range(len(a))))


def identity(k: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(k)] for i in range(k)]


def from_spectrum(spectrum: list[float], eigenvectors: list[list[float]]) -> Matrix:
    """sum over m of s_m u_m u_m^T, for the planted eigenvalues s_m and orthonormal vectors u_m (the rows)."""
    k = len(spectrum)
    return [
        [sum(spectrum[m] * eigenvectors[m][i] * eigenvectors[m][j] for m in range(k)) for j in range(k)]
        for i in range(k)
    ]


def shrunk(clip: Matrix, t: float) -> Matrix:
    """The feasible matrix t * clip + (1 - t) * identity: positive semidefinite and unit diagonal for t in [0, 1]."""
    k = len(clip)
    return [[t * clip[i][j] + (1.0 - t) * (1.0 if i == j else 0.0) for j in range(k)] for i in range(k)]


def as_matrix(rows: object, shape: int) -> Matrix:
    """The returned matrix as a list of shape rows of numbers; any other form fails with the rule it breaks."""
    __tracebackhide__ = True
    if not isinstance(rows, (list, tuple)) or len(rows) != shape:
        pytest.fail("a repair must return a square matrix with one row per input row")
    out: Matrix = []
    for row in rows:
        if not isinstance(row, (list, tuple)) or len(row) != shape:
            pytest.fail("a repair must return a square matrix with one row per input row")
        for x in row:
            if isinstance(x, bool) or not isinstance(x, (int, float)):
                pytest.fail("the entries of a returned matrix must be real numbers, not booleans or text")
        out.append([float(x) for x in row])
    return out


def as_number(value: object) -> float:
    __tracebackhide__ = True
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        pytest.fail("the function must return a real number")
    return float(value)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError. Used only for the four conditions the specification names."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError for this input, and none was raised")


def must_not_raise(call: Callable[[], object], condition: str) -> None:
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        pytest.fail(f"{condition}: this input is valid under the specification, and a ValueError was raised")


def symmetric_pair(base: Matrix, i: int, j: int, delta: float) -> Matrix:
    """A copy of base in which entry (i, j) is raised by delta and entry (j, i) is left alone: asymmetric by delta."""
    out = copy.deepcopy(base)
    out[i][j] = out[i][j] + delta
    return out


# --- the named conditions: non-square, and asymmetric beyond 1e-9 (every matrix function)

MATRIX_FUNCS: dict[str, Callable[[Matrix], object]] = {
    "min_eigenvalue": lambda m: sol.min_eigenvalue(m),
    "is_psd": lambda m: sol.is_psd(m),
    "clip_repair": lambda m: sol.clip_repair(m),
    "projection_repair": lambda m: sol.projection_repair(m),
}

NON_SQUARE: dict[str, Matrix] = {
    "two_rows_three_columns": [[1.0, 0.2, 0.1], [0.2, 1.0, 0.3]],
    "three_rows_two_columns": [[1.0, 0.2], [0.2, 1.0], [0.1, 0.3]],
    "ragged_second_row": [[1.0, 0.2], [0.2]],
}


@pytest.mark.parametrize("name", list(MATRIX_FUNCS))
@pytest.mark.parametrize("shape", list(NON_SQUARE))
def test_non_square_is_refused(name: str, shape: str) -> None:
    """A matrix that is not square is one of the four named ValueError conditions, for every matrix function."""
    call = MATRIX_FUNCS[name]
    must_raise(lambda: call(NON_SQUARE[shape]), f"{name} on a non-square matrix ({shape})")


@pytest.mark.parametrize("name", list(MATRIX_FUNCS))
@pytest.mark.parametrize(("i", "j", "sign"), [(0, 1, 1.0), (0, 1, -1.0), (1, 2, 1.0), (1, 2, -1.0)])
def test_asymmetry_beyond_tolerance_is_refused(name: str, i: int, j: int, sign: float) -> None:
    """An asymmetry of 1e-8 is beyond the 1e-9 tolerance, in each direction and on each side of the diagonal."""
    call = MATRIX_FUNCS[name]
    base = [[1.0, 0.3, 0.1], [0.3, 1.0, -0.2], [0.1, -0.2, 1.0]]
    bad = symmetric_pair(base, i, j, sign * 1e-8)
    must_raise(lambda: call(bad), f"{name} on an entry pair that differs by 1e-8")


@pytest.mark.parametrize("name", list(MATRIX_FUNCS))
@pytest.mark.parametrize("sign", [1.0, -1.0])
def test_asymmetry_exactly_the_tolerance_is_accepted(name: str, sign: float) -> None:
    """The page refuses a pair that differs by MORE than 1e-9, so a pair that differs by exactly 1e-9 is accepted.
    The entries 0.0 and 1e-9 make the difference exactly the tolerance in floating point."""
    call = MATRIX_FUNCS[name]
    tie = [[1.0, 0.0], [sign * 1e-9, 1.0]]
    must_not_raise(lambda: call(tie), f"{name} on an entry pair that differs by exactly 1e-9")


@pytest.mark.parametrize("name", list(MATRIX_FUNCS))
@pytest.mark.parametrize("sign", [1.0, -1.0])
def test_asymmetry_within_tolerance_is_accepted(name: str, sign: float) -> None:
    """An asymmetry of 1e-10 is within the 1e-9 tolerance: the function returns a value, in each direction."""
    call = MATRIX_FUNCS[name]
    base = [[1.0, 0.3, 0.1], [0.3, 1.0, -0.2], [0.1, -0.2, 1.0]]
    near = symmetric_pair(base, 0, 1, sign * 1e-10)
    must_not_raise(lambda: call(near), f"{name} on an entry pair that differs by 1e-10")


@pytest.mark.parametrize("name", list(MATRIX_FUNCS))
@pytest.mark.parametrize("sign", [1.0, -1.0])
def test_asymmetry_of_half_the_tolerance_is_accepted_at_large_entries(name: str, sign: float) -> None:
    """The 1e-9 tolerance is absolute: a pair that differs by 5e-10, with entries about 0.3, is accepted."""
    call = MATRIX_FUNCS[name]
    base = [[1.0, 0.3, 0.1], [0.3, 1.0, -0.2], [0.1, -0.2, 1.0]]
    near = symmetric_pair(base, 0, 1, sign * 5e-10)
    must_not_raise(lambda: call(near), f"{name} on an entry pair that differs by 5e-10 at entries about 0.3")


@pytest.mark.parametrize("name", list(MATRIX_FUNCS))
@pytest.mark.parametrize("sign", [1.0, -1.0])
def test_asymmetry_of_twice_the_tolerance_is_refused_at_large_entries(name: str, sign: float) -> None:
    """A pair that differs by 2e-9, with entries about 0.3, is beyond the 1e-9 tolerance and is refused."""
    call = MATRIX_FUNCS[name]
    base = [[1.0, 0.3, 0.1], [0.3, 1.0, -0.2], [0.1, -0.2, 1.0]]
    bad = symmetric_pair(base, 0, 1, sign * 2e-9)
    must_raise(lambda: call(bad), f"{name} on an entry pair that differs by 2e-9 at entries about 0.3")


# --- min_eigenvalue


@pytest.mark.parametrize("inst", [INST, INST2], ids=["seed", "second_seed"])
def test_min_eigenvalue_matches_planted_spectrum(inst: dict[str, Any]) -> None:
    """A matrix built from planted eigenvalues s and orthonormal u: its smallest eigenvalue is min(s)."""
    a = from_spectrum(inst["spectrum"], inst["eigenvectors"])
    value = as_number(sol.min_eigenvalue(a))
    assert abs(value - min(inst["spectrum"])) <= 1e-8 * max(1.0, max(abs(s) for s in inst["spectrum"])), (
        "min_eigenvalue must return the smallest eigenvalue of the planted matrix, not another eigenvalue"
    )


def test_min_eigenvalue_is_smallest_of_diagonal() -> None:
    """For a diagonal matrix the eigenvalues are the diagonal entries: the smallest is -2 here, not the largest 5."""
    value = as_number(sol.min_eigenvalue([[3.0, 0.0, 0.0], [0.0, -2.0, 0.0], [0.0, 0.0, 5.0]]))
    assert abs(value + 2.0) <= 1e-12, "min_eigenvalue of diag(3, -2, 5) must be -2"


def test_min_eigenvalue_one_by_one() -> None:
    value = as_number(sol.min_eigenvalue([[-0.25]]))
    assert abs(value + 0.25) <= 1e-12, "min_eigenvalue of a one-by-one matrix is its only entry"


def test_min_eigenvalue_repeated_eigenvalue() -> None:
    """diag(-1, -1, 3) has the repeated eigenvalue -1 and the eigenvalue 3: the smallest is -1."""
    value = as_number(sol.min_eigenvalue([[-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 3.0]]))
    assert abs(value + 1.0) <= 1e-12, "min_eigenvalue must return the smallest eigenvalue when it is repeated"


def test_min_eigenvalue_all_negative_spectrum() -> None:
    """-2 times the identity has every eigenvalue equal to -2: the smallest is -2, not 0 and not a positive value."""
    value = as_number(sol.min_eigenvalue([[-2.0, 0.0, 0.0], [0.0, -2.0, 0.0], [0.0, 0.0, -2.0]]))
    assert abs(value + 2.0) <= 1e-12, "min_eigenvalue of -2 times the identity must be -2"


@pytest.mark.parametrize("inst", [INST, INST2], ids=["seed", "second_seed"])
def test_min_eigenvalue_agrees_with_independent_bisection(inst: dict[str, Any]) -> None:
    """On the seeded pairwise matrix, the routine agrees with the Cholesky bisection to 1e-9."""
    value = as_number(sol.min_eigenvalue(inst["corr"]))
    assert abs(value - min_eig(inst["corr"])) <= 1e-9, (
        "min_eigenvalue disagrees with an independent check of the same matrix"
    )


# --- is_psd


def test_is_psd_accepts_planted_zero_eigenvalue() -> None:
    """A rank-deficient positive semidefinite matrix has a zero eigenvalue; rounding must not reject it at the
    default tolerance."""
    for inst in (INST, INST2):
        a = from_spectrum(inst["psd_spectrum"], inst["eigenvectors"])
        assert sol.is_psd(a) is True, (
            "is_psd must accept a positive semidefinite matrix whose smallest eigenvalue is zero"
        )
        assert sol.is_psd(inst["psd_corr"]) is True, "is_psd must accept a positive definite matrix"


@pytest.mark.parametrize(("value", "expected"), [(-0.05, False), (0.05, True)], ids=["negative", "positive"])
def test_is_psd_sign_of_smallest_eigenvalue(value: float, expected: bool) -> None:
    """Planted smallest eigenvalue -0.05 is not positive semidefinite; +0.05 is, on both sides of zero."""
    spectrum = [*INST["psd_spectrum"][1:], value]
    a = from_spectrum(spectrum, INST["eigenvectors"])
    assert sol.is_psd(a) is expected, "is_psd does not give the right verdict for the planted smallest eigenvalue"


def test_is_psd_tolerance_boundary_on_both_sides() -> None:
    """A smallest eigenvalue of -1e-6 passes a tolerance of 1e-5 and fails a tolerance of 1e-8."""
    a = from_spectrum([*INST["psd_spectrum"][1:], -1e-6], INST["eigenvectors"])
    assert sol.is_psd(a, tol=1e-5) is True, "is_psd must accept an eigenvalue above -tol"
    assert sol.is_psd(a, tol=1e-8) is False, "is_psd must reject an eigenvalue below -tol"


def test_is_psd_threshold_is_minus_tol_on_a_diagonal_matrix() -> None:
    """diag(-0.5, 1, 1) has smallest eigenvalue -0.5: accepted at tol 0.5 + 1e-6, refused at tol 0.5 - 1e-6."""
    a = [[-0.5, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    assert sol.is_psd(a, tol=0.5 + 1e-6) is True, "is_psd must accept a smallest eigenvalue above -tol"
    assert sol.is_psd(a, tol=0.5 - 1e-6) is False, "is_psd must reject a smallest eigenvalue below -tol"


def test_is_psd_one_by_one() -> None:
    assert sol.is_psd([[0.0]]) is True, "the zero matrix is positive semidefinite"
    assert sol.is_psd([[-0.1]]) is False, "a negative one-by-one matrix is not positive semidefinite"


def test_is_psd_rejects_pairwise_matrix() -> None:
    """The seeded pairwise matrix is not positive semidefinite by a margin of 0.02 (the instance guarantees it)."""
    assert sol.is_psd(INST["corr"]) is False, "is_psd must reject the seeded pairwise matrix"


# --- clip_repair


@pytest.mark.parametrize("inst", [INST, INST2], ids=["seed", "second_seed"])
def test_clip_repair_has_unit_diagonal_and_is_symmetric(inst: dict[str, Any]) -> None:
    y = as_matrix(sol.clip_repair(inst["corr"]), inst["k"])
    assert all(abs(y[i][i] - 1.0) <= 1e-9 for i in range(inst["k"])), "clip_repair output must have unit diagonal"
    assert all(abs(y[i][j] - y[j][i]) <= 1e-12 for i in range(inst["k"]) for j in range(inst["k"])), (
        "clip_repair output must be symmetric"
    )


@pytest.mark.parametrize("inst", [INST, INST2], ids=["seed", "second_seed"])
def test_clip_repair_is_positive_semidefinite(inst: dict[str, Any]) -> None:
    y = as_matrix(sol.clip_repair(inst["corr"]), inst["k"])
    assert min_eig(y) >= -1e-9, "clip_repair output must be positive semidefinite (smallest eigenvalue at least -1e-9)"


def test_clip_repair_two_by_two_clips_to_rank_one() -> None:
    """[[1, 1.2], [1.2, 1]] has eigenvalues 2.2 and -0.2. Clipping sets -0.2 to 0; rescaling gives off-diagonal 1."""
    y = as_matrix(sol.clip_repair([[1.0, 1.2], [1.2, 1.0]]), 2)
    assert abs(y[0][1] - 1.0) <= 1e-9 and abs(y[1][0] - 1.0) <= 1e-9, (
        "clipping the negative eigenvalue of this two-by-two matrix must give off-diagonal 1 after rescaling"
    )


def test_clip_repair_leaves_positive_definite_unit_matrix_unchanged() -> None:
    for inst in (INST, INST2):
        y = as_matrix(sol.clip_repair(inst["psd_corr"]), inst["k"])
        worst = max(abs(y[i][j] - inst["psd_corr"][i][j]) for i in range(inst["k"]) for j in range(inst["k"]))
        assert worst <= 1e-9, "clip_repair must return a positive semidefinite unit-diagonal matrix unchanged"


def test_clip_repair_one_by_one_is_one() -> None:
    y = as_matrix(sol.clip_repair([[1.0]]), 1)
    assert abs(y[0][0] - 1.0) <= 1e-12, "the one-by-one repair of [[1]] is [[1]]"


def test_clip_repair_with_positive_floor_is_positive_semidefinite() -> None:
    y = as_matrix(sol.clip_repair(INST["corr"], floor=0.01), K)
    assert min_eig(y) >= -1e-9, "clip_repair with floor 0.01 must still return a positive semidefinite matrix"


def test_clip_repair_floor_raises_eigenvalues_below_it() -> None:
    """Planted eigenvalues -0.3 and 0.004 lie below the floor 0.01 and the others above it: clip_repair must equal
    the rescaled matrix whose eigenvalues are max(s, 0.01). A routine that clips at zero fails this."""
    spectrum = [-0.3, 0.004] + [1.0] * (K - 2)
    raised = from_spectrum([max(s, 0.01) for s in spectrum], INST["eigenvectors"])
    d = [raised[i][i] for i in range(K)]
    expected = [[raised[i][j] / math.sqrt(d[i] * d[j]) for j in range(K)] for i in range(K)]
    y = as_matrix(sol.clip_repair(from_spectrum(spectrum, INST["eigenvectors"]), floor=0.01), K)
    worst = max(abs(y[i][j] - expected[i][j]) for i in range(K) for j in range(K))
    assert worst <= 1e-9, "clip_repair must set every eigenvalue below the floor to the floor, then rescale"


def test_clip_repair_floor_below_every_eigenvalue_changes_nothing() -> None:
    """Eigenvalues are set to the floor only when they are below it: with floor -0.5, which lies below every
    eigenvalue of a positive definite unit-diagonal matrix, the matrix comes back unchanged."""
    for inst in (INST, INST2):
        y = as_matrix(sol.clip_repair(inst["psd_corr"], floor=-0.5), inst["k"])
        worst = max(abs(y[i][j] - inst["psd_corr"][i][j]) for i in range(inst["k"]) for j in range(inst["k"]))
        assert worst <= 1e-9, "clip_repair must set only the eigenvalues that lie below the floor"


# --- projection_repair


@pytest.mark.parametrize("inst", [INST, INST2], ids=["seed", "second_seed"])
def test_projection_repair_is_a_valid_repair(inst: dict[str, Any]) -> None:
    y = as_matrix(sol.projection_repair(inst["corr"]), inst["k"])
    assert all(abs(y[i][i] - 1.0) <= 1e-8 for i in range(inst["k"])), (
        "projection_repair output must have unit diagonal to 1e-8"
    )
    assert all(abs(y[i][j] - y[j][i]) <= 1e-9 for i in range(inst["k"]) for j in range(inst["k"])), (
        "projection_repair output must be symmetric"
    )
    assert min_eig(y) >= -1e-8, "projection_repair output must be positive semidefinite to 1e-8"


@pytest.mark.parametrize("inst", [INST, INST2], ids=["seed", "second_seed"])
def test_projection_repair_is_no_farther_than_clipping(inst: dict[str, Any]) -> None:
    """The Frobenius-nearest repair is no farther from the input than any other valid repair, clipping included."""
    y = as_matrix(sol.projection_repair(inst["corr"]), inst["k"])
    clip = as_matrix(sol.clip_repair(inst["corr"]), inst["k"])
    assert frob(y, inst["corr"]) <= frob(clip, inst["corr"]) + 1e-6, (
        "projection_repair must be at least as close to the input as clip_repair (the Frobenius-nearest property)"
    )


@pytest.mark.parametrize("inst", [INST, INST2], ids=["seed", "second_seed"])
def test_projection_repair_is_no_farther_than_shrunk_clipping(inst: dict[str, Any]) -> None:
    """Every t * clip + (1 - t) * identity, t in [0, 1], is valid; the nearest repair is no farther than the
    nearest of them."""
    y = as_matrix(sol.projection_repair(inst["corr"]), inst["k"])
    clip = as_matrix(sol.clip_repair(inst["corr"]), inst["k"])
    best = min(frob(shrunk(clip, t / 200.0), inst["corr"]) for t in range(201))
    assert frob(y, inst["corr"]) <= best + 1e-6, (
        "projection_repair is farther from the input than a valid shrunk matrix"
    )


# The illustrative matrix and volatilities of Lab 3 (project.html), and the numbers Lab 3 prints for them.
LAB3_CORR: Matrix = [
    [1.0, 0.7, 0.3, -0.6],
    [0.7, 1.0, 0.5, 0.4],
    [0.3, 0.5, 1.0, 0.2],
    [-0.6, 0.4, 0.2, 1.0],
]
LAB3_VOLS: list[float] = [0.10, 0.20, 0.15, 0.30]


def as_number_list(values: object, n: int) -> list[float]:
    __tracebackhide__ = True
    if not isinstance(values, (list, tuple)) or len(values) != n:
        pytest.fail("comparison_weights must return one weight per asset")
    return [as_number(x) for x in values]


def test_lab3_reference_numbers_are_matched() -> None:
    """The specification requires the module to match the printed numbers of Lab 3's matrix. Clipping is exact, so
    its printed numbers are checked to 1e-6; the projection is an iteration, so its numbers are checked to 1e-5, which
    is far below the printed gap between the two repairs (0.001570 in distance, 0.011516 in entries). The weights are
    those of the input, whose Sigma is invertible. No weights are checked for the repairs."""
    n = 4
    clip = as_matrix(sol.clip_repair(LAB3_CORR), n)
    proj = as_matrix(sol.projection_repair(LAB3_CORR), n)
    checks: list[tuple[str, float, float, float]] = [
        ("smallest eigenvalue of the input", as_number(sol.min_eigenvalue(LAB3_CORR)), -0.142113, 1e-6),
        ("distance of clipping from the input", frob(clip, LAB3_CORR), 0.176573, 1e-6),
        ("distance of the projection from the input", frob(proj, LAB3_CORR), 0.175003, 1e-5),
        (
            "largest entry difference, projection minus clipping",
            max(abs(proj[i][j] - clip[i][j]) for i in range(n) for j in range(n)),
            0.011516,
            1e-5,
        ),
    ]
    w_input = as_number_list(sol.comparison_weights(LAB3_CORR, LAB3_VOLS), n)
    for got, want in zip(w_input, [1.778929, -1.096718, -0.255613, 0.573402], strict=True):
        checks.append(("a weight of the input", got, want, 1e-6))
    for name, got, want, tol in checks:
        assert abs(got - want) <= tol, f"Lab 3 reference number not matched: {name}"


def test_projection_repair_leaves_positive_definite_unit_matrix_unchanged() -> None:
    for inst in (INST, INST2):
        y = as_matrix(sol.projection_repair(inst["psd_corr"]), inst["k"])
        worst = max(abs(y[i][j] - inst["psd_corr"][i][j]) for i in range(inst["k"]) for j in range(inst["k"]))
        assert worst <= 1e-8, "projection_repair must return a positive semidefinite unit-diagonal matrix unchanged"


def test_projection_repair_two_by_two_nearest_has_correlation_one() -> None:
    """Among unit-diagonal positive semidefinite 2x2 matrices, |rho| <= 1; the one nearest to rho = 1.2 has rho = 1."""
    y = as_matrix(sol.projection_repair([[1.0, 1.2], [1.2, 1.0]]), 2)
    assert abs(y[0][1] - 1.0) <= 1e-6, "projection_repair of [[1, 1.2], [1.2, 1]] must have off-diagonal 1"


def test_projection_repair_one_by_one_is_one() -> None:
    y = as_matrix(sol.projection_repair([[1.0]]), 1)
    assert abs(y[0][0] - 1.0) <= 1e-12, "the one-by-one repair of [[1]] is [[1]]"


# --- comparison_weights


def weights_sum_check(w: list[float], k: int) -> None:
    __tracebackhide__ = True
    if len(w) != k:
        pytest.fail("comparison_weights must return one weight per asset")
    for x in w:
        as_number(x)


@pytest.mark.parametrize("inst", [INST, INST2], ids=["seed", "second_seed"])
def test_weights_sum_to_one(inst: dict[str, Any]) -> None:
    w = sol.comparison_weights(inst["psd_corr"], inst["vols"])
    weights_sum_check(w, inst["k"])
    assert abs(sum(w) - 1.0) <= 1e-12, "comparison_weights must return weights that sum to 1"


def test_weights_two_asset_closed_form() -> None:
    """With Sigma = D C D and two assets, Sigma^-1 1 is proportional to (b(b - rho a), a(a - rho b)), with a, b
    the vols."""
    a, b = INST["vols"][0], INST["vols"][1]
    rho = INST["psd_corr"][0][1]
    w = sol.comparison_weights([[1.0, rho], [rho, 1.0]], [a, b])
    denom = a * a + b * b - 2.0 * rho * a * b
    expected = [b * (b - rho * a) / denom, a * (a - rho * b) / denom]
    assert all(abs(w[i] - expected[i]) <= 1e-9 for i in range(2)), (
        "comparison_weights disagrees with the two-asset closed form"
    )


@pytest.mark.parametrize("inst", [INST, INST2], ids=["seed", "second_seed"])
def test_weights_with_identity_correlation_are_inverse_variance(inst: dict[str, Any]) -> None:
    """With C = I, Sigma is diagonal with entries v^2, and Sigma^-1 1 gives weights proportional to 1 / v^2."""
    k = inst["k"]
    w = sol.comparison_weights(identity(k), inst["vols"])
    raw = [1.0 / (v * v) for v in inst["vols"]]
    total = sum(raw)
    assert all(abs(w[i] - raw[i] / total) <= 1e-9 for i in range(k)), (
        "with identity correlation the weights must be proportional to the inverse squared volatilities"
    )


@pytest.mark.parametrize("inst", [INST, INST2], ids=["seed", "second_seed"])
def test_weights_solve_sigma_times_weights_proportional_to_ones(inst: dict[str, Any]) -> None:
    """The defining property: Sigma w is a constant vector, where Sigma = D C D."""
    k = inst["k"]
    c, v = inst["psd_corr"], inst["vols"]
    sigma = [[v[i] * c[i][j] * v[j] for j in range(k)] for i in range(k)]
    w = sol.comparison_weights(c, v)
    sw = [sum(sigma[i][j] * w[j] for j in range(k)) for i in range(k)]
    scale = max(abs(x) for x in sw)
    assert max(sw) - min(sw) <= 1e-9 * scale, (
        "Sigma times the weights must be a constant vector (weights proportional to Sigma^-1 1)"
    )


@pytest.mark.parametrize("inst", [INST, INST2], ids=["seed", "second_seed"])
def test_weights_do_not_change_when_every_volatility_is_scaled(inst: dict[str, Any]) -> None:
    """Scaling every volatility by 3 scales Sigma by 9 and Sigma^-1 1 by 1/9; the normalised weights do not change."""
    base = sol.comparison_weights(inst["psd_corr"], inst["vols"])
    scaled = sol.comparison_weights(inst["psd_corr"], [3.0 * v for v in inst["vols"]])
    assert all(abs(base[i] - scaled[i]) <= 1e-9 for i in range(inst["k"])), (
        "comparison_weights must not change when all volatilities are multiplied by the same positive number"
    )


def test_weights_one_asset() -> None:
    w = sol.comparison_weights([[1.0]], [0.2])
    weights_sum_check(w, 1)
    assert abs(w[0] - 1.0) <= 1e-12, "a single asset has weight 1"


@pytest.mark.parametrize("shape", list(NON_SQUARE))
def test_weights_refuse_non_square_correlation(shape: str) -> None:
    """One volatility per row is supplied, so the only condition the input breaks is squareness."""
    corr = NON_SQUARE[shape]
    must_raise(
        lambda: sol.comparison_weights(corr, [0.1] * len(corr)),
        f"a non-square correlation matrix ({shape})",
    )


@pytest.mark.parametrize(("i", "j"), [(0, 1), (1, 0)], ids=["upper", "lower"])
@pytest.mark.parametrize("sign", [1.0, -1.0])
def test_weights_refuse_asymmetric_correlation_beyond_tolerance(i: int, j: int, sign: float) -> None:
    """An asymmetry of 1e-8 is beyond the 1e-9 tolerance, in each direction and on each side of the diagonal."""
    base = [[1.0, 0.3], [0.3, 1.0]]
    bad = symmetric_pair(base, i, j, sign * 1e-8)
    must_raise(lambda: sol.comparison_weights(bad, [0.1, 0.2]), "an asymmetric correlation matrix (1e-8 apart)")


@pytest.mark.parametrize(("i", "j"), [(0, 1), (1, 0)], ids=["upper", "lower"])
@pytest.mark.parametrize("sign", [1.0, -1.0])
def test_weights_accept_asymmetry_within_tolerance(i: int, j: int, sign: float) -> None:
    """An asymmetry of 1e-10 is within the 1e-9 tolerance, in each direction and on each side of the diagonal."""
    base = [[1.0, 0.3], [0.3, 1.0]]
    near = symmetric_pair(base, i, j, sign * 1e-10)
    weights_sum_check(sol.comparison_weights(near, [0.1, 0.2]), 2)


@pytest.mark.parametrize(("i", "j"), [(0, 1), (1, 0)], ids=["upper", "lower"])
@pytest.mark.parametrize("sign", [1.0, -1.0])
def test_weights_accept_half_tolerance_asymmetry_at_large_entries(i: int, j: int, sign: float) -> None:
    """The tolerance is absolute: a pair that differs by 5e-10, with entries about 0.3, is accepted."""
    near = symmetric_pair([[1.0, 0.3], [0.3, 1.0]], i, j, sign * 5e-10)
    weights_sum_check(sol.comparison_weights(near, [0.1, 0.2]), 2)


@pytest.mark.parametrize(("i", "j"), [(0, 1), (1, 0)], ids=["upper", "lower"])
@pytest.mark.parametrize("sign", [1.0, -1.0])
def test_weights_refuse_twice_tolerance_asymmetry_at_large_entries(i: int, j: int, sign: float) -> None:
    """A pair that differs by 2e-9, with entries about 0.3, is beyond the 1e-9 tolerance and is refused."""
    bad = symmetric_pair([[1.0, 0.3], [0.3, 1.0]], i, j, sign * 2e-9)
    must_raise(lambda: sol.comparison_weights(bad, [0.1, 0.2]), "an asymmetric correlation matrix (2e-9 apart)")


@pytest.mark.parametrize("position", [0, 1, 2], ids=["first", "middle", "last"])
@pytest.mark.parametrize("bad", [0.0, -0.05], ids=["zero", "negative"])
def test_weights_refuse_volatility_at_or_below_zero(bad: float, position: int) -> None:
    """A volatility of exactly zero, or a negative one, is refused in any position: the rule is a volatility
    strictly greater than zero. The other volatilities are valid and the lengths agree."""
    corr = [[1.0, 0.2, 0.1], [0.2, 1.0, 0.0], [0.1, 0.0, 1.0]]
    vols = [0.1, 0.2, 0.3]
    vols[position] = bad
    must_raise(lambda: sol.comparison_weights(corr, vols), f"a volatility that is not positive (position {position})")


def test_weights_accept_a_tiny_positive_volatility() -> None:
    """A volatility of 1e-6 is strictly positive, so it is accepted: the boundary is on the zero side."""
    w = sol.comparison_weights([[1.0, 0.2], [0.2, 1.0]], [1e-6, 0.2])
    weights_sum_check(w, 2)
    assert abs(sum(w) - 1.0) <= 1e-12, (
        "comparison_weights must return weights that sum to 1 for a tiny positive volatility"
    )


@pytest.mark.parametrize("mode", ["empty", "shorter", "longer"])
def test_weights_refuse_length_mismatch(mode: str) -> None:
    """One volatility per row is required: an empty list, one entry short and one entry long are all refused."""
    vols = {"empty": [], "shorter": INST["vols"][:-1], "longer": [*INST["vols"], 0.2]}[mode]
    must_raise(
        lambda: sol.comparison_weights(INST["psd_corr"], vols), f"a volatility list that is {mode} than the matrix"
    )


def test_weights_accept_matching_length() -> None:
    weights_sum_check(sol.comparison_weights(INST["psd_corr"], INST["vols"]), K)


# --- purity and printing


def test_functions_print_nothing() -> None:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        sol.min_eigenvalue(INST["corr"])
        sol.is_psd(INST["corr"])
        sol.clip_repair(INST["corr"])
        sol.projection_repair(INST["corr"])
        sol.comparison_weights(INST["psd_corr"], INST["vols"])
    assert buffer.getvalue() == "", "no function may print"


def test_inputs_are_not_mutated() -> None:
    corr = copy.deepcopy(INST["corr"])
    vols = copy.deepcopy(INST["vols"])
    sol.clip_repair(corr)
    sol.projection_repair(corr)
    sol.min_eigenvalue(corr)
    sol.comparison_weights(INST["psd_corr"], vols)
    assert corr == INST["corr"], "a repair must not change the matrix it is given"
    assert vols == INST["vols"], "comparison_weights must not change the volatilities it is given"


def test_repeated_calls_agree() -> None:
    first = as_matrix(sol.projection_repair(INST["corr"]), K)
    second = as_matrix(sol.projection_repair(INST["corr"]), K)
    assert max(abs(first[i][j] - second[i][j]) for i in range(K) for j in range(K)) <= 1e-12, (
        "projection_repair must give the same answer on repeated calls"
    )
