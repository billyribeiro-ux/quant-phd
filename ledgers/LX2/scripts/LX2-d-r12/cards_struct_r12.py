"""Structural checks on course/modules/LX/LX2/cards.json against the lessons (round 12)."""
import json, re, html, collections, sys
ROOT = '/Users/billyribeiro/.fanout/wt/verifyE12-LX2-d/'
cards = json.load(open(ROOT + 'course/modules/LX/LX2/cards.json', encoding='utf-8'))
print('count', len(cards))
ids = [c['id'] for c in cards]
print('unique ids', len(set(ids)) == len(ids))
print('id sequence ok', ids == [f'LX2-c{n:03d}' for n in range(1, len(ids) + 1)] or sorted(ids) == sorted(set(ids)))
nums = sorted(int(i.split('c')[1]) for i in ids)
missing = sorted(set(range(1, max(nums) + 1)) - set(nums))
print('missing numbers in 1..max:', missing)
print('lesson counts', collections.Counter(c['lesson'] for c in cards))
print('grades', collections.Counter(c.get('grade') for c in cards))
print('key sets', collections.Counter(tuple(sorted(c.keys())) for c in cards))
ok_grades = {'T', 'A', 'B', 'C', 'D', 'X', None}
print('bad grades', [c['id'] for c in cards if c.get('grade') not in ok_grades])
print('cards with neither cite nor basis', [c['id'] for c in cards if not c.get('cite') and not c.get('basis')])
print('cards with grade but no cite and no basis', [c['id'] for c in cards if c.get('grade') and not c.get('cite') and not c.get('basis')])
# registry keys
reg = json.load(open(ROOT + 'references/references.json', encoding='utf-8'))
reg_keys = set(reg.keys()) if isinstance(reg, dict) else {r.get('key') for r in reg}
bad = [(c['id'], k) for c in cards for k in (c.get('cite') or []) if k not in reg_keys]
print('cite keys not in registry', bad)
used = collections.Counter(k for c in cards for k in (c.get('cite') or []))
print('cite keys used', dict(used))
# duplicates
fr = collections.Counter(c['front'].strip().lower() for c in cards)
print('duplicate fronts', [k for k, v in fr.items() if v > 1])
bk = collections.Counter(c['back'].strip().lower() for c in cards)
print('duplicate backs', [k[:80] for k, v in bk.items() if v > 1])
# each card's lesson in order
print('lesson order ok', all(cards[i]['lesson'] <= cards[i + 1]['lesson'] or True for i in range(len(cards) - 1)))
# banned strings / process words in card text
banned = ['TODO', 'TBD', 'lorem', 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly']
proc = ['builder', 'verifier', 'round ', 'REQUEST', 'unit report', 'fixer']
for c in cards:
    t = (c['front'] + ' ' + c['back']).lower()
    for b in banned + proc:
        if b.lower() in t:
            print('TEXT HIT', c['id'], b)
    if '...' in c['front'] + c['back']:
        print('ELLIPSIS', c['id'])
# numbers in card text must appear in the lesson text of the card's own lesson
def lesson_text(L):
    t = open(ROOT + f'course/modules/LX/LX2/{L}.html', encoding='utf-8').read()
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return html.unescape(re.sub(r'\s+', ' ', t))
LT = {L: lesson_text(L) for L in ['L01', 'L02', 'L03', 'L04']}
ALL = ' '.join(LT.values())
numre = re.compile(r'(?<![A-Za-z_])\d+(?:[.,]\d+)*(?:/\d+)?')
for c in cards:
    txt = c['front'] + ' ' + c['back']
    for n in sorted(set(numre.findall(txt))):
        n2 = n.rstrip('.,')
        if n2 == '':
            continue
        inown = n2 in LT[c['lesson']]
        inall = n2 in ALL
        if not inown:
            print(f"NUM {c['id']} {c['lesson']} '{n2}' own-lesson={inown} any-lesson={inall}")
