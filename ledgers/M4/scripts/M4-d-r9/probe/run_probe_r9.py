"""Round-9 probe (not a mutant: not written to ledgers/M4/mutants): a Student-t-only loss sign flip, which project.html
line 228 says the suite does not test. Also re-runs the three-position last-pivot mutant on seeds 0-9 for the record.
Usage: python -I <this file> from the checkout root."""
import pathlib
import sys
ROOT = pathlib.Path.cwd()
sys.path.insert(0, str(ROOT / "ledgers/M4/scripts"))
import run_alternatives as ra  # noqa: E402
for sol in [ROOT / "ledgers/M4/scripts/M4-d-r9/probe/probe_student_t_sign_flipped.py",
            ROOT / "ledgers/M4/mutants/r9_07_last_pivot_unchecked_for_three_positions.py"]:
    res = [ra.run_one(sol, s) for s in range(10)]
    print(sol.name, "survives all of seeds 0-9" if all(ok for ok, _ in res) else
          f"killed on {sum(not ok for ok, _ in res)} of 10 seeds")
    for s, (ok, d) in enumerate(res):
        if not ok:
            print(f"  seed {s}: {d[:200]}")
