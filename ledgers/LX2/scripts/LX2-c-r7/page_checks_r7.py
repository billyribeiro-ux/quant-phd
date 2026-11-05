"""Structural and prose checks on the LX2 project page: hrefs, rubric cells, first use of terms, banned phrases,
registry citations, and the exemplar passages without annotations (for blind scoring)."""
import html
import os
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve() / "course/modules/LX/LX2"
s = (root / "project.html").read_text(encoding="utf-8")
ids = set(re.findall(r'id="([^"]+)"', s))
bad = []
for h in re.findall(r'href="([^"]+)"', s):
    if h.startswith("#"):
        if h[1:] not in ids:
            bad.append(h)
    elif not h.startswith("http"):
        path, _, frag = h.partition("#")
        full = os.path.normpath(root / path)
        if not os.path.exists(full) or (frag and f'id="{frag}"' not in open(full, encoding="utf-8").read()):
            bad.append(h)
print("unresolved hrefs:", bad)
for c, body in re.findall(r'<tr data-criterion="(C\d)">(.*?)</tr>', s, re.S):
    print(c, "th:", len(re.findall(r"<th", body)), "td:", len(re.findall(r"<td>", body)))
text = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)))
for w in ["model owner", "PF-SIM", "outcomes analysis", "realised", "Atlas", "TODO", "TBD", "lorem", "...", "round 6", "builder", "verifier", "REQUEST"]:
    lines = [i for i, l in enumerate(s.split("\n"), 1) if w.lower() in l.lower()]
    print(f"{w!r}: first lines {lines[:4]}")
print("data-cite counts:", sorted(set(re.findall(r'data-cite="([^"]+)"', s))))
print("claim spans:", len(re.findall(r'class="claim"', s)), "data-locator spans:", len(re.findall(r'data-locator=', s)))
for ex in ["exemplar-a", "exemplar-b"]:
    i = s.find(f'id="{ex}"')
    j = s.find("</article>", i)
    body = s[i:j]
    print("=====", ex, "(annotations removed)")
    for m in re.finditer(r'<div class="memo-text">(.*?)</div>\s*<aside', body, re.S):
        print("--", html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1)))).strip())
