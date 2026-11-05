"""Run every variant file given on the command line through the E4 project suite on seeds 0-49.

Usage: .venv/bin/python ledgers/E4/scripts/E4-d-r12/run_variants.py --seeds 0-49 FILE...
Prints one line per file: ALTERNATIVE PASS (all seeds) or KILLED/SURVIVED with the first failing test and seed.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="0-49")
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    u = unit("E4")
    cfg = panel(u)
    seeds = parse_seeds(args.seeds)
    any_pass = False
    for f in args.files:
        path = Path(f).resolve()
        work = workspace(u, path, cfg)
        killed = None
        passed = 0
        try:
            for seed in seeds:
                ok, output, _ = run_suite(work, cfg["suite"], seed)
                if not ok:
                    found = re.search(r"FAILED \S+::(\S+)", output)
                    killed = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                    break
                passed += 1
        finally:
            shutil.rmtree(work, ignore_errors=True)
        if killed is None:
            print(f"PASS {path.name}: {passed}/{len(seeds)} seeds")
            any_pass = True
        else:
            print(f"KILLED {path.name}: {killed} after {passed} passing seeds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
