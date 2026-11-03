import re, sys
pat = re.compile(sys.argv[1])
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 120
for path in sys.argv[2].split(','):
    s = open(path, encoding='utf-8').read()
    for m in pat.finditer(s):
        line = s.count('\n', 0, m.start()) + 1
        a, b = max(0, m.start() - ctx), min(len(s), m.end() + ctx)
        print(f"{path}:{line}: ...{s[a:b]!r}...")
