"""Round-11: the reference on the suite's fixed 12-response sets (B-side and A-side mirror of test_project.py): score and local-max checks, the 12-response Lab 3 case, and r11d_04's output."""
import math
import sys
from pathlib import Path

work = Path(sys.argv[1])
sys.path.insert(0, str(work))
import test_project as tp  # noqa: E402

sets = {}
b_side = [
    {"pair_id": i, "choice": tp.B_SIDE_CHOICES[i], "prizes_a": [tp.B_SIDE_SURE_A[i]], "probs_a": ["1"],
     "prizes_b": tp.B_SIDE_LOTTERIES[i][0], "probs_b": tp.B_SIDE_LOTTERIES[i][1]}
    for i in range(len(tp.B_SIDE_CHOICES))
]
a_side = [
    {"pair_id": i, "choice": "A" if tp.B_SIDE_CHOICES[i] == "B" else "B", "prizes_a": tp.B_SIDE_LOTTERIES[i][0],
     "probs_a": tp.B_SIDE_LOTTERIES[i][1], "prizes_b": [tp.B_SIDE_SURE_A[i]], "probs_b": ["1"]}
    for i in range(len(tp.B_SIDE_CHOICES))
]
sets["b_side"] = b_side
sets["a_side"] = a_side
for name, resp in sets.items():
    parsed = [tp.parse(r) for r in resp]
    try:
        est = tp.sol.estimate(resp)
    except Exception as err:
        print(name, "raised", type(err).__name__, str(err)[:100])
        continue
    g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
    s5 = tp._largest_score_component(parsed, g, l, k, 1e-5)
    s6 = tp._largest_score_component(parsed, g, l, k, 1e-6)
    lm = max(
        tp.oracle_loglik(parsed, g * (1 + d), l, k) - tp.oracle_loglik(parsed, g, l, k) for d in (1e-3, -1e-3)
    )
    lm = max(lm, max(tp.oracle_loglik(parsed, g, l * (1 + d), k) - tp.oracle_loglik(parsed, g, l, k) for d in (1e-3, -1e-3)))
    lm = max(lm, max(tp.oracle_loglik(parsed, g, l, k * (1 + d)) - tp.oracle_loglik(parsed, g, l, k) for d in (1e-3, -1e-3)))
    print(name, "estimate", {x: round(v, 6) for x, v in est.items()}, f"score(1e-5)={s5:.3e} score(1e-6)={s6:.3e} localmax_excess={lm:.3e}")
