# Round-2 notation scan: every inline and display math expression on L04/L05 against notation/notation.json.
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
reg_syms = [s["symbol"] for s in reg["symbols"]]
macros = list(reg["macros"].keys())
for name in ("L04", "L05"):
    text = (root / f"course/modules/FC/FC1/{name}.html").read_text(encoding="utf-8")
    text = re.sub(r"<pre.*?</pre>", " ", text, flags=re.S)
    exprs = re.findall(r"\\\((.*?)\\\)", text, re.S) + re.findall(r"\\\[(.*?)\\\]", text, re.S)
    tokens = set()
    for e in exprs:
        tokens.update(re.findall(r"\\[A-Za-z]+|[A-Za-z]+(?:_\{?\w+\}?)?", e))
    hits_macro = sorted(m for m in macros if m in tokens)
    hits_sym = []
    for s in reg_syms:
        core = s.split(",")[0].strip().replace("^\\ast", "").replace("\\", "")
        for t in tokens:
            if t.replace("\\", "") in (core, core.replace("gamma_3", "gamma_3")) and core:
                hits_sym.append((s, t))
    print(name, "expressions:", len(exprs), "distinct tokens:", len(tokens))
    print(name, "tokens:", sorted(tokens))
    print(name, "registry macro hits:", hits_macro, "registry symbol hits:", hits_sym)
