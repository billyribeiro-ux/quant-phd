import json, difflib, itertools
d = json.load(open('/Users/billyribeiro/.fanout/wt/verifyS2-M5-b/course/modules/M/M5/cards.json'))
sl = [c for c in d if c['lesson'] in ('L05','L06','L07')]
out = []
for a in sl:
    for b in d:
        if b['id'] == a['id']:
            continue
        sf = difflib.SequenceMatcher(None, a['front'], b['front']).ratio()
        sb = difflib.SequenceMatcher(None, a['back'], b['back']).ratio()
        if sf > 0.55 or sb > 0.55 or (sf + sb) / 2 > 0.5:
            out.append((round((sf+sb)/2, 3), round(sf,3), round(sb,3), a['id'], b['id'], a['front'][:90], b['front'][:90]))
out.sort(reverse=True)
for o in out[:60]:
    print(o)
print('count', len(out))
