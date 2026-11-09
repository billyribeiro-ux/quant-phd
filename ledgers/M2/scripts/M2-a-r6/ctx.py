import re, sys, pathlib
pat = re.compile(sys.argv[1])
w = int(sys.argv[2]) if len(sys.argv) > 2 else 90
for f in sys.argv[3:]:
    txt = pathlib.Path(f).read_text(encoding='utf-8')
    for i, line in enumerate(txt.splitlines(), 1):
        for m in pat.finditer(line):
            s = max(0, m.start() - w); e = min(len(line), m.end() + w)
            print(f"{f}:{i}: {line[s:e]}")
