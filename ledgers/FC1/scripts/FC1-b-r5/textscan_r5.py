"""FC1-b round 5: text scans over L04, L05 and cards.json. Prints symbols and macros in math, scope-word hits,
process-word and banned-phrase hits. Run from the checkout root: .venv/bin/python -I <this file>."""

import json
import re
from pathlib import Path

ROOT = Path(".").resolve()
BASE = ROOT / "course/modules/FC/FC1"
REGISTERED_MACROS = {"\\E", "\\Prob", "\\Var", "\\Cov", "\\Corr", "\\R", "\\N", "\\indic", "\\Normal", "\\iid", "\\dto",
                     "\\pto", "\\argmax", "\\argmin", "\\tr", "\\diag", "\\SR", "\\hSR", "\\PSR", "\\DSR", "\\PBO",
                     "\\FWER", "\\FDR", "\\FDP", "\\se", "\\emgamma"}
REGISTERED_SYMBOLS = {"T", "R_f", "R^\\ast", "R^{e\\ast}", "\\mathbb{Q}", "\\Phi", "\\gamma_3", "\\gamma_4"}
SCOPE = re.compile(r"\b(only|all|every|always|never|any|exactly|same|drives|across|none)\b", re.I)
PROCESS = re.compile(r"\b(builder|verifier|round|request|ledger|planner|architect|slice|fixer)\b", re.I)
BANNED = re.compile(r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|"
                    r"it is important to note|studies show|experts agree|it is well known|obviously|clearly|\.\.\.|…", re.I)

for name in ["L04", "L05"]:
    text = (BASE / f"{name}.html").read_text(encoding="utf-8")
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S)
    macros, singles = set(), set()
    for a, b in maths:
        m = a or b
        macros |= set(re.findall(r"\\[A-Za-z]+", m))
        singles |= set(re.findall(r"(?<![\\A-Za-z])([A-Za-z])(?![A-Za-z])", m))
    print(f"== {name} math expressions: {len(maths)}")
    print("  single-letter symbols:", sorted(singles))
    print("  macros:", sorted(macros))
    print("  registered macros used:", sorted(macros & REGISTERED_MACROS))
    print("  registered symbols present (text):", sorted(s for s in REGISTERED_SYMBOLS if s in text))
    body = re.sub(r"<pre.*?</pre>", "", text.split("<main")[1], flags=re.S)
    plain = re.sub(r"<[^>]+>", " ", body)
    print(f"== {name} scope-word hits (outside code blocks)")
    for line in plain.split("\n"):
        for m in SCOPE.finditer(line):
            print("   ", m.group(0), "|", " ".join(line.split())[:140])
            break
    print(f"== {name} process words:", PROCESS.findall(plain))
    print(f"== {name} banned strings:", BANNED.findall(plain))

cards = json.loads((BASE / "cards.json").read_text(encoding="utf-8"))
blob = " ".join(c["front"] + " " + c["back"] for c in cards)
print("== cards process words:", PROCESS.findall(blob))
print("== cards banned strings:", BANNED.findall(blob))
