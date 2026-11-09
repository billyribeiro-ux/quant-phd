"""Static checks behind fragment rows (round 15, slice c). Run from the checkout root; output to out/static_checks_r15.txt."""
import re
from pathlib import Path

ROOT = Path.cwd()
page = (ROOT / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
lines = page.splitlines()
print("== internal anchors (proj-anchors-links)")
ids = set(re.findall(r'\sid="([^"]+)"', page))
hrefs = re.findall(r'href="#([^"]+)"', page)
print("internal hrefs:", len(hrefs), "unresolved:", sorted({h for h in hrefs if h not in ids}))
print("== process words over page, grader and project labs (proj-banned-and-process-words)")
pat = re.compile(r"\b(round|verif\w*|builder|slice|fixer|ledger|mutant|draft|TODO|blueprint|architect|ruling)\b", re.I)
for f in ["course/modules/BK/BK4/project.html", *sorted(str(p.relative_to(ROOT)) for p in (ROOT / "course/modules/BK/BK4/grader").glob("*.py")), *sorted(str(p.relative_to(ROOT)) for p in (ROOT / "tests/labs/BK4").glob("lab-BK4-project-*.py"))]:
    for n, text in enumerate((ROOT / f).read_text(encoding="utf-8").splitlines(), 1):
        for m in pat.finditer(text):
            print(f"  {f}:{n}: {m.group(0)}")
print("== concept markup on page (proj-dag-concepts)")
print("  data-concept/class=concept hits:", len(re.findall(r'data-concept|class="concept"', page)))
print("== TeX delimiters on page (proj-notation-T)")
print("  \\( hits:", page.count("\\("), "| $ math hits:", len(re.findall(r"(?<![\w$])\$[^$\n]+\$", page)))
print("== vague descriptor words in rubric rows 409-417 (proj-rubric-observable-wording)")
vague = re.compile(r"\b(good|clear|clearly|some|adequate|appropriate|thorough|sufficient|reasonable|various|well|correct|accurate)\b", re.I)
print("  hits:", [m.group(0) for n in range(409, 418) for m in vague.finditer(lines[n - 1])])
print("== docstring or import checks in grader (proj-context-sentences)")
print("  hits:", re.findall(r"__doc__|getdoc|docstring|inspect\.|ast\.parse|sys\.modules", (ROOT / "course/modules/BK/BK4/grader/test_project.py").read_text(encoding="utf-8")))
print("== atlas key in curriculum BK4 block (proj-atlas-studio)")
cur = (ROOT / "curriculum/02-economics-finance-core.yaml").read_text(encoding="utf-8")
start = cur.find("- id: BK4")
end = cur.find("- id: BK5")
print("  BK4 block chars:", end - start, "| 'atlas' hits:", len(re.findall(r"atlas", cur[start:end])), "| 'debate' hits:", len(re.findall(r"debate", cur[start:end])))
