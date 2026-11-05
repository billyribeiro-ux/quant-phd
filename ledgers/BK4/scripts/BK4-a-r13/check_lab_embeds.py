"""Compare each lab twin with the code block and the expected block embedded in its page.

Usage: check_lab_embeds.py <checkout-root>. Prints one line per lab: code equal, expected equal to the twin's output
(when the expected block is compared with the output file given as argv[2:] in the form id=path).
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
outputs = dict(arg.split("=", 1) for arg in sys.argv[2:])
pages = {
    "L01": root / "course/modules/BK/BK4/L01.html",
    "L02": root / "course/modules/BK/BK4/L02.html",
    "L03": root / "course/modules/BK/BK4/L03.html",
}
for page, path in pages.items():
    text = path.read_text(encoding="utf-8")
    lab_id = f"lab-BK4-{page}-1"
    section = re.search(rf'<section class="lab" id="{lab_id}".*?</section>', text, re.S)
    if section is None:
        print(f"{lab_id}: section not found")
        continue
    body = section.group(0)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    twin = (root / f"tests/labs/BK4/{lab_id}.py").read_text(encoding="utf-8")
    code_text = html.unescape(code.group(1))
    exp_text = html.unescape(expected.group(1))
    print(f"{lab_id}: page code equals twin: {code_text == twin} (page {len(code_text)} chars, twin {len(twin)} chars)")
    if lab_id in outputs:
        out = Path(outputs[lab_id]).read_text(encoding="utf-8")
        print(f"{lab_id}: expected block equals a fresh run output: {exp_text.rstrip() == out.rstrip()}")
    else:
        print(f"{lab_id}: no output file supplied")
