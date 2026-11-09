import re, sys
# usage: grepctx.py PATTERN FILE... ; prints file:line: text (context truncated)
pat = re.compile(sys.argv[1])
for f in sys.argv[2:]:
    for i, line in enumerate(open(f, encoding="utf-8"), 1):
        for m in pat.finditer(line):
            s = max(0, m.start() - 60); e = min(len(line), m.end() + 60)
            print(f"{f}:{i}: ...{line[s:e].rstrip()}...")
