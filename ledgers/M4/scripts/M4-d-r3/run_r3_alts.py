"""Round-3 verifier D: run the M4 suite on the round-3 alternatives (alt_r3_*.py) through run_alternatives.run_one.
Usage: python -I run_r3_alts.py <checkout_root> <seed_lo> <seed_hi>"""
import importlib.util
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
lo, hi = int(sys.argv[2]), int(sys.argv[3])
spec = importlib.util.spec_from_file_location("ra", root / "ledgers/M4/scripts/run_alternatives.py")
ra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ra)
ra.GRADER = root / "course/modules/M/M4/grader"
ok_all = True
for sol in sorted((root / "ledgers/M4/scripts/M4-d-r3").glob("alt_r3_*.py")):
    fails = []
    for seed in range(lo, hi):
        ok, detail = ra.run_one(sol, seed)
        if not ok:
            fails.append((seed, detail[:200]))
    print(f"{sol.name}: {'PASS' if not fails else 'FAIL'} ({hi - lo - len(fails)}/{hi - lo} seeds)", flush=True)
    for f in fails[:5]:
        print("   seed", f[0], f[1], flush=True)
    ok_all &= not fails
sys.exit(0 if ok_all else 1)
