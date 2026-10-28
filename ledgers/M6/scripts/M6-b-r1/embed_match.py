import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
for n in ("05", "06", "07", "08"):
    page = (root / f"course/modules/M/M6/L{n}.html").read_text()
    twin = root / f"tests/labs/M6/lab-M6-L{n}-1.py"
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True).stdout
    print(f"L{n} code_equals_twin={code.strip() == twin.read_text().strip()} expected_equals_output={exp.strip() == out.strip()}")
    if exp.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(exp.strip().splitlines(), out.strip().splitlines(), lineterm="")))
