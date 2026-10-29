import json, subprocess, sys
root = sys.argv[1]
old = json.loads(subprocess.check_output(['git', '-C', root, 'show', 'f42f432:course/modules/M/M4/cards.json']))
new = json.load(open(root + '/course/modules/M/M4/cards.json'))
o = {c['id']: c for c in old}
n = {c['id']: c for c in new}
print('count', len(old), len(new), 'unique', len(n) == len(new))
print('removed', sorted(set(o) - set(n)), 'added', sorted(set(n) - set(o)))
print('changed', sorted(k for k in o if k in n and o[k] != n[k]))
print('M4-c123 present', 'M4-c123' in n)
sl = [c for c in new if c['lesson'] in ('L08', 'L09', 'L10')]
print('L08-L10 cards', len(sl), 'unique', len({c['id'] for c in sl}) == len(sl))
for k in ['M4-c118', 'M4-c124', 'M4-c140', 'M4-c163', 'M4-c125', 'M4-c186', 'M4-c132']:
    print(k, n[k]['lesson'], n[k]['grade'], 'changed' if o[k] != n[k] else 'byte-identical-entry')
