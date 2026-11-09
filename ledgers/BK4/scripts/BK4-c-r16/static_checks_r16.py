"""Round-16 static checks on the BK4 project page (slice c): internal anchors, banned process words, TeX math,
concept markup, and that the three changed sentences of the round-15 batch are present. Run from the checkout root.
"""

import re
from pathlib import Path

page = Path("course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
ids = set(re.findall(r'\bid="([^"]+)"', page))
hrefs = re.findall(r'href="#([^"]+)"', page)
unresolved = sorted({h for h in hrefs if h not in ids})
print(f"internal href targets: {len(hrefs)} distinct {len(set(hrefs))} unresolved {unresolved}")
files = [page] + [p.read_text(encoding="utf-8") for p in Path("course/modules/BK/BK4/grader").glob("*.py")]
files += [p.read_text(encoding="utf-8") for p in Path("tests/labs/BK4").glob("lab-BK4-project-*.py")]
words = r"\b(round|verif\w*|builder|slice|fixer|ledger|mutant\w*|draft|TODO|blueprint|architect|ruling)\b"
hits = [m.group(0) for f in files for m in re.finditer(words, f, flags=re.I)]
print("process-word hits:", hits)
print("TeX math delimiters in page:", len(re.findall(r"\\\(|\\\[|\$\$", page)))
print("concept markup in page (data-concept or class=\"concept\"):", len(re.findall(r'data-concept=|class="concept"', page)))
for needle in ("Rung 2 · Completion problem</span><p>Lab 2 below: the same default with two blanks, the survivor share and the sizing index (both defined under",
               "The sizing index (defined under <a href=\"#conventions\">Conventions</a>) is 38.2",
               "so a failure shows only the test's own message, which names the property"):
    print("present:", needle[:60], "->", needle in page)
print("sizing-index definition in Conventions present:", "The sizing index is an exact fraction rounded up" in page)
print("order statistic defined in Conventions:", 'id="conventions"' in page and "<strong>Sizing.</strong>" in page)
