import sys, re
pat = re.compile(sys.argv[1])
for f in sys.argv[2:]:
    for n, line in enumerate(open(f, encoding='utf-8'), 1):
        for m in pat.finditer(line):
            s = max(0, m.start() - 90); e = min(len(line), m.end() + 90)
            print(f"{f}:{n}: ...{line[s:e].strip()}...")
