import re, sys
path, pat = sys.argv[1], sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 250
text = open(path, encoding="utf-8", errors="replace").read()
flat = re.sub(r"\s+", " ", text)
n = 0
for m in re.finditer(pat, flat, flags=re.I):
    s, e = max(0, m.start() - width), min(len(flat), m.end() + width)
    print(f"[{n}] @{m.start()}: ...{flat[s:e]}...")
    n += 1
    if n > 12:
        break
print("matches:", n)
