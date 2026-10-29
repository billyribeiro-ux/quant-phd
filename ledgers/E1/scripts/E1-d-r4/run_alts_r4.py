"""Run correct alternative implementations and the reference through the E1 suite on seeds 0-49 (browser flags)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

SOLUTIONS = [
    ROOT / "course/modules/E/E1/grader/reference.py",
    *sorted((ROOT / "ledgers/E1/scripts").glob("alt*.py")),
    *sorted((ROOT / "ledgers/E1/scripts/E1-d-r2/alternatives").glob("*.py")),
]


def main() -> int:
    u = unit("E1")
    cfg = panel(u)
    seeds = parse_seeds("0-49")
    failures = 0
    for solution in SOLUTIONS:
        work = workspace(u, solution, cfg)
        try:
            bad = [s for s in seeds if not run_suite(work, cfg["suite"], s)[0]]
        finally:
            __import__("shutil").rmtree(work, ignore_errors=True)
        verdict = "PASS" if not bad else f"FAIL on seeds {bad[:5]}"
        failures += bool(bad)
        print(f"{verdict}: {solution.relative_to(ROOT)} ({len(seeds) - len(bad)}/{len(seeds)} seeds)")
    print(f"run_alts_r4: {'PASS' if not failures else 'FAIL'} ({len(SOLUTIONS) - failures}/{len(SOLUTIONS)} implementations)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
