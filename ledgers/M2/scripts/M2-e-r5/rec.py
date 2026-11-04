import json, sys
# usage: rec.py LESSON <<< json-list of [id,status,evidence]
p='/tmp/m2e_r5/card_verdicts.json'
try: d=json.load(open(p))
except FileNotFoundError: d={}
rows=json.load(sys.stdin)
for cid,st,ev in rows:
    d[cid]={'status':st,'evidence':ev}
json.dump(d,open(p,'w'),indent=1)
print('recorded',len(rows),'total',len(d))
