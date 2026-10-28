"""Run each AC4-c mutant or alternative twin against the expected block of its page.

Usage: python3 -I run_mutants.py <checkout> <dir> [<dir> ...]
Prints one line per file: name, page, status (SAME = output equals the page's expected block,
DIFF = output differs, ERR = non-zero exit or stderr). Mutants that are SAME survive.
"""
import html
import os
import re
import subprocess
import sys

checkout = sys.argv[1]
dirs = sys.argv[2:]


def expected(page: str) -> str:
    src = open(os.path.join(checkout, "course/modules/AC/AC4", page + ".html"), encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    return html.unescape(m.group(1)).strip()


exp = {"L05": expected("L05"), "L06": expected("L06")}
for d in dirs:
    for name in sorted(os.listdir(d)):
        if not name.endswith(".py"):
            continue
        path = os.path.join(d, name)
        text = open(path, encoding="utf-8").read()
        page = "L05" if "AC4 L05" in text[:200] else "L06"
        r = subprocess.run([os.path.join(checkout, ".venv/bin/python"), "-I", "-W", "error", path],
                           capture_output=True, text=True, timeout=60)
        out = r.stdout.strip()
        if r.returncode != 0 or r.stderr.strip():
            status = "ERR"
        elif out == exp[page]:
            status = "SAME"
        else:
            status = "DIFF"
        print(f"{status:5} {page} {os.path.basename(d)}/{name}")
