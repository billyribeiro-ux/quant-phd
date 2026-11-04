"""Round-3 PC3 slice a: targeted checks (P0.1 concept ids unused; D1-D9 terms absent; no rhetorical question in
prose; twins read no file; every data-concept id in the slice resolves to a concept in concepts.html).
Run as: .venv/bin/python -I <this file> <checkout-root>
"""

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
pages = [root / "course/modules/PC/PC3" / f"{p}.html" for p in ("index", "L01", "L02", "L03")]
twins = [root / "tests/labs/PC3" / f"lab-PC3-{p}-1.py" for p in ("L01", "L02", "L03")]
concepts = (root / "course/concepts.html").read_text(encoding="utf-8")
start = concepts.index('id="c-P0.1"')
end = concepts.index('</section>', start)
p01_ids = re.findall(r'<li id="([^"]+)"', concepts[start:end])
print("P0.1 concept ids in concepts.html:", len(p01_ids), p01_ids)
used = set()
slice_ids = set()
for f in pages:
    t = f.read_text(encoding="utf-8")
    slice_ids |= set(re.findall(r'data-concept="([^"]+)"', t))
    used |= set(re.findall(r'data-concept="([^"]+)"', t)) & set(p01_ids)
    prose = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<pre.*?</pre>", "", t, flags=re.S)))
    terms = re.findall(r"\b(martingale|Kelly|Poisson|Markov|bayesian inference|adverse selection|winner'?s curse|duration|CAPM|Black[- ]Scholes|binomial distribution)\b", prose, re.I)
    print(f.name, "D-term hits:", terms)
    qs = [s.strip()[:120] for s in re.split(r"(?<=[.!?])\s+", prose) if s.strip().endswith("?")]
    print(f.name, "question sentences in prose:", len(qs), qs[:3])
print("P0.1 concept ids used in slice:", sorted(used))
missing = [c for c in sorted(slice_ids) if f'id="{c}"' not in concepts]
print("data-concept ids in slice not found in concepts.html:", missing)
for tw in twins:
    src = tw.read_text(encoding="utf-8")
    print(tw.name, "opens files:", bool(re.search(r"\bopen\(|Path\(|read_text|read_csv", src)))
