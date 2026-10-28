import html, re, sys
root = sys.argv[1]
for lab, page in (("lab-CF1-L05-1", "L05"), ("lab-CF1-L06-1", "L06")):
    src = open(f"{root}/course/modules/CF/CF1/{page}.html", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S).group(1)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1)
    twin = open(f"{root}/tests/labs/CF1/{lab}.py", encoding="utf-8").read()
    print(lab, "code identical (strict):", html.unescape(code) == twin, "code identical (ignoring one trailing newline):", html.unescape(code).rstrip("\n") == twin.rstrip("\n"), "len", len(twin))
    import subprocess
    out = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/CF1/{lab}.py"], capture_output=True, text=True).stdout
    print(lab, "expected identical to twin output:", html.unescape(exp).strip() == out.strip())
