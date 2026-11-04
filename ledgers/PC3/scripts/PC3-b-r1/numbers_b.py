"""Independent recomputation of the numbers printed or claimed on PC3 L04-L06 (verifier PC3-b, round 1).

Run from the checkout root: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r1/numbers_b.py
Loads the lab twins' game functions by exec (main() call removed) so that the seeded draws are the twins' own.
"""
from __future__ import annotations

import math
import random
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load_twin(name: str) -> dict[str, object]:
    src = (ROOT / "tests/labs/PC3" / name).read_text(encoding="utf-8")
    lines = [ln for ln in src.splitlines() if ln.strip() != "main()"]
    import sys
    import types

    mod = types.ModuleType("twin_" + name.replace("-", "_").replace(".", "_"))
    sys.modules[mod.__name__] = mod
    exec(compile("\n".join(lines), name, "exec"), mod.__dict__)  # noqa: S102 - local lab twin, read from the repo
    return dict(mod.__dict__)


def half_up_floor(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


print("== L04 Problem E1: seed 1 via twin play(1) ==")
l04 = load_twin("lab-PC3-L04-1.py")
path, turns = l04["play"](1)  # type: ignore[operator]
fills = [t for t in turns if t.filled]
cash_flow = sum(t.cash_flow_cents for t in fills)
inv_end = turns[-1].inventory_after
settle = path[20]
print("fills", len(fills), "cash_flow", cash_flow, "inv_end", inv_end, "settlement", settle,
      "mark", inv_end * settle, "pnl", turns[-1].cash_after_cents + inv_end * settle)

print("== L04 Problem E2: informed arrivals on seed 0 ==")
_, arr0 = l04["draw_game"](0)  # type: ignore[operator]
n_inf = sum(1 for a in arr0 if a == "informed")
print("informed", n_inf, "of 20; share", Fraction(n_inf, 20))
se = math.sqrt(0.25 / 20)
print("se", se, "z", (n_inf / 20 - 0.5) / se, "z_0.975", 0.0)
# normal 97.5% quantile via erf inversion by bisection, independent of scipy
lo, hi = 0.0, 5.0
for _ in range(200):
    mid = (lo + hi) / 2
    if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < 0.975:
        lo = mid
    else:
        hi = mid
print("z_0.975 =", round(lo, 6))

print("== L04 Remark 2.4 / E3: seed 0 mid and marks ==")
_, t0 = l04["play"](0)  # type: ignore[operator]
last = t0[-1]
mid = (last.bid_cents + last.ask_cents) // 2
print("last quote", last.bid_cents, last.ask_cents, "mid", mid, "settle", l04["draw_game"](0)[0][20])  # type: ignore[index]
cf = sum(t.cash_flow_cents for t in t0 if t.filled)
print("cash flow", cf, "pnl@settle", cf + last.inventory_after * 9980, "pnl@mid", cf + last.inventory_after * mid)

print("== L04 Prop 3.1 closed form: (1-p)h - p[(v-a)+ + (b-v)+] at p=1/2 vs enumeration already in lab ==")
for v in (9985, 10000, 10020):
    a, b, h = 10010, 9990, 10
    closed = Fraction(h, 2) - Fraction(1, 2) * (max(v - a, 0) + max(b - v, 0))
    print("v", v, "closed", closed)

print("== L04 R1: p=3/5, h=10 ==")
print("d =", Fraction(2, 5) * 10 / Fraction(3, 5), float(Fraction(2, 5) * 10 / Fraction(3, 5)))

print("== L05 E2: seed 6, window 8 (twin functions) ==")
l05 = load_twin("lab-PC3-L05-1.py")
xs6 = l05["make_sequence"](6, 200)  # type: ignore[operator]
nv, nc = l05["naive_maxima"](xs6, 8)  # type: ignore[operator]
dv, ops = l05["deque_maxima"](xs6, 8)  # type: ignore[operator]
print("outputs equal", nv == dv, "naive", nc, "deque comparisons", ops.comparisons, "pushes", ops.pushes, "pops", ops.pops)

print("== L05 E3 / Part 3 rows, k=200 and window sizes (twin) ==")
xs5 = l05["make_sequence"](5, 200)  # type: ignore[operator]
for k in (1, 2, 8, 32, 200):
    _, o = l05["deque_maxima"](xs5, k)  # type: ignore[operator]
    print("k", k, "comparisons", o.comparisons, "pushes", o.pushes, "pops", o.pops)

print("== L05 Remark 3.4: x=(k,k-1,...,2,100), n=k; pops removed in the step-k while loop ==")


def step_k_back_removals(x: list[int], k: int) -> int:
    """Count back removals made in the while loop at step k (1-based), by a plain deque of indices."""
    dq: list[int] = []
    removed_at_k = 0
    for i, v in enumerate(x, start=1):
        while dq and x[dq[-1] - 1] <= v:
            dq.pop()
            if i == k:
                removed_at_k += 1
        dq.append(i)
        if dq[0] <= i - k:
            dq.pop(0)
    return removed_at_k


for k in (5, 50, 100, 101, 150):
    x = list(range(k, 1, -1)) + [100]
    assert len(x) == k
    print("k", k, "entries removed by the 100 at step k:", step_k_back_removals(x, k), "of", k - 1)

print("== L06: exact NPV and break-even ==")
A = sum(Fraction(1, 1) / Fraction(110, 100) ** t for t in range(1, 4))
print("A", A, float(A))
K = 150000 * 100  # cents
m = 5000
for u in (200, 1200, 1300, 1600):
    npv = -K + m * A * u  # cents, exact
    print("units", u, "NPV exact", npv, "float", float(npv), "display half-up", half_up_floor(npv))
print("break-even units", Fraction(K, m) / A, float(Fraction(K, m) / A))
for r in (Fraction(8, 100), Fraction(10, 100), Fraction(12, 100)):
    Ar = sum(1 / (1 + r) ** t for t in range(1, 4))
    be = Fraction(K, m) / Ar
    lo_npv = -K + m * Ar * 200
    hi_npv = -K + m * Ar * 1600
    print("rate", r, "A", float(Ar), "break-even", float(be), "NPV@200", float(lo_npv), "NPV@1600", float(hi_npv),
          "display", half_up_floor(lo_npv), half_up_floor(hi_npv))
be8 = Fraction(K, m) / sum(1 / (1 + Fraction(8, 100)) ** t for t in range(1, 4))
be12 = Fraction(K, m) / sum(1 / (1 + Fraction(12, 100)) ** t for t in range(1, 4))
be10 = Fraction(K, m) / A
print("width 8->12 exact", float(be12 - be8), "per point", float((be12 - be8) / 4))
print("width from displayed 1249.05-1164.10 =", round(1249.05 - 1164.10, 6), "per point", (1249.05 - 1164.10) / 4)
print("8->10 step", float(be10 - be8), "10->12 step", float(be12 - be10))
print("E1 12%: annuity", float(sum(1 / Fraction(112, 100) ** t for t in range(1, 4))),
      "break-even", float(Fraction(3000) / sum(1 / Fraction(112, 100) ** t for t in range(1, 4))))
print("R3: margin for break-even 1600 (cents)", float(Fraction(15000000) / (1600 * A)),
      "ratio", float(Fraction(15000000) / (1600 * A) / 5000), "fall %", float(100 * (1 - Fraction(15000000) / (1600 * A) / 5000)))
print("M3: 1000*1331/(4*3310) =", Fraction(1000 * 1331, 4 * 3310), float(Fraction(1000 * 1331, 4 * 3310)))
print("M2 NPV at 10%:", -100 + Fraction(60, 1) / Fraction(11, 10) + Fraction(60, 1) / Fraction(121, 100), "=", Fraction(500, 121))
print("grid positives at 10%:", [u for u in range(200, 1601, 100) if -K + m * A * u > 0])
print("first negative grid point ascending:", [u for u in range(200, 1601, 100) if -K + m * A * u < 0][:1],
      "largest negative:", [u for u in range(200, 1601, 100) if -K + m * A * u < 0][-1:])
