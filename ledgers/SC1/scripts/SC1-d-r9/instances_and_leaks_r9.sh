#!/bin/bash
# Round-9 checks: instance validity/variety (seeds 0-19), starter failure count, and failure-output leak probe.
REPO=/Users/billyribeiro/dev/quant-phd/.venv/bin
ROOT=/Users/billyribeiro/.fanout/wt/verifyE9-SC1-d
R=$ROOT/ledgers/SC1/scripts/SC1-d-r9
W=$(mktemp -d /tmp/sc1d-r9-leak-XXXX)
cp $ROOT/course/modules/SC/SC1/grader/{instance.py,test_project.py} $W/
cp $ROOT/course/modules/SC/SC1/grader/starter.py $W/bm_checks.py
(cd $W && QF_SEED=0 $REPO/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
cp $ROOT/ledgers/SC1/mutants/m01_reflection_factor_dropped.py $W/bm_checks.py
(cd $W && QF_SEED=0 $REPO/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | grep -c '^E ')
(cd $W && QF_SEED=0 $REPO/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | grep -i -E 'expected|0\.0[0-9]{4}|[0-9]\.[0-9]{6}' | head -5)
rm -rf $W
$REPO/python -I -c "
import sys, importlib.util
sys.path.insert(0, '$ROOT/course/modules/SC/SC1/grader')
from instance import make_instance
spec = importlib.util.spec_from_file_location('ref', '$ROOT/course/modules/SC/SC1/grader/reference.py'); ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
rows = []
for s in range(20):
    i = make_instance(s)
    rows.append((i['H'], i['a'], i['n_steps'], i['n_paths'], round(ref.discrete_max_exceedance(i, i['n_steps'])[0], 4)))
print('valid:', all(h > 0 and a > 0 and 4 <= n <= 256 and 400 <= p <= 800 and n * p <= 200000 for h, a, n, p, _ in rows))
print('distinct levels (seeds 0-19):', len({r[1] for r in rows}), ' distinct estimates:', len({r[4] for r in rows}))
"
