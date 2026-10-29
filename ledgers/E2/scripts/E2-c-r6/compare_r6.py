import sys, re, html
base='/Users/billyribeiro/.fanout/wt/verifyC6-E2-c/'
for L in ['07','08','09']:
    src=open(base+f'course/modules/E/E2/L{L}.html',encoding='utf-8').read()
    # code block: the <pre> that contains the twin code (first <pre> after heading with lab)
    pres=re.findall(r'<pre([^>]*)>(.*?)</pre>', src, re.S)
    code=[p for p in pres if 'expected' not in p[0]]
    exp=[p for p in pres if 'expected' in p[0]]
    twin=open(base+f'tests/labs/E2/lab-E2-L{L}-1.py',encoding='utf-8').read()
    out=open(base+f'ledgers/E2/scripts/E2-c-r6/out/twin_L{L}.stdout',encoding='utf-8').read()
    ctext=[html.unescape(re.sub(r'<[^>]+>','',c[1])) for c in code]
    etext=[html.unescape(re.sub(r'<[^>]+>','',e[1])) for e in exp]
    print(f'L{L}: code blocks {len(code)} expected blocks {len(exp)}')
    # find block equal to twin
    match=[i for i,c in enumerate(ctext) if c.strip()==twin.strip()]
    print('  code block equal to twin (strip):', match, ' len twin', len(twin))
    if not match:
        # show closest
        import difflib
        best=max(range(len(ctext)), key=lambda i: difflib.SequenceMatcher(None, ctext[i], twin).ratio())
        print('  closest ratio', difflib.SequenceMatcher(None, ctext[best], twin).ratio(), 'block', best)
        for d in list(difflib.unified_diff(twin.splitlines(), ctext[best].splitlines(), lineterm=''))[:40]: print('   ',d)
    for e in etext:
        print('  expected equal to stdout (strip):', e.strip()==out.strip(), len(e.strip().splitlines()), len(out.strip().splitlines()))
        if e.strip()!=out.strip():
            for d in list(difflib.unified_diff(out.splitlines(), e.splitlines(), lineterm=''))[:40]: print('   ',d)
