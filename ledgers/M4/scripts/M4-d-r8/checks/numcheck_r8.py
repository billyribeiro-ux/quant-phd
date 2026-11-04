import json, re, collections, sys
cards = json.load(open('/Users/billyribeiro/.fanout/wt/verifyD8-M4-d/course/modules/M/M4/cards.json'))
txt = {}
for L in ['L01','L02','L03','L04','L05','L06','L07','L08','L09','L10']:
    txt[L] = open(f'/tmp/m4d_r8_txt/{L}.html.txt', encoding='utf-8').read()
def nums(s):
    return re.findall(r'\d+(?:\.\d+)?', s)
missing = []
for c in cards:
    body = txt[c['lesson']]
    for side in ('front', 'back'):
        for n in set(nums(c[side])):
            if n in ('1','2','3','0'):
                continue
            if n not in body:
                missing.append((c['id'], c['lesson'], side, n))
by = collections.defaultdict(list)
for cid, L, side, n in missing:
    by[cid].append(f'{side}:{n}')
for cid in sorted(by):
    print(cid, by[cid])
print('cards with unmatched numbers:', len(by))
