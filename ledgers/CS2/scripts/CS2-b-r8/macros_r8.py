"""List every TeX macro and every single-letter symbol used in math spans of L05-L08, against notation.json."""
import collections
import html
import json
import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyB8-CS2-b"
reg = json.load(open(f"{ROOT}/notation/notation.json", encoding="utf-8"))
macros = set(reg["macros"].keys())
for lesson in ["L05", "L06", "L07", "L08"]:
    text = html.unescape(open(f"{ROOT}/course/modules/CS/CS2/{lesson}.html", encoding="utf-8").read())
    spans = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S)
    math = " ".join(a or b for a, b in spans)
    cmds = collections.Counter(re.findall(r"\\[A-Za-z]+", math))
    unknown = {c: n for c, n in cmds.items() if c in ("\\E", "\\Prob", "\\Var", "\\Cov", "\\Corr", "\\R", "\\N") or c in macros}
    letters = collections.Counter(re.findall(r"(?<![\\A-Za-z])([A-Za-z])(?![A-Za-z])", re.sub(r"\\[A-Za-z]+", " ", math)))
    print(lesson, "spans", len(spans), "macros", dict(cmds))
    print(lesson, "letters", dict(letters))
    print(lesson, "registry-macros-used", unknown)
