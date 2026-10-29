"""Round-8 verifier script: every number on a C-grade card must occur in that card's own lab expected block (strict)."""
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1]); t = root / "ledgers/CS2/scripts/CS2-d-r8/text"
cards = json.loads((root / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
num = re.compile(r"(?<![\w.^])\d+(?:\.\d+)?(?:e-?\d+)?(?![\w])")
for c in cards:
    if c["grade"] != "C":
        continue
    exp = (t / f"{c['lesson']}.expected.txt").read_text(encoding="utf-8")
    text = c["front"] + " " + c["back"]
    text = re.sub(r"(Lab \d|Part [A-Z]|Problem [A-Z]\d|Lesson \d|Section \d|Proposition [\d.()a-z]+|Corollary [\d.()a-z]+|Theorem [\d.()a-z]+|Definition [\d.()a-z]+|Remark [\d.()a-z]+)", " ", text)
    miss = sorted({tok for tok in num.findall(text) if tok not in exp})
    if miss:
        print(c["id"], c["lesson"], miss)
print("done")
