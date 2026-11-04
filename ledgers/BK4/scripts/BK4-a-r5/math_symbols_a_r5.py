"""List the TeX symbols in every math span of the four slice pages, and check the registered symbols and macros."""
import html, re, sys
from collections import Counter
from pathlib import Path
root = Path(sys.argv[1])
pages = [root / f"course/modules/BK/BK4/{p}.html" for p in ("index", "L01", "L02", "L03")]
spans = []
for p in pages:
    src = p.read_text(encoding="utf-8")
    text = html.unescape(src)
    found = re.findall(r"\\\((.*?)\\\)", text, re.S) + re.findall(r"\\\[(.*?)\\\]", text, re.S)
    spans += [(p.name, f) for f in found]
cmds = Counter()
for _, f in spans:
    for c in re.findall(r"\\[A-Za-z]+", f):
        cmds[c] += 1
print("math spans:", len(spans))
print("commands:", dict(cmds))
registered = ["T", "\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}", "\\mathbb{R}", "\\mathbb{E}", "\\mathbb{P}"]
for r in registered:
    hits = [(n, f[:90]) for n, f in spans if r in f]
    print("registered", repr(r), "hits:", len(hits), hits[:3])
bare_T = [(n, f[:90]) for n, f in spans if re.search(r"(?<![A-Za-z\\])T(?![A-Za-z])", f)]
print("bare T in math:", bare_T[:5])
