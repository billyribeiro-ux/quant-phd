"""Compare each L06-L08 page's embedded lab code and expected output with its twin and the twin's stdout."""

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
for lab in ("06", "07", "08"):
    page = (root / f"course/modules/M/M1/L{lab}.html").read_text(encoding="utf-8")
    code = html.unescape(re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)[0])
    twin = (root / f"tests/labs/M1/lab-M1-L{lab}-1.py").read_text(encoding="utf-8")
    expected = html.unescape(re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)[0])
    stdout = (Path(sys.argv[2]) / f"lab{lab}.out").read_text(encoding="utf-8")
    print(
        f"L{lab}: code==twin after trailing newline: {code == twin.rstrip(chr(10))} "
        f"(page {len(code)} chars, twin {len(twin)}); expected==stdout: {expected.rstrip(chr(10)) == stdout.rstrip(chr(10))}"
    )
