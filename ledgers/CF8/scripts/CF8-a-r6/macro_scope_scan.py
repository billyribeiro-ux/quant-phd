"""Macro, registered-symbol and scope-word scan of CF8 index, L01, L02 (run with python -I)."""
import pathlib, re, sys
ROOT = pathlib.Path(sys.argv[1]) / "course/modules/CF/CF8"
for name in ["index.html", "L01.html", "L02.html"]:
    t = (ROOT / name).read_text(encoding="utf-8")
    macros = sorted(set(re.findall(r"\\([A-Za-z]+)", t)))
    print(name, "macros:", macros)
    print(name, "unregistered macro hits (mathbb/mathcal/operatorname):", re.findall(r"\\(?:mathbb|mathcal|operatorname)\{", t))
    print(name, "registered-symbol hits (\\Phi, \\gamma_3, \\gamma_4, R^\\ast, \\mathbb{Q}, \\Pr):",
          len(re.findall(r"\\Phi|\\gamma_[34]|R\^\\ast|R\^\{e|\\mathbb\{Q\}|\\R\b|\\E\b", t)))
