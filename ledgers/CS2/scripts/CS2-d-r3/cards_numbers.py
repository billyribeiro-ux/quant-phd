import json, re, sys
cards = json.load(open('/Users/billyribeiro/.fanout/wt/verifyD3-CS2-d/course/modules/CS/CS2/cards.json'))
texts = {}
for L in sorted({c['lesson'] for c in cards}):
    texts[L] = open(f'/tmp/cs2d3/txt/{L}.txt', encoding='utf-8').read()
allp = open('/tmp/cs2d3/txt/project.txt', encoding='utf-8').read()
bad = 0
for c in cards:
    t = texts[c['lesson']]
    nums = set(re.findall(r'\d+(?:\.\d+)?', c['front'] + ' ' + c['back']))
    missing = [n for n in nums if n not in t]
    if missing:
        bad += 1
        print(c['id'], c['lesson'], 'numbers not in lesson text:', missing)
    # grade/basis
    if c['grade'] == 'T' and 'basis' in c: print(c['id'], 'T with basis')
    if c['grade'] == 'C' and 'basis' not in c: print(c['id'], 'C without basis')
    if c['grade'] not in ('T', 'C'): print(c['id'], 'grade', c['grade'])
print('cards', len(cards), 'with unmatched numbers', bad)
