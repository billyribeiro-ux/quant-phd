"""Instances 0-199: validity, distinct outputs across seeds, and strict rounded orderings the grader asserts."""
import sys, importlib.util
from pathlib import Path
root = Path(sys.argv[1]) / "course/modules/E/E1/grader"
spec = importlib.util.spec_from_file_location("inst", root / "instance.py"); inst = importlib.util.module_from_spec(spec); spec.loader.exec_module(inst)
spec2 = importlib.util.spec_from_file_location("ref", root / "reference.py"); ref = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(ref)
bad = []; outs = {}; ranges = {"b": set(), "c": set(), "gap": []}
for s in range(200):
    c = inst.make_instance(s); a, b, cc = c["a"], c["b"], c["c"]
    ranges["b"].add(b); ranges["c"].add(cc); ranges["gap"].append(a - b * cc)
    if not (a > b * cc > 0): bad.append(("invalid", s))
    o = {k: ref.outcome(k, a, b, cc) for k in ref.STRUCTURES}
    outs[s] = tuple(sorted((k, tuple(v.items())) for k, v in o.items()))
    m, co, be = o["monopoly"], o["cournot"], o["bertrand"]
    checks = {
        "vol": m["volume_trades"] < co["volume_trades"] < be["volume_trades"],
        "fee": m["fee_cents"] > co["fee_cents"] > be["fee_cents"] or (m["fee_cents"] > co["fee_cents"] and be["fee_cents"] == cc),
        "welfare": m["welfare_cents"] < co["welfare_cents"] < be["welfare_cents"],
        "dwl": m["deadweight_loss_cents"] > co["deadweight_loss_cents"] > be["deadweight_loss_cents"],
        "profit": m["profit_cents"] > co["profit_cents"],
        "cournot_fee_gt_c": co["fee_cents"] > cc,
    }
    for k, ok in checks.items():
        if not ok: bad.append((k, s))
print("seeds 0-199: invalid or failed orderings:", len(bad), bad[:10])
print("distinct output sets across 200 seeds:", len(set(outs.values())))
print("b values:", sorted(ranges["b"]), "c range:", min(ranges["c"]), max(ranges["c"]), "gap range:", min(ranges["gap"]), max(ranges["gap"]))
print("instances 0-19 distinct:", len({outs[s] for s in range(20)}))
