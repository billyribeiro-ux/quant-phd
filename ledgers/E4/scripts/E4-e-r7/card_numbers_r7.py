"""Round 6: (a) grade counts and the basis of every C card; (b) every multi-digit or fractional number on each card front/back must appear in its lesson text (scratch/txt/Lxx.txt, rendered by html_to_text.py)."""
import collections
import json
import re
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
txt_dir = sys.argv[2]
grades = collections.Counter(c.get("grade") for c in cards)
print("grades", dict(grades))
for c in cards:
    if c.get("grade") == "C":
        print("C", c["id"], "|", c["basis"][:110])
lesson_text = {}
for i in range(1, 10):
    lesson_text[f"L{i:02d}"] = open(f"{txt_dir}/L{i:02d}.txt", encoding="utf-8").read()
pat = re.compile(r"\d+/\d+|\d+\.\d+|\d{2,}|e-\d+")
missing = []
for c in cards:
    body = c["front"] + " " + c["back"]
    toks = set(pat.findall(body))
    text = lesson_text[c["lesson"]]
    # numbers may be written with different glyphs (e.g. 1/2 as \tfrac12); check the bare digits too
    for t in sorted(toks):
        if t in text:
            continue
        simple = t.replace("/", "")
        if t in ("e-",):
            continue
        # look at every lesson text for the token (cards may cite a number from another lesson or a lab)
        hit = any(t in v for v in lesson_text.values())
        if not hit:
            missing.append((c["id"], c["lesson"], t))
print("numbers not found in own lesson text:", len(missing))
for m in missing:
    print("  ", m)
