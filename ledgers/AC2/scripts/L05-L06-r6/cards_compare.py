import json, subprocess, sys
root = '/tmp/verify-ac2r6-l56'
old = json.loads(subprocess.run(['git', '-C', root, 'show', '11b3477:course/modules/AC/AC2/cards.json'], capture_output=True, text=True, check=True).stdout)
new = json.load(open(root + '/course/modules/AC/AC2/cards.json'))
om = {c['id']: c for c in old}
nm = {c['id']: c for c in new}
changed = sorted(i for i in set(om) | set(nm) if om.get(i) != nm.get(i))
print('changed records (all lessons):', changed)
print('L05/L06 changed records:', [i for i in changed if nm.get(i, om.get(i))['lesson'] in ('L05', 'L06')])
print('L05/L06 record count new:', sum(1 for c in new if c['lesson'] in ('L05', 'L06')))
