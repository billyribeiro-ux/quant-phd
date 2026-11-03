"""List the TeX macros used in L01 to L04 math, and any registered notation symbol used with another meaning."""
import re
from collections import Counter
from pathlib import Path
import json

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD4-E3-f")
reg = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(reg["macros"])
cnt = Counter()
for n in ("L01", "L02", "L03", "L04"):
    raw = (ROOT / "course/modules/E/E3" / f"{n}.html").read_text(encoding="utf-8")
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, flags=re.S)
    for a, b in maths:
        body = a or b
        for m in re.findall(r"\\[A-Za-z]+", body):
            cnt[(n, m)] += 1
for (n, m), k in sorted(cnt.items()):
    flag = "" if (m in macros or m in ("\\frac", "\\ln", "\\exp", "\\sum", "\\min", "\\max", "\\cdot", "\\le", "\\ge", "\\ne", "\\in", "\\int", "\\to", "\\infty", "\\sqrt", "\\tfrac", "\\left", "\\right", "\\bigl", "\\bigr", "\\varepsilon", "\\gamma", "\\alpha", "\\beta", "\\sigma", "\\pi", "\\lim", "\\mathrm", "\\text", "\\quad", "\\,", "\\ldots", "\\dots", "\\cdots", "\\partial", "\\blacksquare", "\\operatorname", "\\mathbb", "\\mathcal", "\\overset", "\\,", "\;", "\\prod", "\\mathbf")) else " <-- not registered macro"
    print(n, m, k, flag)
