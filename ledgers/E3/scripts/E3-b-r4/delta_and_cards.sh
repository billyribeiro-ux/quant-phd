#!/bin/bash
# Round-4 delta of the E3-b subjects (ccfdf4c = previous pin, HEAD = b276325) and card checks.
cd /Users/billyribeiro/.fanout/wt/verifyC4-E3-b
for f in course/modules/E/E3/L04.html course/modules/E/E3/L05.html course/modules/E/E3/L06.html tests/labs/E3/lab-E3-L04-1.py tests/labs/E3/lab-E3-L05-1.py tests/labs/E3/lab-E3-L06-1.py course/modules/E/E3/cards.json notation/notation.json references/references.json; do
  a=$(git show ccfdf4c:$f | shasum -a 256 | cut -c1-16); b=$(git show HEAD:$f | shasum -a 256 | cut -c1-16)
  echo "$f $a $b $([ $a = $b ] && echo SAME || echo CHANGED)"
done
python3 -I - <<'PY'
import json, subprocess
def cards(rev):
    s = subprocess.run(['git', 'show', f'{rev}:course/modules/E/E3/cards.json'], capture_output=True, text=True).stdout
    return {c['id']: c for c in json.loads(s)}
a, b = cards('ccfdf4c'), cards('HEAD')
print('changed cards (all units):', sorted(k for k in b if a.get(k) != b[k]))
print('changed cards in L04-L06:', sorted(k for k in b if a.get(k) != b[k] and b[k]['lesson'] in ('L04', 'L05', 'L06')))
cs = list(b.values())
print('c092 grade', b['E3-c092']['grade'], '| c093 grade', b['E3-c093']['grade'], 'basis', b['E3-c093'].get('basis'))
print('key-results row 500 grade is C (L05.html:500); card E3-c093 grade', b['E3-c093']['grade'])
PY
grep -n 'data-grade="C">C</span></td><td>Lab 1 (exact Fraction' course/modules/E/E3/L05.html | cut -c1-120
