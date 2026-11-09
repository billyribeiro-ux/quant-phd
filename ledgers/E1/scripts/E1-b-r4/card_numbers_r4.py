"""Round-4: every number token in each slice card (L04-L06) must appear in its lesson page text or the lesson's lab output block."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))
pages = {}
for L in ("L04", "L05", "L06"):
    raw = (ROOT / f"course/modules/E/E1/{L}.html").read_text(encoding="utf-8")
    pages[L] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
for c in cards:
    if c["lesson"] not in pages:
        continue
    text = pages[c["lesson"]]
    nums = set(re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?", c["front"] + " " + c["back"]))
    absent = []
    for n in sorted(nums):
        if n in ("1", "2", "3", "4", "5", "0", "6", "7", "8", "9"):
            continue
        if not re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d])", text):
            absent.append(n)
    if absent:
        print(c["id"], c["lesson"], "numbers not in lesson text:", absent)
print("scan done")
