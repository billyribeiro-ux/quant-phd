import re, sys, glob, html
root = sys.argv[1]
files = sorted(glob.glob(root + '/course/modules/E/E3/L0[1-8].html')) + [root + '/course/modules/E/E3/cards.json'] + sorted(glob.glob(root + '/tests/labs/E3/lab-E3-L0[1-8]-1.py'))
syms = [r'\\rho', r'\\tau', r'\\tilde', r'\\varsigma', r'\\eta', r'\\varepsilon', r'\\psi', r'\\phi', r'\\varphi', r'\\omega', r'\\alpha', r'\\delta', r'\\kappa', r'\\nu', r'\\upsilon', r'\\chi', r'\\gamma', r'\\lambda', r'\\beta', r'\\sigma', r'\\pi', r'\\mu', r'\\theta', r'\\xi', r'\\zeta', r'\\iota', r'\\Phi', r'\\Psi']
plain = [r'\brho\b', r'\btau\b', r'\btilde\b', r'\bvarsigma\b', r'\beta\b', r'\bEIS\b', r'\bu_tilde\b', r'\bvarepsilon\b', r'\bepsilon\b', r'\beps\b', r'\bpsi\b', r'\bv\b', r'\bq\b', r'\bz\b', r'\bw\b']
for f in files:
    t = open(f, encoding='utf-8').read()
    name = f.replace(root + '/', '')
    counts = {}
    for s in syms:
        n = len(re.findall(s + r'(?![a-zA-Z])', t))
        if n: counts[s.replace('\\\\', '\\')] = n
    print(name, counts)
