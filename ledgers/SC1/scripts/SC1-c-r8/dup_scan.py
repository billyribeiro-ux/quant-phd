import json, re, sys
from difflib import SequenceMatcher
path = sys.argv[1]
cards = json.load(open(path))
def norm(s):
    return re.sub(r'\s+', ' ', s.lower()).strip()
seen_f, seen_b = {}, {}
dups = []
for c in cards:
    f, b = norm(c['front']), norm(c['back'])
    if f in seen_f: dups.append(('same-front', seen_f[f], c['id']))
    if b in seen_b: dups.append(('same-back', seen_b[b], c['id']))
    seen_f.setdefault(f, c['id']); seen_b.setdefault(b, c['id'])
near = []
for i in range(len(cards)):
    for j in range(i+1, len(cards)):
        r = SequenceMatcher(None, norm(cards[i]['front']), norm(cards[j]['front'])).ratio()
        if r >= 0.85: near.append((round(r,3), cards[i]['id'], cards[j]['id']))
print('cards', len(cards), 'ids unique', len({c['id'] for c in cards}) == len(cards))
print('exact duplicates:', dups)
print('near-duplicate fronts (ratio>=0.85):', sorted(near, reverse=True)[:40])
