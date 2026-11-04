"""Compare each slice lab's page code and expected block with its twin and twin output (SC1-b round 6)."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE6-SC1-b")
OUT = ROOT / "ledgers/SC1/scripts/SC1-b-r6/out"
for lab in ("L04", "L05", "L06"):
    page = (ROOT / f"course/modules/SC/SC1/{lab}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    expected = re.search(r'<pre class="expected" data-tolerance="([^"]+)">(.*?)</pre>', page, re.S)
    page_code = html.unescape(code.group(1))
    twin = (ROOT / f"tests/labs/SC1/lab-SC1-{lab}-1.py").read_text(encoding="utf-8")
    same = page_code.rstrip("\n") == twin.rstrip("\n")
    exp_text = html.unescape(expected.group(2))
    stdout = (OUT / f"twin_{lab}.out").read_text(encoding="utf-8")
    stdout_body = "\n".join(l for l in stdout.splitlines() if not l.startswith(("$", "exit=")))
    print(lab, "page code == twin:", same, "| tolerance:", expected.group(1))
    print(lab, "expected == twin stdout (exact):", exp_text.rstrip("\n") == stdout_body.rstrip("\n"))
    print(lab, "page code lines:", page_code.count("\n"), "twin lines:", twin.count("\n"))
    print(lab, "code has 'import' lines:", [l for l in page_code.splitlines() if l.startswith(("import", "from"))])
