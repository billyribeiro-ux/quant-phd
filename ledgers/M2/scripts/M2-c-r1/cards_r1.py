import json, subprocess, re, difflib, sys
REPO = sys.argv[1]
def git_show(rev, path):
    return subprocess.check_output(['git', '-C', REPO, 'show', f'{rev}:{path}'])
CARDS = 'course/modules/M/M2/cards.json'
new = json.loads(git_show('HEAD', CARDS))
old = json.loads(git_show('edbb7aa8', CARDS))
SLICE = {'L13', 'L14', 'L15', 'L16', 'L17', 'L18'}
sn = [c for c in new if c['lesson'] in SLICE]
so = [c for c in old if c['lesson'] in SLICE]
print('slice cards new', len(sn), 'old', len(so))
from collections import Counter
print('grades new', Counter(c.get('grade') for c in sn))
print('grades old', Counter(c.get('grade') for c in so))
print('C without basis', [c['id'] for c in sn if c.get('grade') == 'C' and not c.get('basis')])
print('T with basis', [c['id'] for c in sn if c.get('grade') == 'T' and c.get('basis')])
print('keys', sorted({k for c in sn for k in c}))
# unit-wide exact duplicate fronts / ids
ids = Counter(c['id'] for c in new); print('dup ids', [k for k, v in ids.items() if v > 1])
fr = Counter(c['front'].strip().lower() for c in new); print('exact dup fronts', [k for k, v in fr.items() if v > 1])
# near duplicates within the slice (ratio >= 0.80) on fronts
pairs = []
for i in range(len(sn)):
    for j in range(i + 1, len(sn)):
        r = difflib.SequenceMatcher(None, sn[i]['front'], sn[j]['front']).ratio()
        if r >= 0.80:
            pairs.append((round(r, 3), sn[i]['id'], sn[j]['id']))
print('slice near-dup fronts >=0.80:', sorted(pairs))
# near duplicates unit-wide involving the changed cards
changed = ['M2-c187', 'M2-c233', 'M2-c263']
for cid in changed:
    c = next(x for x in new if x['id'] == cid)
    best = []
    for o in new:
        if o['id'] == cid: continue
        r = difflib.SequenceMatcher(None, c['front'], o['front']).ratio()
        if r >= 0.70: best.append((round(r, 3), o['id'], o['lesson']))
    print('near fronts of', cid, sorted(best, reverse=True)[:5])
