import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
cards = json.load(open(root / "course/modules/LX/LX1/cards.json"))
pages = {k: (root / f"course/modules/LX/LX1/{k}.html").read_text(encoding="utf-8") for k in ("L03", "L04")}
seen = {}
for c in cards:
    if c["lesson"] not in ("L03", "L04"):
        continue
    txt = c["front"] + " " + c["back"]
    key = (c["front"].strip().lower())
    if key in seen:
        print("DUPLICATE front:", c["id"], seen[key])
    seen[key] = c["id"]
    nums = set(re.findall(r"\d+(?:\.\d+)?", txt))
    missing = [n for n in nums if len(n) >= 3 and n not in pages[c["lesson"]]]
    print(c["id"], c["lesson"], c.get("grade", "-"), "| numbers missing from lesson:", missing, "|", c["front"][:110])
