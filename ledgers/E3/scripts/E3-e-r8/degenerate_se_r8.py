"""Round-8: the all-A degenerate set of test_estimate_counts_a_mixed_lottery_whether_or_not_it_was_chosen.

Builds the responses exactly as the test does (the test module's own B_SIDE_SURE_A, B_SIDE_LOTTERIES), runs the reference
estimate (reference.py copied to a scratch directory as elicit.py), and prints every returned field, so that the
docstring's standard-error claim ("standard errors above 10^5") can be checked against the numbers.

Run: .venv/bin/python -I ledgers/E3/scripts/E3-e-r8/degenerate_se_r8.py
"""

import pathlib
import shutil
import subprocess
import sys
import tempfile

CHECKOUT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-E3-e")
GRADER = CHECKOUT / "course/modules/E/E3/grader"
work = pathlib.Path(tempfile.mkdtemp(prefix="e3e_r8_degenerate."))
shutil.copy(GRADER / "instance.py", work / "instance.py")
shutil.copy(GRADER / "test_project.py", work / "test_project.py")
shutil.copy(GRADER / "reference.py", work / "elicit.py")

driver = r"""
import os, sys
sys.path.insert(0, WORK)
os.environ.setdefault("QF_SEED", "0")
import test_project as t
responses = [
    {
        "pair_id": i,
        "choice": "A",
        "prizes_a": [t.B_SIDE_SURE_A[i]],
        "probs_a": ["1"],
        "prizes_b": t.B_SIDE_LOTTERIES[i][0],
        "probs_b": t.B_SIDE_LOTTERIES[i][1],
    }
    for i in range(len(t.B_SIDE_SURE_A))
]
try:
    result = t.sol.estimate(responses)
    for key in sorted(result):
        print(key, repr(result[key]))
except Exception as exc:  # the test accepts any non-ValueError outcome; print what happened
    print("raised", type(exc).__name__, str(exc)[:200])
"""
print("scratch", work)
proc = subprocess.run([sys.executable, "-I", "-c", "WORK = " + repr(str(work)) + "\n" + driver], cwd=work, capture_output=True, text=True, timeout=900)
print(proc.stdout, end="")
print(proc.stderr[-800:], end="")
print("exit", proc.returncode)
