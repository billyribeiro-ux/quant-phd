# CS2-c round 6: whole-deck duplicate scan and L09-L11 card number check (run from the checkout root).
import difflib
import json
import re
import html

cards = json.load(open('course/modules/CS/CS2/cards.json', encoding='utf-8'))
ids = [c['id'] for c in cards]
print('cards', len(cards), 'unique ids', len(set(ids)))
print('lessons', sorted({c['lesson'] for c in cards}))
for c in cards:
    if c['grade'] != 'T' and not ('cite' in c or 'basis' in c):
        print('NO BASIS', c['id'])
    if c['grade'] not in 'TABCDX':
        print('BAD GRADE', c['id'])


def norm(s):
    return re.sub(r'\W+', ' ', s.lower()).strip()


pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a = norm(cards[i]['front'] + ' ' + cards[i]['back'])
        b = norm(cards[j]['front'] + ' ' + cards[j]['back'])
        r = difflib.SequenceMatcher(None, a, b).ratio()
        fr = difflib.SequenceMatcher(None, norm(cards[i]['front']), norm(cards[j]['front'])).ratio()
        if r > 0.55 or fr > 0.7:
            pairs.append((round(r, 2), round(fr, 2), cards[i]['id'], cards[j]['id'], cards[i]['lesson'], cards[j]['lesson']))
pairs.sort(reverse=True)
print('pairs over threshold', len(pairs))
for p in pairs:
    if p[4] in ('L09', 'L10', 'L11') or p[5] in ('L09', 'L10', 'L11'):
        print('SLICE PAIR', p)

# Numbers on L09-L11 cards must appear in their lesson text.
for lesson in ('L09', 'L10', 'L11'):
    page = open(f'course/modules/CS/CS2/{lesson}.html', encoding='utf-8').read()
    text = html.unescape(re.sub(r'<[^>]+>', ' ', page))
    text = re.sub(r'\s+', ' ', text)
    for c in cards:
        if c['lesson'] != lesson:
            continue
        nums = set(re.findall(r'\d+(?:\.\d+)?(?:e-?\d+)?', c['back']))
        missing = [n for n in nums if n not in text and n not in ('1', '0', '2', '3', '4', '5')]
        if missing:
            print('CARD NUMBER NOT IN LESSON', c['id'], missing)
print('L09-L11 card count', sum(1 for c in cards if c['lesson'] in ('L09', 'L10', 'L11')))
for cid in ('CS2-c124', 'CS2-c207', 'CS2-c225', 'CS2-c123', 'CS2-c136', 'CS2-c154', 'CS2-c193'):
    print('absent', cid, cid not in ids)
