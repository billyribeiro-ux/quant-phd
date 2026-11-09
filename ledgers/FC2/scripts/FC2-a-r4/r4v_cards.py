"""Card checks for FC2 slice a (L01-L03 cards): lesson membership, grade and basis fields, duplicate fronts,
and that every number quoted on a card's back appears in the card's lesson text."""
import html, json, re, sys
from pathlib import Path
ROOT = Path(sys.argv[1])
MOD = ROOT / 'course/modules/FC/FC2'
cards = json.loads((MOD / 'cards.json').read_text(encoding='utf-8'))
lessons = {}
for n in ('L01', 'L02', 'L03'):
    raw = (MOD / f'{n}.html').read_text(encoding='utf-8')
    raw = re.sub(r'(?s)<script.*?</script>', ' ', raw)
    lessons[n] = html.unescape(re.sub(r'<[^>]+>', ' ', raw))
sel = [c for c in cards if c['lesson'] in lessons]
print('cards L01-L03:', len(sel), 'by lesson:', {n: sum(1 for c in sel if c['lesson'] == n) for n in lessons})
fronts = [c['front'] for c in cards]
dups = {f for f in fronts if fronts.count(f) > 1}
print('duplicate fronts across all cards:', len(dups))
ids = [c['id'] for c in cards]
print('duplicate ids:', len(ids) - len(set(ids)))
bad = 0
for c in sel:
    if c.get('grade') in ('T', 'A', 'B', 'C', 'D', 'X') and not (c.get('basis') or c['grade'] == 'T'):
        print('graded without basis', c['id']); bad += 1
    nums = re.findall(r'(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])', c['back'])
    for num in nums:
        if num in ('1', '0', '2', '3', '4', '5', '6', '7', '8', '9', '10', '100', '1000000'):
            continue
        if num not in lessons[c['lesson']]:
            print('number not in lesson', c['id'], num); bad += 1
print('card number/basis problems:', bad)
for c in sel:
    if c.get('grade') is None:
        pass
print('grade distribution (L01-L03):', {g: sum(1 for c in sel if c.get('grade') == g) for g in ('T', 'C', None)})
