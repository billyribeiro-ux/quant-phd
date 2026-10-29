"""Every number token on a card's back (integers, decimals, fractions) must appear in the card's own lesson text,
after removing the card's own lesson-number tokens. Misses are printed for manual review."""
import json, re, sys, html
from pathlib import Path
root = Path(sys.argv[1]) / "course/modules/E/E1"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
texts = {}
for i in range(1, 10):
    raw = re.sub(r"<script.*?</script>", " ", (root / f"L0{i}.html").read_text(encoding="utf-8"), flags=re.S)
    texts[f"L0{i}"] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
    texts[f"L0{i}"] = texts[f"L0{i}"].replace("\\(", "").replace("\\)", "")
NUM = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:/\d+)?(?:e-?\d+)?")
miss = []
for c in cards:
    t = texts[c["lesson"]]
    for tok in set(NUM.findall(c["back"] + " " + c["front"])):
        if re.fullmatch(r"\d", tok) and tok in {"0", "1", "2", "3"}:
            continue
        if tok in t:
            continue
        # a fraction like 5000/9 may appear as \frac{5000}{9}
        if "/" in tok and re.search(re.escape(tok.split("/")[0]) + r"\D{0,20}" + re.escape(tok.split("/")[1]), t):
            continue
        miss.append((c["id"], c["lesson"], tok))
print("number tokens not literally in the card's lesson:", len(miss))
for m in miss: print("  ", m)
