"""Round-2: list every TeX command and every bare-letter/subscript symbol used in L08-L10 math, against notation/notation.json."""
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
reg = json.load(open(ROOT / "notation/notation.json", encoding="utf-8"))
macros = set(reg["macros"])
syms = [s["symbol"] for s in reg["symbols"]]
print("registered macros:", sorted(macros))
print("registered symbols:", syms)
for lid in ("L08", "L09", "L10"):
    page = (ROOT / f"course/modules/M/M5/{lid}.html").read_text(encoding="utf-8")
    page = re.sub(r'<pre class="expected".*?</pre>', "", page, flags=re.S)
    page = re.sub(r'<pre><code class="language-python".*?</code></pre>', "", page, flags=re.S)
    segs = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", page, flags=re.S)
    math = [a or b for a, b in segs]
    cmds = collections.Counter()
    for m in math:
        for c in re.findall(r"\\([A-Za-z]+)", m):
            cmds[c] += 1
    print(f"== {lid}: {len(math)} math segments; commands:", dict(cmds))
    letters = collections.Counter()
    for m in math:
        s = re.sub(r"\\[A-Za-z]+", " ", m)
        for c in re.findall(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", s):
            letters[c] += 1
    print(f"   single letters:", dict(sorted(letters.items())))
    for name in ("\\mathbb", "\\Phi", "\\gamma_3", "\\gamma_4", "\\Prob", "\\E", "\\N", "\\norm", "T", "R_f", "\\ast"):
        hits = [m for m in math if name in m]
        if hits:
            print(f"   uses {name}: {len(hits)} segments; e.g. {hits[0][:90]!r}")
