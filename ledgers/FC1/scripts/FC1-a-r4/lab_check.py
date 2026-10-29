import html, re, subprocess, sys, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC4-FC1-a")
for lab, page in [("lab-FC1-L01-1", "L01"), ("lab-FC1-L02-1", "L02"), ("lab-FC1-L03-1", "L03")]:
    twin = root / "tests/labs/FC1" / f"{lab}.py"
    src = twin.read_text(encoding="utf-8")
    text = (root / "course/modules/FC/FC1" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="%s".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>' % lab, text, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd="/tmp")
    r2 = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd="/tmp")
    print(lab, "exit", r.returncode, "stderr_empty", r.stderr == "", "deterministic", r.stdout == r2.stdout)
    print("  code_eq_twin", code.strip() == src.strip())
    print("  expected_eq_output", expected.strip() == r.stdout.strip())
    if expected.strip() != r.stdout.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), r.stdout.strip().splitlines(), lineterm="")))
