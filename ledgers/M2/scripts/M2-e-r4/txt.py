import re, html, sys
t = open(sys.argv[1], encoding="utf-8").read()
t = re.sub(r"<[^>]+>", " ", t); t = html.unescape(t); t = re.sub(r"\s+", " ", t)
for kw in sys.argv[2:]:
    for m in list(re.finditer(re.escape(kw), t))[:2]:
        print(f"[{kw}] ...{t[max(0, m.start()-150):m.start()+330]}...\n")
