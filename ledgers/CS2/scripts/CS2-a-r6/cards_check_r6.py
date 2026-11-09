import json, collections
recs = json.load(open('course/modules/CS/CS2/cards.json'))
ids = [r['id'] for r in recs]
dups = [k for k, v in collections.Counter(ids).items() if v > 1]
print('records', len(recs), 'duplicate ids', dups)
fronts = collections.Counter(r['front'] for r in recs)
print('duplicate fronts', [f for f, v in fronts.items() if v > 1])
bad = []
for r in recs:
    if r['grade'] == 'T' and ('basis' in r or 'cite' in r):
        bad.append(('T with basis/cite', r['id']))
    if r['grade'] != 'T' and not (r.get('basis') or r.get('cite')):
        bad.append(('non-T without basis/cite', r['id']))
    if r['grade'] not in ('T', 'C', 'B', 'A', 'D', 'X'):
        bad.append(('odd grade', r['id'], r['grade']))
print('grade/basis problems', bad)
by = collections.Counter(r['grade'] for r in recs)
print('grade counts', dict(by))
l14 = [r for r in recs if r['lesson'] in ('L01', 'L02', 'L03', 'L04')]
print('L01-L04 cards', len(l14), collections.Counter(r['lesson'] for r in l14))
for r in l14:
    if r['lesson'] == 'L04':
        print(r['id'], r['grade'], r.get('basis', ''), '|', r['front'][:70])
