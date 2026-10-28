"""Round-8 static scans for AC4-e: assert messages, banned phrases, card duplicates and structure, memo word counts, hunk membership."""
import ast, collections, html, json, re, subprocess
from pathlib import Path
root = Path("/tmp/verify8-AC4-e")
tp = root / "course/modules/AC/AC4/grader/test_project.py"
tree = ast.parse(tp.read_text(encoding="utf-8"))
bare = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert) and n.msg is None]
print("asserts without message:", bare)
page = (root / "course/modules/AC/AC4/project.html").read_text(encoding="utf-8")
cards = json.loads((root / "course/modules/AC/AC4/cards.json").read_text(encoding="utf-8"))
ban = re.compile(r"roughly half|about 6%|historically|\.\.\.|…|\bbuilder\b|\bverifier\b|\bround\b|\bREQUESTS\b|unit report", re.I)
hits = [m.group(0) for m in ban.finditer(re.sub(r"<[^>]+>", " ", page))]
hits += [m.group(0) for c in cards for m in ban.finditer(c["front"] + " " + c["back"])]
print("banned hits:", hits)
print("cards:", len(cards), "ids sequential:", [c["id"] for c in cards] == [f"AC4-c{i:03d}" for i in range(1, len(cards) + 1)])
print("duplicate fronts:", [k for k, v in collections.Counter(c["front"].lower() for c in cards).items() if v > 1],
      "duplicate backs:", [k for k, v in collections.Counter(c["back"] for c in cards).items() if v > 1])
for ex in ("exemplar-a", "exemplar-b"):
    m = re.search(r'<article class="exemplar" id="%s".*?<div class="memo-text">(.*?)</div>' % ex, page, re.S)
    print(ex, "memo words:", len(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split()))
d = subprocess.run(["git", "diff", "-U0", "de53f7e", "2c8162b", "--", "course/modules/AC/AC4/project.html"], cwd=root, capture_output=True, text=True).stdout
print("project.html hunks:", re.findall(r"^@@ -\d+(?:,\d+)? \+(\d+(?:,\d+)?) @@", d, re.M))
for f in ["course/modules/AC/AC4/cards.json", "course/modules/AC/AC4/grader/test_project.py", "references/references.json", "course/modules/AC/AC4/grader/reference.py", "course/modules/AC/AC4/grader/starter.py", "course/modules/AC/AC4/grader/instance.py"]:
    r = subprocess.run(["git", "diff", "--stat", "de53f7e", "2c8162b", "--", f], cwd=root, capture_output=True, text=True).stdout.strip()
    print("changed since de53f7e:", f, "->", "yes" if r else "no")
