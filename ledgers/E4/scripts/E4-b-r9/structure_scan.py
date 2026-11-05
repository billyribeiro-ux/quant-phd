"""Structure, count and prose scans for E4 lessons L04-L06 (BUILDER_RULES 4.2, 5-style minimums, banned strings).

Usage: python3 -I structure_scan.py <checkout-root>
Prints measured values; the verifier compares them with the rules in the ledger rows.
"""

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
SCOPE = ("every", "all", "always", "any", "only", "same", "drives", "exactly", "never", "in general")
BANNED = [
    "TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
    "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
    "obviously", "clearly", "registry", "builder", "verifier", "round", "fragment", "ledger", "twin",
    "architect", "unit report", "REQUEST", "process",
]
for page in ("L04", "L05", "L06"):
    raw = (root / f"course/modules/E/E4/{page}.html").read_text(encoding="utf-8")
    body = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
    body = re.sub(r"<pre.*?</pre>", "", body, flags=re.S)  # code and expected blocks excluded from prose
    prose = html.unescape(re.sub(r"<[^>]+>", " ", body))
    prose = re.sub(r"\\\((.*?)\\\)", " ", prose, flags=re.S)  # drop inline math
    prose = re.sub(r"\\\[(.*?)\\\]", " ", prose, flags=re.S)
    print(f"== {page}")
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
    why_text = html.unescape(re.sub(r"<[^>]+>", "", why.group(1)))
    print("why_it_matters words:", len(why_text.split()))
    sols = re.findall(r'<details class="solution">(.*?)</details>', raw, re.S)
    short = []
    for s in sols:
        t = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"\\\((.*?)\\\)", "x", s, flags=re.S)))
        words = len(re.sub(r"Solution", "", t).split())
        if words < 15:
            short.append(words)
    print("solutions:", len(sols), "shorter_than_15_words:", short)
    tiers = {t: len(re.findall(rf'data-tier="{t}"', raw)) for t in ("mechanics", "proof", "empirical", "research")}
    probs = {t: len(re.findall(r'<div class="problem"', re.search(rf'data-tier="{t}">(.*?)</div>\s*(?=<div class="tier"|</section)', raw, re.S).group(1))) if re.search(rf'data-tier="{t}">', raw) else 0 for t in ("mechanics", "proof", "empirical", "research")}
    print("tiers:", tiers, "problems_per_tier:", probs)
    print("misconceptions:", len(re.findall(r'<li class="misconception">', raw)))
    quiz_items = len(re.findall(r'<li class="item"', raw))
    print("quiz_items:", quiz_items, "explain_blocks:", len(re.findall(r'<div class="explain" hidden>', raw)))
    print("key_result_rows:", len(re.findall(r"<tr><td>", raw)) + len(re.findall(r"<tbody>\s*<tr><td>", raw)))
    print("hours data-hours:", re.search(r'data-hours="(\d+)"', raw).group(1))
    print("footer:", re.search(r'<footer class="site-footer">(.*?)</footer>', raw, re.S).group(1)[:200])
    low = prose.lower()
    for b in BANNED:
        hits = [m.start() for m in re.finditer(re.escape(b.lower()), low)]
        if hits:
            ctx = [prose[max(0, h - 60):h + 60].replace("\n", " ") for h in hits[:3]]
            print(f"BANNED '{b}' hits={len(hits)} ctx={ctx}")
    for w in SCOPE:
        hits = len(re.findall(rf"\b{w}\b", low))
        print(f"scope '{w}': {hits}")
    print("raw \\mathbb:", raw.count("\\mathbb"), " \\indic:", raw.count("\\indic"), " \\mathbf:", raw.count("\\mathbf"))
    print("dfn count:", len(re.findall(r"<dfn", raw)), "dfn with data-concept:", len(re.findall(r"<dfn[^>]*data-concept", raw)))
    print("concept links:", sorted(set(re.findall(r'data-concept="([^"]+)"', raw))))
