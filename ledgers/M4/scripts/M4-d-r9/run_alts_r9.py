"""Round-9 check: run the verifier's own alternatives (alts/alt_r9_*.py) and the reference through the M4 suite on seeds
0-9, using run_alternatives.run_one (same flags, same workspace). Usage: python -I <this file> (checkout root as cwd)."""
import pathlib
import sys

ROOT = pathlib.Path.cwd()
sys.path.insert(0, str(ROOT / "ledgers/M4/scripts"))
import run_alternatives as ra  # noqa: E402

here = ROOT / "ledgers/M4/scripts/M4-d-r9/alts"
seeds = range(0, 10)
for sol in [ra.GRADER / "reference.py", *sorted(here.glob("alt_r9_*.py"))]:
    bad = []
    for s in seeds:
        ok, detail = ra.run_one(sol, s)
        if not ok:
            bad.append((s, detail[:300]))
    print(f"{sol.relative_to(ROOT)}: {'PASS' if not bad else 'FAIL'} ({len(seeds) - len(bad)}/{len(seeds)} seeds)")
    for s, d in bad[:5]:
        print(f"    seed {s}: {d}")
