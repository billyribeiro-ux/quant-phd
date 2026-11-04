import json, difflib, itertools, re
cards = json.load(open('course/modules/E/E3/cards.json'))
def norm(s): return re.sub(r'[^a-z0-9 ]', '', s.lower())
exact_f = {}; exact_b = {}
for c in cards:
    exact_f.setdefault(norm(c['front']), []).append(c['id'])
    exact_b.setdefault(norm(c['back']), []).append(c['id'])
print('dup ids', len(cards) - len({c['id'] for c in cards}))
print('dup fronts', [v for v in exact_f.values() if len(v) > 1])
print('dup backs', [v for v in exact_b.values() if len(v) > 1])
rows = []
for a, b in itertools.combinations(cards, 2):
    fr = difflib.SequenceMatcher(None, norm(a['front']), norm(b['front'])).ratio()
    bk = difflib.SequenceMatcher(None, norm(a['back']), norm(b['back'])).ratio()
    if fr > 0.5 or bk > 0.6:
        rows.append((round(fr, 2), round(bk, 2), a['id'], a['lesson'], b['id'], b['lesson']))
for r in sorted(rows, reverse=True)[:40]:
    print(r)
