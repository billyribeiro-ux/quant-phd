import json, re, sys, html
from pathlib import Path
root = Path('/Users/billyribeiro/.fanout/wt/verifyD5-M4-d/course/modules/M/M4')
cards = json.load(open('/tmp/m4d5/cards_cur.json'))
lessons = {}
for p in sorted(root.glob('L*.html')):
    t = html.unescape(re.sub(r'<[^>]+>', ' ', p.read_text(encoding='utf-8')))
    lessons[p.stem] = re.sub(r'\s+', ' ', t)
bad = []
pat = re.compile(r'\b(Proposition|Definition|Example|Remark|Assumption|Section|Problem|Lab|Part|Theorem|Corollary|Exercise)\s+([0-9]+(?:\.[0-9]+)?)(\([a-z]\))?')
for c in cards:
    text = c['front'] + ' ' + c['back']
    lesson_text = lessons[c['lesson']]
    # the card's own lesson, or an explicit Lesson N mention in the same card
    for m in pat.finditer(text):
        kind, num, sub = m.group(1), m.group(2), m.group(3) or ''
        label = f'{kind} {num}'
        # check whether the card's own lesson shows the label; else any lesson (for cross-lesson cites)
        if label in lesson_text:
            continue
        found = [k for k, v in lessons.items() if label in v]
        if not found:
            bad.append((c['id'], c['lesson'], label))
        else:
            bad.append((c['id'], c['lesson'], label + ' (only in ' + ','.join(found) + ')'))
for b in bad: print(b)
print('checked', len(cards), 'issues', len(bad))
