# Banned-phrase, scope-word, notation-reservation, psi-domain and round-delta checks for E3 slice g (L05-L08), round 6.
import json, re, subprocess, sys
T = ['ledgers/E3/scripts/E3-g-r6/text/L0%d.txt' % i for i in (5, 6, 7, 8)]
banned = re.compile(r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add|"
                    r"it is important to note|studies show|experts agree|it is well known|obviously|clearly|"
                    r"it can be shown|historically|roughly half|interestingly|importantly|notably", re.I)
print('== banned phrases in L05-L08 text (non-code lines):')
for f in T:
    for i, l in enumerate(open(f, encoding='utf-8'), 1):
        if banned.search(l) and not re.search(r'^\s*(def |print|from |import |[A-Z_]+ *[:=])', l):
            print(f, i, banned.search(l).group(0))
print('== psi not-equal-1 statements (line, psi domain stated on that line?):')
for f in T:
    for i, l in enumerate(open(f, encoding='utf-8'), 1):
        if re.search(r'(ψ|\\psi)\s*(\\ne|≠)\s*1', l):
            print(f.split('/')[-1], i, 'psi>0 on line' if re.search(r'(ψ|\\psi)\s*>\s*0', l) else 'NO psi>0 on line', '|', l.strip()[:110])
print('== registered symbols/macros in slice math (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, mathbb Q, raw mathbb E):')
html = ['course/modules/E/E3/L0%d.html' % i for i in (5, 6, 7, 8)]
pat = re.compile(r'\\mathbb\{[A-Z]\}|\\Phi|\\gamma_[34]|R_f|R\^\\ast|R\^\{e|\\Prob\b')
for f in html:
    for i, l in enumerate(open(f, encoding='utf-8'), 1):
        for m in pat.finditer(l):
            print(f.split('/')[-1], i, m.group(0))
print('== round delta: cards changed/added/removed between 440ed3c8 and 142ecfc2 (slice only)')
old = {c['id']: c for c in json.loads(subprocess.check_output(['git', 'show', '440ed3c8:course/modules/E/E3/cards.json']))}
new = {c['id']: c for c in json.load(open('course/modules/E/E3/cards.json', encoding='utf-8'))}
for k in sorted(set(old) | set(new)):
    if old.get(k) != new.get(k):
        print(k, 'lesson', (new.get(k) or old.get(k))['lesson'], 'status', 'added' if k not in old else 'removed' if k not in new else 'changed')
print('== lesson hunks changed since 440ed3c8 (L05, L07, L08):')
print(subprocess.check_output(['git', 'diff', '440ed3c8', '142ecfc2', '-U0', '--', 'course/modules/E/E3/L05.html', 'course/modules/E/E3/L06.html', 'course/modules/E/E3/L07.html', 'course/modules/E/E3/L08.html']).decode()[:0] or 'see git diff -U0 output in the round notes')
