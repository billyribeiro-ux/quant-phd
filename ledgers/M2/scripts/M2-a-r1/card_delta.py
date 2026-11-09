import json, sys
base = json.load(open(sys.argv[1]))
head = json.load(open(sys.argv[2]))
def idx(cards):
    d = {}
    for c in cards:
        assert c['id'] not in d, ('duplicate id', c['id'])
        d[c['id']] = c
    return d
b, h = idx(base), idx(head)
print('base cards', len(base), 'head cards', len(head))
print('removed', sorted(set(b) - set(h)))
print('added', sorted(set(h) - set(b)))
changed = sorted(k for k in set(b) & set(h) if b[k] != h[k])
print('changed', changed)
for k in changed:
    print(k, h[k]['lesson'], 'changed fields:', sorted(f for f in set(b[k]) | set(h[k]) if b[k].get(f) != h[k].get(f)))
