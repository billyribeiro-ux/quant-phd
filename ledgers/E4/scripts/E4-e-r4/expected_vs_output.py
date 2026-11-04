"""Compare each lab's printed output with the <pre class="expected"> block of its lesson page.

Usage: python -I expected_vs_output.py <repo-root> <out-dir>
Prints one line per lab: whether the expected block, whitespace-normalised, equals the normalised output.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path


def norm(text: str) -> str:
    return " ".join(text.split())


def main() -> None:
    root = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    for n in range(1, 10):
        page = root / "course/modules/E/E4" / f"L{n:02d}.html"
        text = page.read_text(encoding="utf-8")
        blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', text, flags=re.S)
        out = (out_dir / f"lab-E4-L{n:02d}-1.out").read_text(encoding="utf-8")
        expected = [norm(html.unescape(re.sub(r"<[^>]+>", "", b))) for b in blocks]
        actual = norm(out)
        status = "MATCH" if any(e == actual for e in expected) else "DIFF"
        print(
            f"L{n:02d} expected_blocks={len(blocks)} {status} expected_len={[len(e) for e in expected]} actual_len={len(actual)}"
        )
        if status == "DIFF" and expected:
            e = expected[0]
            i = next((k for k in range(min(len(e), len(actual))) if e[k] != actual[k]), min(len(e), len(actual)))
            print("   first difference at", i, "expected:", e[max(0, i - 60) : i + 60])
            print("   first difference at", i, "actual:  ", actual[max(0, i - 60) : i + 60])


if __name__ == "__main__":
    main()
