import json, re, sys
cards = json.load(open('course/modules/FC/FC2/cards.json', encoding='utf-8'))
lessons = {}
for L in ['L01','L02','L03','L04','L05','L06','L07','L08']:
    raw = open(f'course/modules/FC/FC2/{L}.html', encoding='utf-8').read()
    text = re.sub(r'<[^>]+>', ' ', raw)
    import html as h
    lessons[L] = h.unescape(re.sub(r'\s+', ' ', text))
tok = re.compile(r'(?<![A-Za-z_])(\d+(?:[.,]\d+)?(?:/\d+)?)(?![\w])')
bad = []
for c in cards:
    if c['id'] not in sys.argv[1:] and sys.argv[1:] != ['ALL']:
        continue
    text = lessons[c['lesson']]
    for t in tok.findall(c['front'] + ' ' + c['back']):
        if t not in text:
            bad.append((c['id'], c['lesson'], t))
for b in bad: print(b)
print('checked', len(cards) if sys.argv[1:]==['ALL'] else len(sys.argv[1:]), 'missing', len(bad))
