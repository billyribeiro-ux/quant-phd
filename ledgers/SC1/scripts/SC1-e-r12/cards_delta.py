import json, subprocess, sys
def load(rev):
    s = subprocess.run(['git', 'show', f'{rev}:course/modules/SC/SC1/cards.json'], capture_output=True, text=True, check=True).stdout
    return json.loads(s)
old = {c['id']: c for c in load(sys.argv[1])}
new = {c['id']: c for c in load(sys.argv[2])}
print('old', len(old), 'new', len(new))
print('added', sorted(set(new) - set(old)))
print('removed', sorted(set(old) - set(new)))
changed = []
for k in sorted(set(old) & set(new)):
    if old[k] != new[k]:
        changed.append(k)
print('changed', changed)
for k in changed:
    o, n = old[k], new[k]
    for f in sorted(set(o) | set(n)):
        if o.get(f) != n.get(f):
            print(f'--- {k} field {f}')
            print('OLD:', o.get(f))
            print('NEW:', n.get(f))
