import json, re, html, sys
from pathlib import Path
base = Path(sys.argv[1])
cards = json.load(open(base / 'cards.json', encoding='utf-8'))
def text_of(p):
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"\1/\2", s)
    s = s.replace("{", " ").replace("}", " ")
    return re.sub(r'\s+', ' ', s)
texts = {}
pat = re.compile(r'(?<![A-Za-z_])-?\d+(?:[./]\d+)*(?:\.\d+)?')
dup = {}
for c in cards:
    key = (c['front'].strip().lower(), c['back'].strip().lower())
    dup.setdefault(c['front'].strip().lower(), []).append(c['id'])
    les = c['lesson']
    if les not in texts:
        texts[les] = text_of(base / f'{les}.html')
    nums = pat.findall(c['back'])
    missing = []
    for n in nums:
        n2 = n.lstrip('-')
        if n2 in ('1','0','2','3','4','5','6','7','8','9','10'):
            continue
        if n2 not in texts[les] and n2 not in c['back'].replace(n2,'',0) :
            missing.append(n2)
        elif n2 not in texts[les]:
            missing.append(n2)
    if c['grade'] == 'C' or missing:
        print(c['id'], c['grade'], 'missing-in-lesson:', sorted(set(missing)), '| basis:', c.get('basis'))
print('DUP FRONTS:', {k:v for k,v in dup.items() if len(v)>1})
