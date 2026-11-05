#!/bin/sh
# Round-11 slice-a checks: banned-phrase grep, Dodd/MiFID/Texas grep, and the cards.json scan.
CO="$1"
cd "$CO" || exit 1
echo "== banned phrases (index, L01, L02)"
grep -n -i -E "TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|\.\.\.|…" course/modules/LX/LX2/index.html course/modules/LX/LX2/L01.html course/modules/LX/LX2/L02.html
echo "== Texas|Gulf|Dodd|MiFID in L02"
grep -n "Texas\|Gulf\|Dodd\|MiFID" course/modules/LX/LX2/L02.html
echo "== cards.json scan"
.venv/bin/python -c "
import json,collections
cards=json.load(open('course/modules/LX/LX2/cards.json'))
print('cards',len(cards), dict(collections.Counter(x['lesson'] for x in cards)))
ids=[x['id'] for x in cards]; print('duplicate ids',len(ids)-len(set(ids)))
f=collections.Counter(x['front'].strip().lower() for x in cards); print('duplicate fronts',[k for k,v in f.items() if v>1])
"
echo "== cards delta vs 00a84795"
git show 00a84795:course/modules/LX/LX2/cards.json | .venv/bin/python -c "
import json,sys
old={x['id']:x for x in json.load(sys.stdin)}
new={x['id']:x for x in json.load(open('course/modules/LX/LX2/cards.json'))}
print('removed',sorted(set(old)-set(new)));print('added',sorted(set(new)-set(old)))
print('changed',sorted(k for k in set(old)&set(new) if old[k]!=new[k]))
"
