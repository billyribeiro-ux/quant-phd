"""Round 3 (AC2 project): validity and answer differences over 20 NEW seeds, plus the reference-free truth check.

Seeds: random.Random(20261030).sample(range(1000, 100000), 20). Round 1 used range(50) and round 2 used range(50, 1000)
with random.Random(20261028); neither overlaps this draw (asserted below). Imports the course's instance.py and
reference.py by path, read-only. Usage (repository root): .venv/bin/python ledgers/AC2/scripts/project-r3/new_seeds_check.py
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/AC/AC2/grader"
ROUND2 = {57, 88, 96, 195, 267, 288, 319, 520, 561, 603, 621, 642, 647, 660, 682, 750, 755, 791, 891, 897}


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    inst = load("ac2_instance", GRADER / "instance.py")
    ref = load("ac2_reference", GRADER / "reference.py")
    seeds = sorted(random.Random(20261030).sample(range(1000, 100000), 20))
    assert not set(seeds) & ROUND2 and not set(seeds) & set(range(50)), "overlaps an earlier round"
    print("new seeds:", seeds)
    rows = []
    for seed in seeds:
        made = inst.make_instance(seed)
        payload = json.loads(made["payload"])
        ends = payload["period_ends"]
        problems: list[str] = []
        if not 5 <= len(ends) <= 7:
            problems.append("fiscal years outside 5-7")
        gaps = {(dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days for a, b in zip(ends, ends[1:], strict=False)}
        if not gaps <= set(range(364, 367)):
            problems.append(f"gaps {sorted(gaps)}")
        if made["label"] != "SIMULATED" or "SIMULATED" not in payload["facts"]["entityName"]:
            problems.append("not labelled SIMULATED")
        sample = payload["sample"]
        if not 40 <= len(sample) <= 80 or sum(payload["planted"]) < 4:
            problems.append("sample size or planted count out of range")
        for r in sample:
            if r["lag_assets"] <= 0 or not all(math.isfinite(float(v)) for v in r.values()):
                problems.append("non-positive lag or non-finite sample value")
                break
        # the generator's truth at every cut vs the reference engine, which reads only the company-facts mapping
        for iso, expected in [(None, payload["truth"]["final"])] + [(k, v) for k, v in payload["truth"]["as_of"].items()]:
            got = ref.standardize(payload["facts"], iso)
            if list(got) != list(expected) or any(
                set(got[e]) != set(expected[e]) or any(abs(got[e][i] - expected[e][i]) > 1e-6 * max(1.0, abs(expected[e][i])) for i in expected[e])
                for e in expected
            ):
                problems.append(f"reference standardize differs from the generator truth at cut {iso}")
        latest = ends[-1]
        final = payload["truth"]["final"]
        prior = ends[-2]
        prior2 = ends[-3]
        roic = ref.roic(final, latest, 0.25)
        f = ref.piotroski_f_score(final, latest)
        m = ref.beneish_m_score(final, latest)
        mj = ref.modified_jones(sample)
        rows.append(
            {
                "seed": seed,
                "years": len(ends),
                "problems": problems,
                "latest_revenue": final[latest]["revenue"],
                "roic25": round(roic, 9),
                "F": f["score"],
                "M": round(m["m_score"], 9),
                "mj_a2": round(mj["coefficients"][1], 12),
                "mj_disc0": round(mj["discretionary"][0], 12),
                "same_day": payload["restatement"]["same_day"],
                "restated_item": payload["restatement"]["item"],
                "prior2": prior2,
                "prior": prior,
            }
        )
    bad = [r for r in rows if r["problems"]]
    print("instances with problems:", bad if bad else "none")
    print("seed  years  latest_rev  roic25    F  M-score    mj_a2   mj_disc0  same_day  restated")
    for r in rows:
        print(f"{r['seed']:>6} {r['years']:>5} {r['latest_revenue']:>11.2f} {r['roic25']:>8.5f} {r['F']:>2} "
              f"{r['M']:>9.5f} {r['mj_a2']:>9.6f} {r['mj_disc0']:>10.6f}  {str(r['same_day']):<8} {r['restated_item']}")
    for key in ("latest_revenue", "roic25", "M", "mj_a2", "mj_disc0"):
        print(f"distinct {key}: {len({r[key] for r in rows})} of {len(rows)}")
    print("distinct F-scores:", sorted({r['F'] for r in rows}))
    print("same-day amendment seeds:", sum(r["same_day"] for r in rows), "of", len(rows))
    print("distinct payload fingerprints:", len({inst.make_instance(s)['payload'] for s in seeds}))
    print("years distribution:", sorted({r["years"] for r in rows}))


if __name__ == "__main__":
    main()
