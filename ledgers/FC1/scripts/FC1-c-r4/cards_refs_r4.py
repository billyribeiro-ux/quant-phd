"""Second pass for FC1 cards (verifier r4): case-insensitive lookup of each numbered reference in its lesson, and
the specific numbers the two changed cards (FC1-c014, FC1-c122) rely on."""
import html
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD4-FC1-c/course/modules/FC/FC1")
cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))


def lesson_text(name):
    raw = (ROOT / name).read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw))


texts = {}
miss = []
for c in cards:
    lt = texts.setdefault(c["lesson"], lesson_text(f"{c['lesson']}.html")).lower()
    blob = " ".join(str(c.get(k, "")) for k in ("front", "back", "basis"))
    for kind, label in re.findall(r"\b(Proposition|Assumption|Remark|Definition|Lab|misconception|Example)\s+([0-9A-Za-z]+(?:\.[0-9]+)?)", blob):
        token = f"{kind} {label}".lower()
        if token not in lt:
            miss.append((c["id"], c["lesson"], f"{kind} {label}"))
    for num in re.findall(r"(?<![A-Za-z0-9.])\d+(?:\.\d+)?(?![0-9])", blob):
        if num.rstrip(".") not in lt and num not in lt:
            miss.append((c["id"], c["lesson"], "number " + num))
print("unmatched references/numbers:", len(miss))
for m in miss:
    print("  ", m)
for cid in ("FC1-c014", "FC1-c122"):
    c = next(x for x in cards if x["id"] == cid)
    print(cid, c["lesson"], json.dumps(c, ensure_ascii=False))
    lt = texts[c["lesson"]]
    for token in ("Proposition 3.1", "Lab 1, Part A", "Assumption 4.0", "Proposition 4.1", "λ", "6.8619", "Remark 4.2"):
        print("   ", repr(token), "in lesson:", token.lower() in lt.lower())
