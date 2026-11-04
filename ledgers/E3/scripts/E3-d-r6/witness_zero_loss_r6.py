"""Witness for e3d6_01 and e3d6_02: estimate() on sets the page says must be refused or accepted.

Run: python -I witness_zero_loss_r6.py <dir containing elicit.py to test>
"""
import sys
sys.path.insert(0, sys.argv[1])
import elicit as sol  # noqa: E402

def resp(pid, choice, pa, qa, pb, qb):
    return {"pair_id": pid, "choice": choice, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb}

# W1: the only mixed-looking lottery has a sure zero prize as its "loss"; the page needs a prize below zero.
W1 = [resp(0, "A", [300, 0], ["1/2", "1/2"], [200], ["1"]),
      resp(1, "B", [500], ["1"], [50, 900], ["1/2", "1/2"])]
# W2: the only mixed lottery is the unchosen B lottery; the page's rule counts any lottery of any response.
W2 = [resp(0, "A", [700], ["1"], [1000, -800], ["1/2", "1/2"]),
      resp(1, "A", [600], ["1"], [1500, -400], ["1/2", "1/2"]),
      resp(2, "A", [900], ["1"], [2000, 300], ["1/2", "1/2"]),
      resp(3, "A", [800], ["1"], [1200, 100], ["1/2", "1/2"]),
      resp(4, "B", [500], ["1"], [1100, 400], ["1/2", "1/2"])]
for name, w in (("W1", W1), ("W2", W2)):
    try:
        out = sol.estimate(w)
        print(name, "accepted; returned keys:", sorted(out))
    except ValueError as err:
        print(name, "refused with ValueError:", err)
    except Exception as err:
        print(name, "raised", type(err).__name__, err)
