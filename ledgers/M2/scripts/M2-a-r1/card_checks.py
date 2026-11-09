import json, re, sys, collections
head = json.load(open(sys.argv[1]))
base = json.load(open(sys.argv[2]))
ids = [c['id'] for c in head]
print('cards', len(head), 'unique ids', len(set(ids)))
fronts = collections.Counter(re.sub(r'\s+', ' ', c['front'].strip().lower()) for c in head)
print('duplicate fronts', [f for f, n in fronts.items() if n > 1])
backs = collections.Counter(re.sub(r'\s+', ' ', c['back'].strip().lower()) for c in head)
print('duplicate backs', [f[:60] for f, n in backs.items() if n > 1])
bylesson = collections.Counter(c['lesson'] for c in head)
print('per lesson', dict(sorted(bylesson.items(), key=lambda kv: (kv[0][0], int(kv[0][1:])))))
slice_ids = [c['id'] for c in head if c['lesson'] in {'L01','L02','L03','L04','L05','L06'}]
print('slice cards', len(slice_ids), 'first/last', slice_ids[0], slice_ids[-1])
bmap = {c['id']: c for c in base}
hmap = {c['id']: c for c in head}
print('slice cards byte-identical to base (json dump):', [i for i in slice_ids if i in bmap and json.dumps(bmap[i], sort_keys=True) != json.dumps(hmap[i], sort_keys=True)])
print('keys', sorted({k for c in head for k in c}))
print('grades', collections.Counter(c.get('grade') for c in head))
nograde = [c['id'] for c in head if 'grade' not in c]
print('no grade count', len(nograde))
# card id numbering
nums = sorted(int(i.split('-c')[1]) for i in ids)
missing = sorted(set(range(nums[0], nums[-1]+1)) - set(nums))
print('id range', nums[0], nums[-1], 'missing numbers', missing)
