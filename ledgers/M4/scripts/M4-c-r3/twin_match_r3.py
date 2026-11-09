import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
for page, twin in (("L08", "lab-M4-L08-1"), ("L09", "lab-M4-L09-1"), ("L10", "lab-M4-L10-1")):
    text = (root / f"course/modules/M/M4/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin_src = (root / f"tests/labs/M4/{twin}.py").read_text(encoding="utf-8")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M4/{twin}.py")], capture_output=True, text=True, cwd="/tmp")
    print(page, "code_equals_twin=", code == twin_src, "len", len(code), len(twin_src))
    print(page, "twin_exit=", run.returncode, "stderr_bytes=", len(run.stderr.encode()))
    print(page, "expected_equals_output=", expected.rstrip("\n") == run.stdout.rstrip("\n"), "lines", len(run.stdout.splitlines()))
    if expected.rstrip("\n") != run.stdout.rstrip("\n"):
        print("DIFF"); print(expected); print("----"); print(run.stdout)
