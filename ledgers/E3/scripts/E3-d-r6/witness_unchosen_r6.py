"""Witness for e3d6_02: the grader's B-side data with every choice set to A (the mixed lotteries are then all unchosen).

Run: python -I witness_unchosen_r6.py <dir containing elicit.py>
"""
import sys
sys.path.insert(0, sys.argv[1])
import elicit as sol  # noqa: E402

PRIZES_A = [700, 1900, 0, 2600, -300, 1500, 900, 2100, -600, 1100, 400, 1800]
LOTT = [([2000, -1500], ["1/2", "1/2"]), ([3000, -2500], ["2/5", "3/5"]), ([1500, -1000], ["3/4", "1/4"]),
        ([4000, -3000], ["1/3", "2/3"]), ([2500, -4000], ["1/2", "1/2"]), ([1000, -500], ["4/5", "1/5"]),
        ([3500, -2000], ["1/4", "3/4"]), ([800, -1200], ["1/2", "1/2"]), ([5000, -3000], ["3/10", "7/10"]),
        ([2200, -2800], ["3/5", "2/5"]), ([1200, -600], ["1/2", "1/2"]), ([4500, -5000], ["2/3", "1/3"])]
CHOICES_TEST = ["A", "B", "B", "A", "B", "A", "A", "B", "A", "A", "B", "B"]
for label, choices in (("grader choices", CHOICES_TEST), ("all A", ["A"] * 12)):
    resp = [{"pair_id": i, "choice": choices[i], "prizes_a": [PRIZES_A[i]], "probs_a": ["1"],
             "prizes_b": LOTT[i][0], "probs_b": LOTT[i][1]} for i in range(12)]
    try:
        out = sol.estimate(resp)
        print(label, "accepted: gamma_hat", round(out["gamma_hat"], 4), "lambda_hat", round(out["lambda_hat"], 4))
    except ValueError as err:
        print(label, "refused with ValueError:", err)
    except Exception as err:
        print(label, "raised", type(err).__name__, str(err)[:80])
