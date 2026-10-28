"""Sweep the L05 lab's synthetic set over several discount factors D in (0, 1].

Usage: python3 ledgers/FC2/scripts/FC2-b-r1/l05_discount_sweep.py  (run from the checkout root)
Reads tests/labs/FC2/lab-FC2-L05-1.py, drops its final main() call, and applies the lab's own
bound and convexity checks to the lab's own synthetic price construction with a different D.
The question: does the lab docstring claim that every check holds for any D in (0, 1] hold?
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

root = Path(__file__).resolve().parents[4]
src = (root / "tests/labs/FC2/lab-FC2-L05-1.py").read_text(encoding="utf-8")
src = src.rsplit("\nmain()", 1)[0]
ns: dict[str, object] = {"__name__": "lab_l05"}
exec(compile(src, "lab-FC2-L05-1.py", "exec"), ns)

strikes = ns["STRIKES_CENTS"]
spot = ns["SPOT_CENTS"]
for d in [Fraction(9, 10), Fraction(1, 2), Fraction(1, 10), Fraction(1, 100), Fraction(1)]:
    ns["DISCOUNT"] = d
    row: list[str] = []
    try:
        calls = tuple(ns["synthetic_call"](k) for k in strikes)  # type: ignore[operator]
        puts = tuple(ns["synthetic_put"](k, c) for k, c in zip(strikes, calls, strict=True))  # type: ignore[operator]
    except ValueError as exc:
        print(f"D={d}: set not constructible in integer cents ({exc})")
        continue
    for k, c, p in zip(strikes, calls, puts, strict=True):
        b = ns["bounds_violations"](k, c, p)  # type: ignore[operator]
        if b:
            row.append(f"K={k}: {b}")
    cv = ns["convexity_violations"](strikes, calls)  # type: ignore[operator]
    print(f"D={d}: calls={calls} puts={puts} bound violations={row or 'none'} convexity violations={len(cv)}")
sys.exit(0)
