"""For each L05-L08 card, list numeric tokens (front and back) that do not occur in the lesson's plain text
(which includes the printed lab outputs and the code). Numbers with a single digit are ignored.

Usage: card_numbers_in_lesson.py <cards.json> <text dir with L05.txt ... L08.txt>
"""
import json
import re
import sys
from pathlib import Path

cards = json.load(open(sys.argv[1], encoding="utf-8"))
tdir = Path(sys.argv[2])
texts = {L: (tdir / f"E3g_r2_{L}.txt").read_text(encoding="utf-8") for L in ("L05", "L06", "L07", "L08")}
TOKEN = re.compile(r"(?<![A-Za-z_])(\d+(?:\.\d+)?(?:e-?\d+)?)")
for c in cards:
    if c["lesson"] not in texts:
        continue
    text = texts[c["lesson"]]
    tokens = []
    for field in ("front", "back"):
        for m in TOKEN.finditer(c[field]):
            tok = m.group(1)
            if len(tok.replace(".", "").replace("e", "")) < 2 and "." not in tok:
                continue
            tokens.append((field, tok))
    missing = []
    for field, tok in tokens:
        variants = {tok}
        if "." in tok and "e" not in tok:
            variants.add(f"{float(tok):.4f}")
        if not any(v in text for v in variants):
            # look in the whole E3 text of all four lessons
            if not any(v in t for v in variants for t in texts.values()):
                missing.append((field, tok))
    if missing:
        print(c["id"], c["lesson"], "numbers not found in any L05-L08 text:", missing)
print("scan done for", len(cards), "cards")
