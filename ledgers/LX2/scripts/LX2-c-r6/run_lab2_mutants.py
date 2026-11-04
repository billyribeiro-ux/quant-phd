"""Rung-2 instant check: run every lab-2 mutant and alternative as a standalone program (python -I -W error, scratch
cwd) and compare its whole stdout with the page's expected block, exactly. A mutant is KILLED when its output differs
or it raises; an alternative PASSES when its output equals the expected block.

Usage: python3 -I run_lab2_mutants.py <repo_root> <file> [<file> ...]
"""
import html
import os
import re
import subprocess
import sys
import tempfile

root = sys.argv[1]
page = open(os.path.join(root, "course/modules/LX/LX2/project.html"), encoding="utf-8").read()
m = re.search(r'<section class="lab completion" id="lab-LX2-project-2".*?<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
expected = html.unescape(m.group(1)).rstrip("\n")
for path in sys.argv[2:]:
    with tempfile.TemporaryDirectory() as scratch:
        proc = subprocess.run([sys.executable, "-I", "-W", "error", os.path.abspath(path)], cwd=scratch,
                              capture_output=True, text=True, timeout=60)
    out = proc.stdout.rstrip("\n")
    name = os.path.basename(path)
    if proc.returncode != 0:
        status = f"KILLED (exit {proc.returncode}: {proc.stderr.strip().splitlines()[-1][:120] if proc.stderr.strip() else ''})"
    elif out == expected:
        status = "PASSES (output equals expected block)"
    else:
        diff = [(a, b) for a, b in zip(out.split("\n"), expected.split("\n")) if a != b]
        if len(out.split("\n")) != len(expected.split("\n")):
            diff.append(("<line count>", f"{len(out.split(chr(10)))} vs {len(expected.split(chr(10)))}"))
        status = "KILLED (first differing line: " + repr(diff[0][0]) + " vs expected " + repr(diff[0][1]) + ")"
    print(f"{name}: {status}")
