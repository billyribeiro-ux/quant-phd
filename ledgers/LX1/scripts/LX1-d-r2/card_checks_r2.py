"""Structural checks on course/modules/LX/LX1/cards.json against the four lesson texts (round 2, slice d).

Run: python -I card_checks_r2.py <repo root>
Checks: ids sequence and uniqueness; lesson field; grade/basis; every decimal or integer token in a card's
front and back appears in its lesson's extracted text; Jaccard near-duplicate scan of fronts; banned words;
cards with no grade; each card's cite keys exist in references/references.json.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
MOD = ROOT / "course/modules/LX/LX1"
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards))
ids = [c["id"] for c in cards]
expected = [f"LX1-c{i:03d}" for i in range(1, len(cards) + 1)]
print("ids in file order are LX1-c001..c%03d:" % len(cards), ids == expected, "unique:", len(set(ids)) == len(ids))
print("lessons:", {L: sum(1 for c in cards if c["lesson"] == L) for L in ("L01", "L02", "L03", "L04")})
print("cards without grade:", [c["id"] for c in cards if "grade" not in c])
print("grade T/C cards without basis:", [c["id"] for c in cards if "grade" in c and not c.get("basis")])
print("grades:", {g: sum(1 for c in cards if c.get("grade") == g) for g in "TC"})

texts = {}
for L in ("L01", "L02", "L03", "L04"):
    out = subprocess.run(
        [sys.executable, "-I", str(ROOT / "ledgers/LX1/scripts/LX1-d-r2/extract_text.py"), str(MOD / f"{L}.html")],
        capture_output=True, text=True, check=True).stdout
    texts[L] = out

NUM = re.compile(r"\d+(?:\.\d+)?")
problems = []
for c in cards:
    body = texts[c["lesson"]]
    for field in ("front", "back"):
        for tok in NUM.findall(c[field]):
            if tok not in body:
                problems.append((c["id"], field, tok))
print("number tokens in card front/back absent from lesson text:", problems if problems else "none")

def words(s):
    return set(re.findall(r"[a-z]+", s.lower()))
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        wa, wb = words(a["front"]), words(b["front"])
        j = len(wa & wb) / max(1, len(wa | wb))
        if j >= 0.6:
            pairs.append((a["id"], b["id"], round(j, 2)))
print("front Jaccard >= 0.6 pairs:", pairs)

banned = re.compile(r"\b(todo|tbd|lorem|verif\w*|builder|round|request|obviously|clearly|studies show|experts agree)\b|\.\.\.", re.I)
hits = [(c["id"], m.group(0)) for c in cards for f in ("front", "back") for m in banned.finditer(c[f])]
print("banned or process words in cards:", hits if hits else "none")

refs = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
keys = set()
if isinstance(refs, dict):
    keys = set(refs.get("entries", refs).keys()) if isinstance(refs.get("entries", refs), dict) else set()
elif isinstance(refs, list):
    keys = {r.get("key") for r in refs}
print("cite keys used by cards:", sorted({k for c in cards for k in c.get("cite", [])}))
print("registry keys loaded:", len(keys))
