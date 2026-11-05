"""Scan M2 cards.json, project.html text and grader/test_project.py messages for banned strings (BUILDER_RULES 1.3-1.4) and process words."""
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1]); m2 = root / "course/modules/M/M2"
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise", "you can add more",
          "it is important to note", "studies show", "experts agree", "it is well known", "obviously", "clearly",
          "it can be shown", "roughly", "historically", "about 6%", "...", "…"]
process = ["verifier", "verification", "builder", "fragment", "round ", "reviewer", "revised", "corrected", "fixed in",
           "previous version", "ledger", "auditor", "the fix", "we changed", "updated"]
cards = json.loads((m2 / "cards.json").read_text(encoding="utf-8"))
texts = {"cards.json": "\n".join(c["front"] + "\n" + c["back"] + "\n" + c.get("basis", "") for c in cards)}
raw = (m2 / "project.html").read_text(encoding="utf-8")
import html
texts["project.html"] = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)))
texts["test_project.py"] = (m2 / "grader/test_project.py").read_text(encoding="utf-8")
texts["instance.py"] = (m2 / "grader/instance.py").read_text(encoding="utf-8")
for name, t in texts.items():
    low = t.lower()
    for b in banned:
        for m in re.finditer(re.escape(b.lower()), low):
            print("BANNED", name, repr(b), "...", re.sub(r"\s+", " ", t[max(0, m.start() - 60):m.start() + 60]))
    for p in process:
        for m in re.finditer(re.escape(p), low):
            print("PROCESS?", name, repr(p), "...", re.sub(r"\s+", " ", t[max(0, m.start() - 60):m.start() + 60]))
print("scan done")
