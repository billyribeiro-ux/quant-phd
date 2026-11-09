import re, sys, pathlib
base = pathlib.Path(sys.argv[1])
pats = {'M': r'(?<![A-Za-z\\])M(?![A-Za-z])', 'K': r'(?<![A-Za-z\\])K(?![A-Za-z])', 'kappa': r'\\kappa|κ', 'delta': r'\\delta|δ', 'M_macro': r'\\mathcal\{M\}'}
for f in sys.argv[2:]:
    p = base / f
    for i, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
        for name, pat in pats.items():
            for m in re.finditer(pat, line):
                s = max(0, m.start() - 50); e = min(len(line), m.end() + 40)
                print(f"{f}:{i} [{name}] ...{line[s:e]}...")
