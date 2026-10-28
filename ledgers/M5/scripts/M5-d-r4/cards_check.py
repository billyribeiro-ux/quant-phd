"""Flatten M5 lessons to text and check every card's numbers and key terms against its lesson text.

Usage: python -I cards_check.py <checkout-root> <outdir>
"""
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
m5 = root / "course/modules/M/M5"

def flat(p: Path) -> str:
    t = p.read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"[ \t\r]+", " ", t)

lessons = {f"L{i:02d}": flat(m5 / f"L{i:02d}.html") for i in range(1, 11)}
for k, v in lessons.items():
    (out / f"{k}.txt").write_text(v, encoding="utf-8")
cards = json.loads((m5 / "cards.json").read_text(encoding="utf-8"))
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}))
numre = re.compile(r"\d+(?:\.\d+)?(?:\s*[×x]\s*10\^?[(−\-]*\d+\)?)?|\d+/\d+")
missing = []
for c in cards:
    lt = lessons[c["lesson"]]
    nums = set(numre.findall(c["back"] + " " + c["front"]))
    for n in sorted(nums):
        core = n.strip()
        if core not in lt:
            missing.append((c["id"], c["lesson"], core))
with (out / "card_numbers_not_in_lesson.txt").open("w", encoding="utf-8") as fh:
    for row in missing:
        fh.write("\t".join(row) + "\n")
print("number tokens not literally in their lesson:", len(missing))
for row in missing:
    print(*row)
