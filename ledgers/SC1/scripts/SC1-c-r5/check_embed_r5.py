"""Compare each SC1 lesson page (L07, L08) lab code and expected block with its twin and with the twin's stdout.

Run from the checkout root: python -I -W error ledgers/SC1/scripts/SC1-c-r5/check_embed_r5.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {"L07": "course/modules/SC/SC1/L07.html", "L08": "course/modules/SC/SC1/L08.html"}
TWINS = {"L07": "tests/labs/SC1/lab-SC1-L07-1.py", "L08": "tests/labs/SC1/lab-SC1-L08-1.py"}
PY = sys.executable


def main() -> int:
    ok = True
    for page, rel in PAGES.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        codes = re.findall(r'<code class="language-python" data-run>(.*?)</code>', text, re.S)
        exps = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
        print(f"{page}: data-run blocks {len(codes)}, expected blocks {len(exps)}")
        page_code = html.unescape(codes[0])
        page_expected = html.unescape(exps[0])
        twin = (ROOT / TWINS[page]).read_text(encoding="utf-8")
        same_code = page_code.rstrip() == twin.rstrip()
        proc = subprocess.run(
            [PY, "-I", "-W", "error", str(ROOT / TWINS[page])],
            capture_output=True,
            text=True,
            cwd="/tmp",
            timeout=120,
        )
        same_out = page_expected.rstrip() == proc.stdout.rstrip()
        exact_out = page_expected == proc.stdout
        print(f"{page}: page code chars {len(page_code)}, twin chars {len(twin)}, equal after rstrip {same_code}")
        print(f"{page}: twin exit {proc.returncode}, stderr chars {len(proc.stderr)}")
        print(f"{page}: expected equals twin stdout after rstrip {same_out}; exact {exact_out}")
        print(f"{page}: page code exact equal to twin {page_code == twin}")
        print(f"{page}: twin stdout ---\n{proc.stdout}--- end")
        ok = ok and same_code and same_out and proc.returncode == 0 and not proc.stderr
    print("ALL OK" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
