import re, sys, pathlib, json
root = pathlib.Path(sys.argv[1]) / "course/modules/FC/FC2"
files = [root / "project.html", root / "cards.json", *sorted((root / "grader").glob("*.py")),
         *[pathlib.Path(sys.argv[1]) / f"tests/labs/FC2/{n}" for n in ("lab-FC2-project-1.py", "lab-FC2-project-2.py", "lab-FC2-project-3.py")]]
pats = [r"\bTODO\b", r"\bTBD\b", r"lorem", r"\.\.\.|…", r"for brevity", r"details omitted", r"beyond the scope",
        r"left as an exercise", r"you can add more", r"it is important to note", r"studies show", r"experts agree",
        r"it is well known", r"\bobviously\b", r"\bclearly\b", r"it can be shown", r"roughly", r"historically",
        r"\bAbout \d+%", r"\bround \d\b", r"\bRound \d\b", r"\bverifier\b", r"\bbuilder\b", r"\bfragment\b",
        r"\bledger\b", r"\bpin\b", r"\baudit\b", r"\bprevious draft\b", r"\bearlier\b", r"\bfixed in\b", r"\bR[0-9]\b"]
hits = []
for f in files:
    text = f.read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines(), 1):
        for p in pats:
            for m in re.finditer(p, line):
                hits.append((str(f.relative_to(sys.argv[1])), i, p, line.strip()[:160]))
print("files scanned:", len(files))
for h in hits:
    print(h)
print("hits:", len(hits))
