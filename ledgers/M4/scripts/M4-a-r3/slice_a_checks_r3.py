"""Round-3 slice-a checks: delta card ids, footers, standard-normal definitions, card duplicates, notation symbols.

Run as: .venv/bin/python -I ledgers/M4/scripts/M4-a-r3/slice_a_checks_r3.py <checkout>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
M4 = ROOT / "course/modules/M/M4"
DIFF = ROOT / "ledgers/M4/scripts/M4-a-r3/delta_c737272_a007712_M4.diff"

# 1. Card ids touched by the delta (new-side line numbers of cards.json hunks)
cards_path = M4 / "cards.json"
lines = cards_path.read_text(encoding="utf-8").split("\n")
changed_lines: list[int] = []
cur_new = 0
in_cards = False
for raw in DIFF.read_text(encoding="utf-8").split("\n"):
    if raw.startswith("diff --git"):
        in_cards = raw.endswith("course/modules/M/M4/cards.json")
        continue
    if not in_cards:
        continue
    m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", raw)
    if m:
        cur_new = int(m.group(1))
        continue
    if raw.startswith("+") and not raw.startswith("+++"):
        changed_lines.append(cur_new)
        cur_new += 1
ids_touched: list[str] = []
for ln in changed_lines:
    i = ln - 1
    while not lines[i].lstrip().startswith("{"):
        i -= 1
    j = i
    while '"id"' not in lines[j]:
        j += 1
    ids_touched.append(re.search(r'"id": "([^"]+)"', lines[j]).group(1))
print("cards.json new-side changed lines:", changed_lines)
print("card ids touched by delta:", sorted(set(ids_touched)))

# 2. Card integrity: unique ids, unique fronts, count
cards = json.loads(cards_path.read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
fronts = [c["front"].strip().lower() for c in cards]
print("cards total", len(cards), "dup ids", len(ids) - len(set(ids)), "dup fronts", len(fronts) - len(set(fronts)))
std = [c["id"] for c in cards if "standard normal" in (c["front"] + " " + c["back"]).lower()]
print("cards mentioning standard normal:", std)

# 3. Footers
for name in ["index.html", "L01.html", "L02.html", "L03.html", "L04.html"]:
    text = (M4 / name).read_text(encoding="utf-8")
    m = re.search(r'<footer class="site-footer">(.*?)</footer>', text, re.S)
    print(f"footer {name}: {m.group(1).strip() if m else 'MISSING'}")

# 4. Standard-normal definitions in the lessons of the unit
for name in ["index.html", "L01.html", "L02.html", "L03.html", "L04.html", "L05.html", "L06.html", "L07.html", "L08.html", "L09.html", "L10.html"]:
    p = M4 / name
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8")
    for n, line in enumerate(text.split("\n"), 1):
        if "standard normal law is" in line or "standard normal law \\(" in line or "is standard normal when" in line or "A variable Z with this law is a standard normal variable" in line:
            print(f"definition-like sentence {name}:{n}: {line.strip()[:110]}")

# 5. Notation symbols used on slice pages that the registry lists
nota = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
regs = [s["symbol"] for s in nota["symbols"]]
print("registry symbols:", regs)
print("registry macros:", nota["macros"] if isinstance(nota["macros"], list) else list(nota["macros"]))
for name in ["index.html", "L01.html", "L02.html", "L03.html", "L04.html"]:
    text = (M4 / name).read_text(encoding="utf-8")
    print(f"{name}: operatorname{{Var}} x{text.count('operatorname{Var}')}, \\\\Var macro x{text.count(chr(92) + 'Var')}, gamma_4 x{text.count('gamma_4')}, varphi x{text.count('varphi')}")
