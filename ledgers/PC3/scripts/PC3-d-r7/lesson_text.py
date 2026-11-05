"""Dump each PC3 lesson's visible text, one line per source line, for line-cited reading.

Usage: python -I ledgers/PC3/scripts/PC3-d-r5/lesson_text.py <outdir>
Writes <outdir>/L01.txt .. L06.txt and <outdir>/cards.txt (one card per block).
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
PAGES = ROOT / "course" / "modules" / "PC" / "PC3"
out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
for n in range(1, 7):
    src = PAGES / f"L{n:02d}.html"
    lines = src.read_text(encoding="utf-8").splitlines()
    dumped = []
    for i, line in enumerate(lines, 1):
        text = re.sub(r"<[^>]+>", "", line)
        text = html.unescape(text).strip()
        if text:
            dumped.append(f"{i:4d}: {text}")
    (out / f"L{n:02d}.txt").write_text("\n".join(dumped) + "\n", encoding="utf-8")
cards = json.loads((PAGES / "cards.json").read_text(encoding="utf-8"))
with (out / "cards.txt").open("w", encoding="utf-8") as fh:
    for c in cards:
        fh.write(json.dumps(c, ensure_ascii=False, indent=1) + "\n")
print("wrote", out)
