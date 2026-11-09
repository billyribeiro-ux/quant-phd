import json, re, sys, html
from collections import Counter
base = sys.argv[1]
cards = json.load(open(base + '/course/modules/E/E1/cards.json'))
old = json.load(open(sys.argv[2]))
oldids = {c['id'] for c in old}
changed = {'E1-c018','E1-c023','E1-c030','E1-c039','E1-c056','E1-c101','E1-c161','E1-c162','E1-c163','E1-c164','E1-c165','E1-c166','E1-c160'}
lessons = {}
def text(lesson):
    if lesson not in lessons:
        raw = open(f"{base}/course/modules/E/E1/{lesson}.html", encoding='utf-8').read()
        raw = re.sub(r'<[^>]+>', ' ', raw)
        lessons[lesson] = re.sub(r'\s+', ' ', html.unescape(raw))
    return lessons[lesson]
banned = ['TODO','TBD','lorem','for brevity','beyond the scope','omitted','roughly','historically','you can add more','left as an exercise','it can be shown','clearly','obvious','well known','important to note','studies show','experts agree']
process = ['verif','round','ledger','builder','draft','fixer','slice','audit','sweep','finding','erratum','correction']
fails = []
numfail = []
for c in cards:
    body = c['front'] + ' ' + c['back']
    for b in banned:
        if b.lower() in body.lower(): fails.append((c['id'], 'banned', b))
    for p in process:
        if re.search(p, body, re.I): fails.append((c['id'], 'process', p))
    for sym in ['Phi', 'gamma_3', 'gamma_4', 'R^ast', 'R_f', 'mathbb{Q}', 'R^{e', '\\ast', 'x^\\ast']:
        if sym in body: fails.append((c['id'], 'registry-symbol', sym))
    if not c.get('grade') and c['lesson'] in ('L07','L08','L09'):
        pass
    # numbers: multi-digit integers or fractions in back must occur in the lesson text
    if c['id'] in changed or c['lesson'] in ('L07','L08','L09'):
        t = text(c['lesson'])
        nums = set(re.findall(r'\d+(?:/\d+)?(?:\.\d+)?', c['back']))
        for n in sorted(nums):
            if len(n.replace('/','').replace('.','')) >= 2 and n not in t:
                numfail.append((c['id'], n))
print('cards', len(cards), 'unique ids', len({c['id'] for c in cards}))
print('banned/process/registry-symbol hits:', fails if fails else 'none')
print('multi-digit numbers in back absent from own lesson text:', numfail if numfail else 'none')
print('changed-or-slice cards checked:', sum(1 for c in cards if c['id'] in changed or c['lesson'] in ('L07','L08','L09')))
print('byte-identical objects for L08/L09 cards vs dde0486b:', all(o == n for o, n in ((next(x for x in old if x['id']==c['id']), c) for c in cards if c['lesson'] in ('L08','L09') and c['id'] in oldids)))
print('L07-L09 card count', sum(1 for c in cards if c['lesson'] in ('L07','L08','L09')), Counter(c['lesson'] for c in cards if c['lesson'] in ('L07','L08','L09')))
