import json, re, subprocess, collections, sys
from pathlib import Path
root = Path(sys.argv[1])
new = json.loads((root / 'course/modules/M/M2/cards.json').read_text(encoding='utf-8'))
old = json.loads(subprocess.check_output(['git', '-C', str(root), 'show', '4eb6788f:course/modules/M/M2/cards.json']))
print('cards new', len(new), 'old', len(old))
ids = collections.Counter(c['id'] for c in new)
print('dup ids', [k for k, v in ids.items() if v > 1])
fr = collections.Counter(c['front'].strip().lower() for c in new)
print('dup fronts', [k for k, v in fr.items() if v > 1])
bk = collections.Counter(re.sub(r'\W+', ' ', c['back'].lower()).strip() for c in new)
print('dup backs', [k[:60] for k, v in bk.items() if v > 1])
keys = set(tuple(sorted(c.keys())) for c in new)
print('key sets', keys)
banned = ['TODO', 'TBD', 'lorem', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly', 'left as an exercise', '\\mathbb', 'we will', 'in this lesson', 'as we saw']
scope = re.compile(r'\b(only|all|always|every|any|same|drives|exactly|smooth|fast|small)\b', re.I)
for c in new:
    if c['lesson'] not in ('L19', 'L20', 'L21'):
        continue
    txt = c['front'] + ' || ' + c['back']
    for b in banned:
        if b.lower() in txt.lower():
            print('BANNED', c['id'], b)
    sc = sorted(set(m.group(1).lower() for m in scope.finditer(txt)))
    print(c['id'], c['lesson'], c.get('grade', '-'), 'scope:', sc)
# changed cards vs old
on = {c['id']: c for c in old}
for c in new:
    o = on.get(c['id'])
    if o is not None and o != c:
        pass
print('changed L19-21 ids', [c['id'] for c in new if c['lesson'] in ('L19','L20','L21') and on.get(c['id']) != c])
