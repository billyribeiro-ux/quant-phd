import re, html, subprocess, sys
root = sys.argv[1]
for f, lab in [("L01", "lab-AC4-L01-1"), ("L02", "lab-AC4-L02-1")]:
    page = open(f"{root}/course/modules/AC/AC4/{f}.html").read()
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)).strip()
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1))
    tw = open(f"{root}/tests/labs/AC4/{lab}.py").read()
    print(lab, "page code identical to twin:", code.strip() == tw.strip())
    out = f"/tmp/AC4-v/a/r17/{lab}-page.py"
    open(out, "w").write(code)
    r = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", out], capture_output=True, text=True, cwd="/tmp")
    print(lab, "page code output equals expected block:", r.stdout.strip() == exp, "exit", r.returncode)
