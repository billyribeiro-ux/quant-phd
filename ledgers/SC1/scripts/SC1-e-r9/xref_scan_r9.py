"""Cross-reference, grade-basis and process-word scans for the SC1 cards and lesson text; central-difference check for c174.

Usage: python -I xref_scan_r9.py <repo_root> <out_dir>
"""
import json
import math
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
cards = json.loads((root / "course/modules/SC/SC1/cards.json").read_text(encoding="utf-8"))
lesson_text = {f"L{n:02d}": (out / f"L{n:02d}.txt").read_text(encoding="utf-8") for n in range(1, 9)}

# 1. Problem labels (e.g. M2, P2, R3, E3) and Lab 1 parts named in cards must exist in the card's own lesson.
bad = []
for c in cards:
    s = c["front"] + " " + c["back"]
    txt = lesson_text[c["lesson"]]
    for lab in set(re.findall(r"\b(?:Problem |problem )?([MPRE]\d)\b", s)):
        if not re.search(r"(?<![A-Za-z])" + lab + r" ·", txt) and lab not in txt:
            bad.append((c["id"], "problem", lab))
    for part in set(re.findall(r"Lab 1, Part ([A-E])", s)):
        if f"Part {part}" not in txt and f"{part} ·" not in txt and f"Part {part}" not in txt:
            bad.append((c["id"], "lab part", part))
    for sec in set(re.findall(r"Section (\d)\b", s)):
        if not re.search(r"\n\s*\d+\s*\S|\b" + sec + r"\s*(Definition|Assumption|Lemma|Section)?", txt):
            bad.append((c["id"], "section", sec))
    for res in set(re.findall(r"(Lemma|Proposition|Theorem|Corollary|Remark|Example|Definition) (\d\.\d)", s)):
        key = f"{res[0]} {res[1]}"
        if key not in txt:
            bad.append((c["id"], "result", key))
print("cross-reference misses (own lesson):", bad)

# 2. Grade C cards must name a lab in basis or text; T cards with grade must have a basis.
gc = [(c["id"], c.get("basis")) for c in cards if c.get("grade") == "C" and "Lab" not in (c.get("basis") or "")]
print("grade C without Lab in basis:", gc)
gt = [c["id"] for c in cards if c.get("grade") == "T" and not c.get("basis")]
print("grade T without basis:", gt)

# 3. Process words in lesson text (not in the lab code or quiz only ids).
proc = re.compile(r"\b(builder|verifier|verification round|round \d|fixer|ledger|reviewer|sub-?agent)\b", re.I)
for k, t in lesson_text.items():
    hits = [m.group(0) for m in proc.finditer(t)]
    print(k, "process-word hits:", hits)

# 4. Central difference check for card c174 (density of tau_1 at H=1,2 against finite differences of erfc form).
def F(a, h):
    return math.erfc(a / math.sqrt(2 * h))
def f(a, h):
    return a / (math.sqrt(2 * math.pi) * h ** 1.5) * math.exp(-a * a / (2 * h))
for h in (1.0, 2.0):
    d = 1e-5
    num = (F(1, h + d) - F(1, h - d)) / (2 * d)
    print("c174 H=%g density %.9f central difference %.9f diff %.2e" % (h, f(1, h), num, abs(f(1, h) - num)))
