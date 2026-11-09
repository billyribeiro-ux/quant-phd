import json, collections, re, sys
path = sys.argv[1]
cards = json.load(open(path, encoding='utf-8'))
ids = [c['id'] for c in cards]
print('cards', len(cards), 'unique ids', len(set(ids)), 'sorted', ids == sorted(ids))
print('id range', ids[0], ids[-1])
norm = lambda s: re.sub(r'\s+', ' ', s.strip().lower())
fr = collections.Counter(norm(c['front']) for c in cards)
bk = collections.Counter(norm(c['back']) for c in cards)
print('dup fronts', [k for k, v in fr.items() if v > 1])
print('dup backs', [k for k, v in bk.items() if v > 1])
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
print('key sets', dict(keys))
print('grades', collections.Counter(c.get('grade') for c in cards))
bad = []
for c in cards:
    g = c.get('grade')
    if g == 'C' and not c.get('basis'):
        bad.append((c['id'], 'C without basis'))
    if g not in (None, 'T', 'C'):
        bad.append((c['id'], 'bad grade ' + str(g)))
    if g in ('T', 'C') and c.get('basis') and g == 'T':
        bad.append((c['id'], 'T with basis (informational)'))
print('flags', bad)
print('per lesson', collections.Counter(c['lesson'] for c in cards))
print('L07-L09 ids', [c['id'] for c in cards if c['lesson'] in ('L07','L08','L09')])
print('L07-L09 grade none', [c['id'] for c in cards if c['lesson'] in ('L07','L08','L09') and c.get('grade') is None])
