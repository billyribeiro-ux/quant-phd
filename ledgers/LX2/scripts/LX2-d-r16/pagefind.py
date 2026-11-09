import re, sys
# usage: pagefind.py <txtfile> <regex> [width]
path, pat = sys.argv[1], sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 200
raw = open(path, encoding="utf-8", errors="replace").read()
pages = raw.split("\f")
for pi, pg in enumerate(pages, 1):
    flat = re.sub(r"\s+", " ", pg)
    for m in re.finditer(pat, flat, flags=re.I):
        s, e = max(0, m.start() - width), min(len(flat), m.end() + width)
        nums = re.findall(r"\b(6[4-9]\d|7[0-2]\d)\b", flat[:200])
        print(f"pdfpage {pi} printed-nums {nums[:3]}: ...{flat[s:e]}...")
print("done", pat)
