import json, re, subprocess, sys
sys.path.insert(0, '/Users/billyribeiro/.fanout/wt/verifyF31-SC1-b/ledgers/SC1/scripts/SC1-b-r1')
from hunks import changed_lines, FILES
R = '/Users/billyribeiro/.fanout/wt/verifyF31-SC1-b'
OUT = R + '/ledgers/SC1/scripts/SC1-b-r1/out/'
def show(rev, path):
    return json.loads(subprocess.run(['git', 'show', f'{rev}:{path}'], capture_output=True, text=True, cwd=R).stdout)
# 1. cards diff by id
a = show('8e5751c9', 'course/modules/SC/SC1/cards.json'); b = show('HEAD', 'course/modules/SC/SC1/cards.json')
ka = {c['id']: c for c in a}; kb = {c['id']: c for c in b}
lines = []
lines.append(f'base cards {len(a)} head cards {len(b)}')
lines.append('removed: ' + ', '.join(sorted(set(ka) - set(kb))))
lines.append('added: ' + ', '.join(sorted(set(kb) - set(ka))))
lines.append('changed: ' + ', '.join(sorted(i for i in ka if i in kb and ka[i] != kb[i])))
slice_b = lambda c: c['lesson'] in ('L04', 'L05', 'L06')
lines.append('slice-b cards at HEAD: %d' % sum(1 for c in b if slice_b(c)))
lines.append('slice-b cards at base: %d' % sum(1 for c in a if slice_b(c)))
open(OUT + 'cards_diff_by_id_b_r1.txt', 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
# 2. process words and D1-D9 names in new/changed slice-b card text
pw = re.compile(r'\b(build|builder|round|verifier|verified|fixer|architect|ruling|ledger|planner|precedent)\b', re.I)
dag = re.compile(r'(Ito|SDE|Ornstein|Uhlenbeck|Girsanov|Feynman|Poisson|L[ée]vy|Black-Scholes|barrier|Monte Carlo|bias|estimator|bridge|Bessel|Kolmogorov (forward|backward))', re.I)
hits = []
for c in b:
    if slice_b(c):
        t = c['front'] + ' ' + c['back']
        for m in pw.finditer(t): hits.append(f"process {c['id']} {m.group(0)}")
        for m in dag.finditer(t): hits.append(f"dag {c['id']} {m.group(0)}")
hits.append('scan of %d slice-b cards done' % sum(1 for c in b if slice_b(c)))
open(OUT + 'process_dag_scan_b_r1.txt', 'w').write('\n'.join(hits) + '\n')
print('\n'.join(hits))
# 3. references: keys and changed entries
ra = show('8e5751c9', 'references/references.json'); rb = show('HEAD', 'references/references.json')
ea = {e['key']: e for e in ra['entries']}; eb = {e['key']: e for e in rb['entries']}
out = [f'keys equal: {set(ea) == set(eb)} ({len(eb)} entries)', f"shreve2004stochastic identical: {ea['shreve2004stochastic'] == eb['shreve2004stochastic']}", 'changed keys: ' + ', '.join(k for k in ea if ea[k] != eb.get(k))]
open(OUT + 'refs_check_b_r1.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
# 4. hunk intersection (changed new-side lines per file)
for k in ('L01', 'L02', 'L03', 'index', 'plan', 'open', 'rulings'):
    s, _ = changed_lines(FILES[k])
    nums = sorted(i for side, i in s if side == 'new')
    print(k, FILES[k], 'changed new-side lines:', nums[:40], '...' if len(nums) > 40 else '')
