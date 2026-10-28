import re, sys, html
path, pats = sys.argv[1], sys.argv[2:]
t = html.unescape(re.sub(r"<[^>]+>", " ", open(path, encoding="utf-8").read()))
t = re.sub(r"\s+", " ", t)
for p in pats:
    for m in list(re.finditer(re.escape(p), t))[:3]:
        print(f"[{p}] ...{t[max(0,m.start()-170):m.end()+170]}...")
    print()
