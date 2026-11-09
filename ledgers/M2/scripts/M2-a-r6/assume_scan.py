import re, sys, pathlib, html
root = pathlib.Path(sys.argv[1])
files = sorted(root.glob('L*.html')) + [root / 'index.html']
for f in files:
    txt = f.read_text(encoding='utf-8')
    lines = txt.splitlines()
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'Assumption 2\.1', line):
            # nearest preceding block title
            prior = '\n'.join(lines[max(0, i-6):i-1]) + '\n' + line[:m.start()]
            tb = re.findall(r'block-title[^>]*>(.*?)</span>', prior)
            title = re.sub('<[^>]+>', '', tb[-1]) if tb else '-'
            seg = re.sub('<[^>]+>', '', line[max(0, m.start()-70):m.start()+10])
            print(f"{f.name}:{i} | {html.unescape(title)[:40]!s:40} | ...{html.unescape(seg)}")
