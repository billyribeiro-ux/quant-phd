"""Round-6 check: every number token in a card front/back must appear in its lesson text (extract). Independent of the builder."""
import json, re, sys
base = sys.argv[1]
cards = json.load(open(f"{base}/course/modules/LX/LX1/cards.json", encoding="utf-8"))
text = {L: open(f"/tmp/lx1d6_scratch/{L}.txt", encoding="utf-8").read() for L in ("L01", "L02", "L03", "L04")}
num = re.compile(r"(?<![A-Za-z_])\d[\d,]*(?:\.\d+)?")
missing = []
for c in cards:
    src = text[c["lesson"]]
    for field in ("front", "back"):
        for tok in num.findall(c[field]):
            t = tok.rstrip(",")
            # lesson text may write numbers in LaTeX or with spaces; accept plain occurrence or the same digits without commas
            if t not in src and t.replace(",", "") not in src:
                missing.append((c["id"], field, t))
for m in missing:
    print("NOT-IN-LESSON", *m)
print("cards", len(cards), "unmatched number tokens", len(missing))
