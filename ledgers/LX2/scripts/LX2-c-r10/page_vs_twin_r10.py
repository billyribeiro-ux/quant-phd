import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/LX/LX2/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    twin = root / f"tests/labs/LX2/lab-LX2-project-{n}.py"
    m = re.search(rf'<section class="lab[^"]*" id="lab-LX2-project-{n}".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin_src = twin.read_text(encoding="utf-8")
    diff = [(i, a, b) for i, (a, b) in enumerate(zip(code.splitlines(), twin_src.splitlines())) if a != b]
    print(f"lab {n}: page code lines {len(code.splitlines())}, twin lines {len(twin_src.splitlines())}, differing lines {len(diff)}")
    for d in diff:
        print("   ", d)
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True)
    print(f"  twin exit {r.returncode}, stderr bytes {len(r.stderr)}")
    print("  stdout equals expected block:", r.stdout.rstrip("\n") == expected.rstrip("\n"))
    if r.stdout.rstrip("\n") != expected.rstrip("\n"):
        print("  STDOUT:\n" + r.stdout)
        print("  EXPECTED:\n" + expected)
