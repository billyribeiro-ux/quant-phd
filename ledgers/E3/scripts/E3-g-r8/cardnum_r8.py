import json, re, sys
base = sys.argv[1]
cards = json.load(open(base + '/course/modules/E/E3/cards.json', encoding='utf-8'))
txt = {L: open(f'{base}/ledgers/E3/scripts/E3-g-r8/{L}.txt', encoding='utf-8').read() for L in ('L05', 'L06', 'L07', 'L08')}
num_re = re.compile(r'(?<![A-Za-z_(])-?\d+(?:\.\d+)?(?:e-?\d+)?')
bad = []
for c in cards:
    if c['lesson'] not in txt:
        continue
    body = c['front'] + ' ' + c['back']
    nums = set(num_re.findall(body))
    for n in sorted(nums):
        t = n.lstrip('-')
        if t in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '100', '1000'):
            continue
        if t not in txt[c['lesson']]:
            bad.append((c['id'], c['lesson'], t))
print('slice cards', sum(1 for c in cards if c['lesson'] in txt))
print('numbers not found verbatim in own lesson text:', len(bad))
for b in bad: print(b)
# duplicates
from collections import Counter
sl = [c for c in cards if c['lesson'] in txt]
fr = Counter(re.sub(r'\W+', ' ', c['front'].lower()).strip() for c in cards)
print('duplicate fronts (whole unit):', [k for k, v in fr.items() if v > 1])
bk = Counter(re.sub(r'\W+', ' ', c['back'].lower()).strip() for c in cards)
print('duplicate backs (whole unit):', [k for k, v in bk.items() if v > 1])
ids = Counter(c['id'] for c in cards)
print('duplicate ids:', [k for k, v in ids.items() if v > 1])
print('slice ids:', len(set(c['id'] for c in sl)))
