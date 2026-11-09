"""Round-3 slice b: is 'Definition/Theorem ... below' in a why-it-matters paragraph a repo convention?

Counts course lesson pages whose why-it-matters paragraph carries an explicit forward pointer ('below' or
'defined in Section'), and prints the first few. Used to decide whether the L04-L06 forward pointers are a
convention rather than a define-before-use defect. Run from the checkout root.
"""
import glob
import re

hits = []
pages = sorted(glob.glob("course/modules/*/*/L0*.html"))
for f in pages:
    t = open(f, encoding="utf-8").read()
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', t, re.S)
    if m and re.search(r"(below|defined in Section)", m.group(1)):
        hits.append(f)
print("lesson pages scanned:", len(pages), "with forward pointer in why-it-matters:", len(hits))
for f in hits[:8]:
    print(" ", f)
for f in ("L04", "L05", "L06"):
    p = f"course/modules/M/M3/{f}.html"
    print(p, "forward pointer in why-it-matters:", p in hits)
