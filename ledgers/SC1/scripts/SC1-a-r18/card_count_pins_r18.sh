#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyE18-SC1-a || exit 1
for c in 56cc575a 700bf33f 50559266; do
  git show "${c}:course/modules/SC/SC1/cards.json" > "/tmp/r18_cards_${c}.json"
  python3 -I -c "
import json,collections,sys
c=json.load(open(sys.argv[1]))
l=collections.Counter(x['lesson'] for x in c if x['lesson'] in ('L01','L02','L03'))
print(sys.argv[2], 'total', len(c), 'L01-L03', sum(l.values()), dict(l))" "/tmp/r18_cards_${c}.json" "$c"
done
