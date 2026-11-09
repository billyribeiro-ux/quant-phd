import json, difflib, itertools
cards = json.load(open('course/modules/FC/FC2/cards.json'))
pairs = []
for a, b in itertools.combinations(cards, 2):
    fr = difflib.SequenceMatcher(None, a['front'].lower(), b['front'].lower()).ratio()
    bk = difflib.SequenceMatcher(None, a['back'].lower(), b['back'].lower()).ratio()
    if fr > 0.6 or bk > 0.6:
        pairs.append((round(fr, 2), round(bk, 2), a['id'], a['lesson'], b['id'], b['lesson']))
print('pairs front>0.6 or back>0.6:', len(pairs))
for p in sorted(pairs, reverse=True):
    if p[3] in ('L04', 'L05', 'L06') or p[5] in ('L04', 'L05', 'L06'):
        print(p)
print('--- all new-card (c188-c200) pairs')
new = {c['id'] for c in cards if int(c['id'].split('c')[-1]) >= 188}
for p in pairs:
    if p[2] in new or p[4] in new:
        print(p)
