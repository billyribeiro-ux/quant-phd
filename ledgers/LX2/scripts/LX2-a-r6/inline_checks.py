"""Round-3 checks for LX2 slice a, run as: python3 -I inline_checks.py <repo_root>

1. Concept links (index, L01, L02) resolve to ids in course/concepts.html; local def links resolve.
2. Every claim span on L01 and L02 has a non-empty data-cite, data-locator and data-grade; the cite keys are listed.
3. why-it-matters word counts (BUILDER_RULES 4.2 limit 120).
4. Section numbers the lessons cite, against the list printed at L01 paragraph 'The section numbers in this lesson are'.
5. Process words and banned-era words absent from L01 and L02 text (builder, verifier, round, REQUESTS, fixer).
6. Math macros used on L01 and L02 (every backslash command), against notation/notation.json.
"""

import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
lx = root / "course/modules/LX/LX2"
concepts = (root / "course/concepts.html").read_text(encoding="utf-8")
ids = set(re.findall(r'id="([^"]+)"', concepts))
notation = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(notation["macros"])

for name in ["index", "L01", "L02"]:
    s = (lx / f"{name}.html").read_text(encoding="utf-8")
    links = re.findall(r'href="([^"]*concepts\.html#([^"]+))"', s)
    missing = [a for _, a in links if a not in ids]
    local = re.findall(r'href="#(def-[^"]+)"', s)
    defs = set(re.findall(r'id="(def-[^"]+)"', s))
    print(f"1. {name}: concept links {len(links)}, missing {missing}; local def links {len(local)}, unresolved {[x for x in local if x not in defs]}")

for name in ["L01", "L02"]:
    s = (lx / f"{name}.html").read_text(encoding="utf-8")
    spans = re.findall(r'<span class="claim"([^>]*)>(.*?)</span>', s, flags=re.S)
    bad = 0
    keys: set[str] = set()
    for attrs, _ in spans:
        c = re.search(r'data-cite="([^"]*)"', attrs)
        l = re.search(r'data-locator="([^"]*)"', attrs)
        g = re.search(r'data-grade="([^"]*)"', attrs)
        if not (c and c.group(1).strip() and l and l.group(1).strip() and g):
            bad += 1
        else:
            keys.update(c.group(1).split())
    print(f"2. {name}: claim spans {len(spans)}, without cite/locator/grade {bad}, keys {sorted(keys)}")

for name in ["L01", "L02"]:
    s = (lx / f"{name}.html").read_text(encoding="utf-8")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', s, flags=re.S)
    words = len(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split())
    print(f"3. {name}: why-it-matters words {words} (limit 120)")

s = (lx / "L01.html").read_text(encoding="utf-8")
para = re.search(r"The section numbers in this lesson are (.*?)\.</p>", s, flags=re.S)
print("4. L01 section-number sentence:", html.unescape(para.group(1))[:200] if para else "NOT FOUND")
plain = html.unescape(re.sub(r"<[^>]+>", " ", s))
for sec in ["sections 3 and 4", "section 6(b)", "section 5(b)", "section 12(b)"]:
    print(f"   L01 mentions '{sec}': {sec in plain}")

for name in ["L01", "L02"]:
    s = (lx / f"{name}.html").read_text(encoding="utf-8")
    plain = html.unescape(re.sub(r"<[^>]+>", " ", s))
    hits = [w for w in ["builder", "verifier", "round", "REQUESTS", "fixer"] if re.search(rf"\b{w}\b", plain, flags=re.I)]
    print(f"5. {name}: process words {hits}")

for name in ["L01", "L02"]:
    s = (lx / f"{name}.html").read_text(encoding="utf-8")
    used = sorted(set(re.findall(r"\\([A-Za-z]+)", s)))
    print(f"6. {name}: backslash commands {used}; registered macros among them {[u for u in used if '\\' + u in macros]}")
print("   registered macros:", sorted(macros))
