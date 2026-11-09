"""Run candidate CS2 streamstats solutions through the project grader, exactly as tools/run_graders.py does.

usage: python run_alts_r1.py <seeds> <solution.py> [<solution.py> ...]

Reuses tools/run_graders.py panel(), workspace() and run_suite() from this checkout, so the suite, the
support files, the PYTEST_FLAGS and the environment are the ones the gate uses.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402


def main() -> int:
    seeds = parse_seeds(sys.argv[1])
    u = unit("CS2")
    cfg = panel(u)
    rc = 0
    for arg in sys.argv[2:]:
        solution = Path(arg).resolve()
        work = workspace(u, solution, cfg)
        failing: list[int] = []
        first = ""
        try:
            for seed in seeds:
                ok, output, _ = run_suite(work, cfg["suite"], seed)
                if not ok:
                    failing.append(seed)
                    if not first:
                        first = output.strip().splitlines()[-1][:160] if output.strip() else ""
        finally:
            import shutil

            shutil.rmtree(work, ignore_errors=True)
        verdict = "PASS" if not failing else "FAIL"
        print(f"{verdict} {solution.name}: {len(seeds) - len(failing)}/{len(seeds)} seeds pass; failing seeds: {failing}")
        if first:
            print(f"    last line on first failure: {first}")
        rc |= 1 if failing else 0
    return rc


if __name__ == "__main__":
    sys.exit(main())
