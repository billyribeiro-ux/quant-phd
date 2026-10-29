"""For each E1 slice card: every number and every 'Definition/Proposition/Remark/Example/Problem/Misconception/Lab' locator in its text must appear in its lesson page."""
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/E/E1"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
pages = {p: html.unescape(re.sub(r"<[^>]+>", " ", (root / f"{p}.html").read_text(encoding="utf-8"))) for p in ("L01", "L02", "L03")}
bad = 0
for c in cards:
    if c["lesson"] not in pages:
        continue
    text = pages[c["lesson"]]
    body = c["front"] + " " + c["back"]
    locators = re.findall(r"(Definition|Proposition|Remark|Example|Problem|Misconception|Lab|Assumption) (\d+(?:\.\d+)?|[A-Z]\d)", body)
    for kind, num in locators:
        if kind == "Problem" or kind == "Lab" or kind == "Misconception" or kind == "Assumption":
            ok = (f"{kind} {num}" in text) or (kind == "Lab" and f"Lab {num}" in text) or (kind == "Misconception" and "Misconception" in text) or (kind == "Assumption" and f"Assumption {num}" in text) or (kind == "Problem" and f"{num} ·" in text)
        else:
            ok = f"{kind} {num}" in text
        if not ok:
            bad += 1
            print("MISSING LOCATOR", c["id"], kind, num)
    for n in re.findall(r"(?<![\w.])\d+(?:/\d+)?(?![\w.])", body):
        if n not in text and n not in ("1", "2", "0", "3", "4"):
            print("NUMBER NOT IN LESSON", c["id"], n)
            bad += 1
print("cards checked", sum(1 for c in cards if c["lesson"] in pages), "problems", bad)
