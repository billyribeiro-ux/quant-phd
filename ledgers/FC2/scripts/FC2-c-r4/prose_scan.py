"""Round-4 prose, notation and DAG scans for FC2 L07 and L08 (run from the checkout root).

Prints: banned-phrase hits in visible prose; DAG-sensitive terms; TeX control-sequence counts (math notation);
every 'A8' hit with its line; why-it-matters word counts; quiz item and explanation counts; scope-word hits.
"""

from __future__ import annotations

import html
import re
from collections import Counter
from pathlib import Path

PAGES = ["course/modules/FC/FC2/L07.html", "course/modules/FC/FC2/L08.html"]
TWINS = ["tests/labs/FC2/lab-FC2-L07-1.py", "tests/labs/FC2/lab-FC2-L08-1.py"]
CARDS = "course/modules/FC/FC2/cards.json"
BANNED = ["todo", "tbd", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown", "motivational", "verifier", "builder", "ledger", "fragment",
          "fanout", "ruling"]
DAG_TERMS = ["vega", "greek", "option-greeks", "delta hedg", "convexity", "martingale", "brownian", "itô", "ito's",
             "newton", "floating point", "ieee", "root-finding", "bisection", "lognormal", "american"]
SCOPE = ["every", "all ", "always", "never", "only", "exactly", "any ", "same", "each", "whatever", "unique", "none", "must"]

for p in PAGES:
    raw = Path(p).read_text(encoding="utf-8")
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    prose = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<pre.*?</pre>", " ", body, flags=re.S)))
    prose = re.sub(r"\s+", " ", prose).lower()
    print(f"== {p}")
    print("  banned hits:", {b: prose.count(b) for b in BANNED if prose.count(b)} or "none")
    print("  DAG-term hits in visible prose:", {t: prose.count(t) for t in DAG_TERMS if prose.count(t)} or "none")
    print("  scope-word counts (visible prose):", {w.strip(): len(re.findall(r"\b" + re.escape(w.strip()) + r"\b", prose)) for w in SCOPE})
    ctr = Counter(re.findall(r"\\[A-Za-z]+", raw))
    print("  TeX control sequences (count):", dict(ctr.most_common(40)))
    lines = raw.splitlines()
    print("  A8 hits (line):", [i + 1 for i, l in enumerate(lines) if "A8" in l])
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S).group(1)
    print("  why-it-matters words:", len(html.unescape(re.sub(r"<[^>]+>", " ", why)).split()))
    print("  quiz items:", raw.count('class="item"'), " explain divs:", raw.count('class="explain"'))
    print("  misconceptions:", raw.count('class="misconception"'), " solutions:", raw.count('class="solution"'))
for t in TWINS:
    src = Path(t).read_text(encoding="utf-8").lower()
    print(f"== {t}: DAG-term hits:", {w: src.count(w) for w in DAG_TERMS if src.count(w)} or "none")
import json

cards = json.loads(Path(CARDS).read_text(encoding="utf-8"))
blob = " ".join(c["front"] + " " + c["back"] for c in cards if c["lesson"] in ("L07", "L08")).lower()
print("== L07/L08 cards: DAG-term hits:", {w: blob.count(w) for w in DAG_TERMS if blob.count(w)} or "none")
print("== L07/L08 cards with A8:", [c["id"] for c in cards if "A8" in c["front"] + c["back"] and c["lesson"] in ("L07", "L08")])
