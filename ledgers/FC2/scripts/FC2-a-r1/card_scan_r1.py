import json, difflib, itertools
cards = json.load(open('course/modules/FC/FC2/cards.json', encoding='utf-8'))
ids = {c['id']: c for c in cards}
# 1. near-duplicate fronts over all pairs (ratio > 0.8)
pairs = []
for a, b in itertools.combinations(cards, 2):
    r = difflib.SequenceMatcher(None, a['front'], b['front']).ratio()
    if r > 0.8:
        pairs.append((round(r, 3), a['id'], b['id']))
print('front pairs > 0.8:', sorted(pairs, reverse=True))
# 2. changed cards: best match of front and of back against every other card
for cid in ['FC2-c179', 'FC2-c192', 'FC2-c201']:
    me = ids[cid]
    best = []
    for o in cards:
        if o['id'] == cid:
            continue
        best.append((round(difflib.SequenceMatcher(None, me['front'], o['front']).ratio(), 3), o['id'], o['front'][:90]))
    best.sort(reverse=True)
    print(cid, 'top fronts:', best[:3])
# 3. grades for L01-L03 and changed cards
from collections import Counter
print('grade counts', Counter(c.get('grade') for c in cards))
for cid in ['FC2-c179', 'FC2-c192', 'FC2-c201']:
    print(cid, 'grade field:', ids[cid].get('grade', '<absent>'), 'keys:', sorted(ids[cid].keys()))
# 4. scope words in changed cards
import re
words = re.compile(r'\b(only|all|always|every|any|same|drives|exactly)\b', re.I)
for cid in ['FC2-c179', 'FC2-c192', 'FC2-c201']:
    t = ids[cid]['front'] + ' || ' + ids[cid]['back']
    print(cid, 'scope words:', [m.group(0) for m in words.finditer(t)])
# 5. symbol tokens in changed cards
for cid in ['FC2-c179', 'FC2-c192', 'FC2-c201']:
    t = ids[cid]['front'] + ' || ' + ids[cid]['back']
    print(cid, 'symbol-like tokens:', sorted(set(re.findall(r'\b[A-Za-z]\b|[A-Za-z]+_\{?[A-Za-z0-9]+\}?|\^\+', t))))
