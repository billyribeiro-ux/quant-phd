import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
scratch = pathlib.Path(sys.argv[2])
for lab, page in (("L04", "course/modules/BK/BK4/L04.html"), ("L05", "course/modules/BK/BK4/L05.html")):
    text = (root / page).read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/BK4/lab-BK4-{lab}-1.py").read_text(encoding="utf-8")
    print(lab, "page code == twin (exact):", code == twin, "| rstrip-equal:", code.rstrip() == twin.rstrip(), "| page code chars", len(code), "twin chars", len(twin))
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(exp.group(1))
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/BK4/lab-BK4-{lab}-1.py")], capture_output=True, text=True, cwd=str(scratch))
    print(lab, "exit", r.returncode, "stderr bytes", len(r.stderr))
    print(lab, "stdout rstrip == expected rstrip:", r.stdout.rstrip() == expected.rstrip())
    if r.stdout.rstrip() != expected.rstrip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.rstrip().splitlines(), r.stdout.rstrip().splitlines(), lineterm="")))
    (scratch / f"{lab}.stdout").write_text(r.stdout)
