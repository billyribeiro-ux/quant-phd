import re, sys
for f in sys.argv[1:]:
    t = open(f, encoding="utf-8").read()
    # claim spans
    spans = [(m.start(), m.group(0)) for m in re.finditer(r'<span class="block-title claim" data-grade="([A-Z])">([^<]*)<span class="name">([^<]*)</span>', t)]
    proofs = [m.start() for m in re.finditer(r'<span class="block-title">Proof</span>', t)]
    print(f"== {f}: claim spans {len(spans)}, proof headers {len(proofs)}")
    for pos, s in spans:
        g = re.search(r'data-grade="([A-Z])">([^<]*)', s)
        title = re.search(r'">([^<]*)<span class="name">', s)
        nxt = [p for p in proofs if p > pos]
        gap = (nxt[0] - pos) if nxt else None
        label = re.sub(r'<[^>]+>', '', s)[:70]
        print(f"  grade {g.group(1)} | {label!r} | next proof after {gap} chars")
