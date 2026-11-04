# Round 4 verifier scan, SC1 slice b: card ids, duplicate fronts over all SC1 cards; L04-L06 cards counted and
# checked for lesson tag, and every card number ("Lemma 2.1", "Proposition 1.3", ...) matched against its lesson text.
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
cards = json.load(open(ROOT / "course/modules/SC/SC1/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)))
fronts = collections.Counter(re.sub(r"\s+", " ", c["front"]).strip().lower() for c in cards)
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
backs = collections.Counter(re.sub(r"\s+", " ", c["back"]).strip().lower() for c in cards)
print("duplicate backs:", [f[:60] for f, n in backs.items() if n > 1])
sl = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print("L04-L06 cards:", len(sl), collections.Counter(c["lesson"] for c in sl))
for lesson in ("L04", "L05", "L06"):
    text = (ROOT / f"course/modules/SC/SC1/{lesson}.html").read_text(encoding="utf-8")
    plain = re.sub(r"<[^>]+>", " ", text)
    for c in (x for x in sl if x["lesson"] == lesson):
        refs = set(re.findall(r"\b(Lemma|Proposition|Theorem|Corollary|Definition|Remark|Problem|Assumption) (\d+\.\d+|[A-Z]\d)", c["front"] + " " + c["back"]))
        missing = []
        for kind, num in refs:
            if not re.search(rf"{kind} {re.escape(num)}", plain) and not re.search(rf"{kind} {re.escape(num)}", text):
                missing.append(f"{kind} {num}")
        if missing:
            print("MISSING in", lesson, c["id"], missing)
print("reference scan done")
