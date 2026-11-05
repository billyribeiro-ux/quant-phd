import json, re, collections
d = json.load(open('course/modules/SC/SC1/cards.json'))
sl = [c for c in d if c['lesson'] in ('L04', 'L05', 'L06')]
txt = lambda c: c['front'] + ' ' + c['back']
bad = ['TODO', 'TBD', 'lorem', 'for brevity', 'details omitted', 'beyond the scope', 'clearly', 'obviously',
       'studies show', '...', 'agent', 'verifier', 'round ', 'builder', 'ledger', 'fragment']
hits = [(c['id'], b) for c in sl for b in bad if b.lower() in txt(c).lower()]
print('card banned/process hits:', hits)
fr = [c['front'] for c in sl]
print('dup fronts:', [k[:60] for k, v in collections.Counter(fr).items() if v > 1])
print('dup backs:', [k[:60] for k, v in collections.Counter(c['back'] for c in sl).items() if v > 1])
for page in ['L04', 'L05', 'L06']:
    s = open(f'course/modules/SC/SC1/{page}.html', encoding='utf-8').read()
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', s, re.S)
    t = re.sub(r'<[^>]+>', '', m.group(1))
    t = re.sub(r'\\\((.*?)\\\)', 'X', t)
    print(page, 'why-it-matters words:', len(t.split()))
    plain = re.sub(r'<[^>]+>', ' ', s)
    for w in ['round', 'verifier', 'agent', 'builder', 'ledger', 'batch', 'fragment']:
        if re.search(r'\b' + w + r'\b', plain, re.I):
            print('  process word hit:', page, w)
    for w in ['clearly', 'obviously', 'it is important to note', 'studies show', 'TODO', 'TBD']:
        if w.lower() in plain.lower():
            print('  banned hit:', page, w)
