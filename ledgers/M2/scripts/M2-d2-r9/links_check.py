import re, os
base = '/Users/billyribeiro/.fanout/wt/verifyD9-M2-d2/course/modules/M/M2'
bad = []; checked = 0
for f in ['L22.html', 'L23.html', 'L24.html']:
    src = open(os.path.join(base, f), encoding='utf-8').read()
    for m in re.finditer(r'href="([^"#]*)#([^"]+)"', src):
        path, frag = m.group(1), m.group(2)
        tgt = os.path.normpath(os.path.join(base, path)) if path else os.path.join(base, f)
        if not os.path.exists(tgt):
            bad.append((f, path, frag, 'missing file')); continue
        t = open(tgt, encoding='utf-8').read()
        checked += 1
        if not re.search(r'id="%s"' % re.escape(frag), t):
            bad.append((f, path, frag, 'missing id'))
    for m in re.finditer(r'href="(#[^"]+)"', src):
        checked += 1
        if not re.search(r'id="%s"' % re.escape(m.group(1)[1:]), src):
            bad.append((f, '#', m.group(1), 'missing local id'))
print('checked', checked, 'bad', bad)
