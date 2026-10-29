import re, json, collections, pathlib
root = pathlib.Path('/tmp/verify18-AC1-b')
pages = ['L04','L05','L06']
for p in pages:
    s = (root/f'course/modules/AC/AC1/{p}.html').read_text()
    text = re.sub(r'<[^>]+>', ' ', s)
    for w in ['as much as','always','only','all ','drives','offsets','raises','same ','every ']:
        hits = [m.start() for m in re.finditer(re.escape(w), text)]
        print(p, repr(w), len(hits))
    print(p, 'SIMULATED', s.count('SIMULATED'), 'data-hours', re.findall(r'data-hours="(\d+)"', s))
    h2 = re.findall(r'<h2 id="(s\d+)">', s)
    print(p, 'sections', h2)
    print(p, 'defs', re.findall(r'id="(def-[a-z-]+)"', s))
    print(p, 'process words', [w for w in ['builder','verifier','round','REQUEST','unit report'] if w.lower() in text.lower()])
    print(p, 'banned', [w for w in ['roughly half','about 6%','historically','...'] if w in text])
cards = json.loads((root/'course/modules/AC/AC1/cards.json').read_text())
ids = [c['id'] for c in cards]
print('cards', len(cards), 'dup ids', [k for k,v in collections.Counter(ids).items() if v>1])
fr = [c['front'] for c in cards]
print('dup fronts', [k for k,v in collections.Counter(fr).items() if v>1])
print('slice cards', [c['id'] for c in cards if c['lesson'] in ('L04','L05','L06')][:3], sum(1 for c in cards if c['lesson'] in ('L04','L05','L06')))
