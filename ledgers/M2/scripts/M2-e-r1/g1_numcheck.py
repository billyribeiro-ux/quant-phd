import json, re, pathlib
cards = json.load(open('/tmp/m2e_r1b/new_cards.json'))
miss = []
checked = 0
for c in cards:
    lesson = c['lesson']
    text = pathlib.Path(f"/tmp/m2e_r1b/text/{lesson}.txt").read_text(encoding='utf-8')
    body = text.replace('−', '-')
    for field in ('front', 'back'):
        for tok in re.findall(r'(?<![A-Za-z_])\d+(?:\.\d+)?(?:e-?\d+)?', c[field]):
            checked += 1
            if tok not in body:
                miss.append((c['id'], lesson, field, tok))
print('numeric tokens checked', checked, 'missing', len(miss))
for m in miss[:80]:
    print(m)
