"""Round 7 checks for CF1-c: cards basis fields versus lesson headings, and twin output versus page expected blocks."""
import html
import json
import re
import sys

ROOT = sys.argv[1]
cards = json.load(open(f"{ROOT}/course/modules/CF/CF1/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "distinct ids", len(set(ids)), "missing basis", [c["id"] for c in cards if not c.get("basis")])
for lab in ("L05", "L06"):
    text = open(f"{ROOT}/course/modules/CF/CF1/{lab}.html", encoding="utf-8").read()
    for c in cards:
        if c["lesson"] != lab:
            continue
        head = c["basis"].split(",")[0].split(";")[0].strip()
        status = "found" if head in text else "NOT FOUND"
        print(lab, c["id"], repr(c["basis"]), status)
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    exp = [l.strip() for l in html.unescape(m.group(1)).strip().splitlines()]
    got = [l.strip() for l in open(f"{sys.argv[2]}/{lab}.out", encoding="utf-8").read().strip().splitlines()]
    print(lab, "expected lines", len(exp), "output lines", len(got), "identical", exp == got)
