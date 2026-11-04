"""Round-6 compare: page code block == twin file (modulo final newline); page expected block == twin stdout
(modulo final newline). Twin stdout is read from ledgers/M2/scripts/M2-d2-r6/twin_<L>.out, produced by python -I -W error.
Usage: python3 -I compare_twins_r6.py <repo-root>"""
import html
import re
import sys

root = sys.argv[1]
S = f"{root}/ledgers/M2/scripts/M2-d2-r6"
for L in ("L22", "L23", "L24"):
    raw = open(f"{root}/course/modules/M/M2/{L}.html", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', raw, re.S).group(1)
    code = html.unescape(code)
    twin = open(f"{root}/tests/labs/M2/lab-M2-{L}-1.py", encoding="utf-8").read()
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', raw, re.S).group(1))
    stdout = open(f"{S}/twin_{L}.out", encoding="utf-8").read()
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    exp_eq = expected.rstrip("\n") == stdout.rstrip("\n")
    print(f"{L}: page code == twin (modulo final newline): {code_eq}  [code lines {code.count(chr(10))}, twin lines {twin.count(chr(10))}]")
    print(f"{L}: page expected == twin stdout (modulo final newline): {exp_eq}  [expected lines {expected.count(chr(10))}, stdout lines {stdout.count(chr(10))}]")
    if not code_eq:
        import difflib
        print("\n".join(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:3000])
    if not exp_eq:
        import difflib
        print("\n".join(difflib.unified_diff(stdout.splitlines(), expected.splitlines(), "stdout", "expected", lineterm=""))[:3000])
