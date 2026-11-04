import re, sys
for path in sys.argv[1:]:
    src = open(path, encoding="utf-8").read()
    # raw '<' inside \( ... \) or \[ ... \] math spans (KaTeX source) is parsed as a tag by the browser
    hits = []
    for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", src, re.S):
        body = m.group(1) if m.group(1) is not None else m.group(2)
        if "<" in body:
            ln = src.count("\n", 0, m.start()) + 1
            hits.append((ln, body[:80]))
    # raw '<' followed by a letter in ordinary text (outside math) is also a tag opener
    print(path, "math spans with raw <:", len(hits))
    for h in hits: print("   line", h[0], repr(h[1]))
