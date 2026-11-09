#!/bin/sh
# Banned-phrase and process-word scan over the three slice pages and the slice cards (run from the checkout root).
grep -n -i -E "TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|\.\.\.|…|round|fixer|builder|verifier|ledger|defect|reviewer|open item|architect|planner|blind|exemplar" course/modules/M/M5/L05.html course/modules/M/M5/L06.html course/modules/M/M5/L07.html
python3 -I -c "
import json, re
cards = json.load(open('course/modules/M/M5/cards.json'))
pat = re.compile(r'TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|round|fixer|builder|verifier|ledger|defect|reviewer|architect|planner|\.\.\.|…', re.I)
n = 0
for c in cards:
    if c['lesson'] in ('L05', 'L06', 'L07'):
        n += 1
        s = ' '.join(str(c.get(k, '')) for k in ('front', 'back', 'basis'))
        if pat.search(s): print('card hit', c['id'], pat.findall(s))
print('slice cards scanned', n)
"
