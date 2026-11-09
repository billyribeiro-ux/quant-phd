import json
old={c['id']:c for c in json.load(open('/tmp/e5a/cards_old.json'))}
new={c['id']:c for c in json.load(open('/tmp/e5a/cards_new.json'))}
ids=[i for i in new if i in old and old[i]!=new[i] and new[i]['lesson'] in ('L01','L02','L03')]
print(len(ids), ids)
for i in ids:
    print('=== ',i, new[i]['lesson'])
    for k in ('front','back','grade','basis'):
        if old[i].get(k)!=new[i].get(k):
            print(f'  {k} OLD: {old[i].get(k)!r}')
            print(f'  {k} NEW: {new[i].get(k)!r}')
