"""Slice-b card checks: duplicates over all cards, lesson membership, and every number in a slice card's text
must occur in its lesson page text or in that lesson's lab output (run from the checkout root)."""
import html
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1])
cards = json.loads((ROOT / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
fronts = Counter(c["front"].strip().lower() for c in cards)
print("cards:", len(cards), "dup ids:", [k for k, v in ids.items() if v > 1], "dup fronts:", [k for k, v in fronts.items() if v > 1])
slice_lessons = ["L07", "L08", "L09", "L10", "L11", "L12"]
labs = {"L07": "lab-M2-L07-1", "L08": "lab-M2-L08-1", "L09": "lab-M2-L09-1", "L10": "lab-M2-L10-1",
        "L11": "lab-M2-L11-1", "L12": "lab-M2-L12-1"}
tag = re.compile(r"<(?=/?[A-Za-z!])[^>]*>")
num = re.compile(r"\d+(?:\.\d+)?(?:e-?\d+)?")
for L in slice_lessons:
    page_raw = (ROOT / f"course/modules/M/M2/{L}.html").read_text(encoding="utf-8")
    page_text = html.unescape(tag.sub(" ", page_raw))
    lab_out = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/M2/{labs[L]}.py")],
                             capture_output=True, text=True, cwd="/tmp").stdout
    hay = page_text + "\n" + lab_out
    mine = [c for c in cards if c["lesson"] == L]
    missing = []
    for c in mine:
        for n in set(num.findall(c["back"])):
            if n.rstrip("0").rstrip(".") and n not in hay:
                missing.append((c["id"], n))
    print(f"{L}: cards={len(mine)} ids={sorted(c['id'] for c in mine)[0]}..{sorted(c['id'] for c in mine)[-1]} "
          f"numbers_not_in_page_or_lab={missing}")
