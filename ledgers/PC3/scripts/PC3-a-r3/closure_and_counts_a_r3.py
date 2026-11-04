"""Round-3 PC3 slice a: (1) prerequisite closure of PC3 from tools/coursekit.py, (2) P0.1 entries read 'not yet released',
(3) data-files attributes on PC3 lab sections, (4) problem and quiz counts per lesson, (5) 'Theorem 3.10' and 'adapted' absent.
Run as: .venv/bin/python -I <this file> <checkout-root>
"""

import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tools"))
import coursekit  # noqa: E402

closure = coursekit.prerequisite_closure("PC3")
print("closure:", sorted(closure))
concepts = (root / "course/concepts.html").read_text(encoding="utf-8")
start = concepts.index('id="c-P0.1"')
end = concepts.index("</section>", start)
block = concepts[start:end]
entries = re.findall(r"<li id=\"[^\"]+\">.*?</li>", block)
print("P0.1 entries:", len(entries), "not yet released:", sum("not yet released" in e for e in entries))
for p in ("index", "L01", "L02", "L03"):
    t = (root / "course/modules/PC/PC3" / f"{p}.html").read_text(encoding="utf-8")
    print(p, "data-files:", len(re.findall(r"data-files", t)), "Theorem 3.10:", "Theorem 3.10" in t, "adapted:", "adapted" in t)
    if p != "index":
        print(p, "problems with solution:", len(re.findall(r'<details class="solution">', t)),
              "quiz items:", len(re.findall(r'<li class="item"', t)),
              "misconceptions:", len(re.findall(r'<li class="misconception">', t)))
