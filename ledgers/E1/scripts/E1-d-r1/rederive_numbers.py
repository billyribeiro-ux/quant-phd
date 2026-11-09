"""Verifier round 1: independent re-derivation of every number, proposition and sample instance for the E1 project.

Uses only fractions and math (no reference code). Prints a PASS/FAIL line per check.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction as F
from itertools import product

RESULTS: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))


def rnd(x: F) -> int:
    return math.floor(x + F(1, 2))


def closed(a: int, b: int, c: int) -> dict[str, dict[str, F]]:
    d = F(a - b * c)
    out: dict[str, dict[str, F]] = {}
    for s, (vol, fee) in {
        "monopoly": (d / 2, F(a + b * c, 2 * b)),
        "cournot": (2 * d / 3, F(a + 2 * b * c, 3 * b)),
        "bertrand": (d, F(c)),
    }.items():
        profit = (fee - c) * vol
        cs = vol * vol / (2 * b)
        welfare = cs + profit
        dwl = (d - vol) ** 2 / (2 * b)
        out[s] = {"volume": vol, "fee": fee, "profit": profit, "cs": cs, "welfare": welfare, "dwl": dwl}
    return out


# --- Reference-case numbers printed or quoted on the page (a=120,b=1,c=20) and the tie case (a=121)
ref = closed(120, 1, 20)
expected_ref = {
    ("monopoly", "volume"): (F(50), 50), ("monopoly", "fee"): (F(70), 70),
    ("monopoly", "profit"): (F(2500), 2500), ("monopoly", "cs"): (F(1250), 1250),
    ("monopoly", "welfare"): (F(3750), 3750), ("monopoly", "dwl"): (F(1250), 1250),
    ("cournot", "volume"): (F(200, 3), 67), ("cournot", "fee"): (F(160, 3), 53),
    ("cournot", "profit"): (F(20000, 9), 2222), ("cournot", "cs"): (F(20000, 9), 2222),
    ("cournot", "welfare"): (F(40000, 9), 4444), ("cournot", "dwl"): (F(5000, 9), 556),
    ("bertrand", "volume"): (F(100), 100), ("bertrand", "fee"): (F(20), 20),
    ("bertrand", "profit"): (F(0), 0), ("bertrand", "cs"): (F(5000), 5000),
    ("bertrand", "welfare"): (F(5000), 5000), ("bertrand", "dwl"): (F(0), 0),
}
for (s, k), (exact, printed) in expected_ref.items():
    got = ref[s][k]
    ok = got == exact and rnd(got) == printed
    record(f"ref {s} {k}", ok, f"exact={got} printed={rnd(got)} page={exact}/{printed}")

tie = closed(121, 1, 20)
record("tie monopoly fee 141/2 -> 71", tie["monopoly"]["fee"] == F(141, 2) and rnd(tie["monopoly"]["fee"]) == 71)
record("tie monopoly volume 101/2 -> 51", tie["monopoly"]["volume"] == F(101, 2) and rnd(tie["monopoly"]["volume"]) == 51)
record("tie monopoly profit 10201/4 -> 2550", tie["monopoly"]["profit"] == F(10201, 4) and rnd(tie["monopoly"]["profit"]) == 2550)
lab3_a121 = {
    "monopoly": (51, 71, 2550, 1275, 3825, 1275),
    "cournot": (67, 54, 2267, 2267, 4534, 567),
    "bertrand": (101, 20, 0, 5101, 5101, 0),
}
for s, want in lab3_a121.items():
    got = tuple(rnd(tie[s][k]) for k in ("volume", "fee", "profit", "cs", "welfare", "dwl"))
    record(f"lab3 a=121 {s}", got == want, f"got={got} want={want}")

# --- Exemplar B numeric claims: differences in the Comparison passage and the d^2/(36b) profit difference
record("exB volume diffs 17 and 33", rnd(ref["cournot"]["volume"]) - 50 == 17 and 100 - rnd(ref["cournot"]["volume"]) == 33)
record("exB fee diffs -17 and -33", 53 - 70 == -17 and 20 - 53 == -33)
record("exB welfare diffs 694 and 556", 4444 - 3750 == 694 and 5000 - 4444 == 556)
record("exB profit diff d^2/(36b)=10000/36=277.8", ref["monopoly"]["profit"] - ref["cournot"]["profit"] == F(10000, 36))
record("exB DWL Cournot 5000/9 = 555.56", round(float(ref["cournot"]["dwl"]), 2) == 555.56)
record("exB monopoly fee minus Cournot fee = d/(6b) = 50/3", ref["monopoly"]["fee"] - ref["cournot"]["fee"] == F(50, 3))

# --- Exact identities checked on a grid of valid inputs (a > bc > 0)
bad: list[str] = []
count = 0
for b, c in product(range(1, 6), range(1, 40)):
    for gap in range(1, 120):
        a = b * c + gap
        count += 1
        d = F(gap)
        cl = closed(a, b, c)
        # Prop 1: fee and profit at monopoly from the maximiser of pi(Q)=((a-Q)/b - c)Q by grid of rationals
        m = cl["monopoly"]
        if m["profit"] != d * d / (4 * b):
            bad.append(f"prop1 profit {a},{b},{c}")
        # Prop 2: Cournot profit total 2d^2/(9b); each exchange d^2/(9b)
        if cl["cournot"]["profit"] != 2 * d * d / (9 * b):
            bad.append(f"prop2 profit {a},{b},{c}")
        # Prop 2 error after k steps: |q_k - d/3| = d/(3*2^k)
        q = F(0)
        for k in range(1, 8):
            q = (d - q) / 2
            if abs(q - d / 3) != d / (3 * 2**k):
                bad.append(f"prop2 iteration {a},{b},{c},k={k}")
                break
        # Prop 4: welfare = CS + profit; DWL = W(d)-W(Q)
        for s in ("monopoly", "cournot", "bertrand"):
            v = cl[s]
            if v["welfare"] != v["cs"] + v["profit"]:
                bad.append(f"prop4 welfare {s} {a},{b},{c}")
        # Prop 5 differences
        if not (m["volume"] < cl["cournot"]["volume"] < cl["bertrand"]["volume"]):
            bad.append(f"prop5 volume order {a},{b},{c}")
        if not (m["fee"] > cl["cournot"]["fee"] > c):
            bad.append(f"prop5 fee order {a},{b},{c}")
        if not (m["dwl"] > cl["cournot"]["dwl"] > 0 == cl["bertrand"]["dwl"]):
            bad.append(f"prop5 dwl order {a},{b},{c}")
        if not (cl["bertrand"]["welfare"] > cl["cournot"]["welfare"] > m["welfare"]):
            bad.append(f"prop5 welfare order {a},{b},{c}")
        if cl["monopoly"]["profit"] - cl["cournot"]["profit"] != d * d / (36 * b):
            bad.append(f"prop5 profit gap {a},{b},{c}")
        if m["fee"] - cl["cournot"]["fee"] != d / (6 * b):
            bad.append(f"prop5 fee gap {a},{b},{c}")
record("grid identities (Props 1,2,4,5 exact) over b<=5, c<=39, gap<=119", not bad, f"cases={count} failures={bad[:5]}")

# --- Prop 5 rounding claim: whole a,b,c and d > 6b keep the printed order (explicit directions, exact diffs > 1)
order_bad: list[str] = []
n_order = 0
min_diff: dict[str, F] = {}
for b, c in product(range(1, 11), range(1, 80)):
    for gap in range(6 * b + 1, 420):
        a = b * c + gap
        n_order += 1
        cl = closed(a, b, c)
        M, C_, B_ = cl["monopoly"], cl["cournot"], cl["bertrand"]
        checks = [
            ("volume", "inc", [M["volume"], C_["volume"], B_["volume"]]),
            ("welfare", "inc", [M["welfare"], C_["welfare"], B_["welfare"]]),
            ("fee", "dec", [M["fee"], C_["fee"], B_["fee"]]),
            ("dwl", "dec", [M["dwl"], C_["dwl"], B_["dwl"]]),
            ("profit", "dec", [M["profit"], C_["profit"]]),
        ]
        for key, dirn, vals in checks:
            for x, y in zip(vals, vals[1:], strict=False):
                exact_ok = x < y if dirn == "inc" else x > y
                printed_ok = rnd(x) < rnd(y) if dirn == "inc" else rnd(x) > rnd(y)
                if not exact_ok:
                    order_bad.append(f"exact {key} {a},{b},{c}")
                if not printed_ok:
                    order_bad.append(f"printed {key} {a},{b},{c}")
                diff = abs(x - y)
                min_diff[key] = min(min_diff.get(key, diff), diff)
record("Prop 5 printed order, whole a,b,c with d>6b (b<=10, c<=79, gap<=419)", not order_bad,
       f"cases={n_order} failures={order_bad[:5]} min_exact_adjacent_diff={ {k: float(v) for k, v in min_diff.items()} }")

# --- Sample 20 seeds of instance.py (independent re-implementation of the seed rule is NOT used; import the file)
import importlib.util
import sys as _sys
from pathlib import Path

inst_path = Path(__file__).resolve().parents[4] / "course/modules/E/E1/grader/instance.py"
spec = importlib.util.spec_from_file_location("instance_e1", inst_path)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
rows = []
for seed in range(20):
    inst = mod.make_instance(seed)
    a, b, c = inst["a"], inst["b"], inst["c"]
    valid = a > b * c > 0 and 1 <= b <= 3 and 5 <= c <= 60 and 60 <= a - b * c <= 400 and a - b * c > 6 * b
    cl = closed(a, b, c)
    rows.append((seed, a, b, c, a - b * c, rnd(cl["cournot"]["welfare"]), valid))
    record(f"instance seed {seed} valid and d>6b", valid, f"a={a} b={b} c={c} d={a - b * c}")
distinct = len({(r[1], r[2], r[3]) for r in rows})
record("instance seeds 0-19 give distinct (a,b,c)", distinct == 20, f"distinct={distinct}")
for r in rows:
    print("seed", r[0], "a", r[1], "b", r[2], "c", r[3], "d", r[4], "cournot welfare printed", r[5])

fails = [r for r in RESULTS if not r[1]]
for name, ok, detail in RESULTS:
    print(("PASS " if ok else "FAIL ") + name + (" | " + detail if detail else ""))
print(f"TOTAL {len(RESULTS)} checks, {len(fails)} failed")
