"""Check the numeric claims in the figure captions and the code comments about default seeds (pin 49def2c).

* pvalue-histogram caption: leak and sd of the estimate at lambda 0.5 and 0.05 (closed form, storey_moments).
* bh-geometry caption: over the 39 q values, the carried-rank claim and the Holm-threshold claim.
* bootstrap-variance caption: the readout numbers of seed 186 at phi 0.5, their ranks among seeds 1-200.
* bootstrap-blocks comment: seed 2 is the smallest seed whose block count at b = 4 equals the median over seeds 1-200.
* rc-vs-spa comment: seed 2001 is a median draw across seeds 2000-2029 (observed maximum and p-values).
Usage: .venv/bin/python ledgers/S7/scripts/L03-L04-r27/captions_check.py
"""

from __future__ import annotations

import functools
import pathlib
import statistics
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import figure_expected as fe  # noqa: E402

print("== pvalue-histogram caption (closed form)")
for lam in (0.5, 0.05):
    mo = fe.pi0_moments(lam)
    print(f"lambda {lam}: leak {mo['leak']:.6f} sd {mo['sd']:.6f} leak/sd {mo['leak'] / mo['sd']:.3f}")

print("== bh-geometry caption claims over q = 0.010..0.200 step 0.005 (39 values)")
qs = [round(0.01 + 0.005 * i, 3) for i in range(39)]
carried_q = []
holm_ok = True
for q in qs:
    r = fe.bh(fe.EXAMPLE, q)
    carried = [k for k in range(1, 11) if k <= r["k_star"] and fe.EXAMPLE[k - 1] > r["lines"][k - 1]]
    if carried:
        carried_q.append((q, r["k_star"], carried))
    thr = [q / (10 - j) for j in range(10)]
    if not all(t <= q / 3 + 1e-15 for t in thr[:8]):
        holm_ok = False
print("q values with a carried rank:", carried_q)
print("Holm thresholds of ranks 1-8 never exceed q/3:", holm_ok, "; ranks 9, 10 reach q/2 and q:", True)

print("== bootstrap-variance caption: seed 186, phi 0.5, ranks among seeds 1-200")
rows = {}
for seed in range(1, 201):
    v = fe.variance_expected(seed, 0.5)
    rows[seed] = (v["first"], v["best"][1], v["best"][0], v["last"])
vals = rows[186]
print("seed 186:", [round(x, 4) if isinstance(x, float) else x for x in vals])
for name, idx in [("ratio at b=1", 0), ("peak height", 1), ("block at peak", 2), ("ratio at b=500", 3)]:
    series = sorted(rows[s][idx] for s in rows)
    rank = sum(1 for s in rows if rows[s][idx] < vals[idx]) + 1
    print(f"{name}: value {vals[idx]:.4f}, rank among 200 = {rank}, median {statistics.median(series):.4f}")

print("== bootstrap-blocks comment: block counts at b = 4, seeds 1-200")
counts = {s: fe.blocks_expected(s, 4)["blocks"] for s in range(1, 201)}
med = statistics.median(counts.values())
smallest_match = min(s for s in counts if counts[s] == med)
print("median block count", med, "; seed 2 has", counts[2], "; smallest seed with the median count", smallest_match)

print("== rc-vs-spa comment: seeds 2000-2029, poor = 0")
seeds = list(range(2000, 2030))
stats = {}
for s in seeds:
    u = fe.universe(s)
    now = fe.rc_spa(u, 10)
    stats[s] = (now["v"], now["tObs"], now["pRc"], now["pSpa"])
ref = stats[2001]
names = ["observed V", "observed t", "RC p", "SPA p"]
for i, name in enumerate(names):
    series = sorted(stats[s][i] for s in seeds)
    med_i = statistics.median(series)
    rank = sum(1 for s in seeds if stats[s][i] < ref[i]) + 1
    print(f"{name}: seed 2001 value {ref[i]:.4f}, rank among 30 = {rank}, median {med_i:.4f}")
print("DONE")
