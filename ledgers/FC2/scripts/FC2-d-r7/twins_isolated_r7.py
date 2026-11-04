"""Run each FC2 project lab twin alone, in an empty temp directory, under python -I -W error.

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r5/twins_isolated.py <repo_root>
Also compares each twin's stdout with the expected block of its page (course/modules/FC/FC2/project.html).
"""

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

root = sys.argv[1]
page = open(os.path.join(root, "course", "modules", "FC", "FC2", "project.html"), encoding="utf-8").read()
labs = {
    "lab-FC2-project-1": "lab-FC2-project-1.py",
    "lab-FC2-project-2": "lab-FC2-project-2.py",
    "lab-FC2-project-3": "lab-FC2-project-3.py",
}
for lab_id, twin in labs.items():
    src = os.path.join(root, "tests", "labs", "FC2", twin)
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(src, os.path.join(tmp, twin))
        out = subprocess.run(
            [os.path.join(root, ".venv", "bin", "python"), "-I", "-W", "error", twin],
            cwd=tmp, capture_output=True, text=True,
        )
    print(lab_id, "twin rc", out.returncode, "stderr_bytes", len(out.stderr.encode()))
    # the expected block that follows this lab's code block in the page
    start = page.index(f'id="{lab_id}"')
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page[start:], re.S)
    expected = html.unescape(m.group(1))
    print(lab_id, "expected block equals twin stdout:", expected.rstrip("\n") == out.stdout.rstrip("\n"))
    # the code block of the page equals the twin source
    cm = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page[start:], re.S)
    code = html.unescape(cm.group(1))
    src_text = open(src, encoding="utf-8").read()
    print(lab_id, "page code equals twin (after stripping trailing newline):", code.rstrip("\n") == src_text.rstrip("\n"))
