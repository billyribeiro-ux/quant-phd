import re, html, sys, os
base = sys.argv[1]
for f in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"]:
    s = open(os.path.join(base, "course/modules/E/E5", f + ".html"), encoding="utf-8").read()
    titles = re.findall(r'class="block-title[^>]*>(.*?)</span>\s*</span>', s, re.S)
    out = []
    for t in titles:
        t = html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
        out.append(re.sub(r"\s+", " ", t)[:60])
    print("==", f, len(out))
    print("; ".join(out))
