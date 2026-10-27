"""Compare every recorded browser state (drive_out.json) with the independent Python port (figure_expected.py).

For each state the parameters are the control values read back from the DOM, and the seed is the default seed plus
the number of button presses. The readout and the svg <desc> must match the Python strings exactly.
Usage: .venv/bin/python ledgers/S7/scripts/L03-L04-r27/compare.py
"""

from __future__ import annotations

import collections
import functools
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import figure_expected as fe  # noqa: E402

data = json.loads((HERE / "drive_out.json").read_text(encoding="utf-8"))
ucache = functools.lru_cache(maxsize=None)(fe.universe)
acache = functools.lru_cache(maxsize=None)(fe.ar1_autocov)
pcache = functools.lru_cache(maxsize=None)(fe.pvalue_sample)


def expected(s: dict) -> dict:
    c = s["controls"]
    n = s["presses"]
    chart = s["chart"]
    if chart == "bh-geometry":
        return fe.bh_expected(float(c[0]), bool(c[1]), bool(c[2]))
    if chart == "pvalue-histogram":
        seed = 22 + n
        lam = float(c[0])
        p = pcache(seed)
        # reuse the sample; the helper recomputes it from the same seed
        out = fe.pvalue_expected(seed, lam)
        return out
    if chart == "bootstrap-blocks":
        b = fe.BLOCK_CHOICES[int(c[0])]
        return fe.blocks_expected(2 + n, b)
    if chart == "bootstrap-variance":
        phi = float(c[0])
        return fe.variance_expected(186 + n, phi)
    if chart == "rc-vs-spa":
        poor = int(round(float(c[0])))
        seed = 2001 + n
        return fe.rc_expected(seed, poor, ucache(seed))
    raise KeyError(chart)


tally: collections.Counter = collections.Counter()
mismatches: list[str] = []
for s in data["states"]:
    e = expected(s)
    key = (s["page"], s["chart"], s["width"], s["scheme"])
    tally[key + ("states",)] += 1
    for field in ("readout", "desc"):
        got = s[field]
        if got is None:
            mismatches.append(f"{key} {s['tag']} {s['controls']} {field}: missing in browser")
            tally[key + (field, "missing")] += 1
            continue
        if got != e[field]:
            tally[key + (field, "mismatch")] += 1
            if len(mismatches) < 15:
                mismatches.append(f"{key} {s['tag']} presses={s['presses']} controls={s['controls']} {field}:\n  browser: {got}\n  python:  {e[field]}")
        else:
            tally[key + (field, "match")] += 1

total = len(data["states"])
bad = sum(v for k, v in tally.items() if k[-1] in ("mismatch", "missing"))
print(f"states compared {total}; field comparisons with mismatch or missing: {bad}")
for key in sorted({k[:4] for k in tally}):
    st = tally[key + ("states",)]
    rm = tally[key + ("readout", "match")]
    dm = tally[key + ("desc", "match")]
    print(f"{key[0]} {key[1]:18s} {key[2]:>5} px {key[3]:5s} states {st:4d} readout match {rm:4d} desc match {dm:4d}")
for m in mismatches:
    print(m)
print("DONE")
