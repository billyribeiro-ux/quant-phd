import html, re, subprocess, sys
root = sys.argv[1]
for page, twin in [("course/modules/AC/AC4/L05.html", "tests/labs/AC4/lab-AC4-L05-1.py"),
                   ("course/modules/AC/AC4/L06.html", "tests/labs/AC4/lab-AC4-L06-1.py")]:
    src = open(f"{root}/{page}", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S).group(1)
    code = html.unescape(code)
    twin_src = open(f"{root}/{twin}", encoding="utf-8").read()
    print(page, "code==twin:", code.strip() == twin_src.strip())
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1)
    exp = html.unescape(exp).strip()
    out = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/{twin}"],
                         capture_output=True, text=True).stdout.strip()
    print(page, "expected==output:", exp == out, "lines", len(exp.splitlines()), len(out.splitlines()))
    if exp != out:
        import difflib
        print("\n".join(difflib.unified_diff(exp.splitlines(), out.splitlines(), lineterm="")))
