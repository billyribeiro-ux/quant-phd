import html, re, sys
# usage: txt.py FILE [start end]  -> "N: text" with tags stripped (line numbers match the HTML file)
f = sys.argv[1]
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 1
hi = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
for i, line in enumerate(open(f, encoding="utf-8"), 1):
    if i < lo or i > hi:
        continue
    t = re.sub(r"<[^>]+>", "", line)
    t = html.unescape(t).strip()
    if t:
        print(f"{i}: {t}")
