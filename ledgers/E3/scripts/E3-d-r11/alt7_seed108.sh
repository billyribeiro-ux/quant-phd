#!/bin/sh
# Round-11: the Armijo-Newton alternative through the current suite at seed 108 (the seed where the reference also fails), and its score there.
W=/Users/billyribeiro/.fanout/scratch-E3-d-r11/alt7_108
ROOT="$1"; PY="$2"; ALT="$3"
rm -rf "$W" && mkdir -p "$W" && cp "$ROOT/course/modules/E/E3/grader/test_project.py" "$ROOT/course/modules/E/E3/grader/instance.py" "$W/" && cp "$ALT/elicit.py" "$W/elicit.py"
cd "$W" && QF_SEED=108 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | grep -E "^FAILED|passed|failed" | head -3
QF_SEED=108 "$PY" -c "
import sys, json
sys.path.insert(0, '.')
import elicit
from instance import make_instance
import test_project as tp
r = json.loads(str(make_instance(108)['responses_json']))
e = elicit.estimate(r)
parsed = [tp.parse(x) for x in r]
g, l, k = e['gamma_hat'], e['lambda_hat'], e['kappa_hat']
print('alt7 seed 108 estimate', {x: round(v, 6) for x, v in e.items()})
print('score step1e-5 %.4e step1e-6 %.4e' % (tp._largest_score_component(parsed, g, l, k, 1e-5), tp._largest_score_component(parsed, g, l, k, 1e-6)))
" 2>&1 | tail -3
