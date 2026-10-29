import json, re, sys, html
from pathlib import Path
root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M4/cards.json").read_text())
for L in ("L05", "L06", "L07"):
    page = html.unescape(re.sub(r"<[^>]+>", " ", (root / f"course/modules/M/M4/{L}.html").read_text()))
    page = re.sub(r"\\\(|\\\)|\s+", " ", page)
    for c in cards:
        if c["lesson"] != L:
            continue
        nums = set(re.findall(r"(?<![A-Za-z_])\d+(?:[./]\d+)*", c["back"]))
        missing = sorted(n for n in nums if n not in page)
        print(L, c["id"], "numbers_not_in_lesson:", missing)
