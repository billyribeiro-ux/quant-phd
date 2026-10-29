import html, re, subprocess, sys
root = sys.argv[1]
for page, twin in [("course/modules/E/E3/L07.html", "tests/labs/E3/lab-E3-L07-1.py"), ("course/modules/E/E3/L08.html", "tests/labs/E3/lab-E3-L08-1.py")]:
    t = open(f"{root}/{page}", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', t, re.S).group(1)
    code = html.unescape(code)
    tw = open(f"{root}/{twin}", encoding="utf-8").read()
    print(page, "code==twin:", code.strip() == tw.strip(), len(code), len(tw))
    if code.strip() != tw.strip():
        import difflib
        print("\n".join(list(difflib.unified_diff(tw.splitlines(), code.splitlines(), lineterm=""))[:40]))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', t, re.S).group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/{twin}"], capture_output=True, text=True).stdout
    print(page, "expected==output:", exp.strip() == out.strip())
    if exp.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(exp.splitlines(), out.splitlines(), lineterm="")))
