import json,sys
old={c['id']:c for c in json.load(open('/tmp/e5a/cards_old.json'))}
new={c['id']:c for c in json.load(open('/tmp/e5a/cards_new.json'))}
which=sys.argv[1]
ids=sys.argv[2:]
src = old if which=='old' else new
for i in ids:
    c=src.get(i)
    print(json.dumps(c, ensure_ascii=False, indent=1) if c else f'{i} MISSING in {which}')
