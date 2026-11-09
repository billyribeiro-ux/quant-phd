"""Closing-round check (LX2-c round 1): the code in each project lab on the page against its byte-identical twin.

Reads course/modules/LX/LX2/project.html (the data-run code block of each section lab-LX2-project-N) and compares
it line by line with tests/labs/LX2/lab-LX2-project-N.py. Also compares each expected block with the twin's stdout
(produced by running the twin under python -I -W error, see out/r1_twin_project_N.stdout).
Run from the checkout root: .venv/bin/python ledgers/LX2/scripts/LX2-c-r1/page_vs_twin_r1.py
"""

from __future__ import annotations

import html
import os
import re

ROOT = os.getcwd()
OUT = os.path.join(ROOT, "ledgers/LX2/scripts/LX2-c-r1/out")


def main() -> int:
    page = open(os.path.join(ROOT, "course/modules/LX/LX2/project.html"), encoding="utf-8").read()
    for n in (1, 2, 3):
        start = page.index(f'id="lab-LX2-project-{n}"')
        m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page[start:], re.S)
        assert m, f"lab {n}: code block not found"
        page_code = html.unescape(m.group(1)).split("\n")
        twin = open(os.path.join(ROOT, f"tests/labs/LX2/lab-LX2-project-{n}.py"), encoding="utf-8").read().split("\n")
        if page_code and page_code[-1] == "":
            page_code = page_code[:-1]
        if twin and twin[-1] == "":
            twin = twin[:-1]
        diffs = [
            (i + 1, p, t)
            for i, (p, t) in enumerate(zip(page_code, twin, strict=False))
            if p != t
        ]
        if len(page_code) != len(twin):
            diffs.append((0, f"<{len(page_code)} lines>", f"<{len(twin)} lines>"))
        print(f"lab {n}: page code {len(page_code)} lines, twin {len(twin)} lines, differing lines {len(diffs)}")
        for line_no, p, t in diffs:
            print(f"   line {line_no}: page {p!r} | twin {t!r}")
        # expected block versus the twin's stdout
        start_e = page.index(f'id="lab-LX2-project-{n}"')
        em = re.search(r'<pre class="expected" data-tolerance="[^"]+">(.*?)</pre>', page[start_e:], re.S)
        expected = html.unescape(em.group(1)).split() if em else []
        with open(os.path.join(OUT, f"r1_twin_project_{n}.stdout"), encoding="utf-8") as fh:
            actual = fh.read().split()
        print(f"   expected block tokens {len(expected)}, twin stdout tokens {len(actual)}, "
              f"token-equal {expected == actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
