"""Compare each lab block in L07/L08 with its twin (code) and with a fresh run (expected output). Args: none."""
import html, re, subprocess, sys, pathlib
root = pathlib.Path("/tmp/verifyC2-E3-c")
for page, twin in (("L07", "lab-E3-L07-1"), ("L08", "lab-E3-L08-1")):
    text = (root / f"course/modules/E/E3/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1)
    code = html.unescape(code).strip("\n")
    twin_src = (root / f"tests/labs/E3/{twin}.py").read_text(encoding="utf-8").strip("\n")
    print(page, "code identical to twin:", code == twin_src, "lines", len(code.splitlines()), len(twin_src.splitlines()))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)).strip("\n")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/E3/{twin}.py")],
                         capture_output=True, text=True).stdout.strip("\n")
    print(page, "expected block identical to fresh run:", exp == run, "lines", len(exp.splitlines()))
    if exp != run:
        import difflib
        print("\n".join(difflib.unified_diff(exp.splitlines(), run.splitlines(), lineterm="")))
