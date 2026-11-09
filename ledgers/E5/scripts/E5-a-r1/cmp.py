import json,sys
old=json.load(open('/tmp/e5a/cards_old.json'))
new=json.load(open('/tmp/e5a/cards_new.json'))
print(type(old).__name__, len(old), type(new).__name__, len(new))
def items(x):
    if isinstance(x,dict):
        for k in ('cards',):
            if k in x: return x[k]
    return x
o=items(old); n=items(new)
print(list(o[0].keys()) if isinstance(o,list) else list(o.keys())[:5])
om={c['id']:c for c in o}; nm={c['id']:c for c in n}
print('old ids',len(om),'new ids',len(nm))
print('added',[i for i in nm if i not in om])
print('removed',[i for i in om if i not in nm])
changed=[i for i in nm if i in om and om[i]!=nm[i]]
print('changed',len(changed))
for i in changed:
    diffk=[k for k in set(om[i])|set(nm[i]) if om[i].get(k)!=nm[i].get(k)]
    print(i, diffk, nm[i].get('lesson', nm[i].get('lesson_id','')))
