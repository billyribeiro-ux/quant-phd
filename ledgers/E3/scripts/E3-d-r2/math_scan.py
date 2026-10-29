import re, sys, json, html
base = "/tmp/verifyC2-E3-d/course/modules/E/E3/"
files = sys.argv[1:]
for f in files:
    txt = open(base + f if not f.startswith("/") else f, encoding="utf-8").read()
    txt = html.unescape(txt)
    segs = re.findall(r"\\\((.+?)\\\)", txt, flags=re.S)
    segs += re.findall(r"\$(.+?)\$", txt)
    syms = set()
    for s in segs:
        for tok in re.findall(r"\\[A-Za-z]+|[A-Za-z](?:_\{?\w+\}?)?|\\?[A-Za-z]+\^\{?[^}\s]*\}?", s):
            syms.add(tok)
    print(f, sorted(syms))
