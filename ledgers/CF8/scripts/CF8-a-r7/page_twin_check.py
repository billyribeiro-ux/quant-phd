import html, re, sys, subprocess
pages = {"course/modules/CF/CF8/L01.html": "tests/labs/CF8/lab-CF8-L01-1.py", "course/modules/CF/CF8/L02.html": "tests/labs/CF8/lab-CF8-L02-1.py"}
for page, twin in pages.items():
    src = open(page, encoding="utf-8").read()
    blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(blocks[0]) if blocks else None
    tw = open(twin, encoding="utf-8").read()
    print(page, "code blocks:", len(blocks), "equals twin:", code == tw, "len", len(code or ""), len(tw))
    if code != tw:
        import difflib
        print("".join(list(difflib.unified_diff(tw.splitlines(True), (code or "").splitlines(True), n=1))[:40]))
    # expected blocks: <pre> after the code block
    out = subprocess.run([sys.executable, "-I", "-W", "error", twin], capture_output=True, text=True).stdout
    exp = re.findall(r'<pre class="expected">(.*?)</pre>', src, re.S) or re.findall(r'<pre>(?!<code)(.*?)</pre>', src, re.S)
    print("expected blocks:", len(exp), [html.unescape(e)[:0] for e in exp][:0])
    for e in exp:
        if html.unescape(e).strip() and html.unescape(e).strip() in out:
            print("  expected block found verbatim in output (len", len(e), ")")
    print("twin output lines", len(out.splitlines()), "matches full output:", any(html.unescape(e).strip()==out.strip() for e in exp))
