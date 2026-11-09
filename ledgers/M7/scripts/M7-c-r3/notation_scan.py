"""List every macro and every distinct math token used in L07/L08 math segments and the twins' math-free symbols check."""
import html
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
reg = __import__("json").loads((root / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(reg["macros"].keys())
registered_letters = {"T", "Phi", "R", "Q", "gamma_3", "gamma_4", "R_f", "E", "Prob", "Var", "Cov", "Corr", "N", "SR"}
for lid in ("L07", "L08"):
    page = (root / f"course/modules/M/M7/{lid}.html").read_text(encoding="utf-8")
    page = html.unescape(page)
    segs = re.findall(r"\\\((.*?)\\\)", page, re.S) + re.findall(r"\\\[(.*?)\\\]", page, re.S)
    mac = Counter()
    toks = Counter()
    for seg in segs:
        for m in re.findall(r"\\[A-Za-z]+", seg):
            mac[m] += 1
        s2 = re.sub(r"\\[A-Za-z]+", " ", seg)
        s2 = re.sub(r"\\(text|mathrm|operatorname|mathbb|mathcal|mathbf|mathit|overset|xrightarrow)\{[^}]*\}", " ", s2)
        for tok in re.findall(r"[A-Za-z]|\\?[A-Za-z]+", s2):
            toks[tok] += 1
    print(lid, "segments:", len(segs))
    print(lid, "macros used:", dict(mac))
    print(lid, "single-letter tokens:", dict(sorted(toks.items())))
    print(lid, "macros not in notation.json:", sorted(m for m in mac if m not in macros))
    raw = re.findall(r"\\mathbb\{[A-Za-z]\}|\\mathcal\{[A-Za-z]\}|\\mathrm\{[A-Za-z_]+\}|\\mathbf\{[A-Za-z]\}", "".join(segs))
    print(lid, "blackboard/calligraphic/roman in math:", Counter(raw))
    print(lid, "greek in math:", sorted(set(re.findall(r"\\(alpha|beta|gamma|delta|Delta|sigma|Sigma|lambda|mu|nu|varepsilon|epsilon|tau|rho|Phi|phi|pi|theta)", "".join(segs)))))
