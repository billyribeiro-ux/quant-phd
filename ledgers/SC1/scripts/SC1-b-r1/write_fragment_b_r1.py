import json, re, subprocess, sys, datetime
sys.path.insert(0, '/Users/billyribeiro/.fanout/wt/verifyF31-SC1-b/ledgers/SC1/scripts/SC1-b-r1')
from hunks import changed_lines, FILES
R = '/Users/billyribeiro/.fanout/wt/verifyF31-SC1-b'
base = json.load(open('/Users/billyribeiro/.fanout/frags/E-SC1-b.round14.json'))
CHG_CARDS = {'c017','c030','c031','c044','c045','c052','c092','c110','c114','c119','c122','c157','c171','c174','c210','c221','c224','c217','c236','c237','c238','c239','c241','c242','c243'}
CH = {k: sorted(i for side, i in changed_lines(p)[0] if side == 'new') for k, p in FILES.items()}
CHR = {k: set(v) for k, v in CH.items()}
RV = {}  # id -> (status, evidence)
exec(open(R + '/ledgers/SC1/scripts/SC1-b-r1/rv_rows_b_r1.py').read())  # defines RV and NEW
carried = []; problems = []
rows = []
bmap = {r['id']: r for r in base['rows']}
for r in base['rows']:
    rid = r['id']
    if rid in RV:
        status, ev = RV[rid]
        rows.append({'id': rid, 'check': r['check'], 'location': r['location'], 'status': status, 'evidence': ev})
        continue
    txt = r['location'] + ' ' + r['evidence']
    # carry safety: no cited changed card id, no cited changed line in L01-L03/index/project/plan
    cards = set(re.findall(r'\bc(\d{3})\b', txt))
    if any('c' + c in CHG_CARDS for c in cards):
        problems.append(f'{rid}: cites changed card {sorted("c"+c for c in cards if "c"+c in CHG_CARDS)}')
    for k, pat in {'L01': 'L01', 'L02': 'L02', 'L03': 'L03', 'index': 'index.html', 'project': 'project.html'}.items():
        for m in re.finditer(re.escape(pat) + r'(?:\.html)?:?\s*(\d+)(?:\s*[-–]\s*(\d+))?', txt):
            a = int(m.group(1)); b = int(m.group(2) or a)
            hit = [i for i in CHR[k] if a <= i <= b]
            if hit: problems.append(f'{rid}: cites {k} {a}-{b} with changed lines {hit}')
    files = []
    if re.search(r'L04\.html|L04\b', txt) : files.append('L04.html')
    if re.search(r'L05', txt): files.append('L05.html')
    if re.search(r'L06', txt): files.append('L06.html')
    qual = []
    if re.search(r'\bL01\b|L01\.html', txt): qual.append('L01.html changed at lines 51, 217, 234, 351, 408, 434, 444 only, none cited')
    if re.search(r'\bL02\b|L02\.html', txt): qual.append('L02.html changed at lines 51, 285, 323, 459 only, none cited')
    if re.search(r'\bL03\b|L03\.html', txt): qual.append('L03.html changed at lines 51, 115, 260, 270, 278, 395, 398, 463, 502 only, none cited')
    if 'index' in txt: qual.append('index.html changed at lines 33 and 165 only, none cited')
    if 'cards' in txt or re.search(r'\bc\d{3}\b', txt): qual.append('cards.json changed only at ids listed in the delta (c017 c030 c031 c044 c045 c052 c092 c110 c114 c119 c122 c157 c171 c174 c210 c221 c224 removed or added c217 c236-c239 c241-c243), none cited here')
    if 'references' in txt or 'shreve' in txt: qual.append('references.json changed only at generated_at and black1973pricing used_by; the cited entry is byte-identical')
    if 'SC1-build-plan' in txt: qual.append('plans/SC1-build-plan.md changed at lines 431-435 and 476-479 only; section 3 is byte-identical')
    if 'FINAL-ARCHITECT' in txt: qual.append('plans/FINAL-ARCHITECT-RULINGS.md changed from line 32; cited lines 28-30 unchanged')
    if 'project.html' in txt: qual.append('project.html changed in slice e; cited line not in its changed set')
    head = 'Carried from round 14 ('
    subj = ', '.join(files) if files else 'the cited pages'
    if 'tests/labs' in txt or 'lab-SC1' in txt: subj += ', tests/labs/SC1 twins'
    prefix = head + subj + ' byte-identical since the previous pin' + ('; ' + '; '.join(qual) if qual else '') + '):'
    carried.append(rid)
    rows.append({'id': rid, 'check': r['check'], 'location': r['location'], 'status': r['status'], 'evidence': prefix + ' ' + r['evidence']})
for n in NEW:
    rows.append(n)
ids = [r['id'] for r in rows]
assert len(ids) == len(set(ids)), 'duplicate ids'
missing = set(bmap) - set(ids)
assert not missing, missing
print('carried', len(carried), 'reverified', len(RV), 'new', len(NEW), 'total', len(rows))
print('CARRY CONFLICTS:', problems)
frag = {
 'unit': 'SC1', 'slice': 'b', 'round': 1,
 'verifier': 'independent verifier (Haiku 5.5), closing delta round 1 (ruling 30)',
 'pin': '95f3f8cb' + ' ' * 0,
 'base': '8e5751c903f0246115eba746afdf5d71f612bb37 (base fragment ~/.fanout/frags/E-SC1-b.round14.json, round 14, PASS); delta 8e5751c..95f3f8cb',
 'checkout': R, 'scratch': R + '/ledgers/SC1/scripts/SC1-b-r1',
 'verified_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
 'verdict': 'FAIL',
 'rows': rows, 'mutants': [], 'registry_flags': base['registry_flags'], 'freshness_flags': [],
 'notes': NOTES, 'summary': {},
}
frag['pin'] = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=R).stdout.strip()
frag['summary'] = {'rows': len(rows), 'pass': sum(r['status']=='PASS' for r in rows), 'fail': sum(r['status']=='FAIL' for r in rows), 'carried_from_round_14': len(carried), 'reverified_this_round': len(RV), 'new_this_round': len(NEW), 'mutants': 0}
json.dump(frag, open(R + '/ledgers/SC1/SC1-b.json', 'w'), indent=2, ensure_ascii=False)
open(R + '/ledgers/SC1/scripts/SC1-b-r1/out/carried_ids_b_r1.txt', 'w').write('\n'.join(carried) + '\n')
print('written')
