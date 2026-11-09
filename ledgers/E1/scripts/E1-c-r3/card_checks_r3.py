"""Round-3 card checks: numbers appear in lesson text; duplicate scan over all E1 cards; id uniqueness."""
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)) == len(ids))
text = {}
for L in ("L07", "L08", "L09"):
    raw = (root / f"course/modules/E/E1/{L}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    text[L] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
bad = []
for c in cards:
    if c["lesson"] not in text:
        continue
    for tok in set(re.findall(r"\d+(?:[./]\d+)*", c["front"] + " " + c["back"])):
        if tok not in text[c["lesson"]]:
            bad.append((c["id"], tok))
print("numeric tokens not found verbatim in lesson:", bad)
sl = [c for c in cards if c["lesson"] in text]
print("L07-L09 cards:", len(sl))


def words(c):
    return set(re.findall(r"[a-z0-9]+", (c["front"] + " " + c["back"]).lower()))


pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        wa, wb = words(a), words(b)
        j = len(wa & wb) / max(1, len(wa | wb))
        if j >= 0.45 and (a["lesson"] in text or b["lesson"] in text):
            pairs.append((round(j, 2), a["id"], b["id"]))
for p in sorted(pairs, reverse=True):
    print("pair", p)
# Cards whose text cites a proposition/lemma/theorem/corollary/remark: list for hypothesis review
for c in sl:
    s = c["back"]
    if re.search(r"\((Lemma|Proposition|Theorem|Corollary|Remark|Example)", s):
        print("cites-result", c["id"], "| starts:", s[:70])
