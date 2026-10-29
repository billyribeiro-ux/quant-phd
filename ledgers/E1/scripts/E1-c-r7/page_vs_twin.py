import html, re, subprocess, sys
root = sys.argv[1]
for n in (7, 8, 9):
    page = open(f"{root}/course/modules/E/E1/L{n:02d}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{root}/tests/labs/E1/lab-E1-L{n:02d}-1.py", encoding="utf-8").read()
    print(f"L{n:02d} page code == twin: {code == twin} (page {len(code)} chars, twin {len(twin)} chars)")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/E1/lab-E1-L{n:02d}-1.py"],
                         capture_output=True, text=True, cwd="/tmp")
    print(f"L{n:02d} exit={out.returncode} stderr_len={len(out.stderr)}")
    print(f"L{n:02d} expected == output: {expected.strip() == out.stdout.strip()}")
    if expected.strip() != out.stdout.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), out.stdout.strip().splitlines(), lineterm="")))
