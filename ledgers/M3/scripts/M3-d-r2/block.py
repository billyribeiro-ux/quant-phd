import html, re, sys
from pathlib import Path
root = Path("/tmp/verifyB2-M3-d/course/modules/M/M3")
page, labels = sys.argv[1], sys.argv[2:]
raw = (root / f"{page}.html").read_text(encoding="utf-8")
for lab in labels:
    m = re.search(r'<span class="block-title[^"]*"[^>]*>\s*' + re.escape(lab) + r'\b', raw)
    if not m:
        print(f"== {page} {lab}: NOT FOUND"); continue
    seg = raw[m.start(): m.start() + 1400]
    seg = re.sub(r"</(p|li|div)>", "\n", seg)
    txt = html.unescape(re.sub(r"<[^>]+>", "", seg))
    txt = re.sub(r"[ \t]+", " ", txt).strip()
    print(f"== {page} {lab}:\n{txt[:900]}\n")
