# Validity and diversity check of grader/instance.py over seeds 0-49, and the reference answers per seed.
import sys
sys.path.insert(0, sys.argv[1] + '/course/modules/M/M2/grader')
sys.path.insert(0, sys.argv[1] + '/ledgers/M2/scripts/M2-e-r1')
from instance import make_instance
import importlib.util
spec = importlib.util.spec_from_file_location('ref', sys.argv[1] + '/course/modules/M/M2/grader/reference.py')
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
rows = []
for seed in range(50):
    i = make_instance(seed)
    assert i['maturity_years'] >= 1 and i['yield_bps'] > -10000 and i['face_cents'] > 0
    assert make_instance(seed) == i
    rows.append((seed, round(ref.sensitivities(i)['dprice_dy'], 2), ref.bond_price_cents(i)))
print('valid 50/50; distinct dprice_dy', len({r[1] for r in rows}), '; distinct price', len({r[2] for r in rows}))
