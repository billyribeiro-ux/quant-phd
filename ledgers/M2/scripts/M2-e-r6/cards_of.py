import json, sys
cards = json.load(open('/Users/billyribeiro/.fanout/wt/verifyB6-M2-e/course/modules/M/M2/cards.json'))
for c in cards:
    if c['lesson'] == sys.argv[1]:
        print(c['id'], c.get('grade', '-'), '|', c.get('basis', '-'), '\n  F:', c['front'], '\n  B:', c['back'])
