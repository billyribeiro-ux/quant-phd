#!/usr/bin/env python3
"""Per-seed kill matrix for SC1 slice d: every candidate solution file against the project suite, seeds 0-49.

Usage (from the checkout root, with the repo venv):
    .venv/bin/python ledgers/SC1/scripts/SC1-d-r11/kill_rate.py OUT.json FILE [FILE ...]

Each FILE is a complete bm_checks.py candidate. For every seed in 0-49 the suite is run exactly as the
autograder runs it (tools/run_graders.py: same pytest flags, QF_SEED=seed, same copied grader files). The
output records, per file, the seeds on which the suite failed and the first failing test name on each.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import unit  # noqa: E402
from run_graders import panel, run_suite, workspace  # noqa: E402

SEEDS = range(50)


def one(u: object, cfg: dict[str, str], source: Path, seed: int) -> dict[str, object]:
    work = workspace(u, source, cfg)  # type: ignore[arg-type]
    try:
        ok, output, _ = run_suite(work, cfg["suite"], seed)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    found = re.search(r"FAILED \S+::(\S+)", output)
    return {"seed": seed, "passed": ok, "first_failure": None if ok else (found.group(1) if found else "collection/import error")}


def main() -> int:
    out = Path(sys.argv[1])
    files = [Path(p).resolve() for p in sys.argv[2:]]
    u = unit("SC1")
    cfg = panel(u)
    results: dict[str, list[dict[str, object]]] = {}
    jobs = [(f, s) for f in files for s in SEEDS]
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {(f, s): pool.submit(one, u, cfg, f, s) for f, s in jobs}
        for (f, s), fut in futures.items():
            results.setdefault(str(f), []).append(fut.result())
    summary = {}
    for name, rows in results.items():
        rows.sort(key=lambda r: int(r["seed"]))  # type: ignore[arg-type]
        failing = [r for r in rows if not r["passed"]]
        summary[name] = {
            "failing_seeds_of_50": len(failing),
            "seeds_0_9_failing": sum(1 for r in failing if int(r["seed"]) <= 9),  # type: ignore[arg-type]
            "first_failure_seed": failing[0]["seed"] if failing else None,
            "first_failure_test": failing[0]["first_failure"] if failing else None,
            "rows": rows,
        }
    out.write_text(json.dumps(summary, indent=1, sort_keys=True), encoding="utf-8")
    for name, s in sorted(summary.items()):
        print(
            f"{Path(name).name}: failing {s['failing_seeds_of_50']}/50, "
            f"seeds 0-9 failing {s['seeds_0_9_failing']}, first {s['first_failure_seed']} {s['first_failure_test']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
