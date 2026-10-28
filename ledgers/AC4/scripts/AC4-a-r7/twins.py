import re, subprocess, sys, html
root = sys.argv[1]
for page, twin in (("L01", "lab-AC4-L01-1"), ("L02", "lab-AC4-L02-1")):
    src = open(f"{root}/course/modules/AC/AC4/{page}.html", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(m.group(1)).strip().splitlines()
    out = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/AC4/{twin}.py"],
                         capture_output=True, text=True, check=True).stdout.strip().splitlines()
    print(page, "lines", len(expected), len(out), "equal" if expected == out else "DIFF")
