import re, sys
path = sys.argv[1]; pats = sys.argv[2:]
raw = open(path, encoding="utf-8", errors="replace").read()
pages = raw.split("\f")
for pat in pats:
    hits = []
    for pi, pg in enumerate(pages, 1):
        flat = re.sub(r"\s+", " ", pg)
        for m in re.finditer(pat, flat, flags=re.I):
            hits.append((pi, flat[max(0, m.start()-160): m.end()+160]))
    print(f"== {pat}: {len(hits)} hits")
    for pi, t in hits[:3]:
        print(f"  pdfpage {pi}: ...{t}...")
