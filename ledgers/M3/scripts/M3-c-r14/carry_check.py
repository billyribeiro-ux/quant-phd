import json, re, sys
prev = json.load(open('/Users/billyribeiro/.fanout/frags/B-M3-c.round13.json'))
hunks = {'L07': {52,218,264,271,321,328}, 'L08': {52,293,295,304,308,312,339,357,375,382,406,414}, 'L09': {193,350,360,390,445}}
pat = re.compile(r'(L0[789])\.html:(\d+)(?:[-–](\d+))?')
for r in prev['rows']:
    if r['status'] != 'PASS':
        continue
    loc = r['location']
    refs = pat.findall(loc)
    files_no_line = re.findall(r'(L0[789]\.html|cards\.json|tests/labs/M3|notation)', loc)
    hit = []
    for f, a, b in refs:
        lo = int(a); hi = int(b) if b else lo
        hs = [h for h in hunks[f] if lo <= h <= hi]
        if hs: hit.append((f, hs))
    status = 'CLEAN' if refs and not hit else ('HIT' if hit else 'NOLINES')
    print(r['id'], status, hit if hit else '', '|', loc[:90])
