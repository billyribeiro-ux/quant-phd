import json, re, html, sys
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.out=[]; s.skip=0
    def handle_starttag(s,tag,attrs):
        if tag in ('script','style'): s.skip+=1
        if tag in ('p','li','h1','h2','h3','h4','div','pre','section','dt','dd','tr','br'): s.out.append('\n')
    def handle_endtag(s,tag):
        if tag in ('script','style'): s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
def lesson_text(path):
    p=P(); p.feed(open(path,encoding='utf-8').read()); return re.sub(r'\s+',' ',''.join(p.out))
cards=json.load(open('course/modules/M/M2/cards.json'))
ids=[c['id'] for c in cards]
print('cards', len(cards), 'unique ids', len(set(ids)))
fronts=[c['front'] for c in cards]
dup_fronts=[f for f in set(fronts) if fronts.count(f)>1]
print('duplicate fronts', dup_fronts)
dup_backs=[b for b in set(c['back'] for c in cards) if [c['back'] for c in cards].count(b)>1]
print('duplicate backs', len(dup_backs))
pat=re.compile(r'\b(Definition|Proposition|Theorem|Example|Lemma|Remark|Assumption|Problem|Misconception|Lab|Corollary|Section|Lesson|Result)\s+(\d+(?:\.\d+)?|[A-Z]\d?)\b')
texts={}
bad=[]
for c in cards:
    L=c['lesson']
    if L not in texts: texts[L]=lesson_text(f'course/modules/M/M2/{L}.html')
    t=texts[L]
    for field in ('front','back'):
        for m in pat.finditer(c[field]):
            kind, num = m.group(1), m.group(2)
            if kind=='Lesson':
                continue
            # check that the label appears in the lesson text
            label=f'{kind} {num}'
            if label not in t and label.replace('Lab ','Lab ') not in t:
                bad.append((c['id'], L, field, label))
print('labelled references not found in own lesson:', len(bad))
for b in bad[:40]: print('  ', b)
# locator / lesson existence
import os
for L in sorted(set(c['lesson'] for c in cards)):
    assert os.path.exists(f'course/modules/M/M2/{L}.html'), L
print('lesson pages exist for all', len(set(c['lesson'] for c in cards)), 'lessons')
g=[(c['id'],c.get('grade'),c.get('basis')) for c in cards]
print('grade values', sorted(set(str(x[1]) for x in g)))
print('basis values', sorted(set(str(x[2]) for x in g))[:20])
