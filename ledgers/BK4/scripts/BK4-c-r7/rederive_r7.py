"""Independent re-derivation of every number on the BK4 project page (round 7), with Fraction and integer rules.

Usage: rederive_r7.py <checkout>. Reads the grader instance module from the checkout (for the seeded cases only).
"""

from __future__ import annotations

import pathlib
import random
import sys
from fractions import Fraction
from math import ceil

ROOT = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "course/modules/BK/BK4/grader"))
from instance import make_instance  # noqa: E402

# --- Lab 1 / Lab 3 instance (page constants) ---
MARGIN = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}
FUND = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}
CAP = 20_000
D = 2
rng = random.Random(1)
LOSSES = [rng.randint(0, 120_000) for _ in range(40)]


def pay(loss: int, margin_d: int, fund: dict[int, int], cap: int, d: int) -> tuple[int, int, int, dict[int, Fraction], int]:
    """Layers by the page rules; survivors' exact pro rata shares before the leftover rule."""
    a1 = min(loss, margin_d)
    a2 = min(loss - a1, fund[d])
    a3 = min(loss - a1 - a2, cap)
    R = loss - a1 - a2 - a3
    surv = [m for m in sorted(fund) if m != d]
    pool = sum(fund[m] for m in surv)
    if R >= pool:
        return a1, a2, a3, {m: Fraction(fund[m]) for m in surv}, R - pool
    return a1, a2, a3, {m: Fraction(R * fund[m], pool) for m in surv}, 0


def settle(loss: int, margin_d: int, fund: dict[int, int], cap: int, d: int) -> tuple[int, int, int, dict[int, int], int]:
    a1, a2, a3, exact, unc = pay(loss, margin_d, fund, cap, d)
    floors = {m: int(v) for m, v in exact.items()}
    if unc == 0 and sum(exact.values()) != sum(floors.values()) + 0 and sum(floors.values()) < (loss - a1 - a2 - a3):
        left = (loss - a1 - a2 - a3) - sum(floors.values())
        for m in sorted(floors):
            if left and fund[m] > 0:
                floors[m] += 1
                left -= 1
    return a1, a2, a3, floors, unc


def cover(losses: list[int], margin: int) -> Fraction:
    return Fraction(10_000 * sum(1 for x in losses if x <= margin), len(losses))


out: list[str] = []
say = out.append

# Lab 1 numbers
a1, a2, a3, sh, unc = settle(80_000, MARGIN[D], FUND, CAP, D)
say(f"lab1 layers {a1} {a2} {a3} residual {80_000 - a1 - a2 - a3}")
exact = {m: Fraction((80_000 - a1 - a2 - a3) * FUND[m], 12_000) for m in (1, 3, 4)}
say("lab1 exact shares " + " ".join(f"{m}:{exact[m]}={float(exact[m]):.4f}" for m in exact))
say(f"lab1 floored shares {({m: int(v) for m, v in exact.items()})} sum {sum(int(v) for v in exact.values())}")
say(f"lab1 survivors paid {sh} uncovered {unc} conservation {a1 + a2 + a3 + sum(sh.values()) + unc == 80_000}")
target = 9_550
exact_pos = Fraction(target * 40, 10_000)
k = ceil(exact_pos)
margin = sorted(LOSSES)[k - 1]
say(f"lab1 exact position {float(exact_pos)} k {k} margin {margin} 39th smallest {sorted(LOSSES)[38]}")
say(f"lab1 cover at margin {cover(LOSSES, margin)} cover below {cover(LOSSES, margin - 1)}")
say(f"lab1 38 of 40 is {Fraction(38, 40) * 100} percent")
say(f"lab1 losses sample first 3 {LOSSES[:3]} max {max(LOSSES)}")

# Lab 3 numbers
for loss in (20_000, 55_000, 70_000, 80_000, 100_000):
    r = settle(loss, MARGIN[D], FUND, CAP, D)
    say(f"lab3 loss {loss} -> {r}")
for t in (9_000, 9_500, 9_750):
    k = ceil(Fraction(t * 40, 10_000))
    m = sorted(LOSSES)[k - 1]
    say(f"lab3 target {t} exact {float(Fraction(t*40,10000))} k {k} margin {m} cover {cover(LOSSES, m)} below {cover(LOSSES, m - 1)}")
for t in (9_500, 9_000):
    k = ceil(Fraction(t * 40, 10_000))
    m = sorted(LOSSES)[k - 1]
    past = [sum(1 for x in LOSSES if x > m), sum(1 for x in LOSSES if x > m + FUND[D]),
            sum(1 for x in LOSSES if x > m + FUND[D] + CAP), sum(1 for x in LOSSES if x > m + FUND[D] + CAP + 12_000)]
    say(f"lab3 partC target {t} margin {m} past {past}")
say(f"exemplarB diff 111074-105154={111074-105154} 9500-9000={9500-9000}")
say(f"exemplarB 1334+1666+1000={1334+1666+1000}")

# Layer-order fixture table (page rows), independent oracle
FIXM, FIXF, FIXC = 100, 50, 30
rows = {80: (80, 0, 0, (0, 0), 0), 100: (100, 0, 0, (0, 0), 0), 120: (100, 20, 0, (0, 0), 0), 150: (100, 50, 0, (0, 0), 0),
        151: (100, 50, 1, (0, 0), 0), 170: (100, 50, 20, (0, 0), 0), 180: (100, 50, 30, (0, 0), 0),
        181: (100, 50, 30, (1, 0), 0), 200: (100, 50, 30, (8, 12), 0), 205: (100, 50, 30, (10, 15), 0),
        300: (100, 50, 30, (40, 60), 20)}
fm = {1: 40, 2: 60, 3: 50}
bad = []
for loss, want in rows.items():
    got = settle(loss, FIXM, fm, FIXC, 3)
    if (got[0], got[1], got[2]) != want[:3] or (got[3][1], got[3][2]) != want[3] or got[4] != want[4]:
        bad.append((loss, got, want))
say(f"fixture table rows {len(rows)} mismatches {bad}")
# remainder fixture
for loss in (1, 2, 3, 4):
    say(f"remainder loss {loss} -> {settle(loss, 0, {1: 1, 2: 1, 3: 1, 4: 0}, 0, 4)}")
# sizing fixtures
for losses, t, want in (([10, 20, 30, 40, 50], 8000, 40), ([10, 20, 30, 40, 50], 8001, 50), ([10, 20, 30, 40, 50], 10000, 50), ([10, 20, 30, 40], 5000, 20)):
    k = ceil(Fraction(t * len(losses), 10_000))
    say(f"sizing {losses} {t} k {k} -> {sorted(losses)[k-1]} want {want} {'OK' if sorted(losses)[k-1]==want else 'BAD'}")
say(f"cover fixtures {cover([1,5,9],4)} floor {10_000*1//3} ; {10_000*2//3}")

# Instance validity and materiality, seeds 0-49
ans = set()
bad_inst = []
for s in range(50):
    c = make_instance(s)
    ids = c["member_ids"]
    ok = (4 <= len(ids) <= 6 and all(f >= 1 for f in c["default_fund_cents"]) and c["target_bps"] in (9000, 9500, 9750)
          and 40 <= len(c["losses_cents"]) <= 80 and all(x >= 0 for x in c["losses_cents"]))
    if not ok:
        bad_inst.append(s)
    k = ceil(Fraction(c["target_bps"] * len(c["losses_cents"]), 10_000))
    ans.add(sorted(c["losses_cents"])[k - 1])
say(f"instances seeds 0-49 invalid {bad_inst} distinct sizing answers {len(ans)}")

print("\n".join(out))

# Plan 5.5 materiality: uncovered totals and the three required regions, seeds 0-49
sys.path.insert(0, str(ROOT / "course/modules/BK/BK4/grader"))
ref = {}
exec(compile((ROOT / "course/modules/BK/BK4/grader/reference.py").read_text(encoding="utf-8"), "reference.py", "exec"), ref)
uncov_totals = set()
regions_missing = []
for s in range(50):
    c = make_instance(s)
    margins = dict(zip(c["member_ids"], c["initial_margin_cents"]))
    funds = dict(zip(c["member_ids"], c["default_fund_cents"]))
    d = c["defaulter_id"]
    tot = 0
    for x in c["losses_cents"]:
        w = ref["waterfall"](x, d, margins, funds, c["ccp_capital_cents"])
        tot += w.uncovered_cents
    uncov_totals.add(tot)
    L = c["losses_cents"]
    inside_margin = any(x <= margins[d] for x in L)
    inside_fund = any(margins[d] < x <= margins[d] + funds[d] for x in L)
    past_all = any(x > margins[d] + funds[d] + c["ccp_capital_cents"] for x in L)
    surv_pay = any(margins[d] + funds[d] + c["ccp_capital_cents"] < x <= margins[d] + funds[d] + c["ccp_capital_cents"] + sum(v for m, v in funds.items() if m != d) for x in L)
    if not (inside_margin and inside_fund and past_all and surv_pay):
        regions_missing.append(s)
print(f"plan 5.5 materiality: distinct uncovered totals over seeds 0-49: {len(uncov_totals)}; seeds missing a required region: {regions_missing}")
