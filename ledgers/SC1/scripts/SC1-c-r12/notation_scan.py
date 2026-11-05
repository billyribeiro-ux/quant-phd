"""Scan L07 and L08 prose (outside code/expected blocks) for TeX macros, and list notation.json macros.

Usage: python -I notation_scan.py <repo-root>
"""
import json
import re
import sys
from collections import Counter

root = sys.argv[1]
cmds: Counter[str] = Counter()
for lesson in ("L07", "L08"):
    text = open(f"{root}/course/modules/SC/SC1/{lesson}.html", encoding="utf-8").read()
    text = re.sub(r"<pre.*?</pre>", "", text, flags=re.S)
    text = re.sub(r"<script.*?</script>", "", text, flags=re.S)
    for m in re.findall(r"\\([A-Za-z]+)", text):
        cmds[f"{lesson}:\\{m}"] += 1
for k, v in sorted(cmds.items()):
    print(k, v)
nj = json.load(open(f"{root}/notation/notation.json", encoding="utf-8"))
print("notation.json top-level keys:", list(nj.keys()) if isinstance(nj, dict) else type(nj))
macros = nj.get("macros", []) if isinstance(nj, dict) else []
print("macro names:", [m.get("name", m.get("macro")) if isinstance(m, dict) else m for m in macros][:200])
syms = nj.get("symbols", []) if isinstance(nj, dict) else []
for s in syms:
    print("SYMBOL", json.dumps(s, ensure_ascii=False)[:220])
