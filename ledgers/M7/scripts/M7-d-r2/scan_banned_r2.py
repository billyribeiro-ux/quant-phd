"""Round-2 scan of project.html learner text for BUILDER_RULES 1.3-1.4 banned strings and process words."""
import re, pathlib
s = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD2-M7-d/course/modules/M/M7/project.html").read_text(encoding="utf-8")
banned = [r"TODO", r"TBD", r"lorem", r"\.\.\.", r"…", r"for brevity", r"details omitted", r"beyond the scope",
          r"left as an exercise", r"you can add more", r"it is important to note", r"studies show", r"experts agree",
          r"it is well known", r"obviously", r"clearly", r"about \d", r"roughly", r"historically", r"in summary"]
process = [r"verifier", r"builder", r"ledger", r"fragment", r"round \d", r"checked for this page", r"was checked",
           r"reference solution", r"reference's output", r"the reference\b"]
for label, pats in (("banned", banned), ("process", process)):
    for p in pats:
        for m in re.finditer(p, s, flags=re.IGNORECASE):
            a = max(0, m.start() - 60)
            print(label, repr(p), "::", re.sub(r"\s+", " ", s[a:m.end() + 40]))
print("scan complete")
