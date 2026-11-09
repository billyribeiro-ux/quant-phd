"""Round 17 static checks on course/modules/E/E4/project.html (run from the checkout root; no network).
Anchors (every href="#x" resolves to an id), banned and process phrases, scope words (counts per word), absence of
figure and dataset elements, notation collisions with notation/notation.json, and the hours sum (components of the
time table). Prints one line per check."""
import json
import re
from pathlib import Path

root = Path(".").resolve()
page = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
ids = set(re.findall(r'\sid="([^"]+)"', page))
hrefs = set(re.findall(r'href="#([^"]+)"', page))
print("anchors: hrefs", len(hrefs), "missing", sorted(h for h in hrefs if h not in ids))
banned = ["for brevity", "beyond the scope", "details omitted", "TODO", "TBD", "lorem", "left as an exercise",
          "you can add more", "it is important to note", "obviously", "clearly", "well known", "experts agree",
          "studies show", "it can be shown", "roughly", "historically", "…"]
print("banned hits:", [b for b in banned if b.lower() in page.lower()])
process = ["builder", "verifier", "ruling", "architect", "ledger", "fragment", "batch", "slice", "the agent"]
print("process-word hits:", [p for p in process if re.search(r"\b" + re.escape(p), page, flags=re.I)])
text = re.sub(r"<[^>]+>", " ", page)
for w in ["only", "all", "always", "every", "any", "same", "drives", "exactly"]:
    print(f"scope '{w}' count in tag-stripped text:", len(re.findall(rf"\b{w}\b", text, flags=re.I)))
print("figure/svg/img/data-files elements:", len(re.findall(r"<svg|<img|<figure|data-files", page)))
nota = json.load(open(root / "notation/notation.json", encoding="utf-8"))
entries = [x["symbol"] for x in nota["symbols"]]
print("notation symbols:", entries)
hits = {e: page.count(e) for e in ["\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "\\mathbb{Q}"]}
print("page hits for registry symbols that are not the correlation:", hits)
hours = [1, 1, 5, 8, 5, 5, 3]
print("time table components sum:", sum(hours), "| data-hours-project 28 present:", 'data-hours-project="28"' in page)

macros = set(nota["macros"].keys())
used = set(re.findall(r"\\([A-Za-z]+)", page))
print("registry macros used on the page:", sorted(u for u in used if "\\" + u in macros))
print("custom-looking commands used that are not in the registry (standard LaTeX expected):",
      sorted(u for u in used if "\\" + u not in macros and u[0].isupper()))
