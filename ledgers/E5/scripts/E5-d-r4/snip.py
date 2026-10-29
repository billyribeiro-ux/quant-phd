import re, html, sys
path = sys.argv[1]
src = open(path, encoding="utf-8").read()
txt = re.sub(r"</?[a-zA-Z][^>]*>", "", src)
txt = html.unescape(re.sub(r"\s+", " ", txt))
for marker in sys.argv[2:]:
    for m in re.finditer(re.escape(marker), txt):
        print(f"[{marker}] " + txt[m.start(): m.start() + 700])
        print()
