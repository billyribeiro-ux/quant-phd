"""Slice e, round 3: compare each E4 lesson page's embedded lab code block with its twin file (tests/labs/E4).

Usage (from the checkout root): python -I ledgers/E4/scripts/E4-e-r3/page_twin_equal.py
Prints one line per lesson page: the twin name, and whether each runnable block equals the twin file
(trailing newlines ignored; the page block carries no final newline).
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path()
PATTERN = re.compile(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', re.S)


def main() -> None:
    for i in range(1, 10):
        page = ROOT / f"course/modules/E/E4/L{i:02d}.html"
        twin = ROOT / f"tests/labs/E4/lab-E4-L{i:02d}-1.py"
        blocks = PATTERN.findall(page.read_text(encoding="utf-8"))
        twin_text = twin.read_text(encoding="utf-8").rstrip("\n")
        same = [html.unescape(b).rstrip("\n") == twin_text for b in blocks]
        print(f"{page.name}: runnable blocks={len(blocks)} twin={twin.name} equal={same}")


if __name__ == "__main__":
    main()
