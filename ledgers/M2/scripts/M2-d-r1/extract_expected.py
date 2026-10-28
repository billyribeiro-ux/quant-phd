"""Compare each slice page's embedded expected-output block with the twin's real stdout.

Usage: python -I extract_expected.py <checkout> <page-id e.g. L19>
Prints MATCH or DIFF with the first differing line. Read-only.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for page in sys.argv[2:]:
    text = (root / "course/modules/M/M2" / f"{page}.html").read_text(encoding="utf-8")
    blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    n = page[1:]
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M2/lab-M2-L{n}-1.py")],
        capture_output=True, text=True, check=True,
    ).stdout
    expected = html.unescape(blocks[0]).strip("\n") if blocks else ""
    got = run.strip("\n")
    if expected == got:
        print(f"{page}: MATCH ({len(blocks)} expected block(s), {len(got.splitlines())} lines)")
    else:
        el, gl = expected.splitlines(), got.splitlines()
        for i, (a, b) in enumerate(zip(el, gl)):
            if a != b:
                print(f"{page}: DIFF line {i+1}\n  page: {a!r}\n  run : {b!r}")
                break
        else:
            print(f"{page}: DIFF length page={len(el)} run={len(gl)}")
    print(f"  expected blocks: {len(blocks)}")
