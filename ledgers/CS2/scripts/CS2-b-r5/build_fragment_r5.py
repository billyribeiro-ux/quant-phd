"""Builds ledgers/CS2/CS2-b.json (round 5) from the round-4 rows plus this round's re-verification.
Carried rows keep their round-4 evidence behind the required prefix; re-verified rows get new evidence."""
import json, pathlib, sys
R4 = json.load(open('/tmp/fanout-frags/B-CS2-b.round4.json', encoding='utf-8'))
OUT = pathlib.Path('/tmp/verifyB5-CS2-b/ledgers/CS2/CS2-b.json')
PIN = '09b8751'
r4 = {r['id']: r for r in R4['rows']}
CARRY = 'Carried from round 4 ({files} byte-identical since the previous pin 2657ab5): '
rows = []
def carry(rid, files, status=None, fix=None):
    r = dict(r4[rid])
    base = r['evidence']
    r['evidence'] = CARRY.format(files=files) + base
    r['status'] = status or r['status']
    if status and status != 'PASS':
        r['fix'] = fix or r.get('fix', '')
    elif 'fix' in r and r['status'] == 'PASS':
        r.pop('fix')
    rows.append(r)
def new(rid, check, location, status, evidence, fix=None):
    r = {'id': rid, 'check': check, 'location': location, 'status': status, 'evidence': evidence}
    if status != 'PASS':
        r['fix'] = fix
    rows.append(r)

L06_L07_L08 = 'course/modules/CS/CS2/L05.html, L06.html, L07.html, L08.html'
exec(open(pathlib.Path(__file__).with_name('rows_r5_text.py'), encoding='utf-8').read())
ids4 = [r['id'] for r in R4['rows']]
got = [r['id'] for r in rows]
missing = [i for i in ids4 if i not in got]
assert not missing, missing
order = {i: n for n, i in enumerate(ids4)}
rows.sort(key=lambda r: (order.get(r['id'], 10**6), r['id']))
n_fail = sum(1 for r in rows if r['status'] != 'PASS')
frag = {
    'unit': 'CS2', 'slice': 'CS2-b', 'round': 5,
    'verifier': 'independent verifier (Haiku), round 5, CS2 slice b (L05-L08 and lab twins lab-CS2-L05-1..L08-1); did not build CS2',
    'pin': PIN,
    'base': 'round 4 pin 2657ab5 (round-4 fragment /tmp/fanout-frags/B-CS2-b.round4.json); delta computed with git diff -U0 2657ab5 09b8751',
    'checkout': '/tmp/verifyB5-CS2-b (detached at 09b8751, .venv symlink, vendor present)',
    'scratch': '/tmp/CS2-v/CS2-b-r5',
    'verified_at': '2026-10-28T00:00:00+00:00',
    'verdict': 'FAIL' if n_fail else 'PASS',
    'rows': rows,
    'mutants': [],
    'registry_flags': [],
    'freshness_flags': [],
    'notes': NOTES,
    'summary': f"{len(rows)} rows: {len(rows)-n_fail} PASS, {n_fail} FAIL, 0 UNVERIFIABLE. FAIL rows: " + ', '.join(r['id'] for r in rows if r['status'] != 'PASS') + '.',
}
OUT.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('wrote', OUT, len(rows), 'rows', n_fail, 'FAIL')
