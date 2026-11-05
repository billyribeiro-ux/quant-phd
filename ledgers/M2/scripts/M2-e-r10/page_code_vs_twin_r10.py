"""Compare each data-run code block of project.html with its twin tests/labs/M2/<lab-id>.py; report differing lines."""
import difflib
import html
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/M/M2/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-M2-project-\d)"[^>]*>(.*?)</section>', page, re.S)
for lab_id, body in blocks:
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    code = html.unescape(m.group(1))
    twin = (root / "tests/labs/M2" / f"{lab_id}.py").read_text(encoding="utf-8")
    a = code.strip().splitlines()
    b = twin.strip().splitlines()
    print(f"{lab_id}: page lines {len(a)}, twin lines {len(b)}, identical after strip: {a == b}")
    for line in difflib.unified_diff(b, a, "twin", "page", lineterm="", n=0):
        if not line.startswith(("---", "+++", "@@")):
            print("   ", line)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    print("   expected block lines:", len(html.unescape(exp.group(1)).strip().splitlines()) if exp else None)
