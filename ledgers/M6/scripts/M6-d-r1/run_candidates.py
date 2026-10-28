"""Run the M6 grader suite on candidate martingale_checks modules over seeds, one line per candidate.

Usage: <checkout>/.venv/bin/python ledgers/M6/scripts/M6-d-r1/run_candidates.py SEEDS FILE [FILE ...]
A candidate passes a seed when the suite exits 0 on it. Output: candidate, passing seeds count, first failing seed and
the first failing test name.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402


def main() -> int:
    seeds = parse_seeds(sys.argv[1])
    u = unit("M6")
    cfg = panel(u)
    for name in sys.argv[2:]:
        path = Path(name).resolve()
        passed = 0
        first_fail = None
        for seed in seeds:
            work = workspace(u, path, cfg)
            try:
                ok, output, _ = run_suite(work, cfg["suite"], seed)
            finally:
                pass
            if ok:
                passed += 1
            elif first_fail is None:
                found = re.search(r"FAILED \S+::(\S+)", output)
                first_fail = (seed, found.group(1) if found else output[-300:])
        print(f"{path.name}: {passed}/{len(seeds)} seeds pass; first failure: {first_fail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
