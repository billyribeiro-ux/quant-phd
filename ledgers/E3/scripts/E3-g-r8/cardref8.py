import json, re, collections
R = '/Users/billyribeiro/.fanout/wt/verifyD8-E3-g'
cards = json.load(open(f'{R}/course/modules/E/E3/cards.json', encoding='utf-8'))
texts = {L: open(f'{L}.txt', encoding='utf-8').read() for L in ('L05','L06','L07','L08')}
sl = [c for c in cards if c['lesson'] in texts]
ref_re = re.compile(r'\b(Definition|Proposition|Theorem|Corollary|Remark|Example|Observation|Lemma|Model|Problem|Lab 1, part|Lab 1)\s*([0-9A-Z]+(?:\.[0-9]+)?)?')
bad = []
for c in sl:
    own = texts[c['lesson']]
    for field in ('front','back'):
        for m in re.finditer(r'\((?:[^()]*?)\)', c[field]):
            seg = m.group(0)
            for rm in ref_re.finditer(seg):
                kind, num = rm.group(1), rm.group(2)
                if not num: continue
                pat = f'{kind} {num}'
                found = [L for L in texts if pat in texts[L]]
                if not found:
                    bad.append((c['id'], c['lesson'], field, seg[:80], pat))
                elif c['lesson'] not in found:
                    bad.append((c['id'], c['lesson'], field, seg[:80], pat+' only in '+','.join(found)))
for b in bad: print(b)
print('checked', len(sl), 'bad', len(bad))
# numbers in card text must appear in slice text
num_re = re.compile(r'\d+(?:\.\d+)?(?:e-?\d+)?|\d+/\d+')
allt = '\n'.join(texts.values())
miss = []
for c in sl:
    for f in ('front','back'):
        for tok in num_re.findall(c[f]):
            if tok not in allt: miss.append((c['id'], f, tok))
print('numbers missing:', miss)
# duplicate fronts/backs
print('dup front', [k for k,v in collections.Counter(c['front'] for c in cards).items() if v>1])
print('dup back', [k for k,v in collections.Counter(c['back'] for c in cards).items() if v>1])
# grade consistency
print('grades', collections.Counter((c['lesson'], c.get('grade')) for c in sl))
print('cards lacking grade:', [c['id'] for c in sl if 'grade' not in c])
print('cards with cite:', [(c['id'], c.get('cite')) for c in sl if 'cite' in c])
