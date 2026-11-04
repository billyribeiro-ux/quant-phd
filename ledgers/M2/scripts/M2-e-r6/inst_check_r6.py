import sys
sys.path.insert(0, '.')
from instance import make_instance
import sensitivity_engine as ref
rows = []
import random
seeds = list(range(0, 50))
bad = []
for s in seeds:
    inst = make_instance(s)
    if not (inst['maturity_years'] >= 1 and inst['yield_bps'] > -10000 and inst['face_cents'] > 0):
        bad.append(s)
    p = ref.bond_price_cents(inst); sens = ref.sensitivities(inst)
    rows.append((s, inst['face_cents'], inst['coupon_bps'], inst['maturity_years'], inst['yield_bps'], p, round(sens['dprice_dy'], 2)))
print('invalid seeds', bad)
for r in rows[:20]: print(r)
print('distinct prices', len({r[5] for r in rows}), 'distinct dprice', len({r[6] for r in rows}), 'distinct labels(face,coupon,maturity,yield)', len({r[1:5] for r in rows}))
