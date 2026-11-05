"""Remaining round-12 checks: Dodd-Frank/MiFID cards and registry, grade legend, section 5(d) statute text,
and a notation tally of single-letter symbols in LX2 math (print-only)."""
import json, re
ROOT = '/Users/billyribeiro/.fanout/wt/verifyE12-LX2-d/'
cards = json.load(open(ROOT + 'course/modules/LX/LX2/cards.json', encoding='utf-8'))
print('cards mentioning Dodd/MiFID/Frank:', [c['id'] for c in cards if re.search(r'dodd|frank|mifid', json.dumps(c, ensure_ascii=False), re.I)])
reg = json.load(open(ROOT + 'references/references.json', encoding='utf-8'))['entries']
print('registry records mentioning dodd/frank/mifid:', [x['key'] for x in reg if re.search(r'dodd|frank|mifid', json.dumps(x), re.I)])
for L in ['L01', 'L02', 'L03', 'L04']:
    t = open(ROOT + f'course/modules/LX/LX2/{L}.html', encoding='utf-8').read()
    print(L, 'legend lines:', len(re.findall(r'Ttheorem, proved on the page', t)), 'Xrefuted:', t.count('Xrefuted'))
s1885 = re.sub(r'\s+', ' ', open('/Users/billyribeiro/.fanout/scratch-LX2-d-r11/src/c1884.norm.txt', encoding='utf-8', errors='replace').read())
i = s1885.find('SEC. 5.')
print('1933 s5(d):', s1885[s1885.find('(d) Notwithstanding', i):s1885.find('(d) Notwithstanding', i) + 360] if 'Notwithstanding' in s1885[i:i+8000] else 'pattern not found')
t = open(ROOT + 'course/modules/LX/LX2/L01.html', encoding='utf-8').read()
print('L01 5(d) claim span text:', re.findall(r'data-locator="section 5\(d\)">([^<]{0,200})', t)[:1])
