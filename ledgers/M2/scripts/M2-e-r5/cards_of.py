import json, sys
c = json.load(open('/Users/billyribeiro/.fanout/wt/verifyD5-M2-e/course/modules/M/M2/cards.json'))
L = sys.argv[1]
for x in c:
    if x['lesson'] == L:
        print(f"{x['id']} | F: {x['front']} | B: {x['back']} | grade={x.get('grade')} basis={x.get('basis')}")
