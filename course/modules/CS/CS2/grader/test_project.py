"""Acceptance suite for the CS2 project: streamstats.py.

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with streamstats.py importable from the same directory. Warnings are failures, as in the browser.

Each test checks a property or a number that the specification on the project page states. A failure names the
property it checks and never prints the expected value. The exact reference is Fraction arithmetic on the floats of
the stream, so the tolerances (relative 1e-9, absolute floor 1e-9) are about the library and not about rounding in
the reference. Tests that expect a ValueError do so only for the conditions the specification names. For every
other invalid input the test accepts either an exception of any type or a correct answer, and nothing else.
"""

from __future__ import annotations

import ast
import contextlib
import itertools
import json
import math
import os
import sys
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]  # the grader's own generator
from streamstats import (  # type: ignore[import-not-found, unused-ignore]  # the learner's library, read as source
    QuantileSketch,
    RollingMinMax,
    WelfordAccumulator,
)

pytestmark = pytest.mark.filterwarnings("error")  # the specification: no function warns

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
PAYLOAD: dict[str, Any] = json.loads(INST["payload"])
INVALID: dict[str, Any] = json.loads(INST["invalid"])
VALUES: list[float] = [float(x) for x in PAYLOAD["values"]]
N: int = len(VALUES)
WINDOW: int = PAYLOAD["window"]
EPS: float = PAYLOAD["epsilon"]
PROBES: list[float] = [float(q) for q in PAYLOAD["probes"]]


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail with the named condition unless call() raises ValueError."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError, and none was raised.")


def must_accept(call: Callable[[], Any], condition: str) -> Any:
    """Return call()'s value unless it raises ValueError, which the specification forbids here."""
    __tracebackhide__ = True
    try:
        return call()
    except ValueError:
        pytest.fail(f"{condition}: the specification accepts this input, so a ValueError is wrong.")


def refuse_or_correct(action: Callable[[], Any], correct: Any, property_name: str) -> None:
    """For an input the specification does not name: an exception of any type, or the correct answer."""
    __tracebackhide__ = True
    try:
        answer = action()
    except NotImplementedError:
        raise
    except Exception:
        return
    if answer is None or not close(float(answer), float(correct)):
        pytest.fail(f"{property_name}: the call returned an answer that is not the correct one.")


def close(a: float, b: float, rel: float = 1e-9, absolute: float = 1e-9) -> bool:
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(absolute, rel * max(abs(a), abs(b)))


def exact_stats(values: list[float]) -> tuple[Fraction, Fraction, Fraction]:
    """Exact mean, sample variance and population variance of the given floats (as Fractions)."""
    fr = [Fraction(x) for x in values]
    n = len(fr)
    mean = sum(fr, Fraction(0)) / n
    m2 = sum(((x - mean) ** 2 for x in fr), Fraction(0))
    sample = m2 / (n - 1) if n > 1 else Fraction(0)
    return mean, sample, m2 / n


def sketch_of(values: list[float], eps: float) -> QuantileSketch:
    sketch = QuantileSketch(eps)
    for x in values:
        sketch.add(x)
    return sketch


# ------------------------------------------------------------------ the instance and the standard library


def test_instance_is_deterministic() -> None:
    again = make_instance(SEED)
    if again != INST:
        pytest.fail("make_instance must return the same instance for the same seed.")


def test_instance_is_valid_and_labelled_simulated() -> None:
    if not (20 <= N <= 400):
        pytest.fail("the stream must hold between 20 and 400 values.")
    if not all(math.isfinite(x) for x in VALUES):
        pytest.fail("every value of the stream must be finite.")
    if not (2 <= WINDOW <= 30):
        pytest.fail("the window must be between 2 and 30.")
    if EPS not in (0.05, 0.1, 0.2):
        pytest.fail("epsilon must be one of 0.05, 0.1 and 0.2.")
    if len(PROBES) != 10 or not all(0.0 <= q <= 1.0 for q in PROBES):
        pytest.fail("the instance must give ten probe quantiles in [0, 1].")
    if "SIMULATED" not in INST["label"]:
        pytest.fail("every instance must be labelled SIMULATED.")


def test_standard_library_only() -> None:
    path = Path(__file__).resolve().parent / "streamstats.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module.split(".")[0])
    outside = sorted(name for name in names if name not in sys.stdlib_module_names)
    if outside:
        pytest.fail("streamstats.py may import only the standard library.")


def test_invalid_case_is_refused() -> None:
    kind = INVALID["kind"]
    if kind == "window_zero":
        must_raise(lambda: RollingMinMax(0), "a window below one")
    elif kind == "epsilon_one":
        must_raise(lambda: QuantileSketch(1.0), "an epsilon of one or more")
    elif kind == "q_above_one":
        sketch = sketch_of(VALUES, EPS)
        must_raise(lambda: sketch.quantile(1.5), "a quantile above one")
    elif kind == "welford_nan":
        must_raise(lambda: WelfordAccumulator().update(float("nan")), "a NaN added to the Welford accumulator")
    elif kind == "rolling_nan":
        must_raise(lambda: RollingMinMax(WINDOW).push(float("nan")), "a NaN pushed to the rolling minimum and maximum")
    elif kind == "sketch_nan":
        must_raise(lambda: QuantileSketch(EPS).add(float("nan")), "a NaN added to the quantile sketch")
    else:
        pytest.fail("the instance names an invalid case the grader does not know.")


# ------------------------------------------------------------------ Welford: named conditions


def test_welford_count_starts_at_zero() -> None:
    if WelfordAccumulator().count != 0:
        pytest.fail("a new accumulator must hold no values.")


def test_welford_mean_before_any_value_raises() -> None:
    must_raise(lambda: WelfordAccumulator().mean(), "mean() before any value")


def test_welford_variance_before_any_value_raises() -> None:
    must_raise(lambda: WelfordAccumulator().variance(), "variance() before any value")


def test_welford_population_variance_before_any_value_raises() -> None:
    must_raise(lambda: WelfordAccumulator().variance(0), "variance(0) before any value")


def test_welford_sample_variance_of_one_value_raises() -> None:
    acc = WelfordAccumulator()
    acc.update(VALUES[0])
    must_raise(lambda: acc.variance(1), "variance(1) with one value")


def test_welford_population_variance_of_one_value_is_zero() -> None:
    acc = WelfordAccumulator()
    acc.update(VALUES[0])
    if acc.variance(0) != 0.0:
        pytest.fail("the population variance of one value is zero.")


def test_welford_sample_variance_of_two_values_is_defined() -> None:
    acc = WelfordAccumulator()
    acc.update(1.0)
    acc.update(3.0)
    if not close(must_accept(lambda: acc.variance(1), "variance(1) with two values"), 2.0):
        pytest.fail("the sample variance of 1 and 3 is 2.")


def test_welford_nan_update_raises() -> None:
    acc = WelfordAccumulator()
    acc.update(VALUES[0])
    must_raise(lambda: acc.update(float("nan")), "a NaN update")


def test_welford_nan_first_value_raises() -> None:
    must_raise(lambda: WelfordAccumulator().update(float("nan")), "a NaN as the first value")


def test_welford_constant_stream_has_zero_variance() -> None:
    acc = WelfordAccumulator()
    for _ in range(10):
        acc.update(5.0)
    if not close(acc.mean(), 5.0) or acc.variance(1) != 0.0:
        pytest.fail("on a stream of one repeated value, the mean is that value and the sample variance is zero.")


def test_welford_count_is_read_only_int() -> None:
    acc = WelfordAccumulator()
    acc.update(VALUES[0])
    if type(acc.count) is not int:
        pytest.fail("count must be an int.")
    with contextlib.suppress(Exception):  # refusing the assignment is allowed; so is ignoring it
        acc.count = 99  # a learner may refuse this assignment or ignore it
    if acc.count != 1:
        pytest.fail("count is a read-only property: assigning to it must not change the number of values.")


def test_classes_never_print(capsys: pytest.CaptureFixture[str]) -> None:
    acc = WelfordAccumulator()
    for x in VALUES[:5]:
        acc.update(x)
    acc.mean()
    acc.variance(1)
    rolling = RollingMinMax(WINDOW)
    for x in VALUES[:5]:
        rolling.push(x)
    rolling.minimum()
    rolling.maximum()
    sketch = sketch_of(VALUES[:5], EPS)
    sketch.quantile(0.5)
    captured = capsys.readouterr()
    if captured.out or captured.err:
        pytest.fail("the three classes must never print: the output of a call to them is not empty.")


def test_welford_bool_input_is_refused_or_denotes_one() -> None:
    acc = WelfordAccumulator()
    acc.update(1.0)
    refuse_or_correct(lambda: (acc.update(True), acc.mean())[1], 1.0, "True passed as a value")


def test_welford_padded_string_is_refused_or_correct() -> None:
    acc = WelfordAccumulator()
    acc.update(1.0)
    refuse_or_correct(lambda: (acc.update(" 2.5 "), acc.mean())[1], 1.75, "a padded string passed as a value")


# ------------------------------------------------------------------ Welford: values against the exact reference


def test_welford_count_equals_stream_length() -> None:
    acc = WelfordAccumulator()
    for x in VALUES:
        acc.update(x)
    if acc.count != N:
        pytest.fail("count must equal the number of values added.")


def test_welford_mean_matches_exact_reference() -> None:
    acc = WelfordAccumulator()
    for x in VALUES:
        acc.update(x)
    mean, _, _ = exact_stats(VALUES)
    if not close(acc.mean(), float(mean)):
        pytest.fail("the mean differs from the exact mean of the stream beyond 1e-9 relative.")


def test_welford_sample_variance_matches_exact_reference() -> None:
    acc = WelfordAccumulator()
    for x in VALUES:
        acc.update(x)
    _, sample, _ = exact_stats(VALUES)
    if not close(acc.variance(1), float(sample)):
        pytest.fail("the sample variance differs from the exact value beyond 1e-9 relative (see the update formula).")


def test_welford_population_variance_matches_exact_reference() -> None:
    acc = WelfordAccumulator()
    for x in VALUES:
        acc.update(x)
    _, _, population = exact_stats(VALUES)
    if not close(acc.variance(0), float(population)):
        pytest.fail("the population variance differs from the exact value beyond 1e-9 relative.")


@pytest.mark.parametrize("prefix", range(2, 21))
def test_welford_every_short_prefix_matches_exact(prefix: int) -> None:
    acc = WelfordAccumulator()
    for x in VALUES[:prefix]:
        acc.update(x)
    mean, sample, _ = exact_stats(VALUES[:prefix])
    if not (close(acc.mean(), float(mean)) and close(acc.variance(1), float(sample))):
        pytest.fail("the running mean or sample variance is wrong on an early prefix of the stream.")


def test_welford_population_is_sample_times_n_minus_one_over_n() -> None:
    acc = WelfordAccumulator()
    for x in VALUES:
        acc.update(x)
    if not close(acc.variance(0), acc.variance(1) * (N - 1) / N):
        pytest.fail("variance(0) must equal variance(1) times (n - 1) / n.")


def test_welford_scaling_by_two_scales_variance_by_four() -> None:
    base = WelfordAccumulator()
    doubled = WelfordAccumulator()
    for x in VALUES:
        base.update(x)
        doubled.update(2.0 * x)  # doubling is exact in binary floating point
    if not close(doubled.variance(1), 4.0 * base.variance(1)):
        pytest.fail("doubling every value must multiply the sample variance by four.")


def test_welford_mean_of_doubled_stream_is_twice_the_mean() -> None:
    base = WelfordAccumulator()
    doubled = WelfordAccumulator()
    for x in VALUES:
        base.update(x)
        doubled.update(2.0 * x)
    if not close(doubled.mean(), 2.0 * base.mean()):
        pytest.fail("doubling every value must double the mean.")


def test_welford_wrong_type_input_is_refused_or_correct() -> None:
    acc = WelfordAccumulator()
    acc.update(1.0)
    refuse_or_correct(lambda: (acc.update("2.5"), acc.mean())[1], 1.75, "a string passed as a value")


def test_welford_none_input_is_refused() -> None:
    acc = WelfordAccumulator()
    acc.update(1.0)
    refuse_or_correct(lambda: (acc.update(None), acc.mean())[1], float("nan"), "None passed as a value")


@pytest.mark.parametrize("ddof", [2, -1])
def test_welford_other_ddof_is_refused(ddof: int) -> None:
    acc = WelfordAccumulator()
    for x in VALUES[:5]:
        acc.update(x)
    try:
        answer = acc.variance(ddof)
    except NotImplementedError:
        raise
    except Exception:
        return
    pytest.fail(f"variance(ddof) is defined for ddof 0 and 1 only; ddof {ddof} returned a {type(answer).__name__}.")


def test_welford_infinite_input_gives_no_finite_answer() -> None:
    acc = WelfordAccumulator()
    acc.update(VALUES[0])
    try:
        acc.update(float("inf"))
        mean, var = acc.mean(), acc.variance(1)
    except NotImplementedError:
        raise
    except Exception:
        return
    if math.isfinite(mean) and math.isfinite(var):
        pytest.fail("an infinite value cannot produce a finite mean and variance: the call must fail or say so.")


# ------------------------------------------------------------------ rolling minimum and maximum


def test_rolling_window_zero_raises() -> None:
    must_raise(lambda: RollingMinMax(0), "a window of zero")


def test_rolling_window_negative_raises() -> None:
    must_raise(lambda: RollingMinMax(-3), "a negative window")


def test_rolling_window_one_is_valid() -> None:
    r = RollingMinMax(1)
    for x in VALUES[:5]:
        r.push(x)
        if r.minimum() != x or r.maximum() != x:
            pytest.fail("a window of one must report the latest value as both minimum and maximum.")


def test_rolling_minimum_before_push_raises() -> None:
    must_raise(lambda: RollingMinMax(WINDOW).minimum(), "minimum() before any push")


def test_rolling_maximum_before_push_raises() -> None:
    must_raise(lambda: RollingMinMax(WINDOW).maximum(), "maximum() before any push")


def test_rolling_nan_push_raises() -> None:
    r = RollingMinMax(WINDOW)
    r.push(VALUES[0])
    must_raise(lambda: r.push(float("nan")), "a NaN push")


def test_rolling_nan_first_push_raises() -> None:
    must_raise(lambda: RollingMinMax(WINDOW).push(float("nan")), "a NaN as the first push")


@pytest.mark.parametrize("width", [2, 3])
def test_rolling_ties_expire_with_their_index(width: int) -> None:
    stream = [2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0, 3.0, 3.0]
    r = RollingMinMax(width)
    for i, x in enumerate(stream):
        r.push(x)
        window = stream[max(0, i - width + 1) : i + 1]
        if r.minimum() != min(window) or r.maximum() != max(window):
            pytest.fail("with repeated values, the minimum or maximum of the window differs from brute force.")


def test_rolling_every_window_matches_brute_force() -> None:
    r = RollingMinMax(WINDOW)
    for i, x in enumerate(VALUES):
        r.push(x)
        window = VALUES[max(0, i - WINDOW + 1) : i + 1]
        if r.minimum() != min(window) or r.maximum() != max(window):
            pytest.fail("the minimum or maximum of the last window differs from brute force at some position.")


@pytest.mark.parametrize("width", [1, 2, 3, 5, 8, 13, 21, 34])
def test_rolling_fixed_widths_match_brute_force(width: int) -> None:
    r = RollingMinMax(width)
    for i, x in enumerate(VALUES):
        r.push(x)
        window = VALUES[max(0, i - width + 1) : i + 1]
        if r.minimum() != min(window) or r.maximum() != max(window):
            pytest.fail("a window of this width gives a minimum or maximum that differs from brute force.")


def test_rolling_window_longer_than_stream_uses_every_value() -> None:
    r = RollingMinMax(len(VALUES) + 5)
    for x in VALUES:
        r.push(x)
    if r.minimum() != min(VALUES) or r.maximum() != max(VALUES):
        pytest.fail("before the window is full, the minimum and maximum are over every value pushed so far.")


def test_rolling_expired_extreme_leaves_the_window() -> None:
    r = RollingMinMax(2)
    for x in [9.0, 1.0, 2.0]:
        r.push(x)
    if r.maximum() != 2.0 or r.minimum() != 1.0:
        pytest.fail("a value that has left the window must not be reported as the maximum or minimum.")


def test_rolling_wrong_type_window_is_refused_or_correct() -> None:
    def action() -> float:
        wrong_type: Any = "3"  # a wrong type on purpose
        r = RollingMinMax(wrong_type)
        for x in VALUES[:6]:
            r.push(x)
        smallest: float = r.minimum()
        return smallest

    refuse_or_correct(action, min(VALUES[3:6]), "a string window")


def test_rolling_float_window_that_denotes_three_is_refused_or_correct() -> None:
    def action() -> float:
        wrong_type: Any = 3.0  # not an integer type, but it denotes the window 3
        r = RollingMinMax(wrong_type)
        for x in VALUES[:6]:
            r.push(x)
        smallest: float = r.minimum()
        return smallest

    refuse_or_correct(action, min(VALUES[3:6]), "a float window that denotes three")


# ------------------------------------------------------------------ quantile sketch: named conditions


@pytest.mark.parametrize("bad", [0.0, 1.0, 1.5, -0.1, -1e-6, float("nan"), float("inf"), float("-inf")])
def test_sketch_epsilon_outside_open_interval_raises(bad: float) -> None:
    must_raise(lambda: QuantileSketch(bad), f"epsilon outside (0, 1) ({bad!r})")


def test_sketch_small_epsilon_is_valid() -> None:
    must_accept(lambda: QuantileSketch(1e-6), "epsilon 1e-6")


def test_sketch_epsilon_just_below_one_is_valid() -> None:
    must_accept(lambda: QuantileSketch(0.999999), "epsilon 0.999999")
    must_accept(lambda: QuantileSketch(math.nextafter(1.0, 0.0)), "the float just below one")


def test_sketch_quantile_below_zero_raises() -> None:
    sketch = sketch_of(VALUES[:5], EPS)
    must_raise(lambda: sketch.quantile(-0.1), "a quantile below zero")


def test_sketch_quantile_above_one_raises() -> None:
    sketch = sketch_of(VALUES[:5], EPS)
    must_raise(lambda: sketch.quantile(1.1), "a quantile above one")


def test_sketch_quantile_nan_raises() -> None:
    sketch = sketch_of(VALUES[:5], EPS)
    must_raise(lambda: sketch.quantile(float("nan")), "a NaN quantile")


@pytest.mark.parametrize("bad", [float("inf"), float("-inf"), math.nextafter(1.0, 2.0), math.nextafter(0.0, -1.0)])
def test_sketch_quantile_outside_closed_interval_raises(bad: float) -> None:
    sketch = sketch_of(VALUES[:5], EPS)
    must_raise(lambda: sketch.quantile(bad), f"quantile outside the closed interval [0, 1] ({bad!r})")


def test_sketch_quantile_at_both_ends_is_valid() -> None:
    sketch = sketch_of(VALUES[:5], EPS)
    lo = must_accept(lambda: sketch.quantile(0.0), "quantile(0)")
    hi = must_accept(lambda: sketch.quantile(1.0), "quantile(1)")
    if not (isinstance(lo, float) and isinstance(hi, float)):
        pytest.fail("quantile() must return a float.")


def test_sketch_quantile_just_inside_both_ends_is_valid() -> None:
    sketch = sketch_of(VALUES[:5], EPS)
    must_accept(lambda: sketch.quantile(math.nextafter(0.0, 1.0)), "the float just above zero")
    must_accept(lambda: sketch.quantile(math.nextafter(1.0, 0.0)), "the float just below one")


def test_sketch_quantile_on_empty_sketch_raises() -> None:
    must_raise(lambda: QuantileSketch(EPS).quantile(0.5), "quantile() on an empty sketch")


@pytest.mark.parametrize("q", [0.0, 1.0])
def test_sketch_quantile_on_empty_sketch_raises_at_both_ends(q: float) -> None:
    must_raise(lambda: QuantileSketch(EPS).quantile(q), f"quantile({q}) on an empty sketch")


def test_sketch_nan_add_raises() -> None:
    sketch = sketch_of(VALUES[:3], EPS)
    must_raise(lambda: sketch.add(float("nan")), "a NaN added to the sketch")


def test_sketch_nan_first_add_raises() -> None:
    must_raise(lambda: QuantileSketch(EPS).add(float("nan")), "a NaN as the first value added to the sketch")


# ------------------------------------------------------------------ quantile sketch: the rank guarantee


@pytest.mark.parametrize("index", range(10))
def test_sketch_rank_guarantee_at_each_probe(index: int) -> None:
    q = PROBES[index]
    v = sketch_of(VALUES, EPS).quantile(q)
    below = sum(1 for x in VALUES if x < v)
    at_or_below = sum(1 for x in VALUES if x <= v)
    qn = Fraction(q) * N
    slack = Fraction(EPS) * N
    if not (below <= qn + slack):
        pytest.fail(f"the guarantee's first inequality fails at probe {index}: too many values lie below the answer.")
    if not (at_or_below >= qn - slack):
        pytest.fail(f"the guarantee's second inequality fails at probe {index}: too few values lie at or below it.")


def test_sketch_quantile_is_nondecreasing_in_q() -> None:
    sketch = sketch_of(VALUES, EPS)
    grid = sorted({*PROBES, *(k / 100 for k in range(101))})
    answers = [sketch.quantile(q) for q in grid]
    if any(a > b for a, b in itertools.pairwise(answers)):
        pytest.fail("quantile(q) must not decrease as q increases.")


def test_sketch_constant_stream_returns_the_constant() -> None:
    constant = VALUES[0]
    sketch = sketch_of([constant] * 40, EPS)
    if any(sketch.quantile(q) != constant for q in PROBES):
        pytest.fail("on a stream of one repeated value, every quantile is that value.")


def test_sketch_single_value_returns_that_value() -> None:
    sketch = sketch_of([VALUES[1]], EPS)
    if any(sketch.quantile(q) != VALUES[1] for q in PROBES):
        pytest.fail("with one value added, every quantile is that value.")


@pytest.mark.parametrize("order", ["increasing", "decreasing"])
def test_sketch_guarantee_holds_on_sorted_streams(order: str) -> None:
    stream = sorted(VALUES, reverse=(order == "decreasing"))
    sketch = sketch_of(stream, EPS)
    for q in PROBES:
        v = sketch.quantile(q)
        below = sum(1 for x in stream if x < v)
        at_or_below = sum(1 for x in stream if x <= v)
        qn = Fraction(q) * N
        slack = Fraction(EPS) * N
        if not (below <= qn + slack and at_or_below >= qn - slack):
            pytest.fail("the rank guarantee fails on a sorted stream: the sketch must not assume random order.")


@pytest.mark.parametrize("eps", [0.05, 0.1, 0.2])
@pytest.mark.parametrize("length", range(1, 9))
def test_sketch_rank_guarantee_on_short_streams(length: int, eps: float) -> None:
    """Short streams, where epsilon n is below one half: the slack is smaller than a single rank step."""
    stream = VALUES[:length]
    sketch = sketch_of(stream, eps)
    for q in PROBES:
        v = sketch.quantile(q)
        below = sum(1 for x in stream if x < v)
        at_or_below = sum(1 for x in stream if x <= v)
        qn = Fraction(q) * length
        slack = Fraction(eps) * length
        if not (below <= qn + slack and at_or_below >= qn - slack):
            pytest.fail("the rank guarantee fails on a short stream, where the slack is less than one rank.")


@pytest.mark.parametrize("eps", [0.05, 0.1, 0.2])
def test_sketch_rank_guarantee_with_ties(eps: float) -> None:
    """Repeated values: the guarantee counts every copy, so a tie cannot be split by the answer."""
    stream = [1.0] * 7 + [2.0] * 5 + [3.0] * 9 + [4.0] * 2
    sketch = sketch_of(stream, eps)
    n = len(stream)
    for q in PROBES:
        v = sketch.quantile(q)
        below = sum(1 for x in stream if x < v)
        at_or_below = sum(1 for x in stream if x <= v)
        if not (below <= Fraction(q) * n + Fraction(eps) * n and at_or_below >= Fraction(q) * n - Fraction(eps) * n):
            pytest.fail("the rank guarantee fails on a stream with repeated values.")


def test_instances_hold_their_own_state() -> None:
    first = WelfordAccumulator()
    second = WelfordAccumulator()
    first.update(1.0)
    first.update(3.0)
    if second.count != 0:
        pytest.fail("each accumulator holds its own values: a new one must not see another's.")
    rolling_a = RollingMinMax(2)
    rolling_b = RollingMinMax(2)
    rolling_a.push(-5.0)
    must_raise(lambda: rolling_b.minimum(), "minimum() on a fresh object after another object was pushed")
    sketch_a = QuantileSketch(0.1)
    sketch_b = QuantileSketch(0.1)
    sketch_a.add(7.0)
    must_raise(lambda: sketch_b.quantile(0.5), "quantile() on a fresh sketch after another sketch was filled")
