import re, sys
f = sys.argv[1]; pat = re.compile(sys.argv[2])
lines = open(f, encoding="utf-8").read().split("\n")
for i, ln in enumerate(lines, 1):
    for m in pat.finditer(ln):
        s = max(0, m.start()-90); e = min(len(ln), m.end()+90)
        print(f"{i}: ...{ln[s:e]}...")
