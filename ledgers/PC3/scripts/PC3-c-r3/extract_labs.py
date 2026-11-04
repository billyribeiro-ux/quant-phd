"""Extract data-run code blocks of the three project labs from project.html and diff them with the twins."""
import html
import re
import sys

PAGE = "course/modules/PC/PC3/project.html"
text = open(PAGE, encoding="utf-8").read()
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-PC3-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
for lab_id, code, expected in blocks:
    code = html.unescape(code)
    expected = html.unescape(expected)
    n = lab_id.rsplit("-", 1)[1]
    twin = open(f"tests/labs/PC3/lab-PC3-project-{n}.py", encoding="utf-8").read()
    page_lines = code.splitlines()
    twin_lines = twin.splitlines()
    diff = [(i + 1, a, b) for i, (a, b) in enumerate(zip(page_lines, twin_lines)) if a != b]
    print(f"{lab_id}: page lines {len(page_lines)}, twin lines {len(twin_lines)}, differing lines (same index) {len(diff)}")
    for d in diff:
        print("  ", d)
    open(f"/tmp/pc3c-r3-{lab_id}-page.py", "w").write(code.rstrip("\n") + "\n")
    open(f"/tmp/pc3c-r3-{lab_id}-expected.txt", "w").write(expected.rstrip("\n") + "\n")
print("labs found:", len(blocks))
