"""Structural and text checks of course/modules/LX/LX1/cards.json against the four lesson pages (LX1-d round 3).

Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-d-r3/card_checks_r3.py <repo root>
Checks: id sequence and uniqueness; lesson field; grade and basis; cite keys; every numeric token in a card's
front and back occurs in its lesson's extracted text; near-duplicate fronts (word Jaccard); duplicate backs;
banned process words; each lab twin's printed output occurs verbatim (whitespace-normalised) in its lesson page.
"""

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1])
SCRIPTS = ROOT / "ledgers/LX1/scripts/LX1-d-r3"
MOD = ROOT / "course/modules/LX/LX1"
OUT = SCRIPTS / "out"
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards))
ids = [c["id"] for c in cards]
print("ids unique:", len(set(ids)) == len(ids), " ids in file order LX1-c001..c%03d:" % len(cards),
      ids == [f"LX1-c{i:03d}" for i in range(1, len(cards) + 1)])
print("keys set:", sorted({k for c in cards for k in c}))
print("cards per lesson:", {L: sum(1 for c in cards if c["lesson"] == L) for L in ("L01", "L02", "L03", "L04")})
print("grade values:", Counter(c.get("grade", "-") for c in cards))
print("cards without grade:", [c["id"] for c in cards if "grade" not in c])
print("non-T cards without basis:", [c["id"] for c in cards if c.get("grade") in ("C", "B") and not c.get("basis")])
print("cards with non-empty cite:", [c["id"] for c in cards if c.get("cite")])
print("empty front/back:", [c["id"] for c in cards if not c["front"].strip() or not c["back"].strip()])

texts = {}
for L in ("L01", "L02", "L03", "L04"):
    txt = subprocess.run([sys.executable, "-I", str(SCRIPTS / "html_text.py"), str(MOD / f"{L}.html")],
                         capture_output=True, text=True, check=True).stdout
    lines = [re.sub(r"^\s*\d+ ", "", ln) for ln in txt.splitlines()]
    texts[L] = re.sub(r"\s+", " ", " ".join(lines))

NUM = re.compile(r"\d+(?:\.\d+)?")
missing = []
for c in cards:
    for field in ("front", "back"):
        for tok in NUM.findall(c[field]):
            if tok not in texts[c["lesson"]]:
                missing.append((c["id"], field, tok))
print("numeric tokens absent from their lesson text:", missing if missing else "none")

# Lab twin printed output vs the lesson's embedded expected block (whitespace-normalised, verbatim substring)
twin_map = {"L01": "twin_L01.out", "L02": "twin_L02.out", "L03": "twin_L03.out", "L04": "twin_L04.out"}
for L, name in twin_map.items():
    twin = re.sub(r"\s+", " ", (OUT / name).read_text(encoding="utf-8")).strip()
    print(f"twin {L} output found verbatim in lesson page text:", twin in texts[L])
    bad = [ln for ln in (OUT / name).read_text(encoding="utf-8").splitlines() if ln.strip()
           and re.sub(r"\s+", " ", ln).strip() not in texts[L]]
    print(f"  lines of twin {L} output not in lesson text:", bad if bad else "none")


def words(s: str) -> set[str]:
    return set(re.findall(r"[a-z]+", s.lower()))


pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        wa, wb = words(a["front"]), words(b["front"])
        j = len(wa & wb) / max(1, len(wa | wb))
        if j >= 0.5:
            pairs.append((a["id"], b["id"], round(j, 2)))
print("front Jaccard >= 0.5 pairs:", pairs)
bk = Counter(re.sub(r"\s+", " ", c["back"]).strip().lower() for c in cards)
print("duplicate backs:", [k for k, n in bk.items() if n > 1] or "none")
fk = Counter(re.sub(r"\s+", " ", c["front"]).strip().lower() for c in cards)
print("duplicate fronts:", [k for k, n in fk.items() if n > 1] or "none")

banned = re.compile(r"\b(todo|tbd|lorem|builder|round|request|verif\w*|reference|obviously|clearly|studies show)\b|\.\.\.", re.I)
hits = [(c["id"], f, m.group(0)) for c in cards for f in ("front", "back") for m in banned.finditer(c[f])]
print("banned or process words in cards:", hits if hits else "none")
scope = re.compile(r"\b(only|all|always|every|any|same|generally|exactly|drives|whatever)\b", re.I)
print("scope words in cards:", [(c["id"], f, m.group(0)) for c in cards for f in ("front", "back")
                                for m in scope.finditer(c[f])])
