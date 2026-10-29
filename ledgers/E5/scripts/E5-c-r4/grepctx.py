import re, sys
pat = re.compile(sys.argv[1])
for path in sys.argv[2:]:
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        for m in pat.finditer(line):
            s = max(0, m.start() - 60); e = min(len(line), m.end() + 60)
            print(f"{path}:{n}: ...{line[s:e].strip()}...")
