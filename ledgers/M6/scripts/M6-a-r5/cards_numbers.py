"""For each L01-L04 card, list numeric tokens in front/back that do not appear in the lesson text."""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
cards = json.loads((ROOT / "course/modules/M/M6/cards.json").read_text(encoding="utf8"))
for lesson in ("L01", "L02", "L03", "L04"):
    raw = (ROOT / f"course/modules/M/M6/{lesson}.html").read_text(encoding="utf8")
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = re.sub(r"\s+", " ", text)
    for c in cards:
        if c["lesson"] != lesson:
            continue
        blob = c["front"] + " " + c["back"]
        toks = set(re.findall(r"\d+(?:\.\d+)?(?:/\d+)?(?:\^?\(?-?\d+\)?)?", blob))
        miss = []
        for t in sorted(toks):
            core = t.strip()
            if core and core not in text and core not in raw:
                miss.append(core)
        if miss:
            print(lesson, c["id"], "numbers not literally in lesson:", miss)
print("scan done")
