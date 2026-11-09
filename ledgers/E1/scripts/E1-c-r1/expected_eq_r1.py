import re, html, sys
base = sys.argv[1]
for t in ['L07', 'L08', 'L09']:
    page = open(f'{base}/course/modules/E/E1/{t}.html', encoding='utf-8').read()
    exp_blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = [html.unescape(b) for b in exp_blocks]
    out = open(f'/tmp/E1c_twin_{t}.out', encoding='utf-8').read()
    hits = [i for i, e in enumerate(exp) if e == out or e.rstrip('\n') == out.rstrip('\n')]
    print(t, 'expected blocks on page:', len(exp), 'exact match indexes:', hits, 'stdout lines:', out.count('\n'))
