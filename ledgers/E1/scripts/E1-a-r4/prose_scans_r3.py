"""Scans of learner text for slice a (hub, L01-L03): banned phrases, process words, scope words, out-of-closure names."""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) / "course/modules/E/E1"
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "...", "…"]
PROCESS = ["verif", "builder", "build ", "round ", "planner", "REQUEST", "unit report", "verifier", "orchestr", "Architect"]
OUT_OF_CLOSURE = ["Lagrang", "KKT", "Kuhn", "convex", "Nash", "expected utility", "welfare theorem", "Cournot",
                  "Bertrand", "monopol", "Pareto", "Lerner", "externalit", "public good", "surplus", "elasticit",
                  "Edgeworth", "Pigou", "arrow", "Arrow-Debreu", "Coase"]
SCOPE = r"\b(every|all|never|always|any|only|exactly|none|no one|each)\b"
for page in PAGES:
    raw = (ROOT / page).read_text(encoding="utf-8")
    text = re.sub(r"<pre><code.*?</code></pre>", " ", raw, flags=re.S)  # code blocks excluded from prose scans
    plain = re.sub(r"<[^>]+>", " ", text)
    print(f"== {page}")
    for w in BANNED:
        hits = [m.start() for m in re.finditer(re.escape(w), plain, flags=re.I)]
        if hits:
            print(f"  banned {w!r}: {len(hits)} hit(s)")
    for w in PROCESS:
        for m in re.finditer(re.escape(w), plain, flags=re.I):
            print(f"  process {w!r}: ...{plain[max(0,m.start()-60):m.end()+60]!r}")
    for w in OUT_OF_CLOSURE:
        for m in re.finditer(re.escape(w), plain, flags=re.I):
            print(f"  closure {w!r}: ...{plain[max(0,m.start()-60):m.end()+60]!r}")
    n = 0
    for m in re.finditer(SCOPE, plain, flags=re.I):
        n += 1
        print(f"  scope {m.group(0)!r}: ...{' '.join(plain[max(0,m.start()-70):m.end()+50].split())!r}")
    print(f"  scope-word hits: {n}")
