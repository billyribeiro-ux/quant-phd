"""Round-13 BK4-c prose and link scans of the project page and the grader/lab files. Run from the checkout root:
python3 -I ledgers/BK4/scripts/BK4-c-r13/prose_scans_r13.py
"""

import html
import os
import re
import sys

ROOT = os.getcwd()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import coursekit as ck  # noqa: E402

PAGE = os.path.join(ROOT, "course/modules/BK/BK4/project.html")
text = open(PAGE, encoding="utf-8").read()

# 1. anchors and local links
os.chdir(os.path.dirname(PAGE))
ids = set(re.findall(r'\sid="([^"]+)"', text))
bad = []
hrefs = re.findall(r'href="([^"]+)"', text)
for h in hrefs:
    if h.startswith("#"):
        if h[1:] not in ids:
            bad.append(h)
    elif not h.startswith("http"):
        if not os.path.exists(os.path.normpath(h.split("#")[0])):
            bad.append(h)
print("links: hrefs", len(hrefs), "anchors", sum(1 for h in hrefs if h.startswith("#")), "broken", bad)
os.chdir(ROOT)

# 2. concept names: curriculum concept names found in the page's visible text, with owner and closure membership
c = ck.curriculum()
closure = set(ck.prerequisite_closure("BK4")) | {"BK4"}
prose = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text, flags=re.S)
prose = html.unescape(re.sub(r"<[^>]+>", " ", prose)).lower()
prose = re.sub(r"\s+", " ", prose)
hits = []
for cid, meta in c["concepts"].items():
    name = re.sub(r"\s*\(.*?\)", "", meta["name"].lower()).strip()
    if len(name) >= 6 and re.search(r"(?<![a-z])" + re.escape(name) + r"(?![a-z])", prose):
        hits.append((cid, meta["module"], meta["module"] in closure))
print("concept-name hits on the page:", sorted(hits))
print("concept links (class=concept or data-concept) on the page:", len(re.findall(r'data-concept', text)))

# 3. process words in learner-facing text and in grader/lab code
files = [PAGE] + [os.path.join(ROOT, "course/modules/BK/BK4/grader", n)
                  for n in ("instance.py", "reference.py", "starter.py", "test_project.py")] + [
    os.path.join(ROOT, f"tests/labs/BK4/lab-BK4-project-{i}.py") for i in (1, 2, 3)]
pat = re.compile(r"(verifier|builder|architect|ledger|fixer|batch|planner|slice|\bround \d+|TODO|FIXME|placeholder|lorem|"
                 r"we will|obviously|clearly|simply)", re.I)
pw = [(os.path.relpath(f, ROOT), i) for f in files for i, line in enumerate(open(f, encoding="utf-8"), 1)
      if pat.search(line)]
print("process-word hits:", pw)

# 4. scope words in project-page prose (code blocks removed); counted, each justified in the fragment notes
prose_html = re.sub(r"<pre.*?</pre>", "", text, flags=re.S)
scope = re.findall(r"\b(only|always|every|all|any|same|exactly|drives|never|none)\b", prose_html, flags=re.I)
print("scope-word hits in prose:", len(scope))

# 5. period convention (architect ruling 3): no sentence on the page about a period convention
print("period-convention hits (other than close-out period):",
      [m.start() for m in re.finditer(r"period", text) if "close-out" not in text[m.start() - 12:m.start()]])

# 6. registered notation symbols on the page (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q)
print("math delimiters on page:", len(re.findall(r"\\\(|\\\[", text)),
      "| registered symbols present:", [s for s in ["R^", "R_f", "\\Phi", "\\gamma", "\\mathbb{Q}"] if s in text])
