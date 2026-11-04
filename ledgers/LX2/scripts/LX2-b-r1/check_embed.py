"""Compare each lab section of a lesson page with its twin and with the twin's printed output.

Usage: python -I check_embed.py <page.html> <twin.py> <lab-id>
Prints the code comparison, the expected-block comparison and the first differing line, if any.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

page_path, twin_path, lab_id = sys.argv[1], sys.argv[2], sys.argv[3]
page = Path(page_path).read_text(encoding="utf-8")
section = re.search(r'<section class="lab" id="%s".*?</section>' % re.escape(lab_id), page, re.S)
if section is None:
    raise SystemExit(f"no section {lab_id}")
body = section.group(0)
code = re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S).group(1)
expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1)
code_text = html.unescape(code)
expected_text = html.unescape(expected)
twin_text = Path(twin_path).read_text(encoding="utf-8")
same = code_text.rstrip("\n") == twin_text.rstrip("\n")
print("code equals twin (final newline ignored):", same, "| code chars", len(code_text), "| twin chars", len(twin_text))
if not same:
    a, b = code_text.splitlines(), twin_text.splitlines()
    for i, (x, y) in enumerate(zip(a, b), 1):
        if x != y:
            print("first differing line", i, repr(x), repr(y))
            break
    else:
        print("length differs", len(a), len(b))
run = subprocess.run(
    [sys.executable, "-I", "-W", "error", twin_path], capture_output=True, text=True, check=False
)
print("twin exit", run.returncode, "stderr bytes", len(run.stderr))
print("expected equals printed output:", expected_text.rstrip("\n") == run.stdout.rstrip("\n"))
