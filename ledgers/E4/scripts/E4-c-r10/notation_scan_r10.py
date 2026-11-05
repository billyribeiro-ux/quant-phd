"""Round 10, slice E4-c: list every TeX command used in the math of L07 to L09 and flag registered macros and symbols."""
import collections
import json
import re
from pathlib import Path

BASE = Path("/Users/billyribeiro/.fanout/wt/verifyE10-E4-c")
reg = json.loads((BASE / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(reg["macros"])
for lesson in ("L07", "L08", "L09"):
    src = (BASE / "course/modules/E/E4" / (lesson + ".html")).read_text(encoding="utf-8")
    spans = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", src, re.S)
    tex = " ".join(a or b for a, b in spans)
    cmds = collections.Counter(re.findall(r"\\[A-Za-z]+", tex))
    registered_used = sorted(c for c in cmds if c in macros)
    print(lesson, "math spans", len(spans), "distinct commands", len(cmds))
    print("  registered macros used:", registered_used)
    print("  all commands:", " ".join(sorted(cmds)))
    for sym in ("\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}", "\\SR", "\\Prob", "\\N"):
        if sym in tex:
            print("  registry symbol present:", sym)
    for name in ("T", "R", "Q", "N", "S"):
        hits = re.findall(r"(?<![A-Za-z\\])" + name + r"(?![A-Za-z])", tex)
        if hits:
            print("  bare letter", name, "occurrences in math:", len(hits))
