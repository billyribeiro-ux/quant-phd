"""Scratch check (round 5): would a relative root test at tiny noise volumes kill the two surviving mutants and keep
the reference and the five alternatives passing? Usage: python -I scratch_tiny_root_test_r5.py <checkout-root> <seeds-hi>.
Works in a temp copy of the grader; the course files are untouched.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
seeds_hi = int(sys.argv[2])
sys.path.insert(0, str(root / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, run_suite  # noqa: E402

u = unit("E4")
cfg = panel(u)
grader = u.directory / cfg["grader"]
suite_src = (grader / "test_project.py").read_text(encoding="utf-8")
extra = '''

@pytest.mark.parametrize("sd", [1e-11, 1e-12])
def test_scratch_tiny_root_relative(sd: float) -> None:
    lam = run(sd, 0.15)["informed_fraction"]
    exact = closed_form_root(sd, 0.15)
    expect(exact > 0.0 and abs(lam - exact) <= 1e-8 * exact, "scratch: relative accuracy at tiny noise")
'''
suite = suite_src + extra
candidates = {
    "reference": grader / "reference.py",
    "alt_1": root / "ledgers/E4/alternatives/alt_1.py",
    "alt_2": root / "ledgers/E4/alternatives/alt_2.py",
    "alt_3": root / "ledgers/E4/alternatives/alt_3.py",
    "alt_4": root / "ledgers/E4/alternatives/alt_4.py",
    "alt_5": root / "ledgers/E4/alternatives/alt_5.py",
    "mutant_bracket_floor": root / "ledgers/E4/mutants/mutant_r5_bracket_floor_1e-12.py",
    "mutant_sixty_halvings": root / "ledgers/E4/mutants/mutant_r5_sixty_halvings_no_tolerance.py",
}
for name, src in candidates.items():
    work = Path(tempfile.mkdtemp(prefix="e4r5-"))
    for n in [cfg["suite"], *cfg.get("support", "").split()]:
        shutil.copy(grader / n, work / n)
    (work / cfg["suite"]).write_text(suite, encoding="utf-8")
    shutil.copy(src, work / "solver.py")
    fails = []
    try:
        for seed in range(0, seeds_hi + 1):
            ok, out, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                fails.append(seed)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{name}: {'PASS' if not fails else 'FAIL'} with the scratch tiny-root test on seeds 0-{seeds_hi} (failing seeds {fails[:6]})")
