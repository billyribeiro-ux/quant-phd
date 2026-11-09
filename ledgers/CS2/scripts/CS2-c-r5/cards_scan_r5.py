# CS2-c round 5: full-deck duplicate scan (200 cards) and L09-L11 card-field checks.
import json, difflib, re, sys
cards=json.load(open('course/modules/CS/CS2/cards.json'))
ids=[c['id'] for c in cards]
print('cards', len(cards), 'unique ids', len(set(ids)))
bad=[c['id'] for c in cards if not re.fullmatch(r'CS2-c\d{3}', c['id'])]
print('bad id format', bad)
for c in cards:
    keys=set(c.keys())
    if c['grade']!='T' and not ('cite' in c or 'basis' in c): print('NO BASIS', c['id'])
    if c['grade'] not in 'TABCDX': print('BAD GRADE', c['id'])
    if not c['lesson'] in ('L01','L02','L03','L04','L05','L06','L07','L08','L09','L10','L11'): print('BAD LESSON',c['id'])
def norm(s): return re.sub(r'\W+',' ',s.lower()).strip()
pairs=[]
for i in range(len(cards)):
    for j in range(i+1,len(cards)):
        a=norm(cards[i]['front']+' '+cards[i]['back']); b=norm(cards[j]['front']+' '+cards[j]['back'])
        r=difflib.SequenceMatcher(None,a,b).ratio()
        fr=difflib.SequenceMatcher(None,norm(cards[i]['front']),norm(cards[j]['front'])).ratio()
        if r>0.55 or fr>0.7: pairs.append((round(r,2),round(fr,2),cards[i]['id'],cards[j]['id'],cards[i]['lesson'],cards[j]['lesson']))
pairs.sort(reverse=True)
for p in pairs[:40]: print(p)
print('pairs over threshold', len(pairs))
