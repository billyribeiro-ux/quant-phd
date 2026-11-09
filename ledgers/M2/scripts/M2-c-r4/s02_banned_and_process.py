"""Banned-phrase, process-word, placeholder, notation-macro and data/figure scans for M2 slice c (L13-L18).

Covers the six lesson pages, the six lab twins and the slice cards (lesson in L13..L18).
Run: .venv/bin/python -I <this file> <checkout root>.
"""
import json
import re
import sys

ROOT = sys.argv[1]
PAGES = ["L13", "L14", "L15", "L16", "L17", "L18"]
BANNED = [
    r"\bTODO\b", r"\bTBD\b", r"lorem", r"for brevity", r"details omitted", r"beyond the scope",
    r"left as an exercise", r"you can add more", r"it is important to note", r"studies show",
    r"experts agree", r"it is well known", r"\bobviously\b", r"\bclearly\b", r"it can be shown",
    r"motivat", r"\bin this lesson we\b", r"\.\.\.", r"…",
]
PROCESS = [r"architect", r"builder", r"verifier", r"planner", r"ledger", r"fanout", r"round \d",
           r"page_smoke", r"run_labs", r"check_pages", r"check_dag", r"embed_labs", r"\bMCP\b",
           r"\bfixer\b", r"\bslice\b", r"\bpin\b", r"Ruling", r"\bKNOWN", r"\bblind\b"]
MACROS_OK = {"\\E", "\\Prob", "\\Var", "\\Cov", "\\Corr", "\\R", "\\N", "\\indic", "\\Normal", "\\iid", "\\dto",
             "\\pto", "\\argmax", "\\argmin", "\\tr", "\\diag", "\\SR", "\\hSR", "\\PSR", "\\DSR", "\\PBO", "\\FWER",
             "\\FDR", "\\FDP", "\\se", "\\emgamma"}
STD_OK = set()

def scan(label, text, patterns):
    hits = []
    for pat in patterns:
        for m in re.finditer(pat, text, re.I if pat in BANNED else 0):
            ln = text.count("\n", 0, m.start()) + 1
            hits.append((pat, ln, text[max(0, m.start()-50):m.end()+50].replace("\n", " ")))
    print(f"{label}: {len(hits)} hits")
    for h in hits[:20]:
        print("   ", h)

for p in PAGES:
    t = open(f"{ROOT}/course/modules/M/M2/{p}.html", encoding="utf-8").read()
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    body = re.sub(r"</?summary>|</?details[^>]*>", "", body)
    scan(f"{p} banned", body, BANNED)
    scan(f"{p} process", body, PROCESS)
    macros = set(re.findall(r"\\[A-Za-z]+", body))
    dm = sorted(m for m in macros if m not in MACROS_OK)
    print(f"{p} macros used (not in notation registry, excluding KaTeX/standard names): see next line")
    print("   ", dm)
    print(f"{p} data/figure markup:", len(re.findall(r'data-files|data-chart|<figure|class="chart"|<svg', t)))

for n in range(13, 19):
    t = open(f"{ROOT}/tests/labs/M2/lab-M2-L{n}-1.py", encoding="utf-8").read()
    scan(f"twin L{n} banned", t, BANNED)
    scan(f"twin L{n} process", t, PROCESS)
    print(f"twin L{n} file/network tokens:", re.findall(r"open\(|urllib|requests|socket|http", t))

cards = json.load(open(f"{ROOT}/course/modules/M/M2/cards.json", encoding="utf-8"))
sl = [c for c in cards if c["lesson"] in PAGES]
blob = "\n".join(c["front"] + "\n" + c["back"] + "\n" + str(c.get("basis", "")) for c in sl)
scan("slice cards banned", blob, BANNED)
scan("slice cards process", blob, PROCESS)
print("slice card grades:", {g: sum(1 for c in sl if c.get("grade") == g) for g in ["T", "A", "B", "C", "D", "X", None]})
print("C cards without basis:", [c["id"] for c in sl if c.get("grade") == "C" and not c.get("basis")])
print("T/C-graded cards lacking grade-appropriate fields:", [c["id"] for c in sl if c.get("grade") not in ("T","A","B","C","D","X",None)])
