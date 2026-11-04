"""For each FC2 card, list each decimal or integer (2+ digits) in front/back that does not appear in its lesson HTML
(tags stripped, entities unescaped). A missing token is not necessarily wrong: derived values must be checked by hand.

Usage: python -I cards_numbers_r8.py <FC2 dir>
"""
import html
import json
import re
import sys
from pathlib import Path

d = Path(sys.argv[1])
cards = json.loads((d / "cards.json").read_text(encoding="utf-8"))
text = {}
for p in d.glob("L0*.html"):
    raw = p.read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    text[p.stem] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
# the lab twins and the FC2 lab outputs are part of the lesson's printed numbers
labs = Path(sys.argv[1]).resolve().parents[3] / "tests" / "labs" / "FC2"
lab_text = " ".join(p.read_text(encoding="utf-8") for p in labs.glob("*.py")) if labs.exists() else ""
num = re.compile(r"(?<![A-Za-z_\d.])(\d+(?:\.\d+)?)(?![\d])")
for c in cards:
    body = c["front"] + " " + c["back"]
    own = text[c["lesson"]]
    for m in num.finditer(body):
        tok = m.group(1)
        if len(tok.replace(".", "")) < 2:
            continue
        if tok in own or tok in lab_text:
            continue
        print(c["id"], c["lesson"], repr(tok), "| not in own lesson text")
print("done")
