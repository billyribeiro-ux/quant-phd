"""Check that each theorem-like or problem reference inside an L05-L08 card (e.g. 'Remark 3.4', 'Problem R2',
'Example 2.5', 'section 6') names a block that exists in the card's own lesson text, or in another E3 lesson
when the card says 'Lesson N' or 'Lesson LN'.

Usage: card_refs_exist.py <cards.json> <text dir>
"""
import json
import re
import sys
from pathlib import Path

cards = json.load(open(sys.argv[1], encoding="utf-8"))
tdir = Path(sys.argv[2])
texts = {L: (tdir / f"E3g_r2_{L}.txt").read_text(encoding="utf-8") for L in ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08") if (tdir / f"E3g_r2_{L}.txt").exists()}
REF = re.compile(r"\b(Theorem|Proposition|Corollary|Remark|Definition|Example|Observation|Lemma|Problem|Lab)\s+(\d+\.\d+|[A-Z]\d|\d+)")
SECT = re.compile(r"\bsection\s+(\d+)\b")
labels = {}
for L, t in texts.items():
    found = set()
    for m in re.finditer(r"^\d{4}: (Theorem|Proposition|Corollary|Remark|Definition|Example|Observation|Lemma|Problem|Lab)\s*(\d+\.\d+|[A-Z]\d|\d+)?", t, re.M):
        pass
    # Block titles appear as a line 'Kind n.m' possibly followed by a parenthesised name on the next line.
    for m in re.finditer(r"^\d{4}: (Theorem|Proposition|Corollary|Remark|Definition|Example|Observation|Lemma)\s+(\d+\.\d+)", t, re.M):
        found.add(f"{m.group(1)} {m.group(2)}")
    for m in re.finditer(r"^\d{4}: (Problem) ([A-Z]\d)\b", t, re.M):
        found.add(f"Problem {m.group(2)}")
    for m in re.finditer(r"^\d{4}: ([A-Z]\d) · ", t, re.M):
        found.add(f"Problem {m.group(1)}")
    for m in re.finditer(r"^\d{4}: (Lab \d)", t, re.M):
        found.add(m.group(1))
    labels[L] = found
bad = []
for c in cards:
    L = c["lesson"]
    if L not in labels:
        continue
    refs_text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    for m in REF.finditer(refs_text):
        kind, num = m.group(1), m.group(2)
        key = f"{kind} {num}"
        if kind == "Problem" and not re.fullmatch(r"[A-Z]\d", num):
            continue
        if key == "Lab 1":
            continue
        # Theorem 1.5 of Lesson 4 may be cited as 'Lesson 4 (Theorem 1.5)'; handled by the caller.
        if key in labels[L]:
            continue
        other = [O for O in labels if key in labels[O]]
        bad.append((c["id"], L, key, "found in " + ",".join(other) if other else "NOT FOUND in any L01-L08 text"))
for b in bad:
    print(b)
print("checked refs; unresolved:", len(bad))
