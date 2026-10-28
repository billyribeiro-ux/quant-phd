"""Round 23 (AC1-c): extract the text of L07 and L08 (scripts, tags and styles removed, one line per block)
and scan the two lessons and cards.json for the banned strings of BUILDER_RULES section 1.

Usage: python -I extract_and_scan_r23.py <checkout> <out_dir>
Writes <out_dir>/L07.txt and <out_dir>/L08.txt, prints the banned-string hits (none expected).
"""

import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
PAGES = ["course/modules/AC/AC1/L07.html", "course/modules/AC/AC1/L08.html"]
BANNED = [
    "TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
    "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
    "obviously", "clearly", "roughly", "historically", "it can be shown", "...", "…", "http://", "https://",
    "<iframe", "<script src", "of course", "note that", "importantly", "in summary", "let us", "let's",
]
ABOUT = re.compile(r"about \d")
hits = 0
for rel in PAGES:
    t = (root / rel).read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<(br|/p|/li|/h\d|/dt|/dd|/tr|/section|/div|/pre)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    lines = [line.rstrip() for line in html.unescape(t).splitlines() if line.strip()]
    name = Path(rel).stem
    (out / f"{name}.txt").write_text("\n".join(f"{i} {line}" for i, line in enumerate(lines, 1)) + "\n", encoding="utf-8")
    print(rel, "text lines:", len(lines))
    for label, text in [(rel, (root / rel).read_text(encoding="utf-8"))]:
        for p in BANNED:
            for m in re.finditer(re.escape(p), text, flags=re.I):
                hits += 1
                print("HIT", label, repr(p), text[max(0, m.start() - 40): m.end() + 20].replace("\n", " "))
        for m in ABOUT.finditer(text):
            hits += 1
            print("HIT", label, "about <digit>", text[max(0, m.start() - 40): m.end() + 20].replace("\n", " "))
cards = json.loads((root / "course/modules/AC/AC1/cards.json").read_text(encoding="utf-8"))
slice_text = json.dumps([c for c in cards if c["lesson"] in ("L07", "L08")], ensure_ascii=False)
for p in BANNED + ["about 6", "roughly half"]:
    for m in re.finditer(re.escape(p), slice_text, flags=re.I):
        hits += 1
        print("HIT cards", repr(p), slice_text[max(0, m.start() - 40): m.end() + 20])
print("banned-string hits:", hits)
