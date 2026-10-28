"""Compare each lab twin's printed output with the embedded expected block and the embedded code block of its page.

Run with: python -I cmp_embedded.py <checkout>. Prints MATCH/DIFF per page and per block.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

co = Path(sys.argv[1])
py = co / ".venv/bin/python"
for lab, page in (("L05", "course/modules/AC/AC4/L05.html"), ("L06", "course/modules/AC/AC4/L06.html")):
    twin = co / f"tests/labs/AC4/lab-AC4-{lab}-1.py"
    printed = subprocess.run([str(py), "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=True).stdout
    text = (co / page).read_text(encoding="utf-8")
    blocks = re.findall(r"<pre[^>]*>(.*?)</pre>", text, flags=re.S)
    exp = [html.unescape(b) for b in blocks if "\n" in b and printed.splitlines()[0].split()[0] in b]
    exp_out = [b for b in exp if b.strip().splitlines()[-1].split()[0] == printed.strip().splitlines()[-1].split()[0]]
    print(lab, "output lines", len(printed.splitlines()), "candidate expected blocks", len(exp_out))
    for b in exp_out:
        print(lab, "expected block equals printed output:", b.strip() == printed.strip(), "lines", len(b.strip().splitlines()))
    code_blocks = [html.unescape(b) for b in blocks if "import" in b and "def " in b]
    tw = twin.read_text(encoding="utf-8").strip()
    print(lab, "code blocks", len(code_blocks), "equal to twin:", [c.strip() == tw for c in code_blocks])
