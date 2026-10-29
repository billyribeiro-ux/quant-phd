"""Run the rung-2 student-error mutants and the alternative correct implementations against the printed check.

A mutant survives when its printed output equals the page's expected block (project.html, lab-E5-project-2).
Usage: python -I -W error ledgers/E5/scripts/E5-d-r2/run_project2_mutants.py  (run from the checkout root)
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
PY = sys.executable
EXPECTED = [
    "term spread, 10-year minus 3-month (pp): 0.83",
    "output gap (%): -0.18",
]
groups = {
    "mutants": sorted((ROOT / "ledgers/E5/mutants/project-2").glob("m*.py")),
    "alternatives": sorted((ROOT / "ledgers/E5/mutants/project-2/alt").glob("alt*.py")),
}
for name, files in groups.items():
    for f in files:
        out = subprocess.run([PY, "-I", "-W", "error", str(f)], capture_output=True, text=True, cwd=ROOT).stdout
        survived = all(line in out for line in EXPECTED)
        lines = [l for l in out.splitlines() if "output gap" in l or "term spread" in l]
        print(f"{name:12s} {f.name:30s} {'SURVIVES' if survived else 'killed  '} {' | '.join(lines)}")
