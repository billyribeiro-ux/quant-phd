"""Grade candidate clearing_house.py modules against the BK4 suite (round 2, verifier BK4-c).

Usage (from the checkout root):
    .venv/bin/python ledgers/BK4/scripts/BK4-c-r2/grade_candidates.py <seeds> <candidate.py> [<candidate.py> ...]

For each candidate it runs the suite with the browser's pytest flags (tools/run_graders.py run_suite) on each seed
and prints PASS/FAIL per seed, plus the first failing line and the full output of the first failure (for the
failure-message leak check).
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402


def main() -> int:
    seeds = parse_seeds(sys.argv[1])
    candidates = [Path(p).resolve() for p in sys.argv[2:]]
    u = unit("BK4")
    cfg = panel(u)
    exit_code = 0
    for cand in candidates:
        work = workspace(u, cand, cfg)
        try:
            failed: list[tuple[int, str]] = []
            first_output = ""
            for seed in seeds:
                ok, output, _ = run_suite(work, cfg["suite"], seed)
                if not ok:
                    failed.append((seed, output))
                    if not first_output:
                        first_output = output
            verdict = "PASS" if not failed else "FAIL"
            print(f"{verdict} {cand.name}: {len(seeds) - len(failed)}/{len(seeds)} seeds pass")
            for seed, output in failed[:3]:
                lines = [ln for ln in output.splitlines() if ln.startswith(("FAILED", "E "))]
                print(f"  seed {seed}: {lines[:3]}")
            if failed:
                exit_code = max(exit_code, 0)
            if first_output:
                print("  --- first failing output (tail) ---")
                print(first_output[-1500:])
        finally:
            shutil.rmtree(work, ignore_errors=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
