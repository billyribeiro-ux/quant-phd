"""Compare each project lab's page code and expected block with its twin and with the twin's output (round 14).

Usage: python3 lab_compare_r14.py <checkout> ; run after: python3 -I -W error tests/labs/FC2/lab-FC2-project-N.py > out/twinN.txt
"""

from __future__ import annotations

import difflib
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/FC/FC2/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    m = re.search(
        r'<section class="lab[^"]*" id="lab-FC2-project-%d".*?<pre><code[^>]*>(.*?)</code></pre>\s*'
        r'<pre class="expected"[^>]*>(.*?)</pre>' % n,
        page,
        re.S,
    )
    assert m is not None, n
    code = html.unescape(m.group(1)).strip().splitlines()
    expected = html.unescape(m.group(2)).strip()
    twin = (root / f"tests/labs/FC2/lab-FC2-project-{n}.py").read_text(encoding="utf-8").strip().splitlines()
    output = (root / f"{Path(__file__).parent.as_posix()}/out/twin{n}.txt").read_text(encoding="utf-8").strip()
    print(f"lab {n}: page code lines {len(code)}, twin lines {len(twin)}, identical: {code == twin}")
    print(f"lab {n}: expected block equals twin output: {expected == output}")
    if code != twin:
        for line in difflib.unified_diff(twin, code, "twin", "page", lineterm="", n=0):
            if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
                print("   ", line)
        print(f"lab {n}: differing page lines all contain a blank: {all('___' in a for a, b in zip(code, twin) if a != b)}")
