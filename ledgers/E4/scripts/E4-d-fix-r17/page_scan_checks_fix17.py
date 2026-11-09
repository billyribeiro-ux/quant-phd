"""Fixer round 17: numeric checks behind the whole-page scan of project.html (slice d).

(a) Lab 1 interpretation: the bracket width after 60 halvings, and its value at each halving (exact powers of two?).
(b) Scope claim, exception table: the solver returns the three keys at a noise volume up to 1e150 and a cost up to 350.
(c) Lede directional claim: at a fixed informed fraction the informativeness falls as the noise volume rises, and the
    informed fraction rises with the noise volume at a fixed cost on the interior (Proposition 5).
(d) Lab 3 hypothesis: at cost 0.120 the fractions are proportional to the noise volume (unrounded ratios).

Run: .venv/bin/python -I ledgers/E4/scripts/E4-d-fix-r17/page_scan_checks_fix17.py
"""

import importlib.util
import math
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[4]


def load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ref = load(ROOT / "course/modules/E/E4/grader/reference.py", "ref_solution")


def lab1_widths() -> None:
    """The Lab 1 bisection loop (60 halvings, the lab's own gap function, read from the twin with main() removed)."""
    print("(a) Lab 1 bracket width after each halving (first 60):")
    lab = ROOT / "tests/labs/E4/lab-E4-project-1.py"
    src = lab.read_text(encoding="utf-8").replace("\nmain()", "\n")
    ns: dict[str, object] = {"__name__": "lab1_module"}
    exec(compile(src, str(lab), "exec"), ns)
    gap = ns["gap"]
    assert callable(gap)
    low, high = 0.0, 1.0
    widths = []
    for _ in range(60):
        mid = 0.5 * (low + high)
        if gap(mid) > 0.0:
            low = mid
        else:
            high = mid
        widths.append(high - low)
    for k in (1, 2, 3, 52, 53, 54, 55, 60):
        w = widths[k - 1]
        print(f"    after halving {k:2d}: width {w:.6e}  (2^-{k} = {2.0**-k:.6e}; equal: {w == 2.0**-k})")
    print(f"    width after 60: {widths[-1]:.6e}; equals 2^-53: {widths[-1] == 2.0**-53}")
    print(f"    widths after 53 equal to 2^-53 at every later halving: {all(w == 2.0**-53 for w in widths[52:])}")


def range_claims() -> None:
    print("(b) exception-table range claims (three keys returned, finite):")
    for sd, cost in [(1e150, 0.13), (1e150, 0.0), (1e-50, 0.1707691121), (0.6, 350.0), (1e150, 350.0)]:
        try:
            out = ref.solve_model(sd, cost)
            ok = set(out) == {"informed_fraction", "price_informativeness", "indifference_gap"}
            finite = all(math.isfinite(v) for v in out.values())
            print(f"    sd {sd:.3e} cost {cost:g}: keys ok {ok}, finite {finite}, out {out}")
        except Exception as err:  # the check reports what happens; it does not hide it
            print(f"    sd {sd:.3e} cost {cost:g}: RAISES {type(err).__name__}: {err}")


def directional_claims() -> None:
    print("(c) directional claims:")
    for lam in (0.1, 0.3, 0.6, 0.9):
        ys = [ref.price_informativeness(lam, sd) for sd in (0.5, 0.75, 1.0, 2.0)]
        ok = all(ys[i] > ys[i + 1] for i in range(len(ys) - 1))
        print(f"    informativeness at fixed lam {lam}: strictly decreasing in sd over 0.5,0.75,1,2: {ok}")
    for sd in (0.5, 0.625, 0.75):
        fr = [ref.solve_model(sd, c)["informed_fraction"] for c in (0.12, 0.135, 0.15)]
        decreasing = fr[0] > fr[1] > fr[2]
        print(f"    noise {sd}: fraction at costs 0.12, 0.135, 0.15 = {fr}; decreasing in cost: {decreasing}")


def lab3_ratios() -> None:
    print("(d) Lab 3 proportionality at cost 0.120 (unrounded):")
    f = [ref.solve_model(sd, 0.120)["informed_fraction"] for sd in (0.500, 0.625, 0.750)]
    print(f"    fractions {f}")
    print(f"    ratio 0.625/0.500 = {f[1] / f[0]:.10f}; ratio 0.750/0.500 = {f[2] / f[0]:.10f}")
    shown = (0.6978 / 0.5582, 0.8373 / 0.5582)
    print(f"    ratios of the displayed values 0.6978/0.5582 = {shown[0]:.6f}; 0.8373/0.5582 = {shown[1]:.6f}")


if __name__ == "__main__":
    lab1_widths()
    range_claims()
    directional_claims()
    lab3_ratios()
