"""Round-3: diff each FC2 project lab page code against its twin, and check the completion rule for lab 2."""
import difflib
import html
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
text = (ROOT / "course/modules/FC/FC2/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    lab_id = f"lab-FC2-project-{n}"
    sec = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?</section>', text, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python"[^>]*>(.*?)</code>', sec, re.S).group(1))
    twin = (ROOT / f"tests/labs/FC2/{lab_id}.py").read_text(encoding="utf-8")
    print(f"== {lab_id}: page ends {code[-12:]!r}, twin ends {twin[-12:]!r}")
    for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm="", n=0):
        print("  " + line[:200])
    if n == 2:
        bad = [(i + 1, p, t) for i, (p, t) in enumerate(zip(code.splitlines(), twin.splitlines())) if p != t and "___" not in p]
        print("  completion-rule violations (page line != twin line and no blank):", bad)
