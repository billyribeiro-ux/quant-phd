"""Round-3 structural checks: page-embedded code equals twin; L01 and L02 standardizer ASTs equal;
TAG_PRIORITY equals the contract table; cards: ids, duplicates, count per lesson; notation macros used vs registry.
Usage: .venv/bin/python -I ledgers/AC2/scripts/L01-L02-r3/checks_r3.py   (run from the checkout root)
"""
import ast
import collections
import html
import json
import re

ROOT = "."
for page, twin in [("course/modules/AC/AC2/L01.html", "tests/labs/AC2/lab-AC2-L01-1.py"),
                   ("course/modules/AC/AC2/L02.html", "tests/labs/AC2/lab-AC2-L02-1.py")]:
    h = open(f"{ROOT}/{page}", encoding="utf-8").read()
    code = html.unescape(re.search(r"data-run>(.*?)</code></pre>", h, re.S).group(1))
    print(page, "embedded code == twin (final newline ignored):", code == open(f"{ROOT}/{twin}", encoding="utf-8").read().rstrip("\n"))

def funcs(p):
    t = ast.parse(open(f"{ROOT}/{p}", encoding="utf-8").read())
    names = ("_date", "_observation", "_is_annual", "_us_gaap", "_as_of_pick", "select", "standardize")
    return {n.name: ast.dump(n) for n in t.body if isinstance(n, ast.FunctionDef) and n.name in names}

a = funcs("tests/labs/AC2/lab-AC2-L01-1.py")
b = funcs("tests/labs/AC2/lab-AC2-L02-1.py")
print("standardizer ASTs equal L01 vs L02:", {k: a[k] == b.get(k) for k in a})

rows = {}
for line in open(f"{ROOT}/atlas/A15.contract.md", encoding="utf-8"):
    m = re.match(r"\| `(\w+)` \| `([^`]+)`", line)
    if m:
        rows[m.group(1)] = re.findall(r"`([A-Z]\w+)`", line.split("|")[2])
t = ast.parse(open(f"{ROOT}/tests/labs/AC2/lab-AC2-L01-1.py", encoding="utf-8").read())
tp = next(ast.literal_eval(n.value) for n in t.body if isinstance(n, ast.AnnAssign) and getattr(n.target, "id", "") == "TAG_PRIORITY")
print("TAG_PRIORITY equals contract table:", {k: rows.get(k) == list(v) for k, v in tp.items()})

cards = json.load(open(f"{ROOT}/course/modules/AC/AC2/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "dup ids", [k for k, v in collections.Counter(ids).items() if v > 1],
      "seq ok", ids == [f"AC2-c{i:03d}" for i in range(1, len(ids) + 1)])
print("dup fronts", [k for k, v in collections.Counter(c["front"] for c in cards).items() if v > 1],
      "dup backs", [k for k, v in collections.Counter(c["back"] for c in cards).items() if v > 1])
print("per lesson", {l: sum(c["lesson"] == l for c in cards) for l in ("L01", "L02")})

txt = "".join(open(f"{ROOT}/course/modules/AC/AC2/{p}", encoding="utf-8").read() for p in ("index.html", "L01.html", "L02.html"))
used = sorted(set(re.findall(r"\\[A-Za-z]+", html.unescape(txt))))
reg = json.load(open(f"{ROOT}/notation/notation.json", encoding="utf-8"))
print("macros used:", used)
keys = set()
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(k, str) and k.startswith("\\"):
                keys.add(k)
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(reg)
print("macros used that are registered keys in notation/notation.json:", [m for m in used if m in keys])
