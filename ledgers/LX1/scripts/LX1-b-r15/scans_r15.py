"""LX1-b round 15 scans of L03.html, L04.html, cards.json (L03/L04 items), the L01 P-symbol and the N symbol.

Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r15/scans_r15.py <checkout>
"""

import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
LX = root / "course/modules/LX/LX1"


def prose(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"<pre.*?</pre>", "", t, flags=re.S)
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))


print("== 1 banned and process words (prose with code and expected blocks removed; cards L03/L04)")
BAN = re.compile(
    r"\b(TODO|TBD|lorem|build|builder|builders|round|verifier|verified|REQUEST|unit report|fixer|planner|architect|ruling|"
    r"obviously|clearly)\b|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|"
    r"it is important to note|studies show|experts agree|it is well known|\.\.\.",
    re.I,
)
for name in ("L03.html", "L04.html"):
    print(name, "hits:", [m.group(0) for m in BAN.finditer(prose(LX / name))])
cards = json.loads((LX / "cards.json").read_text(encoding="utf-8"))
for k in cards:
    if k["lesson"] in ("L03", "L04"):
        for m in BAN.finditer(k["front"] + " " + k["back"]):
            print("card", k["id"], "hit", m.group(0))
print("cards L03/L04:", sum(1 for k in cards if k["lesson"] == "L03"), sum(1 for k in cards if k["lesson"] == "L04"))

print("== 2 scope words in L04 prose (count only)")
SCOPE = re.compile(r"\b(every|all|always|any|never|only|same|exactly|the first|the last|no|none)\b", re.I)
for name in ("L03.html", "L04.html"):
    counts: dict[str, int] = {}
    for m in SCOPE.finditer(prose(LX / name)):
        counts[m.group(0).lower()] = counts.get(m.group(0).lower(), 0) + 1
    print(name, dict(sorted(counts.items())))

print("== 3 outside-closure concept terms in prose (L03, L04)")
OUT = re.compile(
    r"bank run|fire.sale|leverage cycle|banking crisis|currency crisis|covered interest|uncovered interest|"
    r"efficient.market|moral hazard|bank reserves|default swap|contagion|term spread|crisis mechanism|"
    r"market structure|sovereign|bailout|bank failure|financial panic|speculative|bubble",
    re.I,
)
for name in ("L03.html", "L04.html"):
    print(name, sorted({m.group(0).lower() for m in OUT.finditer(prose(LX / name))}))

print("== 4 macros and registered symbols (L03, L04, cards)")
src = (LX / "L03.html").read_text(encoding="utf-8") + (LX / "L04.html").read_text(encoding="utf-8")
print("macros:", sorted(set(re.findall(r"\\[A-Za-z]+", src))))
REG = re.compile(r"\\Phi|\\gamma_[34]|R\^\\ast|R\^\{e\\ast\}|R_f|\\mathbb\{Q\}|\bT\b|\\E\b|\\R\b|\\Prob|\\Var|\\Cov|\\N\b")
print("registered-symbol hits in L03/L04 math:", [m.group(0) for m in REG.finditer(src)])
print("card macro/registered hits:", [k["id"] for k in cards if k["lesson"] in ("L03", "L04") and REG.search(k["front"] + k["back"])])

print("== 5 symbol P and N (LX1 pages, twins, cards)")
for name in ("L01.html", "L02.html", "L03.html", "L04.html", "project.html"):
    lines = (LX / name).read_text(encoding="utf-8").split("\n")
    hits = [i for i, line in enumerate(lines, 1) if re.search(r"P_\{?0\}?|P_\{?t\}?", line)]
    print(name, "lines with P_0 or P_t:", hits)
lines = (LX / "L01.html").read_text(encoding="utf-8").split("\n")
print("L01.html lines with A_t or A_0:", [i for i, line in enumerate(lines, 1) if re.search(r"A_\{?[t0]\}?", line)])
print("L01 cards with P_0 or P_t:", [k["id"] for k in cards if k["lesson"] == "L01" and re.search(r"P_0|P_t", k["front"] + k["back"])])
print("N symbol in L03/L04 pages, twins and cards:",
      [name for name in ("L03.html", "L04.html") if re.search(r"\bN_|\bN\b", (LX / name).read_text(encoding="utf-8"))],
      [k["id"] for k in cards if k["lesson"] in ("L03", "L04") and re.search(r"\bN\b|N_", k["front"] + k["back"])])

print("== 6 cards: duplicates across all cards and near-duplicate fronts")
import difflib  # noqa: E402
from collections import Counter  # noqa: E402

print("dup ids", [i for i, n in Counter(k["id"] for k in cards).items() if n > 1])
print("dup fronts", [i for i, n in Counter(k["front"].strip().lower() for k in cards).items() if n > 1])
print("dup backs", [i for i, n in Counter(k["back"].strip().lower() for k in cards).items() if n > 1])
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        r = difflib.SequenceMatcher(None, cards[i]["front"], cards[j]["front"]).ratio()
        if r > 0.85:
            pairs.append((cards[i]["id"], cards[j]["id"], round(r, 2)))
print("near-duplicate fronts (ratio > 0.85):", pairs)
