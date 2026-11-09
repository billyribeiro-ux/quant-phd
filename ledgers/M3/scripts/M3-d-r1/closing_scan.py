"""Closing-delta scans for M3 (read-only): process words, notation macros, backslash counts, keyword counts, hours."""
import json
import re
import sys

ROOT = sys.argv[1]
WORDS = r"\b(revised|corrected|updated|previous|previously|round|fixer|verifier|ledger|fragment|ruling|architect|builder|delta|pin|erratum|rewritten|amended|reviewer|agent|verified|fixed|changed)\b"
pat = re.compile(WORDS, re.IGNORECASE)
cards = json.load(open(f"{ROOT}/course/modules/M/M3/cards.json", encoding="utf-8"))
hits = []
for c in cards:
    for field in ("front", "back", "basis"):
        for m in pat.finditer(c.get(field, "") or ""):
            hits.append((c["id"], field, m.group(0)))
print("process-word hits in cards.json:", hits if hits else "none")
text_all = json.dumps(cards, ensure_ascii=False)
print("backslash count in cards.json:", text_all.count("\\"))
for name in ("correlation", "covariance", "variance", "expectation", "Gaussian", "Cholesky", "IEEE", "standard deviation"):
    print(f"cards.json count {name!r}:", len(re.findall(name, text_all, flags=re.IGNORECASE)))
ids = [c["id"] for c in cards]
nums = [int(i.rsplit("c", 1)[1]) for i in ids]
print("ids in file order ascending:", nums == sorted(nums))
for n in ("L07", "L08", "L09"):
    html = open(f"{ROOT}/course/modules/M/M3/{n}.html", encoding="utf-8").read()
    print(f"{n} process-word hits:", [m.group(0) for m in pat.finditer(html)][:10] or "none")
    print(f"{n} \\mathbb or \\R-free macros check, \\mathbb count:", html.count("\\mathbb"))
    print(f"{n} count of '\\\\(N' local N uses:", len(re.findall(r"\\\(N\b", html)))
proj = open(f"{ROOT}/course/modules/M/M3/project.html", encoding="utf-8").read()
print("project.html process-word hits:", [m.group(0) for m in pat.finditer(proj)][:10] or "none")
hours = 0
for n in range(1, 10):
    html = open(f"{ROOT}/course/modules/M/M3/L0{n}.html", encoding="utf-8").read()
    m = re.search(r'data-hours="([0-9.]+)"', html)
    hours += float(m.group(1)) if m else 0
    print(f"L0{n} data-hours:", m.group(1) if m else None)
print("sum of lesson data-hours L01-L09:", hours)
