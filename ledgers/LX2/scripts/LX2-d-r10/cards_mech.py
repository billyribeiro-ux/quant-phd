import json, re, sys, html
ROOT = sys.argv[1]
cards = json.load(open(ROOT + '/course/modules/LX/LX2/cards.json'))
refs = json.load(open(ROOT + '/references/references.json'))
keys = {e['key'] for e in refs['entries']}
lessons = {}
for L in ['L01', 'L02', 'L03', 'L04']:
    raw = open(f'{ROOT}/course/modules/LX/LX2/{L}.html', encoding='utf-8').read()
    txt = html.unescape(re.sub(r'<[^>]+>', ' ', raw))
    txt = re.sub(r'\s+', ' ', txt)
    lessons[L] = txt
ids = [c['id'] for c in cards]
print('count', len(cards), 'unique ids', len(set(ids)))
print('keys ok:', all(all(k in keys for k in (c.get('cite') or [])) for c in cards))
print('cite-field keys:', sorted({k for c in cards for k in (c.get('cite') or [])}))
print('grades:', {g: sum(1 for c in cards if c.get('grade') == g) for g in ['T', 'C', None]})
print('fields:', sorted({tuple(sorted(c.keys())) for c in cards}))
# numeric tokens
numre = re.compile(r'\d[\d,\.]*\d|\d')
bad = []
for c in cards:
    L = c['lesson']
    toks = set(numre.findall(c['front'] + ' ' + c['back'] + ' ' + (c.get('basis') or '')))
    for t in sorted(toks):
        t2 = t.rstrip('.,')
        if t2 not in lessons[L]:
            bad.append((c['id'], L, t2))
print('numeric tokens absent from own lesson text:', bad)
# dup scan
fr = [c['front'] for c in cards]; bk = [c['back'] for c in cards]
print('dup fronts', len(fr) - len(set(fr)), 'dup backs', len(bk) - len(set(bk)))
# years
print('years in cards:', [(c['id'], m) for c in cards for m in re.findall(r'\b(1[89]\d\d|20\d\d)\b', c['front'] + c['back'])])
# process words
pw = re.compile(r'\b(we (?:decided|changed|fixed)|builder|verifier|round \d|ledger|rubric|process|iteration|the agent)\b', re.I)
print('process words:', [(c['id'], m.group(0)) for c in cards for m in pw.finditer(c['front'] + ' ' + c['back'])])
# symbols
