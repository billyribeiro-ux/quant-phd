import html, re, subprocess, sys
root = "/Users/billyribeiro/.fanout/wt/verifyC13-E5-b"
for l in ["04", "05", "06"]:
    page = open(f"{root}/course/modules/E/E5/L{l}.html", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1)
    code = html.unescape(code)
    twin = open(f"{root}/tests/labs/E5/lab-E5-L{l}-1.py", encoding="utf-8").read()
    same = code.strip() == twin.strip()
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/E5/lab-E5-L{l}-1.py"], capture_output=True, text=True).stdout
    print(f"L{l} code_equals_twin={same} expected_equals_output={exp.strip()==out.strip()} lines_exp={len(exp.splitlines())} lines_out={len(out.splitlines())}")
    if not same:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True)))[:60]))
