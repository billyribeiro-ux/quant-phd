import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
for n in range(13, 19):
    page = (root / f"course/modules/M/M2/L{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/M2/lab-M2-L{n}-1.py").read_text(encoding="utf-8")
    same = code.strip() == twin.strip()
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1)).strip()
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M2/lab-M2-L{n}-1.py")],
                         capture_output=True, text=True).stdout.strip()
    print(f"L{n}: page_code==twin {same}; expected==output {expected == out}; code_bytes {len(code)} twin_bytes {len(twin)}")
    if expected != out:
        for a, b in zip(expected.splitlines(), out.splitlines()):
            if a != b: print("  DIFF", repr(a), repr(b))
