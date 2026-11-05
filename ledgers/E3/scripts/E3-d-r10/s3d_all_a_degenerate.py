"""Round-10 check of the docstring numbers in test_estimate_counts_a_mixed_lottery_whether_or_not_it_was_chosen."""
import sys
sys.path.insert(0, "/tmp/E3d_r10_ws/ref")
import elicit as ref  # noqa: E402
B_SIDE_SURE_A = [700, 1900, 0, 2600, -300, 1500, 900, 2100, -600, 1100, 400, 1800]
B_SIDE_LOTTERIES = [
    ([2000, -1500], ["1/2", "1/2"]), ([3000, -2500], ["2/5", "3/5"]), ([1500, -1000], ["3/4", "1/4"]),
    ([4000, -3000], ["1/3", "2/3"]), ([2500, -4000], ["1/2", "1/2"]), ([1000, -500], ["4/5", "1/5"]),
    ([3500, -2000], ["1/4", "3/4"]), ([800, -1200], ["1/2", "1/2"]), ([5000, -3000], ["3/10", "7/10"]),
    ([2200, -2800], ["3/5", "2/5"]), ([1200, -600], ["1/2", "1/2"]), ([4500, -5000], ["2/3", "1/3"]),
]
responses = [
    {"pair_id": i, "choice": "A", "prizes_a": [B_SIDE_SURE_A[i]], "probs_a": ["1"],
     "prizes_b": B_SIDE_LOTTERIES[i][0], "probs_b": B_SIDE_LOTTERIES[i][1]}
    for i in range(len(B_SIDE_SURE_A))
]
try:
    fit = ref.estimate(responses)
    print({k: round(v, 4) for k, v in fit.items()})
except Exception as e:  # report what the reference does
    print("reference raised", type(e).__name__, str(e)[:200])
