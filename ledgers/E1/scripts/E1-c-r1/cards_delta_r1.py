import json, sys
old = json.load(open(sys.argv[1]))
new = json.load(open(sys.argv[2]))
def idx(cs):
    d = {}
    for c in cs:
        assert c['id'] not in d, ('dup id', c['id'])
        d[c['id']] = c
    return d
o, n = idx(old), idx(new)
print('old cards', len(old), 'new cards', len(new), 'unique new ids', len(n))
print('removed ids', sorted(set(o) - set(n)))
print('added ids', sorted(set(n) - set(o)))
changed = [k for k in sorted(set(o) & set(n)) if o[k] != n[k]]
print('changed ids', changed)
for k in changed:
    diffs = [f for f in set(o[k]) | set(n[k]) if o[k].get(f) != n[k].get(f)]
    print(k, 'fields differing:', sorted(diffs), 'lesson', n[k].get('lesson'))
print('order preserved for common ids:', [c['id'] for c in old if c['id'] in n] == [c['id'] for c in new if c['id'] in o])
# duplicate fronts/backs
from collections import Counter
fr = Counter(c['front'] for c in new); bk = Counter(c['back'] for c in new)
print('dup fronts', [f for f, k in fr.items() if k > 1])
print('dup backs', [b for b, k in bk.items() if k > 1])
print('count by lesson', Counter(c['lesson'] for c in new))
print('missing fields', [c['id'] for c in new if not all(c.get(x) for x in ('id','lesson','front','back'))])
print('grades', Counter(c.get('grade') for c in new))
