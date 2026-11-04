# Round-3 check: twin alone under python -I -W error from an empty temp dir; page code == twin; page expected == stdout.
import html, re, subprocess, sys, tempfile, pathlib, os
root = pathlib.Path(sys.argv[1])
for lab, page in (("lab-BK4-L04-1", "L04"), ("lab-BK4-L05-1", "L05")):
    twin = root / "tests/labs/BK4" / f"{lab}.py"
    src = (root / "course/modules/BK/BK4" / f"{page}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1))
    twin_text = twin.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], cwd=d, capture_output=True, text=True)
    print(lab, "exit", r.returncode, "stderr", repr(r.stderr[:200]))
    print(lab, "page code == twin (rstrip):", code.rstrip() == twin_text.rstrip(), "| code == twin exact:", code == twin_text, "| code endswith newline:", code.endswith("\n"), "twin endswith newline:", twin_text.endswith("\n"))
    print(lab, "expected == stdout (rstrip):", expected.rstrip() == r.stdout.rstrip(), "| expected exact:", expected == r.stdout)
    pathlib.Path(f"/tmp/bk4b-r3/{lab}.stdout").write_text(r.stdout, encoding="utf-8")
