import json,sys
d=json.load(open('/Users/billyribeiro/.fanout/wt/verifyD12-M3-d/course/modules/M/M3/cards.json'))
L=sys.argv[1]
for c in d:
    if c['lesson']==L:
        print(f"{c['id']} | g={c.get('grade')} | b={c.get('basis','-')}\n  F: {c['front']}\n  B: {c['back']}")
