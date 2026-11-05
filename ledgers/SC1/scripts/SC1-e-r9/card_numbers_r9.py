"""For each card, list its decimal / multi-digit numeric tokens and whether the token occurs in the card's own lesson text.

Usage: python -I card_numbers_r9.py <repo_root> <out_dir>
"""
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
cards = json.loads((root / "course/modules/SC/SC1/cards.json").read_text(encoding="utf-8"))
texts = {}
for n in range(1, 9):
    texts[f"L{n:02d}"] = (out / f"L{n:02d}.txt").read_text(encoding="utf-8")
lab_outs = {}
for n in range(1, 9):
    lab_outs[f"L{n:02d}"] = "\n".join(
        l for l in texts[f"L{n:02d}"].splitlines()
    )
tok = re.compile(r"(?<![A-Za-z_])(\d+\.\d+|\d{2,})(?![\d])")
total = 0
missing = []
for c in cards:
    s = c["front"] + " " + c["back"]
    toks = sorted(set(tok.findall(s)))
    toks = [t for t in toks if t not in ("10", "12", "16", "20", "24")] if False else toks
    for t in toks:
        total += 1
        if t not in texts[c["lesson"]]:
            missing.append((c["id"], t))
print("numeric tokens (>=2 digits or decimal):", total)
print("not verbatim in own lesson text:", len(missing))
for m in missing:
    print(m)
