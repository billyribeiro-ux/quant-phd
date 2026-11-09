import re, json, sys, html
root = sys.argv[1]
banned = ['TODO','TBD','lorem','for brevity','details omitted','beyond the scope','left as an exercise','you can add more',
          'it is important to note','studies show','experts agree','it is well known','obviously','clearly',
          'builder','verifier','REQUESTS','unit report','round ', 'convex', 'convexity', 'Convex']
def visible(t):
    t = re.sub(r'<script.*?</script>', ' ', t, flags=re.S)
    t = re.sub(r'<pre.*?</pre>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return html.unescape(t)
hits = []
for p in ['L01','L02','L03','L04']:
    t = visible(open(f'{root}/course/modules/E/E3/{p}.html', encoding='utf-8').read())
    for b in banned:
        for m in re.finditer(re.escape(b), t):
            hits.append((p, b, t[max(0,m.start()-60):m.end()+40].replace('\n',' ')))
cards = json.load(open(f'{root}/course/modules/E/E3/cards.json', encoding='utf-8'))
for c in cards:
    s = c['front'] + ' ' + c['back']
    for b in banned:
        if b in s:
            hits.append((c['id'], b, s[:200]))
print('hits', len(hits))
for h in hits: print(h)
