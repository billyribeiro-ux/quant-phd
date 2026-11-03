"""Sample seeds 0-19 of the M2 instance generator: validity, and whether the answers (not only labels) differ.

Usage: python3 -I check_instances.py <grader dir>
"""
import sys
sys.path.insert(0, sys.argv[1])
from instance import make_instance  # noqa: E402
import reference  # noqa: E402

rows = []
for seed in range(20):
    inst = make_instance(seed)
    price = reference.bond_price_cents(inst)
    s = reference.sensitivities(inst)
    rows.append((seed, inst["face_cents"], inst["coupon_bps"], inst["maturity_years"], inst["yield_bps"], price,
                 round(s["dprice_dy"], 3), round(s["d2price_dy2"], 3), inst["x0"], tuple(inst["cubic"])))
    assert 1 <= inst["maturity_years"] and inst["yield_bps"] > -10000 and inst["face_cents"] > 0
for r in rows[:5]:
    print(r)
print("distinct prices over seeds 0-19:", len({r[5] for r in rows}), "of 20")
print("distinct dprice_dy over seeds 0-19:", len({r[6] for r in rows}), "of 20")
print("distinct cubic coefficients:", len({r[9] for r in rows}), "of 20")
print("all instances valid (maturity>=1, yield>-1, face>0): True")
