"""LX1-b round 16: every L03 and L04 card, its numbers, and its byte-identity against the round-15 pin.

Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r16/cards_r16.py <checkout> <round-15 pin>
"""

import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
pin15 = sys.argv[2]
cards = json.loads((root / "course/modules/LX/LX1/cards.json").read_text(encoding="utf-8"))
old = {c["id"]: c for c in json.loads(subprocess.run(
    ["git", "-C", str(root), "show", f"{pin15}:course/modules/LX/LX1/cards.json"],
    capture_output=True, text=True, check=True).stdout)}
lesson_text = {
    "L03": (root / "course/modules/LX/LX1/L03.html").read_text(encoding="utf-8"),
    "L04": (root / "course/modules/LX/LX1/L04.html").read_text(encoding="utf-8"),
}
NUM = re.compile(r"(?<![A-Za-z_])\d[\d,]*(?:\.\d+)?")
missing = []
for c in cards:
    if c["lesson"] not in lesson_text:
        continue
    same = old.get(c["id"]) == c
    text = lesson_text[c["lesson"]].replace("&lt;", "<").replace("&gt;", ">")
    nums = set(NUM.findall(c["front"] + " " + c["back"]))
    absent = sorted(n for n in nums if n.replace(",", "") not in text.replace(",", "") and n not in text)
    status = "same-as-round15" if same else ("NEW" if c["id"] not in old else "CHANGED")
    print(f"{c['id']} {c['lesson']} {status} numbers={sorted(nums)} absent_from_lesson={absent}")
    if absent:
        missing.append((c["id"], absent))
print("cards read:", sum(1 for c in cards if c["lesson"] in lesson_text), "| numbers absent from lesson:", missing)
