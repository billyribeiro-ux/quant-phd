"""Verifier script (M7-b round 2): notation collisions, stray CU, process words, banned phrases, concept words.

Run from the checkout root with: python3 -I ledgers/M7/scripts/M7-b-r2/notation_and_prose_check.py
"""
import html
import json
import re

pages = ["course/modules/M/M7/L04.html", "course/modules/M/M7/L05.html", "course/modules/M/M7/L06.html"]
twins = ["tests/labs/M7/lab-M7-L04-1.py", "tests/labs/M7/lab-M7-L05-1.py", "tests/labs/M7/lab-M7-L06-1.py"]
reg = json.load(open("notation/notation.json", encoding="utf-8"))["symbols"]
print("registry symbols:", [r["symbol"] for r in reg])
registry_tokens = ["\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}", "\\Prob"]
symbols_in_math = set()
for p in pages:
    src = open(p, encoding="utf-8").read()
    maths = re.findall(r"\\\((.*?)\\\)", src, re.S) + re.findall(r"\\\[(.*?)\\\]", src, re.S)
    body = html.unescape(" ".join(maths))
    for tok in registry_tokens:
        if tok in body:
            print("COLLISION CANDIDATE", p, tok)
    for t in re.findall(r"\b(?:T|M|R|V|F|L|K|Q|S|G|D|I)\b", body):
        symbols_in_math.add(t)
print("single capital letters used in L04-L06 math:", sorted(symbols_in_math))
print("registry-token collisions: none printed above means none")
for p in pages + twins:
    src = open(p, encoding="utf-8").read()
    hits = re.findall(r"\bCU\b", src)
    print("CU hits in", p, len(hits))
process = re.compile(r"\b(round|builder|verifier|ledger|corrected|updated|previous|earlier version|TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|it is important to note|obviously|clearly|well known|studies show|experts agree|you can add)\b", re.I)
for p in pages:
    src = html.unescape(re.sub(r"<[^>]+>", " ", open(p, encoding="utf-8").read()))
    hits = [m.group(0) for m in process.finditer(src)]
    print("process/banned hits in", p, hits)
for p in pages:
    src = open(p, encoding="utf-8").read()
    for m in re.finditer(r"covariance|efficient frontier|dynamic programming|convexity|efficient set", src):
        ctx = src[max(0, m.start() - 60): m.end() + 20]
        linked = 'data-concept="' in src[max(0, m.start() - 200): m.start()] and "</a>" not in src[m.start(): m.start() + 40]
        print("concept word", m.group(0), "in", p, "linked-context:", linked)
