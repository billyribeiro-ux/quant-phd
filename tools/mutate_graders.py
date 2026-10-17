#!/usr/bin/env python3
"""Mutation-test a unit's autograder with the verifier's wrong solutions.

The verifier (VERIFIER_RULES §2.6) writes at least three plausible wrong
solutions as complete modules in ``ledgers/<UNIT>/mutants/*.py``, each opening
with a one-line docstring that describes the error. Every mutant must fail at
least one test on at least one seed in the window. A surviving mutant means the
suite cannot tell that error from a correct solution, and the unit fails.

Usage::

    python3 tools/mutate_graders.py --unit S7 --seeds 0-9
"""

from __future__ import annotations

import argparse
import ast
import re
import shutil
import sys

from coursekit import LEDGERS, Unit, built_units, unit
from run_graders import panel, parse_seeds, run_suite, workspace


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--unit")
    target.add_argument("--all", action="store_true", help="every built unit with an autograder")
    parser.add_argument("--seeds", default="0-9")
    args = parser.parse_args()
    targets = built_units() if args.all else [unit(args.unit)]
    graded = [u for u in targets if u.entry["project"]["grading"] in ("autograder", "both")]
    return max((mutate(u, args.seeds) for u in graded), default=0)


def mutate(u: Unit, seeds: str) -> int:
    cfg = panel(u)
    mutants = sorted((LEDGERS / u.id / "mutants").glob("*.py"))
    if len(mutants) < 3:
        print(f"FAIL {u.id}: {len(mutants)} mutants in ledgers/{u.id}/mutants (the verifier must write at least 3)")
        return 1
    survivors = 0
    for mutant in mutants:
        description = ast.get_docstring(ast.parse(mutant.read_text(encoding="utf-8"))) or "(no description)"
        killed_by = None
        work = workspace(u, mutant, cfg)
        try:
            for seed in parse_seeds(seeds):
                ok, output, _ = run_suite(work, cfg["suite"], seed)
                if not ok:
                    found = re.search(r"FAILED \S+::(\S+)", output)
                    killed_by = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                    break
        finally:
            shutil.rmtree(work, ignore_errors=True)
        survivors += killed_by is None
        print(f"{'KILLED' if killed_by else 'SURVIVED'} {mutant.name}: {description.splitlines()[0]} -> {killed_by}")
    verdict = "PASS" if not survivors else "FAIL"
    print(f"mutate_graders {u.id}: {verdict} ({len(mutants) - survivors}/{len(mutants)} killed)")
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
