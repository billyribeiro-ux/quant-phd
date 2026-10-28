import sys, pathlib
from collections import Counter
ROOT = pathlib.Path("/tmp/verify42-AC4-e")
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import load_page
page = load_page(ROOT / "course/modules/AC/AC4/project.html")
rubric = page.dom.first("table", "rubric")
criteria = [row.get("data-criterion") for row in rubric.select("tr", None, data_criterion=None)]
print("criteria", criteria, "rubric rows", len(rubric.select("tr")) - 1)
for ex in page.dom.select(None, "exemplar"):
    name = ex.get("id")
    scores = [int(x) for x in ex.get("data-scores").split(",")]
    print(name, "data-level", ex.get("data-level"), "most common", Counter(scores).most_common(1)[0][0], "scores", scores)
    notes = ex.select("li", None, data_criterion=None)
    for criterion, score in zip(criteria, scores, strict=True):
        mine = [n for n in notes if n.get("data-criterion") == criterion]
        meets = [int(n.get("data-level")) for n in mine if "meets" in n.classes]
        misses = [int(n.get("data-level")) for n in mine if "misses" in n.classes]
        reached = max(meets, default=1)
        ok = reached == score and all(m > score for m in misses)
        print("  ", criterion, "meets", meets, "misses", misses, "score", score, "OK" if ok else "MISMATCH")
