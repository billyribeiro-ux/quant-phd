"""FC2 slice b round 3: page lab code and expected block vs twin source and twin output (own extraction)."""
import html, re, subprocess, sys, tempfile, pathlib, os
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS3-FC2-b")
for page, lab in [("L04", "lab-FC2-L04-1"), ("L05", "lab-FC2-L05-1"), ("L06", "lab-FC2-L06-1")]:
    src = (ROOT / f"course/modules/FC/FC2/{page}.html").read_text(encoding="utf-8")
    sec = re.search(rf'<section class="lab" id="{lab}".*?</section>', src, re.S).group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)
    code = html.unescape(code)
    expected = html.unescape(expected)
    twin = (ROOT / f"tests/labs/FC2/{lab}.py").read_text(encoding="utf-8")
    print(page, "code==twin (modulo final newline):", code.rstrip("\n") == twin.rstrip("\n"), "twin len", len(twin), "page code len", len(code))
    with tempfile.TemporaryDirectory() as d:
        tw = pathlib.Path(d) / "twin.py"
        tw.write_text(twin, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(tw)], cwd=d, capture_output=True, text=True, timeout=60)
    print(page, "twin exit", r.returncode, "stderr empty", r.stderr == "")
    print(page, "stdout == expected block:", r.stdout.rstrip("\n") == expected.rstrip("\n"), "lines", len(r.stdout.splitlines()))
    if r.stdout.rstrip("\n") != expected.rstrip("\n"):
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), r.stdout.splitlines(), lineterm="")))
