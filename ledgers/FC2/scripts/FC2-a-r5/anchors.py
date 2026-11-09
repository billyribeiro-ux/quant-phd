import re, os, sys
base = '/Users/billyribeiro/.fanout/wt/verifyS5-FC2-a/course/modules/FC/FC2'
bad = []
checked = 0
for pg in ['index.html','L01.html','L02.html','L03.html']:
    src = open(os.path.join(base, pg), encoding='utf-8').read()
    ids = set(re.findall(r'\bid="([^"]+)"', src))
    for href in re.findall(r'href="([^"]+)"', src):
        if href.startswith('http') or href.startswith('mailto'):
            continue
        checked += 1
        if '#' in href:
            f, frag = href.split('#', 1)
            target = os.path.normpath(os.path.join(base, f)) if f else os.path.join(base, pg)
            if not os.path.exists(target):
                bad.append((pg, href, 'missing file'))
                continue
            tsrc = open(target, encoding='utf-8').read()
            tids = set(re.findall(r'\bid="([^"]+)"', tsrc))
            if frag and frag not in tids:
                bad.append((pg, href, 'missing anchor'))
        else:
            target = os.path.normpath(os.path.join(base, href))
            if not os.path.exists(target):
                bad.append((pg, href, 'missing file'))
print('hrefs checked', checked, 'bad', len(bad))
for b in bad: print(b)
