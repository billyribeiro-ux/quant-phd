"""Verifier r10: the all-A fixture of test_estimate_counts_a_mixed_lottery_whether_or_not_it_was_chosen, reference output."""
import re, sys, ast
GRADER = "/Users/billyribeiro/.fanout/wt/verifyD10-E3-e/course/modules/E/E3/grader"
sys.path.insert(0, GRADER)
import reference as ref
src = open(GRADER + "/test_project.py", encoding="utf-8").read()
def grab(name):
    m = re.search(rf"^{name}: list\[.*?\] = (\[.*?\n\])\n", src, re.S | re.M)
    return ast.literal_eval(m.group(1)) if m else None
sure = [700, 1900, 0, 2600, -300, 1500, 900, 2100, -600, 1100, 400, 1800]
lot_src = re.search(r"B_SIDE_LOTTERIES: list\[.*?\] = (\[.*?\n\])\n", src, re.S).group(1)
from fractions import Fraction
lots = eval(lot_src, {"Fraction": Fraction})
resp = [{"pair_id": i, "choice": "A", "prizes_a": [sure[i]], "probs_a": ["1"], "prizes_b": lots[i][0], "probs_b": lots[i][1]} for i in range(12)]
try:
    print({k: round(v, 4) for k, v in ref.estimate(resp).items()})
except Exception as e:
    print("raised", type(e).__name__, str(e)[:200])
