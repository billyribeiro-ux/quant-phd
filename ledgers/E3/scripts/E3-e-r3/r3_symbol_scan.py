import re, glob
pages = sorted(glob.glob('L0*.html')) + ['project.html']
for s in ['kappa', 'zeta', 'eta', 'omega', 'alpha', 'delta', 'psi', 'beta', 'mathbb', 'Phi', 'lambda', 'T', 'R', 'Q']:
    print('==', s)
    for p in pages:
        t = open(p, encoding='utf-8').read()
        for m in re.finditer(r'(?<![A-Za-z])\\?' + re.escape(s) + r'(?![A-Za-z])', t):
            line = t[:m.start()].count('\n') + 1
            ctx = t[max(0, m.start() - 50):m.end() + 50].replace('\n', ' ')
            if s in ('T', 'R', 'Q') and not re.search(r'\\\(|\\\[|\$', ctx):
                continue
            print(f'  {p}:{line}: ...{ctx}...'[:230])
