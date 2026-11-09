#!/usr/bin/env python3
"""Five alternative correct implementations of the E3 engine, built from the reference by function replacement.

Each alternative must pass the grader suite (course/modules/E/E3/grader/test_project.py) on every requested seed.
The alternatives differ from the reference in the numerical method only:

* alt1: a grid, then a 26-direction compass search, then a Newton polish (central differences, step 1e-6);
* alt2: a grid, then Newton's method with central-difference gradient and Hessian (step 1e-6);
* alt3: a grid, then Nelder-Mead on the negative log-likelihood (restarted once), then the same Newton polish;
* alt4: the prospect certainty equivalent by bisection inversion of the value function (no closed form);
* alt5: the reference's optimiser, with the half-cent rule applied to the decimal value of the float
  (Decimal: floor of the value plus one half, which is an exact half toward plus infinity).

Usage: python3 run_alternatives.py [--seeds 0-9]
"""

from __future__ import annotations

import argparse
import ast
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GRADER = Path(__file__).resolve().parents[3] / "course" / "modules" / "E" / "E3" / "grader"

HEADER = """def _maximise(parsed: list[Parsed]) -> list[float]:
    def f(t: list[float]) -> float:
        return _objective(t, parsed)
"""

GRID = """    best_t: list[float] = [0.0, 0.0, 0.0]
    best_v = -math.inf
    for gamma in (0.05, 0.25, 0.45, 0.65, 0.85):
        for lam in (1.0, 2.0, 4.0):
            for kappa in (0.5, 2.0, 5.0):
                start = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
                if f(start) > best_v:
                    best_v, best_t = f(start), start
"""

NEWTON = """    t, h = list(best_t), 1e-6

    def _stalled(point: list[float]) -> list[float]:
        # A stalled search is returned only if its score is near zero; otherwise it raises, as the reference does.
        worst = 0.0
        for i in range(3):
            up = [x + (h if k == i else 0.0) for k, x in enumerate(point)]
            down = [x - (h if k == i else 0.0) for k, x in enumerate(point)]
            worst = max(worst, abs(f(up) - f(down)) / (2 * h))
        if worst < 1e-5:
            return point
        raise RuntimeError("the search stalled before a stationary point: the maximisation did not converge")

    for _ in range(100):
        f0 = f(t)
        grad = [0.0, 0.0, 0.0]
        neg_hess = [[0.0] * 3 for _ in range(3)]
        for i in range(3):
            up = [x + (h if k == i else 0.0) for k, x in enumerate(t)]
            down = [x - (h if k == i else 0.0) for k, x in enumerate(t)]
            grad[i] = (f(up) - f(down)) / (2 * h)
            neg_hess[i][i] = -(f(up) - 2 * f0 + f(down)) / (h * h)
        for i in range(3):
            for j in range(i + 1, 3):
                pp = [x + (h if k in (i, j) else 0.0) for k, x in enumerate(t)]
                pm = [x + (h if k == i else 0.0) - (h if k == j else 0.0) for k, x in enumerate(t)]
                mp = [x - (h if k == i else 0.0) + (h if k == j else 0.0) for k, x in enumerate(t)]
                mm = [x - (h if k in (i, j) else 0.0) for k, x in enumerate(t)]
                neg_hess[i][j] = neg_hess[j][i] = -(f(pp) - f(pm) - f(mp) + f(mm)) / (4 * h * h)
        lower = _cholesky(neg_hess)
        step_dir = _solve(lower, grad) if lower is not None else grad
        scale = 1.0
        while scale > 1e-14 and f([x + scale * d for x, d in zip(t, step_dir, strict=True)]) <= f0:
            scale /= 2.0
        if scale <= 1e-14:
            return _stalled(t)
        t = [x + scale * d for x, d in zip(t, step_dir, strict=True)]
        if max(abs(g) for g in grad) < 1e-7:
            return t
        if max(abs(scale * d) for d in step_dir) < 1e-10:
            return _stalled(t)
    return _stalled(t)
"""

COMPASS = """    import itertools

    t, v, step = list(best_t), best_v, 0.5
    directions = [list(d) for d in itertools.product((-1.0, 0.0, 1.0), repeat=3) if any(d)]
    while step > 1e-9:
        candidates = [[x + step * d for x, d in zip(t, dv, strict=True)] for dv in directions]
        scored = max(candidates, key=f)
        if f(scored) > v:
            t, v = scored, f(scored)
        else:
            step /= 2.0
    best_t = t
"""

SIMPLEX = """    def g(t: list[float]) -> float:
        return -_objective(t, parsed)

    def simplex_search(start: list[float]) -> list[float]:
        points = [start] + [[x + (0.5 if k == i else 0.0) for k, x in enumerate(start)] for i in range(3)]
        values = [g(p) for p in points]
        for _ in range(20000):
            order = sorted(range(4), key=lambda k: values[k])
            points = [points[k] for k in order]
            values = [values[k] for k in order]
            spread = max(abs(v - values[0]) for v in values)
            size = max(abs(x - y) for p in points[1:] for x, y in zip(p, points[0], strict=True))
            if spread < 1e-13 and size < 1e-11:
                break
            centroid = [sum(p[k] for p in points[:3]) / 3.0 for k in range(3)]
            worst = points[3]
            reflected = [c + (c - w) for c, w in zip(centroid, worst, strict=True)]
            f_r = g(reflected)
            if values[0] <= f_r < values[2]:
                points[3], values[3] = reflected, f_r
            elif f_r < values[0]:
                expanded = [c + 2.0 * (c - w) for c, w in zip(centroid, worst, strict=True)]
                f_e = g(expanded)
                points[3], values[3] = (expanded, f_e) if f_e < f_r else (reflected, f_r)
            else:
                contracted = [c + 0.5 * (w - c) for c, w in zip(centroid, worst, strict=True)]
                f_c = g(contracted)
                if f_c < values[3]:
                    points[3], values[3] = contracted, f_c
                else:
                    best = points[0]
                    points = [best] + [[b + 0.5 * (p - b) for b, p in zip(best, q, strict=True)] for q in points[1:]]
                    values = [values[0]] + [g(q) for q in points[1:]]
        return points[0]

    start = [0.0, 0.0, 0.0]
    for gamma in (0.05, 0.25, 0.45, 0.65, 0.85):
        for lam in (1.0, 2.0, 4.0):
            for kappa in (0.5, 2.0, 5.0):
                trial = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
                if _objective(trial, parsed) > _objective(start, parsed):
                    start = trial
    once = simplex_search(start)
    best_t = simplex_search(once)
"""

ALT4 = '''def _prospect_ce(prizes: list[int], probs: list[Fraction], gamma: float, lam: float) -> float:
    """Bisection inversion of the prospect value: the sure change c between the least and the greatest prize with
    value(c) equal to the lottery's value, found to machine precision (no closed form is used)."""
    total = sum(float(p) * _value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    low, high = float(min(prizes)), float(max(prizes))
    for _ in range(300):
        mid = 0.5 * (low + high)
        value_mid = _value(mid, gamma, lam)  # type: ignore[arg-type]
        if value_mid < total:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)
'''

ALT5 = '''def _half_up(y: float) -> int:
    """The nearest whole cent, an exact half going toward plus infinity, applied to the decimal value of the float."""
    from decimal import ROUND_FLOOR, Decimal

    return int((Decimal(repr(y)) + Decimal("0.5")).to_integral_value(rounding=ROUND_FLOOR))
'''

ALTERNATIVES: dict[str, dict[str, str]] = {
    "alt1": {"_maximise": HEADER + GRID + COMPASS + NEWTON},
    "alt2": {"_maximise": HEADER + GRID + NEWTON},
    "alt3": {"_maximise": HEADER + SIMPLEX + NEWTON},
    "alt4": {"_prospect_ce": ALT4},
    "alt5": {"_half_up": ALT5},
}


def build(name: str) -> str:
    """The reference with the named functions replaced by the alternative's definitions."""
    source = (GRADER / "reference.py").read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)
    spans = {n.name: (n.lineno, n.end_lineno) for n in tree.body if isinstance(n, ast.FunctionDef)}
    replacements = ALTERNATIVES[name]
    for fname in sorted(replacements, key=lambda k: -spans[k][0]):
        first, last = spans[fname]
        lines[first - 1 : last] = [replacements[fname].rstrip("\n") + "\n"]
    text = "".join(lines)
    docstring_end = text.index('"""', text.index('"""') + 3) + 3
    return (
        f'"""Alternative correct implementation {name} (ledgers/E3/scripts), built from the reference."""'
        + text[docstring_end:]
    )


def seeds_of(text: str) -> list[int]:
    out: list[int] = []
    for chunk in text.split(","):
        lo, _, hi = chunk.partition("-")
        out.extend(range(int(lo), int(hi or lo) + 1))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seeds", default="0-9")
    parser.add_argument("--alts", default=",".join(ALTERNATIVES), help="comma-separated alternative names to run")
    args = parser.parse_args()
    seeds = seeds_of(args.seeds)
    status = 0
    for name in args.alts.split(","):
        work = Path(tempfile.mkdtemp(prefix=f"e3-{name}-"))
        try:
            for f in ("test_project.py", "instance.py"):
                shutil.copy(GRADER / f, work / f)
            (work / "elicit.py").write_text(build(name), encoding="utf-8")
            failed: list[int] = []
            for seed in seeds:
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pytest",
                        "-q",
                        "-p",
                        "no:cacheprovider",
                        "--assert=plain",
                        "-W",
                        "error",
                        "test_project.py",
                    ],
                    cwd=work,
                    capture_output=True,
                    text=True,
                    check=False,
                    env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
                )
                if result.returncode != 0:
                    failed.append(seed)
                    # Keep the failing output: a first-run failure with no captured output cannot be diagnosed.
                    print(f"--- {name} seed {seed}: pytest exit {result.returncode}")
                    print(result.stdout[-4000:])
                    print(result.stderr[-2000:])
            status |= bool(failed)
            verdict = "PASS" if not failed else "FAIL"
            print(
                f"{name}: {verdict} ({len(seeds) - len(failed)}/{len(seeds)} seeds"
                f"{'' if not failed else f'; failing seeds {failed}'})"
            )
        finally:
            shutil.rmtree(work, ignore_errors=True)
    return status


if __name__ == "__main__":
    sys.exit(main())
