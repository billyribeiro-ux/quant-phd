import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
ok_all = True
for n in ["L01", "L02", "L03"]:
    page = (root / f"course/modules/SC/SC1/{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab"[^>]*id="lab-SC1-%s-1".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>' % n, page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (root / f"tests/labs/SC1/lab-SC1-{n}-1.py").read_text(encoding="utf-8")
    code_eq = code.strip("\n") == twin.strip("\n")
    import subprocess, os, tempfile
    d = tempfile.mkdtemp()
    out = subprocess.run([str(root / ".venv/bin/python"), "-I", "-W", "error", str(root / f"tests/labs/SC1/lab-SC1-{n}-1.py")], cwd=d, capture_output=True, text=True)
    exp_eq = out.stdout.strip("\n") == expected.strip("\n")
    print(n, "code_eq_twin", code_eq, "expected_eq_output_exact", exp_eq, "rc", out.returncode, "stderr", len(out.stderr))
    if not exp_eq:
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip("\n").splitlines(), out.stdout.strip("\n").splitlines(), lineterm="")))
    ok_all = ok_all and code_eq and exp_eq
print("ALL", ok_all)
