import html, re, subprocess, sys
root = sys.argv[1]
for L in ("01", "02", "03"):
    page = open(f"{root}/course/modules/E/E3/L{L}.html", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1)
    code = html.unescape(code)
    twin = open(f"{root}/tests/labs/E3/lab-E3-L{L}-1.py", encoding="utf-8").read()
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
    exp = html.unescape(exp)
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/E3/lab-E3-L{L}-1.py"], capture_output=True, text=True).stdout
    print(f"L{L} code==twin: {code.strip() == twin.strip()} (len {len(code)} vs {len(twin)})")
    print(f"L{L} expected==output: {exp.strip() == out.strip()}")
    if exp.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(exp.strip().splitlines(), out.strip().splitlines(), lineterm="")))
