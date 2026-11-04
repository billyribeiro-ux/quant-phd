"""Compare each E4 project lab on project.html with its twin and run the twin under python -I -W error.

Usage: python -I -W error ledgers/E4/scripts/E4-d-r2/cmp_project_labs.py <repo-root>
Prints, per lab: page code == twin (line by line, blanks allowed for the completion lab), the twin's stdout
equals the page's expected block, and the twin's exit status.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    lab_id = f"lab-E4-project-{n}"
    m = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?</section>', page, flags=re.S)
    assert m, lab_id
    section = m.group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', section, flags=re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, flags=re.S).group(1))
    twin = (root / f"tests/labs/E4/lab-E4-project-{n}.py").read_text(encoding="utf-8")
    code_lines = code.rstrip("\n").split("\n")
    twin_lines = twin.rstrip("\n").split("\n")
    if "completion" in section.split(">")[0]:
        diffs = [
            (i, a, b)
            for i, (a, b) in enumerate(zip(code_lines, twin_lines), 1)
            if a != b and "___" not in a
        ]
        print(lab_id, "completion: page lines", len(code_lines), "twin lines", len(twin_lines), "non-blank diffs", diffs)
    else:
        print(lab_id, "page code == twin:", code.rstrip("\n") == twin.rstrip("\n"))
    out = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / f"tests/labs/E4/lab-E4-project-{n}.py")],
        capture_output=True,
        text=True,
        cwd=root,
    )
    print(lab_id, "twin exit", out.returncode, "stderr", repr(out.stderr[:200]))
    print(lab_id, "twin stdout == expected block:", out.stdout.rstrip("\n") == expected.rstrip("\n"))
    if out.stdout.rstrip("\n") != expected.rstrip("\n"):
        print("STDOUT:\n" + out.stdout)
        print("EXPECTED:\n" + expected)
