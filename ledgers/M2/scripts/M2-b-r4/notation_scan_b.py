"""Notation check for slice-b pages: macros used in math vs the registry, registered symbols vs local use."""
import json, re, html, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS4-M2-b")
reg = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
registered_macros = set(reg["macros"].keys())
registered_symbols = [s["symbol"] for s in reg["symbols"]]
STD_OK = {"\\frac", "\\dfrac", "\\tfrac", "\\sum", "\\int", "\\prod", "\\sup", "\\inf", "\\max", "\\min", "\\lim", "\\to",
          "\\le", "\\ge", "\\ne", "\\in", "\\subseteq", "\\subset", "\\cdot", "\\times", "\\pm", "\\circ", "\\mapsto",
          "\\infty", "\\ldots", "\\cdots", "\\qquad", "\\bigl", "\\bigr", "\\left", "\\right", "\\displaystyle", "\\text",
          "\\Delta", "\\delta", "\\eta", "\\varepsilon", "\\xi", "\\varphi", "\\approx", "\\ell", "\\mathcal"}
for L in ["L07", "L08", "L09", "L10", "L11", "L12"]:
    raw = (ROOT / f"course/modules/M/M2/{L}.html").read_text(encoding="utf-8")
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, re.S)
    cmds = set()
    for a, b in maths:
        cmds |= set(re.findall(r"\\[A-Za-z]+", a or b))
    unknown = sorted(c for c in cmds if c not in STD_OK and c not in registered_macros and c not in {"\\R"})
    print(L, "commands used:", len(cmds), "| not standard and not registered:", unknown,
          "| mathbb:", raw.count("mathbb"), "| \\R uses:", raw.count("\\R"))
print("registered symbols (must not take another meaning):", registered_symbols)
for L in ["L07", "L08", "L09", "L10", "L11", "L12"]:
    raw = (ROOT / f"course/modules/M/M2/{L}.html").read_text(encoding="utf-8")
    hits = [s for s in ["\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}", "\\emgamma"] if s in raw]
    print(L, "registered-symbol hits:", hits)
