import re, sys
for page in ["L05", "L06", "L07", "L08"]:
    path = f"course/modules/E/E3/{page}.html"
    text = open(path, encoding="utf-8").read()
    spans = [m for m in re.finditer(r'<span class="grade" data-grade="([TC])">', text)]
    claims = len(re.findall(r'<span class="claim"', text))
    cites = len(re.findall(r'data-cite=', text))
    print(f"{page}: grade spans={len(spans)} T={sum(1 for m in spans if m.group(1)=='T')} C={sum(1 for m in spans if m.group(1)=='C')} claim spans={claims} data-cite={cites}")
    for m in spans:
        line_no = text.count("\n", 0, m.start()) + 1
        row = text[m.start(): m.start() + 600]
        row = re.sub(r"<[^>]+>", " | ", row)
        row = re.sub(r"\s+", " ", row)
        print(f"  L{line_no} {m.group(1)}: {row[:230]}")
