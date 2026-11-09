"""Round-4 independent text checks for FC2 L04-L06 (visible text, math tokens, word counts, banned phrases)."""
import html
import json
import re
from pathlib import Path

PAGES = ["L04", "L05", "L06"]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown that", "builder", "verifier", "round", "agent", "reviewer",
          "planner", "architect", "orchestrat", "mutant", "ellipsis", "…"]
SCOPE = ["every", "all ", "never", "any", "always", "only", "exactly", "same", "drives"]

def visible(text: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)

for p in PAGES:
    raw = Path(f"course/modules/FC/FC2/{p}.html").read_text(encoding="utf-8")
    # visible text without lab code blocks and expected blocks (student-facing prose only)
    prose = re.sub(r'<section class="lab".*?</section>', " ", raw, flags=re.S)
    vis = visible(prose)
    print(f"== {p}")
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S).group(1)
    print(f"why-it-matters words: {len(visible(why).split())}")
    low = vis.lower()
    for b in BANNED:
        n = low.count(b.lower())
        if n:
            idx = [m.start() for m in re.finditer(re.escape(b.lower()), low)][:5]
            print(f"  banned/process '{b}': {n} hits; contexts: {[low[max(0,i-60):i+40].replace(chr(10),' ') for i in idx]}")
    for s in SCOPE:
        print(f"  scope '{s.strip()}': {len(re.findall(r'\\b' + re.escape(s.strip()) + r'\\b', low))}", end=";")
    print()
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, re.S)
    toks = sorted({m for pair in maths for m in pair if m})
    cmds = sorted(set(re.findall(r"\\[A-Za-z]+", " ".join(toks))))
    print(f"  math spans: {len(toks)}; macros used: {cmds}")
    print(f"  raw \\mathbb uses: {len(re.findall(r'mathbb', raw))}; \\E macro uses: {len(re.findall(r'\\\\E(?![a-zA-Z])', raw))}")
