"""Round-6 verifier (slice d): run the five alternative implementations in ledgers/M4/scripts/M4-d-r6/alts/ and the
root alt_1..alt_5 (both sets) against the grader suite, seed by seed, with the browser's pytest flags.

Usage: .venv/bin/python ledgers/M4/scripts/M4-d-r6/run_alts_r6.py 0-9
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
sys.path.insert(0, str(SCRIPTS))
from run_alternatives import parse_seeds, run_one  # noqa: E402

seeds = parse_seeds(sys.argv[1] if len(sys.argv) > 1 else "0-9")
files = sorted((HERE / "alts").glob("*.py")) + sorted(SCRIPTS.glob("alt_*.py"))
bad_total = 0
for solution in files:
    bad = []
    for seed in seeds:
        ok, detail = run_one(solution, seed)
        if not ok:
            bad.append((seed, detail))
    bad_total += bool(bad)
    print(f"{solution.name}: {'PASS' if not bad else 'FAIL'} ({len(seeds) - len(bad)}/{len(seeds)} seeds)")
    for seed, detail in bad[:3]:
        print(f"    seed {seed}: {detail[:200]}")
print("alternatives failing:", bad_total)
