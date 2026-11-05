import json, re, sys
cards = json.load(open('course/modules/FC/FC1/cards.json', encoding='utf-8'))
texts = {L: open(f'{sys.argv[1]}/{L}.txt', encoding='utf-8').read() for L in ['L01','L02','L03','L04','L05']}
pat = re.compile(r'\b(Definition|Proposition|Remark|Example|Assumption|Problem|Corollary|Lemma|Theorem|Section|Lab|misconception|Assumption A\d|Assumption B\d|Assumption \d\.\d|Assumption \d\.\d′)\b\s*([0-9A-Z][0-9A-Z.\(\)ivx′]*)?')
cites = {}
for c in cards:
    fields = c['back'] + ' ' + c['front']
    found = []
    for m in re.finditer(r'\(([^()]*)\)', c['back']):
        for part in re.split(r';', m.group(1)):
            part = part.strip()
            mm = re.match(r'^(Definition|Proposition|Remark|Example|Assumption|Problem|Corollary|Section|misconception|Lab)\s*(\S+)?', part)
            if mm: found.append(part)
    cites[c['id']] = found
    own = texts[c['lesson']]
    for part in found:
        # extract label
        lab = re.match(r'^(Definition|Proposition|Remark|Example|Assumption|Problem|Corollary|Section)\s+([0-9][0-9.]*|[A-Z][0-9]*)(\([a-z]+\))?', part)
        if lab:
            key = f"{lab.group(1)} {lab.group(2)}"
            if key not in own:
                where = [L for L in texts if key in texts[L]]
                print(c['id'], c['lesson'], 'MISSING in own lesson:', repr(part), '| found in', where)
        elif part.startswith('misconception'):
            n = re.match(r'misconception (\d)', part)
            if n and f"misconception {n.group(1)}" not in own.lower():
                print(c['id'], c['lesson'], 'misconception not in own lesson', part)
print('cards checked', len(cards))
