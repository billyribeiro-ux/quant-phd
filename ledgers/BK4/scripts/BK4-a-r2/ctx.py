import re, sys, glob
pat = re.compile(sys.argv[1], re.I)
files = sys.argv[2:]
for f in files:
    for n, line in enumerate(open(f, encoding="utf-8"), 1):
        for m in pat.finditer(line):
            s = max(0, m.start() - 70); e = min(len(line), m.end() + 70)
            print(f"{f.split('/')[-1]}:{n}: ...{line[s:e].strip()}...")
