"""Compare each L07/L08 page's lab code block with its twin, and each expected block with the twin's stdout."""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
for lid in ("L07", "L08"):
    page = (root / f"course/modules/M/M7/{lid}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/M7/lab-M7-{lid}-1.py").read_text(encoding="utf-8")
    stdout = (root / f"ledgers/M7/scripts/M7-c-r3/twin_{lid}.stdout").read_text(encoding="utf-8")
    codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exps = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(codes[0])
    exp = html.unescape(exps[0])
    print(lid, "code blocks:", len(codes), "expected blocks:", len(exps))
    print(lid, "code == twin exactly:", code == twin, "| code == twin.rstrip('\\n'):", code == twin.rstrip("\n"),
          "| len page", len(code), "len twin", len(twin))
    print(lid, "expected == twin stdout exactly:", exp == stdout, "| rstrip-equal:", exp.rstrip("\n") == stdout.rstrip("\n"))
    if code != twin:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
    if exp != stdout:
        import difflib
        for line in difflib.unified_diff(stdout.splitlines(), exp.splitlines(), "stdout", "expected", lineterm=""):
            print("   ", line)
    # interpretation/hypothesis lines in page: check any printed line names exist
