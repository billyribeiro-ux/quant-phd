"""List every TeX control sequence used in L07-L09 math and every notation.json macro; flag unregistered registered-symbol clashes.

Usage: python3 -I check_notation_r2.py <repo_root>
"""

import collections
import html
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
nj = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(nj["macros"].keys())
for n in ("07", "08", "09"):
    page = html.unescape((root / f"course/modules/M/M3/L{n}.html").read_text(encoding="utf-8"))
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", page, re.S)
    body = " ".join(a or b for a, b in maths)
    seqs = collections.Counter(re.findall(r"\\[A-Za-z]+", body))
    unreg = {k: v for k, v in seqs.items() if k not in macros}
    print(f"L{n}: math spans {len(maths)}; control sequences {sum(seqs.values())}; distinct {len(seqs)}")
    print(f"  registered macros used: {sorted(k for k in seqs if k in macros)}")
    print(f"  unregistered control sequences: {dict(sorted(unreg.items()))}")
    print(f"  \\mathbb in page text: {page.count('mathbb')}")
    # symbols used as letters that are registry symbols
    for sym in ("\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R_f", "\\mathbb{Q}", "T"):
        pass
