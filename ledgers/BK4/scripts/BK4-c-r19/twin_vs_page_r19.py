"""Round 19 (BK4 slice c): compare each project lab's page code block with its twin, and its expected block with a fresh run.

Usage: python -I twin_vs_page_r19.py <checkout-root>. The page code is html-unescaped; the twin must equal it exactly
(Rung 2 is the completion case: every page line equals the twin line or contains a blank ___).
"""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
PY = str(ROOT / ".venv/bin/python")
page = (ROOT / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
for lab in ("project-1", "project-2", "project-3"):
    m = re.search(rf'<section class="lab[^"]*" id="lab-BK4-{lab}".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (ROOT / f"tests/labs/BK4/lab-BK4-{lab}.py").read_text(encoding="utf-8")
    same = code == twin
    print(f"{lab}: page code == twin: {same} (page {len(code)} chars, twin {len(twin)} chars)")
    if not same:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
    if lab != "project-2":
        run = subprocess.run([PY, "-I", "-W", "error", "-c", code], capture_output=True, text=True)
        out = run.stdout.rstrip("\n")
        print(f"{lab}: run exit {run.returncode}; output == expected block: {out == expected.rstrip(chr(10))}")
        if out != expected.rstrip("\n"):
            print("   got:", out)
    else:
        print("project-2: completion blanks present:", code.count("___"), "; twin blanks: ", twin.count("___"))
        twin_run = subprocess.run([PY, "-I", "-W", "error", str(ROOT / "tests/labs/BK4/lab-BK4-project-2.py")], capture_output=True, text=True)
        print("project-2 twin output == expected block:", twin_run.stdout.rstrip("\n") == expected.rstrip("\n"))
        print("project-2 twin output:", twin_run.stdout.rstrip("\n").replace("\n", " | "))
    # every page line equals the twin line or contains a blank
    pl, tl = code.splitlines(), twin.splitlines()
    ok = len(pl) == len(tl) and all(a == b or "___" in a for a, b in zip(pl, tl))
    print(f"{lab}: line-by-line equal-or-blank rule: {ok} ({len(pl)} vs {len(tl)} lines)")
