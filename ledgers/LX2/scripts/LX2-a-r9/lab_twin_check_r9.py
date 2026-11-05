import html, re, subprocess, sys
root = sys.argv[1]
pairs = [("course/modules/LX/LX2/L01.html", "tests/labs/LX2/lab-LX2-L01-1.py", "lab-LX2-L01-1"),
         ("course/modules/LX/LX2/L02.html", "tests/labs/LX2/lab-LX2-L02-1.py", "lab-LX2-L02-1")]
for page, twin, name in pairs:
    t = open(f"{root}/{page}", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', t, re.S)
    code = html.unescape(m.group(1))
    tw = open(f"{root}/{twin}", encoding="utf-8").read()
    same = code.strip("\n") == tw.strip("\n")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', t, re.S)
    expected = html.unescape(e.group(1)).strip("\n")
    r = subprocess.run([sys.executable, "-I", "-W", "error", twin], cwd=root, capture_output=True, text=True)
    out = r.stdout.strip("\n")
    print(f"{name}: page_code_equals_twin={same} exit={r.returncode} stderr_bytes={len(r.stderr.encode())} expected_equals_output={expected == out}")
    if expected != out:
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), out.splitlines(), lineterm="")))
