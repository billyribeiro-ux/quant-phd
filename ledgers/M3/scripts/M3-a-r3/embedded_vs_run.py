import html, re, subprocess, sys, pathlib
root = pathlib.Path("/tmp/verifyB3-M3-a")
py = str(root / ".venv/bin/python")
for lab, page in [("L01", "L01.html"), ("L02", "L02.html"), ("L03", "L03.html")]:
    text = (root / "course/modules/M/M3" / page).read_text()
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin = (root / f"tests/labs/M3/lab-M3-{lab}-1.py").read_text()
    out = subprocess.run([py, "-I", "-W", "error", "-c", "import sys; exec(compile(open(sys.argv[1]).read(), sys.argv[1], 'exec'))", str(root / f"tests/labs/M3/lab-M3-{lab}-1.py")], capture_output=True, text=True, cwd="/tmp").stdout
    print(lab, "code==twin:", code.strip() == twin.strip(), "| expected==run:", expected.strip() == out.strip(), "| lines", len(out.splitlines()))
    if expected.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), out.strip().splitlines(), lineterm="")))
