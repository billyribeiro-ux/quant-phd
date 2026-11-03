"""Round-3 verifier (E3-d): scan the E3 project page and grader for curriculum concept names owned outside the closure.

Closure of E3 = {E1, M1, M2, M4, P0.1} plus E3's own concepts. Each concept's name and id (hyphen or space variants)
is searched in project.html (visible text) and in grader/*.py (learner-visible source). Run from the repository root:
    .venv/bin/python -B ledgers/E3/scripts/E3-d-r3/concept_scan_r3.py
"""
import html
import json
import re

concepts = json.load(open("curriculum/curriculum.json", encoding="utf-8"))["concepts"]
allowed = {"E1", "M1", "M2", "M4", "P0.1", "E3"}
page = open("course/modules/E/E3/project.html", encoding="utf-8").read()
visible = html.unescape(re.sub(r"<script.*?</script>|<[^>]+>", " ", page, flags=re.S))
texts = {"project.html": visible}
for name in ("test_project.py", "reference.py", "instance.py", "starter.py"):
    texts[name] = open(f"course/modules/E/E3/grader/{name}", encoding="utf-8").read()
hits = []
for cid, meta in sorted(concepts.items()):
    if meta.get("module") in allowed:
        continue
    for variant in {cid, meta.get("name", "")}:
        variant = variant.lower().strip()
        if len(variant) < 5:
            continue
        pattern = re.compile(r"\b" + re.escape(variant).replace(r"\-", "[- ]").replace(r"\ ", "[- ]") + r"s?\b")
        for fname, text in texts.items():
            for m in pattern.finditer(text.lower()):
                hits.append((cid, meta.get("module"), fname, text[max(0, m.start() - 40): m.end() + 20].replace("\n", " ")))
for hit in hits:
    print(hit)
print("concept hits outside the closure:", len(hits))
