import json, re, sys, html
sys.path.insert(0, '/tmp/M2-v/M2-e/indep')
from txt import text
BASE = '/tmp/verifyB1-M2-e/course/modules/M/M2/'
cards = json.load(open(BASE + 'cards.json', encoding='utf-8'))
# duplicate scan
from collections import Counter
fr = Counter(re.sub(r'\W+', ' ', c['front'].lower()).strip() for c in cards)
print('duplicate fronts:', [k for k, v in fr.items() if v > 1])
ids = Counter(c['id'] for c in cards)
print('duplicate ids:', [k for k, v in ids.items() if v > 1])
print('keys:', Counter(tuple(sorted(c.keys())) for c in cards))
nums_missing = []
for c in cards:
    lesson = c['lesson']
    t = text(BASE + lesson + '.html')
    for field in ('front', 'back'):
        for n in re.findall(r'\d+(?:\.\d+)?', c[field]):
            if n not in t:
                nums_missing.append((c['id'], lesson, field, n))
print('numbers in cards not found verbatim in lesson text:', len(nums_missing))
for x in nums_missing[:60]: print(x)
