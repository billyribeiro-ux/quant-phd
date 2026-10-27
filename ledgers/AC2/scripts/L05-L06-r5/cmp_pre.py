import re, html, difflib, sys
base = '/tmp/verify-ac2r5-l56/course/modules/AC/AC2/'
for pg, out in [('L05', '/tmp/ac2-v/L05-L06-r5/lab05.out'), ('L06', '/tmp/ac2-v/L05-L06-r5/lab06.out')]:
    t = open(base + pg + '.html').read()
    pres = re.findall(r'<pre[^>]*>(.*?)</pre>', t, re.S)
    o = [l.strip() for l in open(out).read().strip().splitlines()]
    texts = [[l.strip() for l in html.unescape(re.sub(r'<[^>]+>', '', p)).strip().splitlines() if l.strip()] for p in pres]
    hit = [b for b in texts if b and b[0] == o[0]]
    print(pg, 'pre blocks', len(pres), 'matching first line', len(hit))
    for b in hit:
        print('page lines', len(b), 'run lines', len(o), 'IDENTICAL' if b == o else 'DIFF')
        if b != o:
            print('\n'.join(difflib.unified_diff(b, o, lineterm='')))
