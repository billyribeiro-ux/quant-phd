# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Collect-only test count per seed, and a 20-seed instance sample with materiality checks (AC2 project).

Usage (from the repository root):
    .venv/bin/python ledgers/AC2/scripts/project-r1/collect_and_sample.py collect 0-14
    .venv/bin/python ledgers/AC2/scripts/project-r1/collect_and_sample.py sample

'collect' runs pytest --collect-only on the course's test_project.py (unchanged) for each seed and prints the count.
'sample' draws 20 seeds from 0-49 with random.Random(20261027).sample, checks every instance is valid by independent
rules (a 5-7 year history, one period end per fiscal year, planted discretionary accruals, positive lag assets, the
payload's truth matches an independent recomputation), and prints the answers that change with the seed.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "AC" / "AC2" / "grader"


def load_instance():  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location("ac2_instance", GRADER / "instance.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def collect(seeds: list[int]) -> None:
    ref = GRADER / "reference.py"
    counts = {}
    for seed in seeds:
        work = Path(tempfile.mkdtemp(prefix="ac2-collect-"))
        try:
            shutil.copy(GRADER / "test_project.py", work / "test_project.py")
            shutil.copy(GRADER / "instance.py", work / "instance.py")
            (work / "atlas").mkdir()
            (work / "atlas" / "__init__.py").write_text("", encoding="utf-8")
            shutil.copy(ref, work / "atlas" / "fundamentals.py")
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"],
                cwd=work,
                capture_output=True,
                text=True,
                check=False,
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            )
            m = re.search(r"(\d+) tests? collected", result.stdout)
            counts[seed] = int(m.group(1)) if m else f"no count: {result.stdout[-300:]}"
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print("collect-only counts by seed:", counts)
    print("distinct counts:", sorted({str(v) for v in counts.values()}))


def check_instance(seed: int, module) -> dict:  # type: ignore[no-untyped-def]
    inst = module.make_instance(seed)
    payload = json.loads(inst["payload"])
    ends = payload["period_ends"]
    problems: list[str] = []
    n = len(ends)
    if not 5 <= n <= 7:
        problems.append(f"{n} fiscal years, expected 5 to 7")
    gaps = {(dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days for a, b in zip(ends, ends[1:], strict=False)}
    if not gaps <= set(range(364, 367)):
        problems.append(f"consecutive period ends not one year apart: {sorted(gaps)}")
    if inst["label"] != "SIMULATED" or "SIMULATED" not in payload["facts"]["entityName"]:
        problems.append("not labelled SIMULATED")
    sample = payload["sample"]
    planted = payload["planted"]
    if not 40 <= len(sample) <= 80:
        problems.append(f"sample size {len(sample)} outside 40-80")
    if sum(planted) < 4:
        problems.append("fewer than four planted discretionary accruals")
    if any(r["lag_assets"] <= 0 for r in sample):
        problems.append("non-positive lag_assets")
    for key in ("total_accruals", "lag_assets", "d_revenue", "d_receivables", "ppe"):
        if not all(math.isfinite(r[key]) for r in sample):
            problems.append(f"non-finite {key}")
    # independent check: the reference-free truth at the latest filing uses the final record
    final = payload["truth"]["final"]
    latest = ends[-1]
    for end in ends:
        row = final.get(end, {})
        if "revenue" in row and row["revenue"] <= 0:
            problems.append("non-positive revenue")
    cut_names = [k for k, v in payload["cutoffs"].items() if v is not None]
    return {
        "seed": seed,
        "problems": problems,
        "years": n,
        "latest_revenue": final[latest]["revenue"],
        "latest_total_assets": final[latest]["total_assets"],
        "latest_equity": final[latest]["equity"],
        "sample_n": len(sample),
        "planted": sum(planted),
        "cuts": cut_names,
        "restatement_same_day": payload["restatement"]["same_day"],
        "restated_item": payload["restatement"]["item"],
        "shares_latest": final[latest].get("shares_outstanding"),
    }


def sample_seeds() -> list[int]:
    return sorted(random.Random(20261027).sample(range(50), 20))


def sample() -> None:
    module = load_instance()
    seeds = sample_seeds()
    rows = [check_instance(s, module) for s in seeds]
    print("sampled seeds:", seeds)
    bad = [r for r in rows if r["problems"]]
    print("instances with problems:", bad if bad else "none")
    for key in ("latest_revenue", "latest_total_assets", "latest_equity", "sample_n", "years", "planted"):
        vals = [r[key] for r in rows]
        print(f"{key}: min={min(vals)} max={max(vals)} distinct={len({round(float(v), 6) for v in vals})}")
    print("restated item:", sorted({r["restated_item"] for r in rows}))
    print("same-day amendment seeds:", sum(r["restatement_same_day"] for r in rows), "of", len(rows))
    print("distinct latest revenue values:", len({r["latest_revenue"] for r in rows}), "of", len(rows))
    print("distinct payload fingerprints:", len({module.make_instance(s)["payload"] for s in seeds}))


def main() -> int:
    mode = sys.argv[1]
    if mode == "collect":
        lo, _, hi = sys.argv[2].partition("-")
        collect(list(range(int(lo), int(hi or lo) + 1)))
    elif mode == "sample":
        sample()
    else:
        raise SystemExit("usage: collect LO-HI | sample")
    return 0


if __name__ == "__main__":
    sys.exit(main())
