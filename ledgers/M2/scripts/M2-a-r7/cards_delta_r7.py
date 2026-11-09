import json, subprocess, sys
REPO = sys.argv[1]
PIN = 'e896b7a4'
def load(rev):
    raw = subprocess.run(['git', '-C', REPO, 'show', f'{rev}:course/modules/M/M2/cards.json'], capture_output=True, text=True, check=True).stdout
    return json.loads(raw)
old = {c['id']: c for c in load(PIN)}
new = {c['id']: c for c in load('HEAD')}
slice_l = {'L01', 'L02', 'L03', 'L04', 'L05', 'L06'}
print('old count', len(old), 'new count', len(new))
print('removed:', sorted(set(old) - set(new)))
print('added:', sorted(set(new) - set(old)))
changed = sorted(k for k in set(old) & set(new) if old[k] != new[k])
print('changed (all lessons):', changed)
for k in changed:
    print('  ', k, old[k].get('lesson'), 'SLICE' if old[k].get('lesson') in slice_l else 'outside')
for k in sorted(set(old) - set(new)):
    print('  removed', k, old[k].get('lesson'), 'SLICE' if old[k].get('lesson') in slice_l else 'outside')
for k in sorted(set(new) - set(old)):
    print('  added', k, new[k].get('lesson'), 'SLICE' if new[k].get('lesson') in slice_l else 'outside')
sl_new = [c for c in new.values() if c['lesson'] in slice_l]
print('slice cards at HEAD', len(sl_new), 'cards without grade key', sum(1 for c in sl_new if 'grade' not in c))
print('no-grade slice ids', [c['id'] for c in sl_new if 'grade' not in c])
