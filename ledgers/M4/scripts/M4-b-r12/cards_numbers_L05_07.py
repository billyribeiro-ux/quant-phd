"""Round 12 slice b: every decimal number on a L05-L07 card must appear in its lesson page (raw HTML text)."""
import json
import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyD12-M4-b/"
cards = json.load(open(ROOT + "course/modules/M/M4/cards.json", encoding="utf-8"))
pages = {l: open(ROOT + f"course/modules/M/M4/{l}.html", encoding="utf-8").read() for l in ("L05", "L06", "L07")}
bad = []
n_checked = 0
for c in cards:
    if c["lesson"] not in pages:
        continue
    text = c["front"] + " " + c["back"]
    nums = re.findall(r"(?<![A-Za-z_])\d+\.\d+(?:e-?\d+)?|\b\d{3,}\b", text)
    for num in nums:
        n_checked += 1
        if num not in pages[c["lesson"]]:
            bad.append((c["id"], c["lesson"], num))
print("numbers checked", n_checked, "not found in lesson", bad)
