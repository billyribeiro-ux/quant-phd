import sys, re
L, pat, w = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 250
t = open(f"/tmp/E1d-r2/{L}.txt", encoding="utf-8").read()
for m in re.finditer(re.escape(pat), t):
    print(f"[{L}@{m.start()}]", t[max(0, m.start() - w): m.end() + w].strip())
    print("--")
