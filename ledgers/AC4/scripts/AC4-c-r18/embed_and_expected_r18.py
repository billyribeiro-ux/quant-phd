import html, re, subprocess, sys
root = sys.argv[1]
for page, twin in [("L05", "tests/labs/AC4/lab-AC4-L05-1.py"), ("L06", "tests/labs/AC4/lab-AC4-L06-1.py")]:
    src = open(f"{root}/course/modules/AC/AC4/{page}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(m.group(1))
    tw = open(f"{root}/{twin}", encoding="utf-8").read()
    print(page, "embedded code equals twin:", code.strip() == tw.strip(), len(code), len(tw))
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1)
    out = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/{twin}"], capture_output=True, text=True).stdout
    print(page, "expected block equals run output:", html.unescape(exp).strip() == out.strip())
