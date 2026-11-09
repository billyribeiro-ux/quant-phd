"""Check each slice lab's page code equals its twin, and its expected output block equals the twin's run output.

Usage: python3 -I expected_vs_output.py <repo-root> <run-dir-with-out1..out4.txt>
Exit 0 when all four labs match on both counts.
"""

import html
import re
import sys

root, run_dir = sys.argv[1], sys.argv[2]
ok = True
for n in (1, 2, 3, 4):
    with open(f"{root}/course/modules/CS/CS2/L0{n}.html", encoding="utf-8") as fh:
        page = fh.read()
    with open(f"{root}/tests/labs/CS2/lab-CS2-L0{n}-1.py", encoding="utf-8") as fh:
        twin = fh.read()
    with open(f"{run_dir}/out{n}.txt", encoding="utf-8") as fh:
        out = fh.read()
    sec = re.search(rf'<section class="lab" id="lab-CS2-L0{n}-1".*?</section>', page, re.S).group(0)
    code_pre = re.search(r"<pre><code[^>]*data-run>(.*?)</code></pre>", sec, re.S).group(1)
    exp_pre = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)
    code = html.unescape(code_pre).rstrip("\n")
    expected = html.unescape(exp_pre).rstrip("\n")
    code_eq = code == twin.rstrip("\n")
    exp_eq = expected == out.rstrip("\n")
    print(f"L0{n}: code==twin {code_eq}; expected==run output {exp_eq}; ")
    ok = ok and code_eq and exp_eq
print("ALL LAB PAGES MATCH" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
