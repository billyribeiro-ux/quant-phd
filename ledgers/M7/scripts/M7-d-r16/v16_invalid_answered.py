"""Check the sweep cases that the float-based start check calls invalid but the reference answers (round-16 verifier).

The reference reads each decimal value exactly (reference.py:46, Fraction(repr(value))); this script applies the page's
starting checks with the same decimal reading, and reports any case that the page refuses but the reference answers.
Run from the repository root with -I.
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import v16_probe as P  # noqa: E402
import v16_sweep as S  # noqa: E402

F = Fraction
TOL = F(1, 10**9)


def dec(x: float) -> Fraction:
    return Fraction(repr(float(x)))


def decimal_start_ok(case: dict) -> bool:
    n = len(case["mu"])
    w0 = [dec(x) for x in case["w0"]]
    lo = [dec(x) for x in case["lower"]]
    up = [dec(x) for x in case["upper"]]
    if abs(sum(w0, F(0)) - 1) > TOL:
        return False
    if any(w0[i] < lo[i] - TOL or w0[i] > up[i] + TOL for i in range(n)):
        return False
    for k, cap in enumerate(case["sector_caps"]):
        if sum((w0[i] for i in range(n) if case["sector"][i] == k), F(0)) > dec(cap) + TOL:
            return False
    return all(lo[i] <= up[i] for i in range(n))


def main() -> None:
    for seed in (16, 17):
        rng = random.Random(seed)
        n_flagged = n_real = 0
        for idx in range(1500):
            case = S.gen(rng)
            if S.valid_start(case):
                continue
            n_flagged += 1
            try:
                P.REF.allocate(json.loads(json.dumps(case)))
            except Exception:
                continue
            if not decimal_start_ok(case):
                n_real += 1
                print("REAL_INVALID_ANSWERED seed", seed, "idx", idx, json.dumps(case))
        print(f"seed {seed}: float-check flagged {n_flagged} answered cases; decimal-reading refuses-but-answered: {n_real}")


if __name__ == "__main__":
    main()


def refused_but_decimal_valid() -> None:
    """The reverse check: a case the decimal reading accepts that the reference refuses (a false refusal)."""
    for seed in (16, 17):
        rng = random.Random(seed)
        count = 0
        for _ in range(1500):
            case = S.gen(rng)
            if not decimal_start_ok(case):
                continue
            try:
                P.REF.allocate(json.loads(json.dumps(case)))
            except Exception as exc:
                count += 1
                print("FALSE_REFUSAL seed", seed, type(exc).__name__, exc)
        print(f"seed {seed}: false refusals of decimal-valid starts: {count}")


if __name__ == "__main__":
    refused_but_decimal_valid()
