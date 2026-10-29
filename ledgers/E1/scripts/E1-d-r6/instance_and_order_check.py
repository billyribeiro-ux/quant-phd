"""Round-6 E1-d: (1) sample 20 grader seeds, check validity and that outputs differ; (2) brute-force Proposition 5's
printed-ordering claim over whole-number a, b, c with d > 6b (b 1..3, c 1..60, d 6b+1..400) using the reference."""
import sys
sys.path.insert(0, sys.argv[1])
from instance import make_instance
from reference import outcome

rows = []
for seed in range(20):
    case = make_instance(seed)
    a, b, c = case["a"], case["b"], case["c"]
    assert a > b * c > 0 and b * c < a and (a - b * c) > 6 * b, case
    rows.append(((a, b, c), tuple(outcome(s, a, b, c)[k] for s in ("monopoly", "cournot", "bertrand")
                                  for k in ("volume_trades", "fee_cents", "welfare_cents"))))
print("seeds 0-19 valid; distinct inputs:", len({r[0] for r in rows}), "distinct outputs:", len({r[1] for r in rows}))

bad = 0
checked = 0
for b in (1, 2, 3):
    for c in range(1, 61):
        for d in range(6 * b + 1, 401):
            a = b * c + d
            checked += 1
            m, cu, be = (outcome(s, a, b, c) for s in ("monopoly", "cournot", "bertrand"))
            ok = (m["volume_trades"] < cu["volume_trades"] < be["volume_trades"]
                  and m["fee_cents"] > cu["fee_cents"] > be["fee_cents"]
                  and m["welfare_cents"] < cu["welfare_cents"] < be["welfare_cents"]
                  and m["deadweight_loss_cents"] > cu["deadweight_loss_cents"] > be["deadweight_loss_cents"]
                  and m["profit_cents"] > cu["profit_cents"] > be["profit_cents"])
            bad += not ok
print("checked", checked, "triples; ordering failures:", bad)
