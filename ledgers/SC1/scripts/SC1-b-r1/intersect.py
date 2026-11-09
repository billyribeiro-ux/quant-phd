import json, re, sys
sys.path.insert(0, '/Users/billyribeiro/.fanout/wt/verifyF31-SC1-b/ledgers/SC1/scripts/SC1-b-r1')
from hunks import FILES, changed_lines
d = json.load(open('/Users/billyribeiro/.fanout/frags/E-SC1-b.round14.json'))
CH = {k: {i for side, i in changed_lines(p)[0] if side == 'new'} for k, p in FILES.items()}
KEYS = {'L01': 'L01', 'L02': 'L02', 'L03': 'L03', 'L04': 'L04', 'L05': 'L05', 'L06': 'L06', 'index': 'index', 'project': 'project', 'rulings': 'FINAL', 'plan': 'SC1-build-plan', 'open': 'SC1-open-items'}
for r in d['rows']:
    txt = r['location'] + ' || ' + r['evidence']
    for k, pat in KEYS.items():
        if k in ('L04', 'L05', 'L06'):
            continue
        for m in re.finditer(re.escape(pat) + r'(?:\.html|\.md)?', txt):
            seg = txt[m.end(): m.end() + 60]
            nums = re.findall(r'(\d+)(?:\s*[-–]\s*(\d+))?', seg)
            # take first numeric range in the segment
            rng = None
            mm = re.match(r'[^0-9]{0,12}?(\d+)(?:\s*[-–]\s*(\d+))?', seg)
            if mm:
                a = int(mm.group(1)); b = int(mm.group(2) or a)
                rng = (a, b)
            hit = None
            if rng:
                hit = sorted(i for i in CH[k] if rng[0] <= i <= rng[1])
            print(f"{r['id']} | {k} | cited={rng} | changed_hits={hit} | seg={seg[:50]!r}")
            break
