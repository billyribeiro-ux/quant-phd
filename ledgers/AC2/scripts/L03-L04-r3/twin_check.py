"""Round-3 verifier check: each lesson's data-run code and expected block against its lab twin.

Usage: .venv/bin/python -I ledgers/AC2/scripts/L03-L04-r3/twin_check.py <checkout>
Compares (1) the data-run <code> text with the twin file (modulo trailing newline) and
(2) the <pre class="expected"> text with the twin's stdout captured in /tmp/ac2-v/L03-L04/r3/twin_<L>.out.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
for lesson in ("L03", "L04"):
    page = (root / f"course/modules/AC/AC2/{lesson}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/AC2/lab-AC2-{lesson}-1.py").read_text(encoding="utf-8")
    run_code = re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
    assert run_code is not None, lesson
    code = html.unescape(run_code.group(1))
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    assert expected is not None, lesson
    exp_text = html.unescape(expected.group(1))
    out = Path(f"/tmp/ac2-v/L03-L04/r3/twin_{lesson}.out").read_text(encoding="utf-8")
    print(f"{lesson}: code_equals_twin={same_code} expected_equals_twin_stdout={exp_text.rstrip() == out.rstrip()}"
          f" expected_lines={len(exp_text.rstrip().splitlines())}")
