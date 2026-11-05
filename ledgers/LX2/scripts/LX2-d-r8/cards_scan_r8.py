import json, re, html, difflib, sys
base = sys.argv[1].rstrip('/') + '/'
cards = json.load(open(base + 'cards.json', encoding='utf-8'))
ids = [c['id'] for c in cards]
print('cards', len(cards), 'unique', len(set(ids)))
exp = ['LX2-c%03d' % i for i in range(1, 100)]
print('missing', [i for i in exp if i not in ids], 'extra', [i for i in ids if i not in exp])
txt = {}
for L in ['L01', 'L02', 'L03', 'L04']:
    t = html.unescape(open(base + L + '.html', encoding='utf-8').read())
    t = re.sub(r'<[^>]+>', ' ', t)
    txt[L] = re.sub(r'\s+', ' ', t)
ungraded = [c['id'] for c in cards if 'grade' not in c]
print('ungraded', len(ungraded), ungraded)
print('graded C', sum(1 for c in cards if c.get('grade') == 'C'), 'graded T', sum(1 for c in cards if c.get('grade') == 'T'))
lab_readoffs = [c['id'] for c in cards if re.search(r'Lab 1', (c.get('basis') or '') + c['front'] + c['back']) and 'grade' not in c]
print('ungraded cards that name Lab 1 output', lab_readoffs)
def norm(s): return re.sub(r'\W+', ' ', s.lower()).strip()
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        r = difflib.SequenceMatcher(None, norm(a['front'] + ' ' + a['back']), norm(b['front'] + ' ' + b['back'])).ratio()
        if r > 0.6:
            pairs.append((round(r, 3), a['id'], b['id']))
print('near-duplicate pairs (ratio > 0.6):', sorted(pairs, reverse=True))
numre = re.compile(r'(?<![\w.])(\d+(?:[.,]\d+)?(?:/\d+)?)')
bad = []
for c in cards:
    toks = set(numre.findall(c['front'] + ' ' + c['back']))
    for t in toks:
        if t not in txt[c['lesson']]:
            bad.append((c['id'], c['lesson'], t))
print('numeric tokens absent from the card\'s own lesson:', bad)
proc = re.compile(r'\b(round|verif\w*|builder|auditor|todo|fixme|agent|reviewer|previous)\b', re.I)
print('process words in card text:', [c['id'] for c in cards if proc.search(c['front'] + ' ' + c['back'])])
