"""Round 7 verifier: (1) page lab code equals the twin byte-for-byte after HTML unescape;
(2) the page expected block equals the live output of the twin under python -I -W error;
(3) raw '<' followed by a letter, '/' or digit inside a page's text (HTML tokenizer hazard) is listed."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB7-CS2-c")
PY = str(ROOT / ".venv/bin/python")
pages = {"L09": "course/modules/CS/CS2/L09.html", "L10": "course/modules/CS/CS2/L10.html",
         "L11": "course/modules/CS/CS2/L11.html"}
for lid, rel in pages.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin = (ROOT / f"tests/labs/CS2/lab-CS2-{lid}-1.py").read_text(encoding="utf-8")
    print(lid, "code == twin:", code.rstrip("\n") == twin.rstrip("\n"), "len", len(code), len(twin))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    out = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/CS2/lab-CS2-{lid}-1.py")],
                         capture_output=True, text=True, cwd="/tmp")
    print(lid, "exit", out.returncode, "stderr:", out.stderr.strip()[:200])
    live = out.stdout.rstrip("\n")
    print(lid, "expected == live:", expected.strip() == live.strip())
    # raw '<' hazards: '<' followed by a letter, '/' or '!' outside a recognised tag form
    for ln_no, line in enumerate(text.splitlines(), 1):
        for mm in re.finditer(r"<(?=[A-Za-z/!])", line):
            tag = line[mm.start():mm.start() + 40]
            if not re.match(r"<(/?[a-zA-Z][a-zA-Z0-9-]*)(\s|>|/|$)|<!", tag):
                print(lid, "suspect raw '<' at line", ln_no, repr(tag))
    # all \( \) math spans containing a raw '<' (not \lt)
    for ln_no, line in enumerate(text.splitlines(), 1):
        for mm in re.finditer(r"\\\((.*?)\\\)", line):
            if "<" in mm.group(1):
                print(lid, "math span with raw '<' at line", ln_no, ":", mm.group(0)[:60])
