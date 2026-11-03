"""Verifier r4: prose/notation scans on L07-L09 and a tie counterexample for the Definition 3.1 match (L08)."""
import re
import sys
from collections import Counter

import numpy as np

ROOT = sys.argv[1]
PAGES = ["course/modules/M/M3/L07.html", "course/modules/M/M3/L08.html", "course/modules/M/M3/L09.html"]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "builder", "verifier", "architect", "round ", " pin ", "Treasury", "data-cite",
          "data-locator", "data-files", "mathbb", "Litterman", "Higham", "Eckart", "Nelson", "Strang", "Axler"]
for p in PAGES:
    text = open(f"{ROOT}/{p}", encoding="utf-8").read()
    hits = {b: len(re.findall(re.escape(b), text, re.I)) for b in BANNED}
    print(p, "banned/attribution hits:", {k: v for k, v in hits.items() if v})
    ell = re.findall(r".{25}(?:…|\.\.\.).{5}", text)
    print(p, "ellipsis occurrences:", len(ell), [e[-30:] for e in ell][:8])
    macros = Counter(re.findall(r"\\([A-Za-z]+)", text))
    print(p, "macros:", sorted(macros))
    print(p, "PSD restated in prose (\"written PSD\"):", len(re.findall(r"written PSD", text)))
    print(p, "dfn ids:", re.findall(r'<dfn id="([^"]+)"', text))

# tie counterexample: distinct eigenvalues, shape equidistant from two principal directions
M = np.diag([3.0, 2.0, 1.0])
lam, V = np.linalg.eigh(M)
order = np.argsort(lam)[::-1]
V = V[:, order]
f = (V[:, 0] + V[:, 1]) / np.sqrt(2.0)
cos = np.abs(V.T @ f)
print("tie check: |cos(v_k, f)| =", np.round(cos, 12), "maximum attained by", np.flatnonzero(np.isclose(cos, cos.max(), rtol=0, atol=1e-12)) + 1)
