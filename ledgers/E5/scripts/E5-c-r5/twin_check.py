import html, re, subprocess, sys
root = sys.argv[1]
for page, twin in [("L07", "lab-E5-L07-1"), ("L08", "lab-E5-L08-1")]:
    src = open(f"{root}/course/modules/E/E5/{page}.html", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S).group(1)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1)
    code = html.unescape(code)
    exp = html.unescape(exp)
    tw = open(f"{root}/tests/labs/E5/{twin}.py", encoding="utf-8").read()
    print(page, "code==twin:", code.strip() == tw.strip(), len(code), len(tw))
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/E5/{twin}.py"], capture_output=True, text=True).stdout
    print(page, "expected==output:", exp.strip() == out.strip())
    if exp.strip() != out.strip():
        print(repr(out[:500]))
