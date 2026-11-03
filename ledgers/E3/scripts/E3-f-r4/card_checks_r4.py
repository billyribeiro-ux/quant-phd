"""E3 slice f round 4: structural checks on the L01-L04 cards against their lessons (no PASS carried from round 3)."""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD4-E3-f/course/modules/E/E3")
SLICE = ("L01", "L02", "L03", "L04")
cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
slice_cards = [c for c in cards if c["lesson"] in SLICE]
print("slice cards:", len(slice_cards), Counter(c["lesson"] for c in slice_cards))
print("slice ids:", [c["id"] for c in slice_cards])

def lesson_text(name):
    raw = (ROOT / f"{name}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw))

texts = {n: lesson_text(n) for n in SLICE}

# 1. numeric tokens on each card are present in its own lesson text
num_re = re.compile(r"\d+(?:\.\d+)?(?:e-?\d+)?")
missing = []
for c in slice_cards:
    for tok in set(num_re.findall(c["front"] + " " + c["back"] + " " + c.get("basis", ""))):
        if tok not in texts[c["lesson"]]:
            missing.append((c["id"], tok))
print("numeric tokens absent from own lesson:", missing)

# 2. duplicates across all cards (normalized front, and near-identical backs)
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
fronts = Counter(norm(c["front"]) for c in cards)
print("duplicate normalized fronts (all cards):", [f for f, n in fronts.items() if n > 1])
ids = Counter(c["id"] for c in cards)
print("duplicate ids (all cards):", [i for i, n in ids.items() if n > 1], "total cards", len(cards))

# 3. scope words on slice cards
scope = re.compile(r"\b(only|all|always|every|any|never|exactly|same|drives|each)\b", re.I)
for c in slice_cards:
    hits = sorted(set(m.group(0).lower() for m in scope.finditer(c["front"] + " " + c["back"])))
    if hits:
        print("scope words", c["id"], hits)

# 4. grade/basis field sanity
for c in slice_cards:
    g = c.get("grade")
    if g == "C" and not c.get("basis"):
        print("C without basis", c["id"])
    if g == "T" and c.get("basis"):
        print("T with basis", c["id"])
    if g in (None,) and c.get("basis"):
        print("basis without grade", c["id"])

# 5. banned / process words on slice cards and lessons
banned = re.compile(r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|\.\.\.|builder|verifier|round |ledger|REQUESTS", re.I)
for c in slice_cards:
    for m in banned.finditer(c["front"] + " " + c["back"]):
        print("banned/process hit", c["id"], m.group(0))
for n in SLICE:
    for m in banned.finditer(texts[n]):
        print("banned/process hit in", n, repr(texts[n][max(0, m.start()-40):m.end()+40]))
