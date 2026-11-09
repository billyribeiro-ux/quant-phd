"""Blind-scoring extract for the LX1 project exemplars (round 14). Argument 1 is the checkout root.
Writes the two exemplar essays with the annotations (<aside>), the official scoring (<p class="exemplar-verdict">),
the data-level and data-scores attributes, and the labels removed, so a scorer sees only the essay text and the rubric
table (project.html rubric section, which is printed separately by the scorer)."""
import pathlib, re, sys
root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
out = []
for ex in ("exemplar-a", "exemplar-b"):
    m = re.search(r'<article class="exemplar" id="%s".*?</article>' % ex, page, re.S)
    body = m.group(0)
    body = re.sub(r'<aside class="annotation".*?</aside>', "", body, flags=re.S)
    body = re.sub(r'<p class="exemplar-verdict".*?</p>', "", body, flags=re.S)
    body = re.sub(r'<h4 id="[^"]*">.*?</h4>', "", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"[ \t]+", " ", body)
    body = "\n".join(l.strip() for l in body.splitlines() if l.strip())
    out.append(f"=== {ex} (essay text only) ===\n{body}\n")
print("\n".join(out))
