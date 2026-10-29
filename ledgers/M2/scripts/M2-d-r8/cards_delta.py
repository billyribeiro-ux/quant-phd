import json, sys
old = json.load(open(sys.argv[1])); new = json.load(open(sys.argv[2]))
def key(c): return c.get('id')
print('old count', len(old), 'new count', len(new))
oi = {key(c): c for c in old}; ni = {key(c): c for c in new}
print('ids only old:', sorted(set(oi)-set(ni)))
print('ids only new:', sorted(set(ni)-set(oi)))
for k in sorted(set(oi)&set(ni)):
    if oi[k] != ni[k]:
        print('CHANGED', k, ni[k].get('lesson'), ni[k].get('grade'))
        for f in ('front','back','grade','basis'):
            if oi[k].get(f) != ni[k].get(f): print('   ', f, 'OLD:', oi[k].get(f)); print('    ', f, 'NEW:', ni[k].get(f))
