import re, sys, html
pat = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
for f in sys.argv[1:]:
    t = open(f, encoding="utf-8").read()
    segs = [m.group(1) or m.group(2) for m in pat.finditer(t)]
    syms = set()
    for s in segs:
        s2 = html.unescape(re.sub(r"<[^>]+>", "", s))
        for tok in re.findall(r"\\[A-Za-z]+|[A-Za-z](?:_\{?[A-Za-z0-9,]+\}?)?|\\mathbb\{[A-Z]\}|\\mathrm\{[A-Za-z]+\}|\\mathcal\{[A-Za-z]\}", s2):
            syms.add(tok)
    print(f.split('/')[-1], len(segs), "segments")
    print("  ", " ".join(sorted(syms)))
    bad = [s for s in segs if re.search(r"\\mathbb\{R\}|\\mathbb\{Q\}|\\Phi|\\gamma|R_f|R\^\\ast|\\ast", s)]
    print("  forbidden-hits:", len(bad), [b[:60] for b in bad][:5])
    tt = [s for s in segs if re.search(r"(?<![A-Za-z\\])T(?![A-Za-z])", re.sub(r"\\text\{[^}]*\}|\\mathrm\{[^}]*\}", "", s))]
    print("  bare-T-hits:", len(tt), [b[:60] for b in tt][:5])
