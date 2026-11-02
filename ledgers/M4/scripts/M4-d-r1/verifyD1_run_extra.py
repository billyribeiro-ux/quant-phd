"""Verifier round-1 runner: the M4 suite against the two extra conforming implementations, seed by seed.

Usage (checkout root): .venv/bin/python ledgers/M4/scripts/M4-d-r1/verifyD1_run_extra.py --seeds 0-9
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("run_alternatives", ROOT / "ledgers/M4/scripts/run_alternatives.py")
assert spec is not None and spec.loader is not None
run_alternatives = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_alternatives)

HERE = Path(__file__).resolve().parent
SOLUTIONS = [HERE / "verifyD1_alt_negated_normals.py", HERE / "verifyD1_alt_tolerances.py"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="0-9")
    args = parser.parse_args()
    seeds = run_alternatives.parse_seeds(args.seeds)
    failures = 0
    for solution in SOLUTIONS:
        bad = []
        for seed in seeds:
            ok, detail = run_alternatives.run_one(solution, seed)
            if not ok:
                bad.append(f"seed {seed}: {detail}")
        failures += bool(bad)
        print(f"{solution.relative_to(ROOT)}: {'PASS' if not bad else 'FAIL'} ({len(seeds) - len(bad)}/{len(seeds)} seeds)")
        for line in bad[:5]:
            print(f"    {line}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
