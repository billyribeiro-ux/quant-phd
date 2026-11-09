"""Run each project lab twin under python -I -W error and compare its stdout line by line with the page's expected block.
Usage: python3 -I twin_output_r18.py <checkout root>"""
import html
import re
import subprocess
import sys

root = sys.argv[1]
page = open(f"{root}/course/modules/SC/SC1/project.html", encoding="utf-8").read()
for lab in ("lab-SC1-project-1", "lab-SC1-project-2", "lab-SC1-project-3"):
    sec = re.search(rf'<section[^>]*id="{lab}".*?</section>', page, re.S).group(0)
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)).split("\n")
    run = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/SC1/{lab}.py"],
                         capture_output=True, text=True, cwd="/tmp")
    got = run.stdout.rstrip("\n").split("\n")
    print(f"== {lab}: exit {run.returncode}, stderr bytes {len(run.stderr)}, lines expected {len(expected)} got {len(got)}")
    for e, g in zip(expected, got):
        print(("SAME " if e == g else "DIFF ") + g)
    print("all lines equal:", expected == got)
