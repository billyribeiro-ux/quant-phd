"""Round 8: every numeric token in a card (front/back/basis) must occur in that card's own lesson text (extract_text output)."""
import json, re, sys
base = sys.argv[1]
cards = json.load(open(f"{base}/course/modules/LX/LX1/cards.json", encoding="utf-8"))
texts = {}
for L in ("L01", "L02", "L03", "L04"):
    texts[L] = open(f"{base}/ledgers/LX1/scripts/LX1-d-r8/out/{L}.txt", encoding="utf-8").read()
tok = re.compile(r"\d[\d,]*(?:\.\d+)?")
missing = []
for c in cards:
    t = texts[c["lesson"]]
    for field in ("front", "back", "basis"):
        for m in tok.findall(c.get(field) or ""):
            n = m.replace(",", "")
            if n not in t and m not in t:
                missing.append((c["id"], field, m))
print("tokens checked over", len(cards), "cards")
print("absent from own lesson text:", missing)
