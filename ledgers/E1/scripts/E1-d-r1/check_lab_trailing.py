"""Verifier check: confirm page-vs-twin differences for labs 1-3 are only trailing newline or the lab-2 blanks."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
text = (ROOT / "course/modules/E/E1/project.html").read_text(encoding="utf-8")
labs = re.findall(
    r'id="(lab-E1-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>', text, flags=re.S
)
for lab_id, code_html in labs:
    code = html.unescape(code_html)
    twin = (ROOT / "tests/labs/E1" / f"{lab_id}.py").read_text(encoding="utf-8")
    print(lab_id, "page ends with newline:", code.endswith("\n"), "| twin ends with newline:", twin.endswith("\n"))
    print(lab_id, "page == twin.rstrip('\\n'):", code == twin.rstrip("\n"))
    if lab_id.endswith("2"):
        filled = code.replace("return ___", "return (d - rival) / 2").replace(
            "return half_up(___)", "return half_up((a * volume - volume * volume / 2) / b - c * volume)"
        )
        print(lab_id, "blanks filled == twin.rstrip('\\n'):", filled == twin.rstrip("\n"), "| remaining ___:", code.count("___"))
