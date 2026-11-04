"""Scan the visible prose of L22-L24 (scripts and expected blocks removed) for banned phrases, process words,
scope words, later-module concept names, and the Lagrange-multiplier/Fubini/Riemann/Lebesgue/epsilon-delta names."""
import html
import re
import sys
from pathlib import Path

base = Path(sys.argv[1]) / "course/modules/M/M2"
banned = r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|important to note|studies show|experts agree|well known|obviously|clearly|it can be shown"
process = r"\b(round \d|builder|verifier|architect|fixed|revised|previous version|Round|Builder|Verifier|Architect)\b"
later = r"Lagrange multiplier|Lagrangian|Fubini|Riemann-Stieltjes|Lebesgue|epsilon-delta|linear map|vector space|positive-semidefinite"
scope = r"\b(only|all|always|every|any|same|exactly|most|small|about|never|drives)\b"
for page in ("L22.html", "L23.html", "L24.html"):
    s = (base / page).read_text(encoding="utf-8")
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<pre><code.*?</code></pre>", " ", s, flags=re.S)
    s = re.sub(r'<pre class="expected".*?</pre>', " ", s, flags=re.S)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = re.sub(r"\\\(|\\\)|\\\[|\\\]", " ", s)
    s = re.sub(r"[ \t]+", " ", s)
    counts = {}
    for name, pat in (("banned", banned), ("process", process), ("later-module", later), ("ellipsis", r"\.\.\.|…"), ("scope", scope)):
        hits = [m.group(0) for m in re.finditer(pat, s, flags=re.I)]
        counts[name] = len(hits)
        if name in ("banned", "process", "later-module", "ellipsis"):
            print(page, name, "hits:", hits)
    print(page, "scope-word count (each checked in context by the verifier):", counts["scope"])
