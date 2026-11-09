"""M7-a round 1 witness: hours, why-it-matters word counts, dfn ownership across M7, link targets, concept anchors."""
import os
import re
import sys
from html.parser import HTMLParser

root = sys.argv[1]
M7 = os.path.join(root, "course/modules/M/M7")
pages = {f: open(os.path.join(M7, f), encoding="utf-8").read() for f in sorted(os.listdir(M7)) if f.endswith(".html")}

# hours
hours = {}
for f, t in pages.items():
    m = re.search(r'data-hours="(\d+)"', t)
    if m:
        hours[f] = int(m.group(1))
print("lesson data-hours:", hours, "sum", sum(v for k, v in hours.items() if k.startswith("L")))
hub = pages["index.html"]
print("hub main:", re.search(r'<main[^>]*>', hub).group(0))

# why-it-matters word counts
for f in ("L01.html", "L02.html", "L03.html"):
    t = pages[f]
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', t, re.S)
    txt = re.sub(r"<[^>]+>", " ", m.group(1))
    txt = re.sub(r"\\\(.*?\\\)", " X ", txt)
    print(f, "why-it-matters words (math as one token each):", len(txt.split()))

# dfn ownership across all M7 lessons
dfns = {}
for f, t in pages.items():
    for m in re.finditer(r'<dfn id="def-([^"]+)" data-concept="([^"]+)"', t):
        dfns.setdefault(m.group(2), []).append(f)
print("dfn concepts:", {k: v for k, v in sorted(dfns.items())})
print("dfn count", len(dfns), "multiply defined", {k: v for k, v in dfns.items() if len(v) > 1})

# relative links / anchors
for f, t in pages.items():
    for m in re.finditer(r'href="([^"#]*)(#[^"]*)?"', t):
        target = m.group(1)
        if not target or target.startswith(("http", "mailto")):
            continue
        p = os.path.normpath(os.path.join(M7, target))
        if not os.path.exists(p):
            print("BROKEN link", f, target)
        if m.group(2) and p.endswith(".html") and os.path.exists(p):
            anchor = m.group(2)[1:]
            if f"id=\"{anchor}\"" not in open(p, encoding="utf-8").read():
                print("MISSING anchor", f, target, m.group(2))
# concept anchors in concepts.html
concepts = open(os.path.join(root, "course/concepts.html"), encoding="utf-8").read()
for cid in sorted({m for t in pages.values() for m in re.findall(r'data-concept="([^"]+)"', t)}):
    if f'id="{cid}"' not in concepts and cid not in dfns:
        print("concept not in concepts.html and not defined in M7:", cid)
print("done")
